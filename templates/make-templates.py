#!/usr/bin/env python3
"""Build the two templates grant-export fills: templates/grant-dossier.docx
and templates/grant-budget.xlsx.

They are plain OOXML packages written with the standard library only (no
package manager in this project), so the tags Sovrium fills sit in runs of
their own and no editor splits them. Run it again after changing the layout:

    python3 -I templates/make-templates.py

then check the result with sample data:

    sovrium render templates/grant-dossier.docx --data templates/grant-sample.json --out /tmp/dossier.docx
    sovrium render templates/grant-budget.xlsx --data templates/grant-sample.json --out /tmp/budget.xlsx

The data each tag reads is built by the `gather` step of
config/automations/grant-export.yaml; templates/grant-sample.json is a copy
of its shape.
"""
import os
import zipfile
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
NAVY = "273A61"
ORANGE = "F08137"
GREY = "5D6A88"

W_NS = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"')


# ---------------------------------------------------------------- Word ----

def run(text, bold=False, italic=False, color=None, size=None):
    props = ""
    if bold:
        props += "<w:b/>"
    if italic:
        props += "<w:i/>"
    if color:
        props += f'<w:color w:val="{color}"/>'
    if size:
        props += f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
    rpr = f"<w:rPr>{props}</w:rPr>" if props else ""
    return f'<w:r>{rpr}<w:t xml:space="preserve">{escape(text)}</w:t></w:r>'


def para(*runs, style=None, align=None, keep_next=False, space_after=None):
    ppr = ""
    if style:
        ppr += f'<w:pStyle w:val="{style}"/>'
    if keep_next:
        ppr += "<w:keepNext/>"
    if space_after is not None:
        ppr += f'<w:spacing w:after="{space_after}"/>'
    if align:
        ppr += f'<w:jc w:val="{align}"/>'
    ppr = f"<w:pPr>{ppr}</w:pPr>" if ppr else ""
    body = "".join(r if r.startswith("<w:r") else run(r) for r in runs)
    return f"<w:p>{ppr}{body}</w:p>"


def tag(t):
    """A control tag ({{#each}}, {{/if}}…) in a paragraph of its own."""
    return para(run(t))


def cell(content, width, fill=None, bold=False, align=None, color=None):
    tcpr = f'<w:tcW w:w="{width}" w:type="dxa"/>'
    if fill:
        tcpr += f'<w:shd w:val="clear" w:color="auto" w:fill="{fill}"/>'
    jc = '<w:jc w:val="%s"/>' % align if align else ""
    ppr = f'<w:pPr><w:spacing w:before="40" w:after="40"/>{jc}</w:pPr>'
    return f'<w:tc><w:tcPr>{tcpr}</w:tcPr><w:p>{ppr}{run(content, bold=bold, color=color)}</w:p></w:tc>'


def row(cells, header=False):
    trpr = "<w:trPr><w:tblHeader/><w:cantSplit/></w:trPr>" if header else "<w:trPr><w:cantSplit/></w:trPr>"
    return f"<w:tr>{trpr}{''.join(cells)}</w:tr>"


def table(widths, rows):
    grid = "".join(f'<w:gridCol w:w="{w}"/>' for w in widths)
    borders = "".join(f'<w:{b} w:val="single" w:sz="4" w:space="0" w:color="B5CCE4"/>' for b in ("top", "left", "bottom", "right", "insideH", "insideV"))
    tblpr = (f'<w:tblPr><w:tblW w:w="{sum(widths)}" w:type="dxa"/><w:tblBorders>{borders}</w:tblBorders>'
             '<w:tblLayout w:type="fixed"/><w:tblCellMar><w:left w:w="80" w:type="dxa"/><w:right w:w="80" w:type="dxa"/></w:tblCellMar></w:tblPr>')
    return f"<w:tbl>{tblpr}<w:tblGrid>{grid}</w:tblGrid>{''.join(rows)}</w:tbl>"


def paragraphs_block(path):
    """The paragraphs of a section: plain text, or a bullet."""
    return (tag(f"{{{{#each {path}}}}}")
            + tag("{{#if plain}}") + para(run("{{text}}")) + tag("{{/if}}")
            + tag("{{#if bullet}}") + para(run("• "), run("{{text}}"), style="Bullet") + tag("{{/if}}")
            + tag("{{/each}}"))


def section_list(name):
    """A repeated list of sections: an optional subtitle, then its paragraphs."""
    return (tag(f"{{{{#each {name}}}}}")
            + tag("{{#if show_title}}") + para(run("{{title}}"), style="Heading2", keep_next=True) + tag("{{/if}}")
            + paragraphs_block("paragraphs")
            + tag("{{/each}}"))


def document_xml():
    b = []
    b.append(para(run("{{org.legal_name}}"), style="Title"))
    b.append(para(run("Dossier de demande de subvention — {{app.type_label}} {{app.exercise_year}}"), style="Subtitle"))
    b.append(para(run("Adressé à : ", bold=True), run("{{app.addressed_to}}")))
    b.append(para(run("Montant sollicité : ", bold=True), run("{{app.amount_requested_label}}")))

    b.append(tag("{{#if has_preambule}}"))
    b.append(para(run("Préambule"), style="Heading1", keep_next=True))
    b.append(section_list("preambule"))
    b.append(tag("{{/if}}"))

    b.append(para(run("Objet de la demande"), style="Heading1", keep_next=True))
    b.append(section_list("objet"))
    b.append(tag("{{#if has_actions}}"))
    b.append(para(run("Nous prévoyons ainsi les actions suivantes :")))
    b.append(tag("{{#each actions}}"))
    b.append(para(run("• "), run("{{title}}"), style="Bullet"))
    b.append(tag("{{/each}}"))
    b.append(tag("{{#each actions_described}}"))
    b.append(para(run("{{title}}"), style="Heading2", keep_next=True))
    b.append(paragraphs_block("paragraphs"))
    b.append(tag("{{#if partners}}"))
    b.append(para(run("Partenaires : ", bold=True), run("{{partners}}")))
    b.append(tag("{{/if}}"))
    b.append(tag("{{#if frequency_label}}"))
    b.append(para(run("Fréquence prévue : ", bold=True), run("{{frequency_label}}")))
    b.append(tag("{{/if}}"))
    b.append(tag("{{/each}}"))
    b.append(tag("{{/if}}"))

    b.append(tag("{{#if has_principes}}"))
    b.append(para(run("Principes directeurs de nos actions"), style="Heading1", keep_next=True))
    b.append(section_list("principes"))
    b.append(tag("{{/if}}"))

    b.append(tag("{{#each autres}}"))
    b.append(para(run("{{title}}"), style="Heading1", keep_next=True))
    b.append(paragraphs_block("paragraphs"))
    b.append(tag("{{/each}}"))

    # Modalités de calcul: the text, the cost table, the request table.
    b.append(para(run("Modalités de calcul de la demande"), style="Heading1", keep_next=True))
    b.append(section_list("calcul"))
    b.append(tag("{{#if has_costs}}"))
    b.append(para(run("Coût des personnels et de fonctionnement, et part qui concourt à l'activité subventionnée, sur l'année {{app.exercise_year}} :"), keep_next=True))
    widths = [3000, 1550, 1500, 1500, 1500]
    rows = [row([cell("Poste", widths[0], NAVY, True, color="FFFFFF"), cell("Coût", widths[1], NAVY, True, "right", "FFFFFF"),
                 cell("Part activité commerciale", widths[2], NAVY, True, "right", "FFFFFF"), cell("Part subventionnable", widths[3], NAVY, True, "right", "FFFFFF"),
                 cell("Répartition", widths[4], NAVY, True, "right", "FFFFFF")], header=True),
            row([cell("{{#each cost_rows}}{{label}}", widths[0]), cell("{{cost}}", widths[1], align="right"), cell("{{commercial}}", widths[2], align="right"),
                 cell("{{event}}", widths[3], align="right"), cell("{{split}}{{/each}}", widths[4], align="right")]),
            row([cell("Total", widths[0], "E3ECF5", True), cell("{{costs_total.cost}}", widths[1], "E3ECF5", True, "right"), cell("{{costs_total.commercial}}", widths[2], "E3ECF5", True, "right"),
                 cell("{{costs_total.event}}", widths[3], "E3ECF5", True, "right"), cell("", widths[4], "E3ECF5")])]
    b.append(table(widths, rows))
    b.append(para(run("")))
    b.append(para(run("Nous demandons une subvention couvrant {{app.share_label}} de ces dépenses :"), keep_next=True))
    widths2 = [4550, 2250, 2250]
    rows2 = [row([cell("Poste", widths2[0], NAVY, True, color="FFFFFF"), cell("Coût", widths2[1], NAVY, True, "right", "FFFFFF"),
                  cell("Part demandée ({{app.share_label}})", widths2[2], NAVY, True, "right", "FFFFFF")], header=True),
             row([cell("{{#each request_rows}}{{label}}", widths2[0]), cell("{{cost}}", widths2[1], align="right"), cell("{{requested}}{{/each}}", widths2[2], align="right")]),
             row([cell("Total", widths2[0], "E3ECF5", True), cell("{{request_total.cost}}", widths2[1], "E3ECF5", True, "right"),
                  cell("{{request_total.requested}}", widths2[2], "E3ECF5", True, "right")])]
    b.append(table(widths2, rows2))
    b.append(tag("{{/if}}"))

    # Budget prévisionnel (CERFA).
    b.append(para(run("Budget prévisionnel {{app.exercise_year}}"), style="Heading1", keep_next=True))
    b.append(para(run("Établi à partir du scénario « {{app.scenario_name}} » du prévisionnel de l'association.", italic=True, color=GREY)))
    for side, label in (("budget_charges", "Charges"), ("budget_produits", "Produits")):
        b.append(para(run(label), style="Heading2", keep_next=True))
        w3 = [900, 3900, 1600, 2650]
        rows3 = [row([cell("Compte", w3[0], NAVY, True, color="FFFFFF"), cell("Poste", w3[1], NAVY, True, color="FFFFFF"),
                      cell("Montant", w3[2], NAVY, True, "right", "FFFFFF"), cell("Précisions", w3[3], NAVY, True, color="FFFFFF")], header=True),
                 row([cell("{{#each " + side + "}}{{code}}", w3[0]), cell("{{label}}", w3[1]), cell("{{amount}}", w3[2], align="right"), cell("{{precisions}}{{/each}}", w3[3])])]
        b.append(table(w3, rows3))
    b.append(para(run("")))
    b.append(para(run("Total des charges : ", bold=True), run("{{budget.charges}}"), run("   ·   "), run("Total des produits : ", bold=True), run("{{budget.produits}}")))
    b.append(tag("{{#if budget.unbalanced}}"))
    b.append(para(run("Budget à équilibrer : écart de {{budget.gap}} entre charges et produits.", bold=True, color="CF1769")))
    b.append(tag("{{/if}}"))

    # Moyens humains and pièces.
    b.append(para(run("Moyens humains"), style="Heading1", keep_next=True))
    b.append(para(run("Salarié·es : ", bold=True), run("{{hr.staff_count}} personne(s), {{hr.staff_fte}} ETPT")))
    b.append(para(run("Bénévoles : ", bold=True), run("{{hr.volunteers_count}} personne(s), {{hr.volunteers_fte}} ETPT")))
    b.append(tag("{{#if hr.recruitment_planned}}"))
    b.append(para(run("Recrutement envisagé sur l'exercice : ", bold=True), run("{{hr.recruitment_fte}} ETPT")))
    b.append(tag("{{/if}}"))
    b.append(tag("{{#if has_attachments}}"))
    b.append(para(run("Pièces jointes"), style="Heading1", keep_next=True))
    b.append(tag("{{#each attachments}}"))
    b.append(para(run("• "), run("{{title}}"), style="Bullet"))
    b.append(tag("{{/each}}"))
    b.append(tag("{{/if}}"))

    b.append(para(run("")))
    b.append(para(run("Fait à {{org.city}}, le {{signed_on}}"), align="right"))
    b.append(para(run("{{signatory.name}}, {{signatory.role}}"), align="right"))

    sect = ('<w:sectPr><w:footerReference w:type="default" r:id="rIdFooter"/>'
            '<w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1300" w:right="1300" w:bottom="1300" w:left="1300" w:header="600" w:footer="500" w:gutter="0"/></w:sectPr>')
    return f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document {W_NS}><w:body>{"".join(b)}{sect}</w:body></w:document>'


def styles_xml():
    def style(sid, name, rpr="", ppr="", based="Normal"):
        basedon = f'<w:basedOn w:val="{based}"/>' if based else ""
        return (f'<w:style w:type="paragraph" w:styleId="{sid}"><w:name w:val="{name}"/>{basedon}<w:qFormat/>'
                f"<w:pPr>{ppr}</w:pPr><w:rPr>{rpr}</w:rPr></w:style>")
    font = '<w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/>'
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            f'<w:styles {W_NS}>'
            f'<w:docDefaults><w:rPrDefault><w:rPr>{font}<w:sz w:val="21"/><w:szCs w:val="21"/><w:lang w:val="fr-FR"/></w:rPr></w:rPrDefault>'
            '<w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="276" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>'
            + style("Normal", "Normal", based=None)
            + style("Title", "Title", f'<w:b/><w:color w:val="{NAVY}"/><w:sz w:val="44"/>', '<w:spacing w:after="60"/>')
            + style("Subtitle", "Subtitle", f'<w:i/><w:color w:val="{GREY}"/><w:sz w:val="26"/>', f'<w:spacing w:after="240"/><w:pBdr><w:bottom w:val="single" w:sz="8" w:space="6" w:color="{ORANGE}"/></w:pBdr>')
            + style("Heading1", "heading 1", f'<w:b/><w:color w:val="{NAVY}"/><w:sz w:val="32"/>', '<w:keepNext/><w:spacing w:before="360" w:after="120"/><w:outlineLvl w:val="0"/>')
            + style("Heading2", "heading 2", f'<w:b/><w:color w:val="{NAVY}"/><w:sz w:val="25"/>', '<w:keepNext/><w:spacing w:before="220" w:after="80"/><w:outlineLvl w:val="1"/>')
            + style("Bullet", "List Bullet", "", '<w:spacing w:after="60"/><w:ind w:left="400" w:hanging="200"/>')
            + style("Footer", "footer", f'<w:color w:val="{GREY}"/><w:sz w:val="16"/>', '<w:jc w:val="center"/>')
            + "</w:styles>")


def footer_xml():
    page = ('<w:r><w:fldChar w:fldCharType="begin"/></w:r><w:r><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'
            '<w:r><w:fldChar w:fldCharType="separate"/></w:r><w:r><w:t>1</w:t></w:r><w:r><w:fldChar w:fldCharType="end"/></w:r>')
    return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:ftr {W_NS}>'
            + para(run("{{org.footer}}"), style="Footer")
            + f'<w:p><w:pPr><w:pStyle w:val="Footer"/></w:pPr>{page}</w:p></w:ftr>')


def write_docx(path):
    files = {
        "[Content_Types].xml": ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                                '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                                '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
                                '<Default Extension="xml" ContentType="application/xml"/>'
                                '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
                                '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
                                '<Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>'
                                '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
                                '</Types>'),
        "_rels/.rels": ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
                        '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
                        '</Relationships>'),
        "docProps/core.xml": ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                              '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/">'
                              '<dc:title>Dossier de demande de subvention</dc:title><dc:creator>La Plage Digitale</dc:creator></cp:coreProperties>'),
        "word/_rels/document.xml.rels": ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                                         '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                                         '<Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
                                         '<Relationship Id="rIdFooter" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/>'
                                         '</Relationships>'),
        "word/document.xml": document_xml(),
        "word/styles.xml": styles_xml(),
        "word/footer1.xml": footer_xml(),
    }
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in files.items():
            z.writestr(name, data)


# ---------------------------------------------------------------- Excel ---

def col(i):
    return "ABCDEFGH"[i]


def xlsx_sheet(rows, widths):
    """rows: list of (cells, style) where cells are strings (shared) or ('f', formula) or ('n', number)."""
    cols = "".join(f'<col min="{i + 1}" max="{i + 1}" width="{w}" customWidth="1"/>' for i, w in enumerate(widths))
    out = []
    for r, (cells, style) in enumerate(rows, start=1):
        cs = []
        for c, v in enumerate(cells):
            ref = f"{col(c)}{r}"
            s = f' s="{style}"' if style else ""
            if v is None:
                continue
            if isinstance(v, tuple) and v[0] == "f":
                cs.append(f'<c r="{ref}"{s}><f>{escape(v[1])}</f></c>')
            else:
                cs.append(f'<c r="{ref}" t="inlineStr"{s}><is><t xml:space="preserve">{escape(v)}</t></is></c>')
        out.append(f'<row r="{r}">{"".join(cs)}</row>')
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
            f'<cols>{cols}</cols><sheetData>{"".join(out)}</sheetData></worksheet>')


def write_xlsx(path):
    # Styles: 0 default, 1 title, 2 header (navy), 3 amount (#,##0.00 €), 4 total (bold amount), 5 bold text.
    styles = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
              '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
              '<numFmts count="1"><numFmt numFmtId="164" formatCode="#,##0.00\\ &quot;€&quot;"/></numFmts>'
              '<fonts count="4"><font><sz val="11"/><name val="Calibri"/></font>'
              f'<font><b/><sz val="14"/><color rgb="FF{NAVY}"/><name val="Calibri"/></font>'
              '<font><b/><sz val="11"/><color rgb="FFFFFFFF"/><name val="Calibri"/></font>'
              '<font><b/><sz val="11"/><name val="Calibri"/></font></fonts>'
              '<fills count="4"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill>'
              f'<fill><patternFill patternType="solid"><fgColor rgb="FF{NAVY}"/></patternFill></fill>'
              '<fill><patternFill patternType="solid"><fgColor rgb="FFE3ECF5"/></patternFill></fill></fills>'
              '<borders count="1"><border/></borders><cellStyleXfs count="1"><xf/></cellStyleXfs>'
              '<cellXfs count="6"><xf/>'
              '<xf fontId="1" applyFont="1"/>'
              '<xf fontId="2" fillId="2" applyFont="1" applyFill="1"/>'
              '<xf numFmtId="164" applyNumberFormat="1"/>'
              '<xf numFmtId="164" fontId="3" fillId="3" applyNumberFormat="1" applyFont="1" applyFill="1"/>'
              '<xf fontId="3" fillId="3" applyFont="1" applyFill="1"/></cellXfs></styleSheet>')
    budget = xlsx_sheet([
        (["Budget prévisionnel {{app.exercise_year}} — {{org.legal_name}}"], 1),
        (["{{app.title}} · scénario « {{app.scenario_name}} »"], 0),
        ([""], 0),
        (["CHARGES"], 1),
        (["Compte", "Poste", "Montant", "Total du chapitre", "Précisions"], 2),
        (["{{#each xlsx_charges}}{{code}}", "{{label}}", "{{line_amount}}", "{{chapter_amount}}", "{{precisions}}{{/each}}"], 3),
        (["", "TOTAL DES CHARGES", ("f", "SUM(C6:C6)"), ("f", "SUM(D6:D6)"), ""], 4),
        ([""], 0),
        (["PRODUITS"], 1),
        (["Compte", "Poste", "Montant", "Total du chapitre", "Précisions"], 2),
        (["{{#each xlsx_produits}}{{code}}", "{{label}}", "{{line_amount}}", "{{chapter_amount}}", "{{precisions}}{{/each}}"], 3),
        (["", "TOTAL DES PRODUITS", ("f", "SUM(C11:C11)"), ("f", "SUM(D11:D11)"), ""], 4),
        ([""], 0),
        (["", "Écart charges − produits (doit valoir 0)", ("f", "C7-C12"), "", ""], 4),
    ], [10, 52, 16, 18, 60])
    calc = xlsx_sheet([
        (["Modalités de calcul — {{app.title}}"], 1),
        ([""], 0),
        (["Groupe", "Poste", "Détail", "Coût", "Part commerciale (%)", "Part subventionnable", "Part demandée (%)", "Montant demandé"], 2),
        (["{{#each xlsx_costs}}{{group}}", "{{poste}}", "{{label}}", "{{amount}}", "{{commercial_pct}}", "{{event_amount}}", "{{eligible_pct}}", "{{requested_amount}}{{/each}}"], 3),
        (["", "TOTAL", "", ("f", "SUM(D4:D4)"), "", ("f", "SUM(F4:F4)"), "", ("f", "SUM(H4:H4)")], 4),
    ], [26, 34, 30, 14, 14, 16, 14, 16])
    files = {
        "[Content_Types].xml": ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                                '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                                '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
                                '<Default Extension="xml" ContentType="application/xml"/>'
                                '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
                                '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
                                '<Override PartName="/xl/worksheets/sheet2.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
                                '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
                                '</Types>'),
        "_rels/.rels": ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
                        '</Relationships>'),
        "xl/workbook.xml": ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                            '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
                            '<sheets><sheet name="Budget CERFA" sheetId="1" r:id="rId1"/><sheet name="Modalités de calcul" sheetId="2" r:id="rId2"/></sheets>'
                            '<calcPr fullCalcOnLoad="1"/></workbook>'),
        "xl/_rels/workbook.xml.rels": ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                                       '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                                       '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
                                       '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet2.xml"/>'
                                       '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
                                       '</Relationships>'),
        "xl/worksheets/sheet1.xml": budget,
        "xl/worksheets/sheet2.xml": calc,
        "xl/styles.xml": styles,
    }
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in files.items():
            z.writestr(name, data)


if __name__ == "__main__":
    write_docx(os.path.join(HERE, "grant-dossier.docx"))
    write_xlsx(os.path.join(HERE, "grant-budget.xlsx"))
    print("templates/grant-dossier.docx and templates/grant-budget.xlsx written")
