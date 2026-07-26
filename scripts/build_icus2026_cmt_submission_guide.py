from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PDF_SCRIPT = ROOT / "scripts" / "build_icus2026_submission_ready_pdf.py"
OUT_PATH = ROOT / "docs" / "submission" / "icus2026_cmt_submission_guide.txt"


def load_pdf_module():
    spec = importlib.util.spec_from_file_location("icus_pdf", PDF_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def main() -> Path:
    m = load_pdf_module()
    tr_keywords = (
        "kentsel morfometri, yaya erişilebilirliği, sosyal kırılganlık, "
        "hiyerarşik kümeleme, çok ölçütlü karar analizi"
    )
    en_keywords = (
        "urban morphometrics, pedestrian accessibility, social vulnerability, "
        "hierarchical clustering, multi-criteria decision analysis"
    )

    guide = f"""ICUS 2026 CMT SUBMISSION GUIDE
Generated from the current final abstract package.

IMPORTANT
- CMT ekranındaki 'Bildiri Özeti / Abstract' alanı tek bir 500-750 kelimelik özet alanı gibi görünüyor.
- Türkçe ve İngilizce özet birlikte 7000 karakter sınırını aşıyor. Bu nedenle ana CMT abstract alanına Türkçe sunum için yalnızca Türkçe özeti yapıştırın.
- Sistem ayrı bir English abstract alanı veya dosya yükleme alanı açarsa, aşağıdaki English Title / English Abstract / English Keywords bloklarını ayrıca kullanın.
- Özet gövdesine yazar adı, ORCID, kurum, kaynakça, tablo veya şekil eklemeyin.
- Resmi yönergedeki etik/özgünlük hükümleri nedeniyle, göndermeden önce metni Yusuf Eminoğlu ve Halil Topçu olarak son kez okuyup akademik sorumluluğunuzla nihai yazar metni haline getirin.

------------------------------------------------------------
MAIN CMT FIELDS
------------------------------------------------------------

Title
{m.TR_TITLE}

Authors
Primary contact should remain:
Yusuf Eminoğlu
Email: yusuf.eminoglu@deu.edu.tr
Organization: Dokuz Eylül University
Country/Region: Turkey

Add co-author:
Email: halil.topcu2001@hotmail.com
First Name: Halil
Last Name: Topçu
Organization: İzmir Demokrasi University
Country/Region: Turkey

Recommended Subject Areas
1. Resilient Cities and Urban Policies
2. Adaptation policies and urban strategies
3. Disaster risks, inequalities, and spatial justice
4. Disaster management, urban planning, and water governance
5. Biodiversity, green infrastructure, and ecological resilience (optional secondary fit)

Additional Question 1 - Başvuru Onayı / Submission Confirmation
Select: I agree

Additional Question 2 - Yazarlar ve Sıralama Bilgisi
Paste:
1. Yusuf Eminoğlu - Sorumlu Yazar / Corresponding Author
2. Halil Topçu - Sunucu Yazar / Presenter

Additional Question 3 - Akademik Unvan ve Kurum
Paste:
Yusuf Eminoğlu - Research Assistant and PhD Candidate, Department of City and Regional Planning, Dokuz Eylül University, İzmir, Türkiye. ORCID: https://orcid.org/0009-0005-6000-2934.
Halil Topçu - Master's Student, Urban Design Master's Program, Graduate School of Natural and Applied Sciences, İzmir Demokrasi University, İzmir, Türkiye. ORCID: https://orcid.org/0009-0009-3366-179X.

Additional Question 4 - İklim Değişikliği Alanındaki Deneyim
Paste:
Evet. Yazarlar kentsel morfoloji, açık kaynak CBS, mekansal analiz, kentsel dirençlilik ve iklim uyumu ile ilişkili kentsel tasarım/planlama konularında akademik çalışma yürütmektedir. Bu bildiri, PlanX Urban Resilience merkezli açık kaynak QGIS iş akışı üzerinden kentsel doku, yaya erişilebilirliği, sosyal kırılganlık, aşırı sıcak, plüvyal taşkın ve kıyı maruziyeti göstergelerini birlikte ele alan yöntemsel bir pilot protokol geliştirmektedir. Akademik profil bağlantıları: Yusuf Eminoğlu ORCID https://orcid.org/0009-0005-6000-2934; Halil Topçu ORCID https://orcid.org/0009-0009-3366-179X.

Additional Question 5 - Bildiri Özeti / Abstract (500-750 words)
Paste the Turkish abstract below:

{m.TR_ABSTRACT}

Turkish abstract word count: {m.word_count(m.TR_ABSTRACT)}

Additional Question 6 - Anahtar Kelimeler / Keywords
Paste:
{tr_keywords}

Additional Question 7 - Presentation Language
Recommended selection:
Türkçe

Additional Question 8 - Publication Consent and Agreement
Select: I agree

Note for Question 8:
You are submitting abstract-only for the congress. Full text is optional after acceptance if you request publication in the listed publication channels.

------------------------------------------------------------
ENGLISH MATERIAL REQUIRED BY THE OFFICIAL GUIDELINES
Use this if CMT shows a separate English title/abstract/keywords field,
or if a Word/PDF upload field appears.
------------------------------------------------------------

English Title
{m.EN_TITLE}

English Abstract
{m.EN_ABSTRACT}

English abstract word count: {m.word_count(m.EN_ABSTRACT)}

English Keywords
{en_keywords}

------------------------------------------------------------
FINAL PRE-SUBMISSION CHECKLIST
------------------------------------------------------------

[ ] Title field uses Turkish title.
[ ] Yusuf Eminoğlu is first/corresponding author.
[ ] Halil Topçu is second author and presenter.
[ ] Subject areas are selected.
[ ] Q1 and Q8 confirmations are checked.
[ ] Abstract field contains no author names, affiliations, ORCID, references, figures or tables.
[ ] Turkish abstract is between 500 and 750 words.
[ ] Keywords are comma-separated and no more than five.
[ ] English title/abstract/keywords are supplied if CMT provides an extra field or upload option.
[ ] Final text has been reviewed and approved by the authors before submission.
"""

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(guide, encoding="utf-8-sig")
    return OUT_PATH


if __name__ == "__main__":
    print(main())
