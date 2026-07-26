from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from build_icus2026_review_packet import ENGLISH_ABSTRACT, TURKISH_ABSTRACT, word_count


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = PROJECT_ROOT / "docs" / "submission"
OUT_PDF = OUT_DIR / "icus2026_ozet_bildiri_degerlendirme_paketi.pdf"

BLUE = colors.HexColor("#2E74B5")
DARK_BLUE = colors.HexColor("#1F4D78")
INK = colors.HexColor("#1E1E1E")
MUTED = colors.HexColor("#5A5A5A")
LIGHT_FILL = colors.HexColor("#F2F4F7")
CALLOUT_FILL = colors.HexColor("#F4F6F9")
BORDER = colors.HexColor("#D9E2EC")


def register_fonts() -> tuple[str, str, str]:
    candidates = [
        (
            Path("C:/Windows/Fonts/calibri.ttf"),
            Path("C:/Windows/Fonts/calibrib.ttf"),
            Path("C:/Windows/Fonts/calibrii.ttf"),
            "Calibri",
        ),
        (
            Path("C:/Windows/Fonts/arial.ttf"),
            Path("C:/Windows/Fonts/arialbd.ttf"),
            Path("C:/Windows/Fonts/ariali.ttf"),
            "Arial",
        ),
        (
            Path("C:/Windows/Fonts/dejavusans.ttf"),
            Path("C:/Windows/Fonts/dejavusans-bold.ttf"),
            Path("C:/Windows/Fonts/dejavusans-oblique.ttf"),
            "DejaVu",
        ),
    ]
    for regular, bold, italic, family in candidates:
        if regular.exists() and bold.exists() and italic.exists():
            pdfmetrics.registerFont(TTFont(family, str(regular)))
            pdfmetrics.registerFont(TTFont(f"{family}-Bold", str(bold)))
            pdfmetrics.registerFont(TTFont(f"{family}-Italic", str(italic)))
            return family, f"{family}-Bold", f"{family}-Italic"
    return "Helvetica", "Helvetica-Bold", "Helvetica-Oblique"


FONT, FONT_BOLD, FONT_ITALIC = register_fonts()


def styles():
    sample = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "TitleCustom",
            parent=sample["Title"],
            fontName=FONT_BOLD,
            fontSize=22,
            leading=26,
            textColor=BLUE,
            alignment=TA_LEFT,
            spaceAfter=4,
        ),
        "subtitle": ParagraphStyle(
            "SubtitleCustom",
            parent=sample["Normal"],
            fontName=FONT,
            fontSize=12.5,
            leading=16,
            textColor=MUTED,
            spaceAfter=14,
        ),
        "h1": ParagraphStyle(
            "Heading1Custom",
            parent=sample["Heading1"],
            fontName=FONT_BOLD,
            fontSize=15.5,
            leading=20,
            textColor=BLUE,
            spaceBefore=14,
            spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "Heading2Custom",
            parent=sample["Heading2"],
            fontName=FONT_BOLD,
            fontSize=12.5,
            leading=16,
            textColor=BLUE,
            spaceBefore=10,
            spaceAfter=5,
        ),
        "body": ParagraphStyle(
            "BodyCustom",
            parent=sample["Normal"],
            fontName=FONT,
            fontSize=10.6,
            leading=13.6,
            textColor=INK,
            alignment=TA_JUSTIFY,
            spaceAfter=6,
        ),
        "body_left": ParagraphStyle(
            "BodyLeftCustom",
            parent=sample["Normal"],
            fontName=FONT,
            fontSize=10.6,
            leading=13.6,
            textColor=INK,
            alignment=TA_LEFT,
            spaceAfter=6,
        ),
        "muted": ParagraphStyle(
            "MutedCustom",
            parent=sample["Normal"],
            fontName=FONT_ITALIC,
            fontSize=9.5,
            leading=12,
            textColor=MUTED,
            spaceAfter=6,
        ),
        "small": ParagraphStyle(
            "SmallCustom",
            parent=sample["Normal"],
            fontName=FONT,
            fontSize=9.2,
            leading=11.4,
            textColor=INK,
        ),
        "table_label": ParagraphStyle(
            "TableLabelCustom",
            parent=sample["Normal"],
            fontName=FONT_BOLD,
            fontSize=9.2,
            leading=11.2,
            textColor=DARK_BLUE,
        ),
        "table_value": ParagraphStyle(
            "TableValueCustom",
            parent=sample["Normal"],
            fontName=FONT,
            fontSize=9.2,
            leading=11.2,
            textColor=INK,
        ),
        "callout": ParagraphStyle(
            "CalloutCustom",
            parent=sample["Normal"],
            fontName=FONT,
            fontSize=10,
            leading=12.8,
            textColor=INK,
            spaceAfter=0,
        ),
    }


S = styles()


def p(text: str, style="body") -> Paragraph:
    text = text.replace("&", "&amp;")
    return Paragraph(text, S[style])


def add_paragraphs(story, text: str):
    for para in text.split("\n\n"):
        story.append(p(para.strip()))


def kv_table(rows, col_widths=(1.65 * inch, 4.85 * inch), header=None):
    data = []
    if header:
        data.append([Paragraph(f"<b>{header}</b>", S["table_label"]), ""])
    for label, value in rows:
        data.append([Paragraph(label, S["table_label"]), Paragraph(value, S["table_value"])])
    table = Table(data, colWidths=list(col_widths), hAlign="CENTER")
    commands = [
        ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("BACKGROUND", (0, 0), (0, -1), LIGHT_FILL),
    ]
    if header:
        commands.extend(
            [
                ("SPAN", (0, 0), (1, 0)),
                ("BACKGROUND", (0, 0), (1, 0), LIGHT_FILL),
            ]
        )
    table.setStyle(TableStyle(commands))
    return table


def callout(label: str, text: str):
    content = Paragraph(f"<font name='{FONT_BOLD}' color='#1F4D78'>{label}: </font>{text}", S["callout"])
    table = Table([[content]], colWidths=[6.5 * inch], hAlign="CENTER")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), CALLOUT_FILL),
                ("BOX", (0, 0), (-1, -1), 0.6, BORDER),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    return table


def bullet_list(items):
    return ListFlowable(
        [ListItem(Paragraph(item, S["body_left"]), leftIndent=16) for item in items],
        bulletType="bullet",
        start="bulletchar",
        bulletFontName=FONT,
        bulletFontSize=8,
        leftIndent=16,
    )


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont(FONT, 8.5)
    canvas.setFillColor(MUTED)
    canvas.drawRightString(7.5 * inch, 10.55 * inch, "ICUS 2026 | Öğrenci Görüş Paketi")
    canvas.drawCentredString(4.25 * inch, 0.45 * inch, f"Taslak belge | 13 Haziran 2026 | Sayfa {doc.page}")
    canvas.restoreState()


def build():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUT_PDF),
        pagesize=letter,
        rightMargin=1 * inch,
        leftMargin=1 * inch,
        topMargin=0.9 * inch,
        bottomMargin=0.8 * inch,
        title="ICUS 2026 Özet Bildiri Değerlendirme Paketi",
        author="Yusuf Eminoğlu",
    )

    story = [
        Paragraph("Özet Bildiri Değerlendirme Paketi", S["title"]),
        Paragraph("ICUS 2026 / 11. Kent Araştırmaları Kongresi için öğrenci görüş taslağı", S["subtitle"]),
        kv_table(
            [
                ("Çalışma yönü", "Sokak bazlı kentsel doku analitiği, kentsel morfoloji ve iklim dirençliliği"),
                ("Kongre", "11. Kent Araştırmaları Kongresi / ICUS 2026, Ankara, 12-14 Ekim 2026"),
                ("Ana tema", "İklim Değişikliğine Dirençli Kentler"),
                ("Teslim tipi", "Yalnızca özet bildiri. Tam metin bu kongreye gönderilmeyecek; genişletilmiş makale daha sonra ayrı bir dergiye hedeflenecek."),
                ("Özet son tarihi", "29 Haziran 2026"),
                ("Sunum", "Kongre sunumunu Halil Topçu yapacak şekilde planlanmaktadır."),
            ],
            header="Belge amacı",
        ),
        Spacer(1, 9),
        callout(
            "Kısa öneri",
            "Çalışmayı eklenti tanıtımı olarak değil, İzmir Körfezi çevresindeki farklı kentsel dokuların iklim dirençliliği açısından karşılaştırılması olarak konumlandırmak daha güçlüdür.",
        ),
        Spacer(1, 12),
        Paragraph("1. Yazar ve Sunum Bilgisi", S["h1"]),
        kv_table(
            [
                ("1. yazar", "Yusuf Eminoğlu"),
                ("E-posta", "yusuf.eminoglu@deu.edu.tr"),
                ("ORCID", "https://orcid.org/0009-0005-6000-2934"),
                ("Kurum / görev", "Araştırma Görevlisi ve Doktora Adayı, Şehir ve Bölge Planlama Bölümü, Dokuz Eylül Üniversitesi, İzmir, Türkiye"),
                ("2. yazar / sunucu", "Halil Topçu"),
                ("E-posta", "halil.topcu2001@hotmail.com"),
                ("ORCID", "https://orcid.org/0009-0009-3366-179X"),
                ("Kurum / program", "Yüksek Lisans Öğrencisi, İzmir Demokrasi Üniversitesi, Fen Bilimleri Enstitüsü, Kentsel Tasarım Programı"),
            ],
            col_widths=(1.8 * inch, 4.7 * inch),
        ),
        Spacer(1, 3),
        Paragraph(
            "Not: CMT sistemindeki kör değerlendirme alanlarında yazar bilgisi özet gövdesine yazılmamalıdır. Bu bilgiler yalnızca sistemdeki yazar alanlarına girilmelidir.",
            S["muted"],
        ),
        Paragraph("2. Çalışma Konumu", S["h1"]),
    ]

    add_paragraphs(
        story,
        "Bu özet bildiri, iklim dirençliliğini yalnızca tehlike katmanları veya idari birim skorları üzerinden değil, kentsel doku ve sokak ağı ölçeğinde okumayı hedeflemektedir. Ana fikir, İzmir Körfezi çevresindeki farklı doku tiplerinin morfolojik, erişilebilirlik ve dirençlilik göstergeleri üzerinden karşılaştırılmasıdır.\n\n"
        "Teknik iş akışı PlanX Urban Resilience şemsiyesi altında anlatılacaktır. Ancak analiz omurgası, gerektiğinde PlanX ana eklentisinin morfoloji, space syntax, ağ merkeziliği, Spacematrix, erişilebilirlik ve mikroiklim araçlarıyla desteklenecektir. Bu ifade biçimi çalışmayı yazılım tanıtımı olmaktan çıkarır ve kentsel tasarım ile planlama araştırması olarak konumlandırır.",
    )

    story.extend(
        [
            Paragraph("3. Önerilen Örnek Alan Mantığı", S["h1"]),
            Paragraph("Halil’in özellikle değerlendirmesi istenen kısım örnek alan seçimi ve doku tipolojisidir.", S["muted"]),
            bullet_list(
                [
                    "Tarihî merkez / geleneksel yoğun doku: Kemeraltı ve çevresi gibi alanlar.",
                    "Planlı ızgara ve yüksek erişilebilirlik dokusu: Alsancak, Karşıyaka veya Bostanlı çevresi.",
                    "Orta-yüksek yoğunluklu apartman blok dokusu: Göztepe, Hatay, Bayraklı veya benzeri kesitler.",
                    "Kıyı dönüşüm ve karma kullanım dokusu: Bayraklı-Salhane hattı gibi dönüşen parçalar.",
                    "Sanayi ve lojistik kenar: Çiğli, Atatürk OSB veya liman/arka alanları.",
                    "Yamaç veya kademeli gelişmiş konut dokusu: Kadifekale çevresi, Bornova yamaçları veya benzer örnekler.",
                    "Periferik yeni gelişme alanı: Körfezle ilişkili yeni konut/gelişme kesitleri.",
                ]
            ),
            Paragraph("4. CMT’ye Uygun Taslak Başlıklar", S["h1"]),
            Paragraph("Türkçe başlık", S["h2"]),
            Paragraph(
                "<b>Sokak Bazlı Kentsel Doku Analitiği ile İklim Dirençliliği: İzmir Körfezi Örneğinde Açık Kaynaklı Bir QGIS İş Akışı</b>",
                S["body_left"],
            ),
            Paragraph("English title", S["h2"]),
            Paragraph(
                "<b>Street-Based Urban Tissue Analytics for Climate Resilience: An Open-Source QGIS Workflow in the Izmir Gulf</b>",
                S["body_left"],
            ),
            PageBreak(),
            Paragraph("5. Türkçe Özet Taslağı", S["h1"]),
            Paragraph(f"Kelime sayısı: {word_count(TURKISH_ABSTRACT)}", S["muted"]),
        ]
    )

    add_paragraphs(story, TURKISH_ABSTRACT)
    story.extend(
        [
            Paragraph("Türkçe Anahtar Kelimeler", S["h2"]),
            Paragraph("kentsel dirençlilik; kentsel morfoloji; kentsel doku; sokak ağı; açık kaynak CBS", S["body_left"]),
            Paragraph("6. English Abstract Draft", S["h1"]),
            Paragraph(f"Word count: {word_count(ENGLISH_ABSTRACT)}", S["muted"]),
        ]
    )
    add_paragraphs(story, ENGLISH_ABSTRACT)
    story.extend(
        [
            Paragraph("English Keywords", S["h2"]),
            Paragraph("urban resilience; urban morphology; urban fabric; street networks; open-source GIS", S["body_left"]),
            Paragraph("7. Halil Topçu’dan Beklenen Görüş", S["h1"]),
            bullet_list(
                [
                    "Örnek doku aileleri İzmir Körfezi için doğru ve savunulabilir mi?",
                    "Kentsel tasarım açısından hangi 5-7 örnek alan daha temsilî olur?",
                    "Analiz birimi 400/800 m yürüme yakalaması mı, 500 m grid mi, yoksa sokak koridoru mu olmalı?",
                    "Başlık çalışma fikrini doğru taşıyor mu?",
                    "Özet metni öğrencinin sunabileceği kadar anlaşılır mı, yoksa yöntem kısmı sadeleştirilmeli mi?",
                    "Kongrede sunum yapılırken hangi harita/şema dili daha iyi çalışır?",
                ]
            ),
            Paragraph("8. Kongre Uyum Kontrolü", S["h1"]),
            kv_table(
                [
                    ("Özet uzunluğu", f"Türkçe özet {word_count(TURKISH_ABSTRACT)} kelime. CMT alanına göre gerekirse son sıkıştırma yapılacak."),
                    ("Dil koşulu", "Türkçe ve İngilizce başlık, özet ve anahtar kelimeler hazırlanmıştır."),
                    ("Yazar bilgisi", "Özet gövdesinde yazar bilgisi yoktur; bilgiler yalnızca metadata kısmındadır."),
                    ("Kaynakça / tablo / şekil", "Özet gövdesinde kaynakça, tablo veya şekil yoktur."),
                    ("Kongre teması", "İklim dirençliliği, kentsel kırılganlık, mekânsal adalet, yerel planlama ve kentsel ekosistemler temalarıyla uyumludur."),
                    ("Tam metin kararı", "Bu kongreye tam metin gönderilmeyecek; genişletilmiş makale başka bir dergiye hazırlanacaktır."),
                ],
                col_widths=(1.75 * inch, 4.75 * inch),
            ),
        ]
    )

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(OUT_PDF)


if __name__ == "__main__":
    build()
