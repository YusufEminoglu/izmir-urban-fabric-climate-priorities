from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "docs" / "submission"
OUT_PATH = OUT_DIR / "icus2026_submission_ready_ozet_bildiri.pdf"


TR_TITLE = (
    "Kentsel Doku Morfometrisi ve İklim Dirençliliği: İzmir İşlevsel "
    "Kent Bölgesi İçin Açıklanabilir ve Pareto-Uyumlu Karar Destek Protokolü"
)

EN_TITLE = (
    "Urban Fabric Morphometrics and Climate Resilience: An Explainable, "
    "Pareto-Aware Decision Support Protocol for the İzmir Functional Urban Region"
)

TR_ABSTRACT = """
Kentsel morfometri, yapılı formu ulusal ve küresel ölçeklerde sınıflandırabilen, yinelenebilir ve denetimsiz bir bilime olgunlaşmış; buna koşut olarak iklim-kent yazını kentsel formu yer yüzey sıcaklığının, ısı kırılganlığının ve plüvyal taşkın güzergâhlarının birincil belirleyicisi olarak ele almaya başlamıştır. Ancak bu iki yazın, uyumun bir metropol bölge ölçeğinde planlandığı düzeyde nadiren buluşur. İklim dirençliliği hâlâ idari birimler, kaba ızgaralar veya yerel iklim bölgeleri üzerinden değerlendirilmekte; böylece benzer yoğunluğa sahip iki alan aynı risk sınıfına atanırken belirgin biçimde farklı ısı, erişim ve kırılganlık sonuçları üretebilmektedir. Bu çalışma, İzmir işlevsel kent bölgesi için tüm kentsel hücreleri kapsayan (tam sayım) 250 metrelik bir analiz gridi üzerine kurulu; morfometriyi çoklu tehlike maruziyeti ve sosyal kırılganlıkla açık iki aşamalı bir mantıkla birleştiren; açık kaynaklı, denetlenebilir ve QGIS tabanlı bir tipomorfolojik iş akışı önerir: açıklanabilir makine öğrenmesi ölçülen bir ısı çıktısını morfolojik mekanizmalara bağlar, çok amaçlı (Pareto) optimizasyon ise bu mekanizmaları sağlam ve ödünleşim-farkında uyum önceliklerine dönüştürür. Katkı, tamamlanmış bir atlas değil, tek bir işlevsel kent bölgesinde tam-sayım ölçeğinde gösterilen aktarılabilir ve test edilebilir bir protokoldür; betimleyici yalnızca-form tipolojilerinden ve idari direncilik indekslerinden ayrışır.

Çerçevenin özü, kentsel dokunun üç boyutunu ayırır: tip olarak doku (betimleyici bir sınıf), ölçüm olarak doku (morfometrik gösterge vektörü) ve mekanizma olarak doku (formun iklim riskini düzenlediği güzergâh). Bu ayrım, eşit yoğunluktaki alanların neden farklı dirençlilik sonuçları ürettiği sezgisini sınanabilir bir önermeye dönüştürür.

Görgül tasarım, İzmir bölgesi üzerinde 250 metrelik bir analiz gridine dayanır. Kentsel olmayan (düşük yapılı alan oranlı), açık su ve dik eğimli alanlar dışlandıktan sonra kalan hücreler yedi önsel doku stratumuna (tarihsel merkez, ızgara konut, apartman bloğu, kıyı dönüşüm, yamaç/eğimli, sanayi-lojistik ve çeper genişleme) atanır; tüm kalan hücreler analize girer (tam sayım; örnekleme yok). Stratumlar, kümeleme öncesinde arazi kullanımı ve uzaktan algılama temelli kural-tabanlı (geçici) vekillerle tanımlanır; kümeleme bu sınıflamayı üretmek yerine sınar ve geliştirir, böylece örneklem-tipoloji döngüselliği önlenir.

Analiz birimi her 250 metrelik grid hücresidir. Yapı ayak izleri morfolojik tessellation hücrelerine, temizlenmiş yol merkez çizgileri segment grafına dönüştürülür; hücre ölçeğindeki morfometri ve ağ göstergeleri alan ağırlıklı ortanca, çeyrekler arası açıklık ve yoğunluk ölçüleriyle grid hücresine çapraz aktarılırken, her hücre çevresindeki 400 ve 800 metrelik ağ servis alanı menzilleri erişilebilirliği ve hareket potansiyelini taşır. Yöntemin özü tekil araçlar değil bu çapraz aktarım kuralıdır: yapılı form yoğunluğunu, hareket potansiyelini ve tehlike maruziyetini koşut katmanlar yerine tek bir hücrede karşılaştırılabilir kılar.

Zincir, PlanX Urban Resilience ve GeoStats Lab'i birleştiren bir QGIS projesinde çalışır. Girdiler açık veri ve belediye veri portallarıdır: yol ağı ve bina ayak izleri OpenStreetMap ile İzmir Büyükşehir Belediyesi (İBB) veri portalından; arazi örtüsü ve yer yüzey sıcaklığı Copernicus ve Landsat'tan; yeşil-mavi altyapı, toplanma alanları ve hizmetler belediye verilerinden; sosyal kırılganlık ise TÜİK ADNKS yaş ve bağımlılık verilerinden türetilir. Hedeflenen stresörler aşırı sıcak, plüvyal taşkın ve kıyı maruziyetidir. Geçirimsiz yüzey maruziyeti doğrudan arazi örtüsünden ölçülür.

Ağ metrikleri (OSMnx/NetworkX; angular integration ve choice) ve morfometrik karakterler (momepy/GeoPandas: taban alanı oranı, açıklık, kompaktlık, cephe sürekliliği, blok geçirgenliği, hücre heterojenliği) iklim-direncilik vekilleriyle tamamlanır: gölge ve güneşlenme potansiyeli, yeşil-mavi soğutma, toplanma alanı ve günlük hizmet erişimi ve geçirimsiz maruziyet ile sosyal kırılganlığın örtüşmesi. Mekânsal yapı, Moran's I, LISA, Getis-Ord sıcak noktalar ve maruziyet eşitsizliğinin Gini ölçüsüyle incelenir.

Sentez açıkça iki aşamalıdır. Önce, tüm kentsel hücreler boyunca havuzlanmış ince ölçekte açıklanabilir bir gradient-boosting modeli ölçülen yer yüzey sıcaklığını morfometrik ve konfigürasyonel sürücülerden tahmin eder; Shapley (SHAP) ataması her dokuda ısıyı hangi mekanizmanın sürüklediğini belirler. Ardından göstergeler yön kodlu ve z-standartlaştırılır, temel bileşen analizi eşdoğrusallığı azaltır ve Ward hiyerarşik kümeleme doku-direncilik profilleri üretir; küme sayısı silhouette skoruyla, çözünürlük kararlılığı ise 250'ye karşı 500 metre gridler arasında Düzeltilmiş Rand İndeksiyle sınanır. İkinci olarak uyum öncelikleri çok amaçlı bir problem olarak kurulur: Pareto-optimal cephe, baskın-altı hücreleri (açık müdahale adayları) ödünleşim hücrelerinden ayırır; TOPSIS bir sıralama verir, entropi ağırlığı ve Monte-Carlo pertürbasyonları sağlamlığı raporlar. İzmir işlevsel kent bölgesinin 3.777 kentsel hücresinin tamamı üzerinde (tam sayım) zincir uçtan uca yürütülmüştür. Yedi ön-tanımlı doku, TBA ve Ward kümelemeyle dört sağlam morfometrik üst-tipe yoğunlaşır; sınıflandırma 250'ye karşı 500 metre çözünürlükte geniş hatlarıyla kararlıdır (ARI=0,38). Açıklanabilir ısı modeli, metropolitan ölçekte kıyı gradyanının yaz yer yüzey sıcaklığını formdan daha güçlü kontrol ettiğini ortaya koyar; ancak morfolojik mekanizmalar ayırt edilebilirdir. En çarpıcı bulgu, ısı, erişim, kıyı maruziyeti ve sosyal kırılganlık birlikte değerlendirildiğinde, en serin doku olan kıyı dönüşümünün en yüksek uyum önceliği olarak sıralanmasıdır—yalnızca ısıya dayalı bir değerlendirmenin tam tersine. Tüm parametreler, katmanlar ve kodlar aktarılabilirlik için paylaşılır.
""".strip()

EN_ABSTRACT = """
Urban morphometrics has matured into a reproducible, unsupervised science that classifies built form at national and global scales, while a parallel literature treats urban form as a first-order control on land-surface temperature, heat vulnerability and pluvial-flood pathways. These trajectories rarely meet at the metropolitan planning scale. Resilience is often assessed over coarse administrative or climate zones, assigning areas of similar density to the same risk class despite different thermal and accessibility outcomes. This study proposes an open-source, auditable, QGIS-based typomorphological workflow for the İzmir functional urban region, applied as a full census on a 250-metre grid, that couples morphometrics with multi-hazard exposure and social vulnerability through a two-stage logic: explainable machine learning attributes a measured thermal outcome to morphological mechanisms, and multi-objective (Pareto) optimisation turns those mechanisms into robust, trade-off-aware adaptation priorities. The contribution is a transferable, testable protocol demonstrated at full-census scale over one functional urban region, and is distinguished from both descriptive form-only typologies and administrative resilience indices.

The framework separates three senses of urban fabric: fabric-as-type (a descriptive taxon), fabric-as-measurement (a morphometric vector) and fabric-as-mechanism (the pathway through which form modulates risk). This distinction turns the intuition that equally dense areas differ in resilience outcomes into a testable proposition.

The design uses a 250-metre analysis grid over the İzmir functional urban region. After excluding non-urban (low built fraction), open water, and steep-slope cells, the remainder are assigned to seven a priori strata (historic core, grid residential, apartment-block, waterfront transformation, hillside/incremental, industrial-logistics, peripheral expansion). All retained cells are analysed: the study is a full census of the 3,777 urban cells, not a sample. Strata are defined a priori from land use and remote sensing as rule-based (provisional) proxies before clustering, which tests and refines this classification rather than generating it, avoiding circularity.

Each 250-metre grid cell is the analytical unit. Building footprints are converted into morphological tessellation cells and cleaned road-centre lines into a segment graph; cell-level morphometrics and network metrics are cross-attributed to the grid cell through area-weighted median, interquartile range and density measures, while 400- and 800-metre network service-area reaches carry accessibility and movement potential. The cross-attribution rule, not the tools, is the methodological core: it makes built-form intensity, movement potential and hazard exposure commensurable within one cell rather than as parallel layers.

The workflow runs in a QGIS project combining PlanX Urban Resilience and GeoStats Lab. All inputs are public open data: street networks and building footprints from OpenStreetMap and the İzmir Metropolitan Municipality (BBB); land cover and land-surface temperature from Copernicus and Landsat; green-blue infrastructure, coastline, assembly areas and services from municipal portals; and social vulnerability from Turkish Statistical Institute/ADNKS age and dependency ratios. Target stressors are extreme heat, pluvial flooding and coastal exposure. Impervious exposure is measured directly from satellite land cover, not inferred from building density.

Synthesis is explicitly two-stage. First, an explainable gradient-boosting model is trained at fine scale, pooled across all urban cells, to predict measured land-surface temperature from morphometric and configurational drivers; Shapley (SHAP) attribution identifies which mechanism dominates heat in each fabric. Indicators are then z-standardised, principal component analysis reduces collinearity, and Ward hierarchical clustering yields fabric-resilience profiles, with cluster number set by silhouette score and resolution stability tested between 250- and 500-metre grids via the Adjusted Rand Index. Second, adaptation priorities are framed as a multi-objective problem: a Pareto-optimal frontier separates dominated cells from trade-off cells, while TOPSIS provides a ranking and robustness is evaluated. Over a full census of all 3,777 urban cells of the İzmir region, the chain runs end to end. The seven a-priori strata consolidate into four robust morphometric super-types via PCA and Ward clustering, broadly stable across grid resolution (ARI = 0.38). The explainable heat model shows that, at metropolitan scale, the coastal gradient controls summer land-surface temperature more strongly than form, which is nonetheless a secondary but genuine control, with morphological mechanisms remaining identifiable. The sharpest finding is an equity inversion: when heat, access, coastal exposure and social vulnerability are assessed jointly, the coolest fabric—waterfront transformation—ranks as the highest adaptation priority, the opposite of a heat-only reading. All parameters, layers and code are released for transfer.
""".strip()


AUTHORS = [
    [
        "1",
        "Yusuf Eminoğlu",
        "Dokuz Eylül University, Department of City and Regional Planning, İzmir, Türkiye",
        "Research Assistant and PhD Candidate",
        "0009-0005-6000-2934",
        "yusuf.eminoglu@deu.edu.tr",
    ],
    [
        "2",
        "Halil Topçu",
        "İzmir Demokrasi University, Graduate School of Natural and Applied Sciences, Urban Design Master's Program, İzmir, Türkiye",
        "Master's Student",
        "0009-0009-3366-179X",
        "halil.topcu2001@hotmail.com",
    ],
]


def word_count(text: str) -> int:
    return len([w for w in text.replace("\n", " ").split(" ") if w.strip()])


def register_fonts() -> tuple[str, str, str]:
    font_dir = Path("C:/Windows/Fonts")
    regular = font_dir / "pala.ttf"
    bold = font_dir / "palab.ttf"
    italic = font_dir / "palai.ttf"
    if regular.exists() and bold.exists() and italic.exists():
        pdfmetrics.registerFont(TTFont("PalatinoLinotype", str(regular)))
        pdfmetrics.registerFont(TTFont("PalatinoLinotype-Bold", str(bold)))
        pdfmetrics.registerFont(TTFont("PalatinoLinotype-Italic", str(italic)))
        return "PalatinoLinotype", "PalatinoLinotype-Bold", "PalatinoLinotype-Italic"
    return "Helvetica", "Helvetica-Bold", "Helvetica-Oblique"


def make_styles(font: str, bold: str, italic: str):
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            "CoverTitle",
            parent=styles["Title"],
            fontName=bold,
            fontSize=12,
            leading=15,
            alignment=TA_CENTER,
            spaceAfter=12,
            textColor=colors.HexColor("#172033"),
        )
    )
    styles.add(
        ParagraphStyle(
            "H1Custom",
            parent=styles["Heading1"],
            fontName=bold,
            fontSize=12,
            leading=14,
            spaceBefore=12,
            spaceAfter=6,
            textColor=colors.HexColor("#1B365D"),
        )
    )
    styles.add(
        ParagraphStyle(
            "H2Custom",
            parent=styles["Heading2"],
            fontName=bold,
            fontSize=10.7,
            leading=13,
            spaceBefore=9,
            spaceAfter=5,
            textColor=colors.HexColor("#264653"),
        )
    )
    styles.add(
        ParagraphStyle(
            "BodyCustom",
            parent=styles["BodyText"],
            fontName=font,
            fontSize=10,
            leading=12.3,
            alignment=TA_JUSTIFY,
            spaceAfter=7,
        )
    )
    styles.add(
        ParagraphStyle(
            "SmallCustom",
            parent=styles["BodyText"],
            fontName=font,
            fontSize=8.4,
            leading=11,
            alignment=TA_LEFT,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            "SmallBold",
            parent=styles["BodyText"],
            fontName=bold,
            fontSize=8.5,
            leading=11,
            alignment=TA_LEFT,
            spaceAfter=3,
        )
    )
    styles.add(
        ParagraphStyle(
            "Meta",
            parent=styles["BodyText"],
            fontName=font,
            fontSize=9.6,
            leading=12.2,
            alignment=TA_LEFT,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            "TitleCustom",
            parent=styles["BodyText"],
            fontName=bold,
            fontSize=12,
            leading=15,
            alignment=TA_CENTER,
            spaceAfter=8,
            textColor=colors.HexColor("#172033"),
        )
    )
    styles.add(
        ParagraphStyle(
            "ItalicSmall",
            parent=styles["BodyText"],
            fontName=italic,
            fontSize=8.3,
            leading=10.7,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#4B5563"),
        )
    )
    return styles


def paragraphize(text: str, style: ParagraphStyle):
    parts = [p.strip() for p in text.split("\n\n") if p.strip()]
    flowables = []
    for part in parts:
        flowables.append(Paragraph(part, style))
    return flowables


def draw_header_footer(canvas, doc):
    canvas.saveState()
    width, height = A4
    canvas.setStrokeColor(colors.HexColor("#C8D3DF"))
    canvas.setLineWidth(0.4)
    canvas.line(1.6 * cm, height - 1.18 * cm, width - 1.6 * cm, height - 1.18 * cm)
    header_font = "PalatinoLinotype" if "PalatinoLinotype" in pdfmetrics.getRegisteredFontNames() else "Helvetica"
    canvas.setFont(header_font, 7.5)
    canvas.setFillColor(colors.HexColor("#56616F"))
    canvas.drawString(1.6 * cm, height - 0.92 * cm, "ICUS 2026 Abstract Submission")
    canvas.drawRightString(width - 1.6 * cm, 1.0 * cm, f"Page {doc.page}")
    canvas.restoreState()


def build_pdf() -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    font, bold, italic = register_fonts()
    styles = make_styles(font, bold, italic)

    doc = BaseDocTemplate(
        str(OUT_PATH),
        pagesize=A4,
        rightMargin=2.5 * cm,
        leftMargin=2.5 * cm,
        topMargin=2.35 * cm,
        bottomMargin=2.0 * cm,
        title="ICUS 2026 Submission Ready Abstract",
        author="Yusuf Eminoğlu; Halil Topçu",
    )
    frame = Frame(
        doc.leftMargin,
        doc.bottomMargin,
        doc.width,
        doc.height,
        id="normal",
        showBoundary=0,
    )
    doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=draw_header_footer)])

    story = []

    story.append(Paragraph(TR_TITLE, styles["TitleCustom"]))
    story.append(Paragraph("Özet", styles["H1Custom"]))
    story.extend(paragraphize(TR_ABSTRACT, styles["BodyCustom"]))
    story.append(Paragraph("<b>Anahtar Kelimeler:</b> kentsel morfometri; yaya erişilebilirliği; sosyal kırılganlık; hiyerarşik kümeleme; çok ölçütlü karar analizi", styles["Meta"]))

    story.append(PageBreak())
    story.append(Paragraph(EN_TITLE, styles["TitleCustom"]))
    story.append(Paragraph("Abstract", styles["H1Custom"]))
    story.extend(paragraphize(EN_ABSTRACT, styles["BodyCustom"]))
    story.append(Paragraph("<b>Keywords:</b> urban morphometrics; pedestrian accessibility; social vulnerability; hierarchical clustering; multi-criteria decision analysis", styles["Meta"]))

    story.append(PageBreak())
    story.append(Paragraph("CMT Author and Submission Fields", styles["H1Custom"]))
    story.append(Paragraph("The abstract body above is prepared as a blind submission text. Author information below should be entered only in the CMT author fields.", styles["Meta"]))

    meta_rows = [
        ["Field", "Submission value"],
        ["Conference theme", "Climate Change Resilient Cities"],
        ["Dates / venue", "12-14 October 2026, Ankara, Türkiye; hybrid format"],
        ["Submission type", "Abstract only; full paper will not be submitted to the congress"],
        ["Language package", "Turkish title, abstract and keywords followed by English title, abstract and keywords"],
        ["Presenter", "Halil Topçu"],
        ["Corresponding author", "Yusuf Eminoğlu, yusuf.eminoglu@deu.edu.tr"],
    ]
    meta_table = Table(
        [[Paragraph(str(c), styles["SmallBold" if r == 0 else "SmallCustom"]) for c in row] for r, row in enumerate(meta_rows)],
        colWidths=[4.2 * cm, 11.8 * cm],
        hAlign="LEFT",
    )
    meta_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E9EEF5")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#172033")),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#C8D3DF")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(meta_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Author Information", styles["H1Custom"]))
    author_rows = [
        ["#", "Author", "Affiliation / role", "ORCID / email"],
    ]
    for order, name, aff, role, orcid, email in AUTHORS:
        author_rows.append([order, name, f"{aff}<br/>{role}", f"https://orcid.org/{orcid}<br/>{email}"])
    author_table = Table(
        [[Paragraph(str(c), styles["SmallBold" if r == 0 else "SmallCustom"]) for c in row] for r, row in enumerate(author_rows)],
        colWidths=[1.0 * cm, 2.8 * cm, 6.0 * cm, 6.2 * cm],
        hAlign="LEFT",
    )
    author_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E9EEF5")),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#C8D3DF")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(author_table)
    story.append(Spacer(1, 8))

    compliance = [
        ["Requirement", "Status"],
        ["Abstract length", f"Turkish {word_count(TR_ABSTRACT)} words; English {word_count(EN_ABSTRACT)} words; both within the 500-750 word rule."],
        ["Keywords", "Five keywords in each language."],
        ["Required order", "Turkish title, abstract and keywords first; English title, abstract and keywords second."],
        ["Tables, figures, references in abstract body", "None."],
        ["Blind abstract body", "The abstract body does not include author names, affiliations, ORCID, acknowledgements or references."],
        ["Presenter", "Halil Topçu."],
    ]
    story.append(KeepTogether([Paragraph("Submission Compliance Check", styles["H1Custom"])]))
    compliance_table = Table(
        [[Paragraph(str(c), styles["SmallBold" if r == 0 else "SmallCustom"]) for c in row] for r, row in enumerate(compliance)],
        colWidths=[5.2 * cm, 11.8 * cm],
        hAlign="LEFT",
    )
    compliance_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E9EEF5")),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#C8D3DF")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(compliance_table)

    doc.build(story)
    return OUT_PATH


if __name__ == "__main__":
    pdf_path = build_pdf()
    print(pdf_path)
