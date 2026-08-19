#!/usr/bin/env python3
# ============================================================
#  مولّد بيانات تطبيق «موسوعة السوق» (Souq)
#  يقرأ المصادر الأصلية من ../source/ وينتج ../js/data.js
#  يحتوي على كل الفصول (15) + قاعدة العبارات (CSV) + نظرة عامة.
#  لا يتم تجاهل أي محتوى: كل نص يُضمَّن كما هو.
# ============================================================
import csv, json, os, re, glob

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "source")
OUT = os.path.join(HERE, "..", "js", "data.js")

# أيقونات وألوان كل قسم (مرتبة حسب رقم الملف 01..15)
ICONS = {
    1:  ("🧭", "c-teal"),
    2:  ("👋", "c-amber"),
    3:  ("🗣️", "c-blue"),
    4:  ("🛍️", "c-green"),
    5:  ("🤝", "c-purple"),
    6:  ("😄", "c-rose"),
    7:  ("🧑‍🤝‍🧑", "c-orange"),
    8:  ("🏪", "c-cyan"),
    9:  ("🌍", "c-teal"),
    10: ("📋", "c-amber"),
    11: ("💬", "c-blue"),
    12: ("🔤", "c-green"),
    13: ("⚠️", "c-rose"),
    14: ("⭐", "c-purple"),
    15: ("📚", "c-slate"),
}

PREFIX_RE = re.compile(r'^(?:القسم|الأقسام)\s+[\d\u2013\u2014–-]+\s*[\u2014\u2013-]\s*(.*)$')

def short_title(title):
    m = PREFIX_RE.match(title.strip())
    label = m.group(1) if m else title.strip()
    label = re.sub(r'\s*\([^)]*\)\s*$', '', label).strip()
    return label or title.strip()

def read_chapters():
    chapters = []
    files = sorted(glob.glob(os.path.join(SRC, "[0-9][0-9]-*.md")))
    for path in files:
        base = os.path.basename(path)
        num = int(base[:2])
        with open(path, encoding="utf-8") as f:
            raw = f.read()
        # عنوان الفصل = أول سطر يبدأ بـ #
        title = base
        for line in raw.splitlines():
            if line.startswith("# "):
                title = line[2:].strip()
                break
        icon, color = ICONS.get(num, ("📄", "c-slate"))
        chapters.append({
            "id": f"ch{num:02d}",
            "num": num,
            "file": base,
            "title": title,
            "label": short_title(title),
            "icon": icon,
            "color": color,
            "raw": raw,
        })
    return chapters

def read_about():
    path = os.path.join(SRC, "README.md")
    if not os.path.exists(path):
        return {"id": "about", "title": "عن الموسوعة", "raw": ""}
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    title = "موسوعة لغة السوق والبائع والزبون"
    for line in raw.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            break
    return {"id": "about", "title": title, "raw": raw}

def read_phrases():
    path = os.path.join(SRC, "phrases-db.csv")
    phrases = []
    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            phrases.append({
                "id": (row.get("id") or "").strip(),
                "phrase": (row.get("phrase") or "").strip(),
                "msa": (row.get("msa") or "").strip(),
                "country": (row.get("country") or "").strip(),
                "dialect": (row.get("dialect") or "").strip(),
                "situation": (row.get("situation") or "").strip(),
                "addressee": (row.get("addressee") or "").strip(),
                "formality": (row.get("formality") or "").strip(),
                "familiarity": (row.get("familiarity") or "").strip(),
                "humor": (row.get("humor") or "").strip(),
                "frequency": (row.get("frequency") or "").strip(),
                "notes": (row.get("notes") or "").strip(),
            })
    return phrases

FUNC_KEYWORDS = {
    'A': ['جذب', 'لفت', 'شارع', 'ممر', 'نداء', 'تعال'],
    'B': ['ترحيب', 'دعوة دخول', 'هلا', 'دخول', 'نورت'],
    'C': ['فتح الحديث', 'حوار', 'حديث', 'استطلاع'],
    'D': ['اكتشاف الحاجة', 'الحاجة'],
    'E': ['عرض', 'منتج', 'سلعة', 'تقديم'],
    'F': ['تعزيز القيمة', 'إقناع', 'قيمة', 'تأكيد', 'مميزات'],
    'G': ['اعتراض', 'رفض', 'تحفظ'],
    'H': ['تفاوض', 'مساومة', 'مكاسرة', 'خصم', 'سومة', 'السوم', 'مفاصلة', 'تشطار'],
    'I': ['إغلاق', 'قفل', 'إنهاء', 'حسم', 'ختام'],
    'J': ['بيع إضافي', 'إضافة', 'ملحق', 'أكسسوار', 'إضافي'],
    'K': ['محافظة', 'توديع', 'وداع', 'علاقة', 'متابعة', 'وفاء', 'بعد البيع'],
}
FUNC_ORDER = 'ABCDEFGHIJK'


def read_functions(chapters):
    """يستخرج التصنيف الوظيفي (A–K) من جدول القسم 1 في الموسوعة."""
    ch1 = next((c for c in chapters if c.get('num') == 1), None)
    funcs = []
    if not ch1:
        return funcs
    lines = ch1['raw'].split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith('|') and i + 1 < len(lines) and re.match(r'^\|[\s:\-|]+\|', lines[i + 1]):
            j = i + 2
            while j < len(lines) and lines[j].strip().startswith('|'):
                cells = [c.strip() for c in lines[j].strip().strip('|').split('|')]
                if cells and len(cells[0]) == 1 and cells[0] in FUNC_ORDER:
                    code = cells[0]
                    name = re.sub(r'\*\*', '', cells[1]).strip() if len(cells) > 1 else ''
                    examples = re.sub(r'\*\*', '', cells[2]).strip() if len(cells) > 2 else ''
                    where = cells[3].strip() if len(cells) > 3 else ''
                    m = re.search(r'ملف\s*(\d{2})', where)
                    chap = 'ch' + m.group(1) if m else ''
                    funcs.append({'code': code, 'name': name, 'examples': examples, 'where': where, 'chapterId': chap})
                j += 1
            i = j
        else:
            i += 1
    seen = set()
    ordered = []
    for code in FUNC_ORDER:
        for f in funcs:
            if f['code'] == code and f['code'] not in seen:
                ordered.append(f)
                seen.add(f['code'])
    return ordered


def assign_function(p):
    text = ((p.get('situation') or '') + ' ' + (p.get('phrase') or '')).lower()
    for code in FUNC_ORDER:
        for kw in FUNC_KEYWORDS[code]:
            if kw in text:
                return code
    return ''


ML_LANGS = [
    {'code': 'tr', 'name': 'التركية', 'flag': '🇹🇷', 'color': 'c-blue'},
    {'code': 'id', 'name': 'الإندونيسية', 'flag': '🇮🇩', 'color': 'c-green'},
    {'code': 'tg', 'name': 'الطاجيكية', 'flag': '🇹🇯', 'color': 'c-rose'},
    {'code': 'fr', 'name': 'الفرنسية', 'flag': '🇫🇷', 'color': 'c-purple'},
    {'code': 'en', 'name': 'الإنجليزية', 'flag': '🇬🇧', 'color': 'c-orange'},
]
ML_LANG_FILE = {'turki': 'tr', 'indunisi': 'id', 'tajiki': 'tg', 'faransi': 'fr', 'inglizi': 'en'}
ML_ROLE = {
    '00-manhaj': 'manhaj',
    '05-muqarana': 'compare',
    '06-qawalib': 'templates',
    '07-hiwarat': 'dialogues',
    '08-qamus': 'dictionary',
    '09-tahthir-wa-masadir': 'warnings',
    '10-tadrib': 'training',
    'README': 'about',
}
ML_ROLE_ICON = {'main': '🌐', 'manhaj': '🧭', 'compare': '🔁', 'templates': '📋',
                'dialogues': '💬', 'dictionary': '🔤', 'warnings': '⚠️', 'training': '🎯', 'about': 'ℹ️'}


def read_ml_docs():
    """يقرأ ملفات الموسوعة متعددة اللغات (markdown)."""
    docs = []
    base = os.path.join(SRC, 'multilingual')
    for path in sorted(glob.glob(os.path.join(base, '*.md'))):
        fn = os.path.basename(path)
        stem = fn[:-3]
        if stem in ('_gen_csv',):
            continue
        with open(path, encoding='utf-8') as f:
            raw = f.read()
        title = stem
        for line in raw.splitlines():
            if line.startswith('# '):
                title = line[2:].strip()
                break
        lang = 'all'
        role = 'doc'
        for kw, code in ML_LANG_FILE.items():
            if kw in stem:
                lang = code
                role = 'main'
                break
        if role != 'main':
            role = ML_ROLE.get(stem, 'doc')
        icon = ML_ROLE_ICON.get(role, '📄')
        color = 'c-slate'
        if role == 'main':
            lo = next((l for l in ML_LANGS if l['code'] == lang), None)
            if lo:
                icon = lo['flag']
                color = lo['color']
        docs.append({'id': 'ml-' + stem, 'file': fn, 'lang': lang, 'role': role,
                     'title': title, 'label': title, 'icon': icon, 'color': color, 'raw': raw})
    return docs


def read_ml_phrases():
    path = os.path.join(SRC, 'multilingual', 'phrases-ml.csv')
    out = []
    with open(path, encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            out.append({k: (row.get(k) or '').strip() for k in reader.fieldnames})
    return out


def main():
    chapters = read_chapters()
    about = read_about()
    phrases = read_phrases()
    for p in phrases:
        p["func"] = assign_function(p)
    functions = read_functions(chapters)
    for f in functions:
        f["count"] = sum(1 for p in phrases if p.get("func") == f["code"])

    ml_docs = read_ml_docs()
    ml_phrases = read_ml_phrases()
    ml_counts = {l["code"]: sum(1 for p in ml_phrases if p.get("targetLanguage") == l["code"]) for l in ML_LANGS}

    countries = sorted({p["country"] for p in phrases if p["country"]})
    dialects = sorted({p["dialect"] for p in phrases if p["dialect"]})
    situations = sorted({p["situation"] for p in phrases if p["situation"]})
    addressees = sorted({p["addressee"] for p in phrases if p["addressee"]})

    meta = {
        "appName": "موسوعة السوق",
        "subtitle": "دليل لغة البائع والزبون في الأسواق العربية",
        "source": "مشروع seller — فرع arena/019ff95f-seller",
        "chaptersCount": len(chapters),
        "phrasesCount": len(phrases),
        "countriesCount": len(countries),
        "dialectsCount": len(dialects),
        "situationsCount": len(situations),
        "functionsCount": len(functions),
        "mlPhrasesCount": len(ml_phrases),
        "mlLanguages": [l["name"] for l in ML_LANGS],
        "mlLangCounts": ml_counts,
        "countries": countries,
        "dialects": dialects,
        "situations": situations,
        "addressees": addressees,
        "generated": "2026-08-18",
    }

    out = []
    out.append("/* ============================================================")
    out.append("   موسوعة السوق — ملف البيانات المولّد تلقائياً")
    out.append("   يحتوي على كل الفصول + قاعدة العبارات + نظرة عامة.")
    out.append("   لا تعدّل هذا الملف يدوياً؛ عدّل المصادر في ../source ثم شغّل build_data.py")
    out.append("   ============================================================ */")
    out.append("")
    out.append("const SOUQ_META = " + json.dumps(meta, ensure_ascii=False, indent=1) + ";")
    out.append("")
    out.append("const CHAPTERS = " + json.dumps(chapters, ensure_ascii=False, indent=1) + ";")
    out.append("")
    out.append("const ABOUT = " + json.dumps(about, ensure_ascii=False, indent=1) + ";")
    out.append("")
    out.append("const FUNCTIONS = " + json.dumps(functions, ensure_ascii=False, indent=1) + ";")
    out.append("")
    out.append("const ML_LANGS = " + json.dumps(ML_LANGS, ensure_ascii=False, indent=1) + ";")
    out.append("const ML_DOCS = " + json.dumps(ml_docs, ensure_ascii=False, indent=1) + ";")
    out.append("const ML_PHRASES = " + json.dumps(ml_phrases, ensure_ascii=False, indent=1) + ";")
    out.append("")
    out.append("const PHRASES = " + json.dumps(phrases, ensure_ascii=False, indent=1) + ";")
    out.append("")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(out))

    print(f"✔ تم توليد data.js")
    print(f"   الفصول: {len(chapters)}")
    print(f"   العبارات: {len(phrases)}")
    print(f"   الدول/المناطق: {len(countries)} | اللهجات: {len(dialects)} | المواقف: {len(situations)}")
    print(f"   الوثائق متعددة اللغات: {len(ml_docs)} | العبارات المتعددة اللغات: {len(ml_phrases)}")
    print(f"   الحجم: {os.path.getsize(OUT)//1024} KB")

if __name__ == "__main__":
    main()
