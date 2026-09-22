#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv, os

path = os.path.join(os.path.dirname(__file__), "phrases-ml.csv")
fields = [
    "id", "category", "subcategory", "arabic", "targetLanguage", "originalText",
    "arabicTranslation", "literalTranslation", "arabicPronunciation", "country",
    "region", "dialect", "register", "audience", "gender", "ageGroup", "situation",
    "tone", "formality", "familiarity", "frequency", "culturalNotes", "usageNotes",
    "alternatives", "relatedPhrases", "confidence", "sources", "noDirectArabic",
]

rows = []


def add(**k):
    row = {f: "" for f in fields}
    row.update(
        region=k.get("region", "عام"),
        dialect=k.get("dialect", ""),
        audience=k.get("audience", "الجميع"),
        gender=k.get("gender", "الجميع"),
        ageGroup=k.get("age", "الجميع"),
        tone=k.get("tone", "ودود"),
        familiarity=k.get("fam", "منخفضة"),
        literalTranslation=k.get("lit", ""),
        culturalNotes=k.get("notes", ""),
        usageNotes=k.get("usage", ""),
        alternatives=k.get("alt", ""),
        relatedPhrases=k.get("rel", ""),
        noDirectArabic=k.get("nodirect", "no"),
        formality=k.get("register", ""),
    )
    row.update(k)
    # normalize keys that are aliases
    if "register" in k:
        row["register"] = k["register"]
        row["formality"] = k["register"]
    rows.append({f: row.get(f, "") for f in fields})


# ===================== TURKISH =====================
add(id="TR001", category="B ترحيب", subcategory="ترحيب عام", arabic="يا هلا وسهلا",
    targetLanguage="tr", originalText="Hoş geldiniz",
    arabicTranslation="أهلًا وسهلًا / مرحبًا بقدومكم", lit="جئتم طيبين",
    arabicPronunciation="هوش گِلدينيز", country="تركيا", situation="ترحيب عند الدخول",
    register="محترم وودود", frequency="🔥 شائعة جدًا", confidence="عالية", sources="T1 T2",
    notes="يُكرر كثيرًا. للمفرد القريب: Hoş geldin. رد الزبون: Hoş bulduk.",
    usage="أول جملة بعد دخول الزبون.", alt="Merhaba, hoş geldiniz", rel="TR002,TR003",
    dialect="تركية معيارية يومية")

add(id="TR002", category="B ترحيب", subcategory="دعوة", arabic="تفضل",
    targetLanguage="tr", originalText="Buyurun",
    arabicTranslation="تفضل / ادخل / خذ", lit="تفضّلوا",
    arabicPronunciation="بويورون", country="تركيا", situation="دعوة الدخول أو الأخذ",
    register="شعبي", frequency="🔥 شائعة جدًا", confidence="عالية", sources="T1 T5",
    notes="أوسع من تفضل العربية: ادخل، خذ، اجلس، تكلم.", alt="Buyurun bakın")

add(id="TR003", category="K وداع/علاقة", subcategory="رد ترحيب", arabic="(لا مقابل مباشر)",
    targetLanguage="tr", originalText="Hoş bulduk",
    arabicTranslation="وجدنا الترحيب طيبًا", lit="وجدنا طيبًا",
    arabicPronunciation="هوش بولْدوك", country="تركيا", situation="رد الزبون على Hoş geldiniz",
    register="محترم وودود", frequency="🔥 شائعة جدًا", confidence="عالية", sources="T2",
    nodirect="yes", notes="إلزام اجتماعي بعد الترحيب. يقوله الزبون لا البائع.")

add(id="TR004", category="A جذب", subcategory="نداء", arabic="تعال شوف",
    targetLanguage="tr", originalText="Buyurun bakın",
    arabicTranslation="تفضل انظر", arabicPronunciation="بويورون باقِن",
    country="تركيا", situation="جذب عند الباب أو البسطة", register="شعبي",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="T1",
    alt="Bir bakın isterseniz|Gel gel")

add(id="TR005", category="A جذب", subcategory="نداء شعبي", arabic="تعال تعال",
    targetLanguage="tr", originalText="Gel gel!", arabicTranslation="تعال تعال",
    arabicPronunciation="گِل گِل", country="تركيا", situation="بسطة/بازار",
    register="شعبي", frequency="🔥 شائعة جدًا", confidence="عالية", sources="T2",
    audience="مارّ في السوق", notes="ثقيل في محل راقٍ أو مول.")

add(id="TR006", category="A جذب", subcategory="بلا التزام", arabic="بس شوف ما بتخسر شيء",
    targetLanguage="tr", originalText="Bir bakın, belki hoşunuza gider",
    arabicTranslation="شوف، يمكن يعجبك", arabicPronunciation="بير باقِن، بلكى هوشونوزا گيدر",
    country="تركيا", situation="جذب بالفضول", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="T1 T5",
    alt="Sadece bakın, zorunlu değil")

add(id="TR007", category="A جذب", subcategory="منتج", arabic="جديد وصل اليوم",
    targetLanguage="tr", originalText="Yeni geldi!", arabicTranslation="وصل جديد",
    arabicPronunciation="ييني گلدي", country="تركيا", situation="نداء بالحداثة",
    register="شعبي", frequency="🔥 شائعة جدًا", confidence="عالية", sources="T5")

add(id="TR008", category="C مخاطبة", subcategory="رجل شعبي", arabic="يا أخوي",
    targetLanguage="tr", originalText="Abi", arabicTranslation="يا أخوي", lit="أخ كبير",
    arabicPronunciation="آبي", country="تركيا", situation="مخاطبة رجل في السوق",
    register="شعبي", frequency="🔥 شائعة جدًا", confidence="عالية", sources="T1 T2",
    gender="رجل", audience="رجل", notes="لغريب في pazar. في Boutique: Beyefendi.")

add(id="TR009", category="C مخاطبة", subcategory="رجل مهذب", arabic="يا أستاذ",
    targetLanguage="tr", originalText="Beyefendi", arabicTranslation="يا سيدي",
    arabicPronunciation="بي أفندي", country="تركيا", situation="مخاطبة مهذبة لرجل",
    register="محترم وودود", frequency="🔥 شائعة جدًا", confidence="عالية", sources="T5",
    gender="رجل", alt="Efendim")

add(id="TR010", category="C مخاطبة", subcategory="امرأة مهذبة", arabic="يا أستاذة",
    targetLanguage="tr", originalText="Hanımefendi", arabicTranslation="يا سيدتي",
    arabicPronunciation="هانِم أفندي", country="تركيا", situation="مخاطبة مهذبة لامرأة",
    register="محترم وودود", frequency="🔥 شائعة جدًا", confidence="عالية", sources="T5",
    gender="امرأة", alt="Hanım")

add(id="TR011", category="C مخاطبة", subcategory="امرأة يومية", arabic="يا أختي",
    targetLanguage="tr", originalText="Abla", arabicTranslation="يا أختي", lit="أخت كبيرة",
    arabicPronunciation="آبلا", country="تركيا", situation="سوق شعبي لامرأة",
    register="شعبي", frequency="⭐ شائعة", confidence="عالية", sources="T1",
    gender="امرأة")

add(id="TR012", category="C مخاطبة", subcategory="كبير سن", arabic="يا عم",
    targetLanguage="tr", originalText="Amca", arabicTranslation="يا عم",
    arabicPronunciation="آمجه", country="تركيا", situation="رجل أكبر سنًا",
    register="محترم وودود", frequency="🔥 شائعة جدًا", confidence="عالية", sources="T5",
    gender="رجل", age="كبار", alt="Teyze للنساء")

add(id="TR013", category="D اكتشاف", subcategory="تفرج أم طلب",
    arabic="بتدور على شيء ولا بتتفرج؟", targetLanguage="tr",
    originalText="Bakınıyor musunuz, yoksa bir şey mi arıyorsunuz?",
    arabicTranslation="بتتفرج ولا تدور على شيء؟",
    arabicPronunciation="باقِنِيور موسونوز يوكسا بير شيء مي آرِيورسونوز",
    country="تركيا", situation="فتح حديث بعد الترحيب", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="T5")

add(id="TR014", category="D اكتشاف", subcategory="بس أتفرج", arabic="خذ راحتك أنا موجود",
    targetLanguage="tr", originalText="Tabii, rahatınıza bakın",
    arabicTranslation="أكيد، خذ راحتك", arabicPronunciation="طابي، راهاتِنِزا باقِن",
    country="تركيا", situation="رد على المتفرج", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="T1 T5")

add(id="TR015", category="E عرض", subcategory="تقديم", arabic="شوف هذا",
    targetLanguage="tr", originalText="Şuna bir bakın", arabicTranslation="شوف هذا",
    arabicPronunciation="شونا بير باقِن", country="تركيا", situation="عرض منتج",
    register="شعبي", frequency="🔥 شائعة جدًا", confidence="عالية", sources="T5")

add(id="TR016", category="E عرض", subcategory="جودة", arabic="شغل نظيف / خامة ممتازة",
    targetLanguage="tr", originalText="Kaliteli mal", arabicTranslation="بضاعة جودة",
    arabicPronunciation="كاليتلي مال", country="تركيا", situation="مدح المنتج",
    register="شعبي", frequency="🔥 شائعة جدًا", confidence="عالية", sources="T1",
    notes="mal هنا = بضاعة محايدة في السوق.")

add(id="TR017", category="E عرض", subcategory="أصلي", arabic="هذا أصلي",
    targetLanguage="tr", originalText="Hakiki / orijinal",
    arabicTranslation="أصلي / حقيقي", arabicPronunciation="هاكيقي / أوريجينال",
    country="تركيا", situation="تمييز عن التقليد", register="شعبي",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="T1")

add(id="TR018", category="E عرض", subcategory="يليق", arabic="هذا على ذوقك / يليق عليك",
    targetLanguage="tr", originalText="Size yakışır", arabicTranslation="يليق عليك",
    arabicPronunciation="سِزه ياقيشير", country="تركيا", situation="مجاملة المنتج",
    register="محترم وودود", frequency="⭐ شائعة", confidence="عالية", sources="T5",
    notes="مع النساء بنبرة مهنية لا غزل.")

add(id="TR019", category="E عرض", subcategory="طلب", arabic="عليه طلب",
    targetLanguage="tr", originalText="Bu çok satıyor", arabicTranslation="هذا ينباع كثير",
    arabicPronunciation="بو چوك ساتِيور", country="تركيا", situation="إثبات اجتماعي",
    register="شعبي", frequency="⭐ شائعة", confidence="عالية", sources="T5",
    alt="Çok soruyorlar bunu")

add(id="TR020", category="H سعر", subcategory="سؤال الزبون", arabic="بكم هذا؟",
    targetLanguage="tr", originalText="Bu ne kadar?", arabicTranslation="بكم هذا؟",
    arabicPronunciation="بو نه قدَر", country="تركيا", situation="سؤال سعر",
    register="شعبي", frequency="🔥 شائعة جدًا", confidence="عالية", sources="T1",
    alt="Kaç lira?|Kaça?")

add(id="TR021", category="H سعر", subcategory="آخر سعر", arabic="آخر سعر",
    targetLanguage="tr", originalText="Son fiyat", arabicTranslation="آخر سعر",
    arabicPronunciation="سون فيات", country="تركيا", situation="إغلاق تفاوض",
    register="شعبي", frequency="🔥 شائعة جدًا", confidence="عالية", sources="T1",
    alt="En son bu|Bunun altına inemem")

add(id="TR022", category="H سعر", subcategory="ثابت", arabic="السعر ثابت",
    targetLanguage="tr", originalText="Fiyatımız net", arabicTranslation="سعرنا ثابت",
    arabicPronunciation="فياتِمِز نِت", country="تركيا", situation="محل حديث / ماركة",
    register="محترم وودود", frequency="🔥 شائعة جدًا", confidence="عالية", sources="T5",
    alt="Pazarlık yok")

add(id="TR023", category="H خصم", subcategory="شخصي", arabic="عشانك نضبطها",
    targetLanguage="tr", originalText="Size özel bir fiyat vereyim",
    arabicTranslation="أعطيك سعرًا خاصًا", arabicPronunciation="سِزه أوزيل بير فيات فيرييم",
    country="تركيا", situation="خصم شخصي", register="شعبي",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="T1 T5")

add(id="TR024", category="H تفاوض", subcategory="كمية", arabic="إذا أخذت اثنين",
    targetLanguage="tr", originalText="İki alırsanız indirim yaparım",
    arabicTranslation="إذا أخذت اثنين أنزّل", arabicPronunciation="إيكي آلِرسانِز إنديريم ياپارِم",
    country="تركيا", situation="خصم مشروط", register="شعبي",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="T1")

add(id="TR025", category="H تفاوض", subcategory="خسارة", arabic="والله ما أقدر",
    targetLanguage="tr", originalText="Zararına veriyorum",
    arabicTranslation="ببيعها بخسارة", arabicPronunciation="زارارِنا فيريوروم",
    country="تركيا", situation="رفض نزول إضافي", register="شعبي",
    frequency="⭐ شائعة", confidence="عالية", sources="T5",
    notes="مبالغة سوقية لا تُؤخذ حرفيًا.", alt="Bunun altına inemem")

add(id="TR026", category="H تفاوض", subcategory="اتفاق", arabic="اتفقنا",
    targetLanguage="tr", originalText="Anlaştık", arabicTranslation="اتفقنا",
    arabicPronunciation="أنلاشتِك", country="تركيا", situation="إغلاق المساومة",
    register="شعبي", frequency="🔥 شائعة جدًا", confidence="عالية", sources="T1")

add(id="TR027", category="G اعتراض", subcategory="غالي", arabic="غالي؟ شوف الجودة",
    targetLanguage="tr", originalText="Pahalı değil, kaliteli",
    arabicTranslation="مو غالي، جودته عالية", arabicPronunciation="پاهالِ دييل، كاليتلي",
    country="تركيا", situation="رد على pahalı", register="شعبي",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="T1")

add(id="TR028", category="G اعتراض", subcategory="بديل", arabic="عندي خيار أرخص",
    targetLanguage="tr", originalText="Daha uygun bir model göstereyim",
    arabicTranslation="أوريك موديل أنسب", arabicPronunciation="داها أويغون بير موديل گوسترييم",
    country="تركيا", situation="تحويل الاعتراض", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="T5")

add(id="TR029", category="I إغلاق", subcategory="تغليف", arabic="نغلفها لك؟",
    targetLanguage="tr", originalText="Paketleyeyim mi?", arabicTranslation="أغلفها لك؟",
    arabicPronunciation="پاكتليييم مي", country="تركيا", situation="إغلاق ناعم",
    register="محترم وودود", frequency="🔥 شائعة جدًا", confidence="عالية", sources="T5")

add(id="TR030", category="K وداع", subcategory="دعوة عودة", arabic="ننتظرك / حياك مرة ثانية",
    targetLanguage="tr", originalText="Yine bekleriz", arabicTranslation="ننتظرك مرة ثانية",
    arabicPronunciation="يينه بكلريز", country="تركيا", situation="توديع",
    register="محترم وودود", frequency="🔥 شائعة جدًا", confidence="عالية", sources="T3 T5")

add(id="TR031", category="K وداع", subcategory="بركة استخدام", arabic="(لا مقابل مباشر بنفس الشيوع)",
    targetLanguage="tr", originalText="Güle güle kullanın",
    arabicTranslation="استعملها وأنت فرحان", lit="استخدم بضحكات",
    arabicPronunciation="گوله گوله قوللانِن", country="تركيا", situation="بعد إتمام البيع",
    register="محترم وودود", frequency="🔥 شائعة جدًا", confidence="عالية", sources="T5",
    nodirect="yes")

add(id="TR032", category="K وداع", subcategory="بركة شراء", arabic="(لا مقابل مباشر)",
    targetLanguage="tr", originalText="Hayırlı olsun",
    arabicTranslation="مبروك الشراء / بالبركة", arabicPronunciation="هايرلِ أولسون",
    country="تركيا", situation="بعد الشراء", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="T5", nodirect="yes")

add(id="TR033", category="K وداع", subcategory="دعاء للبائع", arabic="يعطيك العافية (قريب لا مطابق)",
    targetLanguage="tr", originalText="Kolay gelsin",
    arabicTranslation="تيسيرًا لشغلك", lit="فليأتِ سهلًا",
    arabicPronunciation="كولاي گِلسين", country="تركيا", situation="يقوله الزبون للبائع",
    register="محترم وودود", frequency="🔥 شائعة جدًا", confidence="عالية", sources="T2 T3",
    nodirect="yes", notes="من أشهر العبارات التركية بلا نظير عربي بنفس التواتر.")

add(id="TR034", category="L ضيافة", subcategory="شاي", arabic="تفضل قهوة/شاي؟",
    targetLanguage="tr", originalText="Çay içer misiniz?", arabicTranslation="تشرب شاي؟",
    arabicPronunciation="تشاي إيچر ميسينيز", country="تركيا", situation="بازار/سجاد/ذهب",
    register="شعبي", frequency="🔥 شائعة جدًا", confidence="عالية", sources="T1",
    notes="طقس بيع. القبول لا يُلزم بالشراء.")

add(id="TR035", category="M مزاح", subcategory="دائم", arabic="غبت علينا",
    targetLanguage="tr", originalText="Neredeydin, özlemiştik",
    arabicTranslation="وينك، اشتقنا", arabicPronunciation="نرده يدين، أوزله ميشتيك",
    country="تركيا", situation="زبون دائم", register="عفوي",
    frequency="⭐ شائعة", confidence="متوسطة", sources="T5", audience="زبون دائم")

add(id="TR036", category="N غضب", subcategory="اعتذار", arabic="معك حق",
    targetLanguage="tr", originalText="Haklısınız, dinliyorum",
    arabicTranslation="معك حق، أسمعك", arabicPronunciation="حقْلِسِنِز، دينليوروم",
    country="تركيا", situation="زبون غاضب", register="رسمي جدًا",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="T5")

add(id="TR037", category="N إرجاع", subcategory="حل", arabic="نبدله",
    targetLanguage="tr", originalText="Değiştiririz / iade ederiz",
    arabicTranslation="نبدّل / نرجّع", arabicPronunciation="دييشتيريريز / إياده إديريز",
    country="تركيا", situation="عيب/إرجاع", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="T5")

add(id="TR038", category="N إرجاع", subcategory="فاتورة", arabic="معك الفاتورة؟",
    targetLanguage="tr", originalText="Fişiniz var mı?", arabicTranslation="معك الإيصال؟",
    arabicPronunciation="فيشينيز فار مِ", country="تركيا", situation="إرجاع",
    register="محترم وودود", frequency="🔥 شائعة جدًا", confidence="عالية", sources="T5")

add(id="TR039", category="J إضافي", subcategory="مكمل", arabic="خذ معها هذا يكملها",
    targetLanguage="tr", originalText="Yanına şunu alın, tamamlar",
    arabicTranslation="خذ معه هذا يكمّله", arabicPronunciation="يانِنا شونو آلِن، تمامْلار",
    country="تركيا", situation="بيع إضافي", register="شعبي",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="T5")

add(id="TR040", category="C مخاطبة", subcategory="تحذير", arabic="يا حبيبتي (ممنوع)",
    targetLanguage="tr", originalText="Canım / tatlım / güzelim",
    arabicTranslation="يا روحي / يا حلو — لا تُقال لغريبة",
    arabicPronunciation="جانِم / تاتلِم / گوزليم", country="تركيا",
    situation="⚠️ لا تُقال لامرأة غريبة", register="حميمي",
    frequency="⚠️ حساسة", confidence="عالية", sources="T5", gender="امرأة")

add(id="TR041", category="P مثل", subcategory="ثقافة", arabic="الزبون غالي",
    targetLanguage="tr", originalText="Müşteri velinimetimizdir",
    arabicTranslation="الزبون ولي نعمتنا", arabicPronunciation="موشتري فلي نعمتِمِزدير",
    country="تركيا", situation="لافتات وتجار تقليديون", register="رسمي جدًا",
    frequency="⭐ شائعة", confidence="عالية", sources="T4", nodirect="yes")

add(id="TR042", category="I إغلاق", subcategory="محاسبة", arabic="نحسبها لك؟",
    targetLanguage="tr", originalText="Kasaya geçelim mi?",
    arabicTranslation="نروح على الصندوق؟", arabicPronunciation="كاسايا گه چه ليم مي",
    country="تركيا", situation="إغلاق", register="محترم وودود",
    frequency="⭐ شائعة", confidence="عالية", sources="T5")

add(id="TR043", category="A جذب", subcategory="استدعاء أخير", arabic="لا تروح عشانك أنزل",
    targetLanguage="tr", originalText="Abi, durun! Bir fiyat daha vereyim",
    arabicTranslation="قف! أعطيك سعر أحسن", arabicPronunciation="آبي دورون بير فيات داها فيرييم",
    country="تركيا", situation="الزبون يغادر بعد السعر", register="شعبي",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="T5",
    notes="مرة أو مرتين بابتسامة فقط.")

add(id="TR044", category="H تفاوض", subcategory="نتوسط", arabic="خلينا نتفق",
    targetLanguage="tr", originalText="Orta yolda buluşalım",
    arabicTranslation="نتوسط الطريق", arabicPronunciation="أورتا يولدا بولوشالِم",
    country="تركيا", situation="مساومة", register="شعبي",
    frequency="⭐ شائعة", confidence="عالية", sources="T5")

add(id="TR045", category="K دائم", subcategory="طلب معتاد", arabic="ماذا نجهز لك اليوم؟",
    targetLanguage="tr", originalText="Her zamanki mi?", arabicTranslation="طلبك المعتاد؟",
    arabicPronunciation="هر زمانكي مي", country="تركيا", situation="زبون دائم",
    register="عفوي", frequency="⭐ شائعة", confidence="عالية", sources="T5",
    audience="زبون دائم")

# ===================== INDONESIAN =====================
add(id="ID001", category="B ترحيب", subcategory="دعوة", arabic="تفضل",
    targetLanguage="id", originalText="Silakan", arabicTranslation="تفضل",
    arabicPronunciation="سيلاكان", country="إندونيسيا", situation="ترحيب ودعوة",
    register="محترم وودود", frequency="🔥 شائعة جدًا", confidence="عالية", sources="I1 I4",
    alt="Silakan masuk|Monggo")

add(id="ID002", category="B ترحيب", subcategory="ترحيب رسمي", arabic="أهلًا وسهلًا",
    targetLanguage="id", originalText="Selamat datang", arabicTranslation="أهلًا وسهلًا",
    lit="سلامة القدوم", arabicPronunciation="سلامات داتانغ", country="إندونيسيا",
    situation="محل حديث/لافتة", register="محترم وودود", frequency="⭐ شائعة",
    confidence="عالية", sources="I4")

add(id="ID003", category="B ترحيب", subcategory="جاوي", arabic="تفضل",
    targetLanguage="id", originalText="Monggo", arabicTranslation="تفضل / تكرّم",
    arabicPronunciation="مونغّو", country="إندونيسيا", situation="جاوة خصوصًا",
    register="شعبي", frequency="🔥 شائعة جدًا", confidence="متوسطة", sources="I4",
    region="جاوة", nodirect="yes", notes="جاوية حية. ليست فصحى مدرسية.")

add(id="ID004", category="A جذب", subcategory="نداء", arabic="تعال شوف / ادخل",
    targetLanguage="id", originalText="Mampir, Kak!", arabicTranslation="عرّج/ادخل",
    arabicPronunciation="مامبير، كاك", country="إندونيسيا", situation="warung/بسطة",
    register="شعبي", frequency="🔥 شائعة جدًا", confidence="عالية", sources="I4",
    nodirect="yes")

add(id="ID005", category="A جذب", subcategory="بلا التزام", arabic="بس شوف ما بتخسر",
    targetLanguage="id", originalText="Lihat dulu, nggak wajib beli",
    arabicTranslation="شوف أول، مو لازم تشتري",
    arabicPronunciation="ليهات دولو، إنغّاك واجب بيلي", country="إندونيسيا",
    situation="جذب", register="شعبي", frequency="🔥 شائعة جدًا", confidence="عالية",
    sources="I1 I4")

add(id="ID006", category="A جذب", subcategory="جديد", arabic="وصل اليوم",
    targetLanguage="id", originalText="Yang ini baru datang",
    arabicTranslation="هذا وصل جديد", arabicPronunciation="يانغ إيني بارو داتانغ",
    country="إندونيسيا", situation="نداء منتج", register="شعبي",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="I4")

add(id="ID007", category="C مخاطبة", subcategory="محايد حديث", arabic="يا أستاذ/أختي (قريب العمر)",
    targetLanguage="id", originalText="Kak", arabicTranslation="يا كاك",
    arabicPronunciation="كاك", country="إندونيسيا", situation="تجزئة حديثة",
    register="شعبي", frequency="🔥 شائعة جدًا", confidence="عالية", sources="I1",
    notes="للجنسين.")

add(id="ID008", category="C مخاطبة", subcategory="رجل محترم", arabic="يا أستاذ",
    targetLanguage="id", originalText="Pak", arabicTranslation="يا أستاذ / يا عم",
    arabicPronunciation="پاك", country="إندونيسيا", situation="رجل أكبر أو محترم",
    register="محترم وودود", frequency="🔥 شائعة جدًا", confidence="عالية", sources="I1",
    gender="رجل")

add(id="ID009", category="C مخاطبة", subcategory="امرأة محترمة", arabic="يا أستاذة",
    targetLanguage="id", originalText="Bu", arabicTranslation="يا مدام / يا أستاذة",
    arabicPronunciation="بو", country="إندونيسيا", situation="امرأة أكبر أو محترمة",
    register="محترم وودود", frequency="🔥 شائعة جدًا", confidence="عالية", sources="I1",
    gender="امرأة")

add(id="ID010", category="C مخاطبة", subcategory="جاوة رجل", arabic="يا أخوي",
    targetLanguage="id", originalText="Mas", arabicTranslation="يا أخ (جاوي)",
    arabicPronunciation="ماس", country="إندونيسيا", situation="رجل",
    register="شعبي", frequency="🔥 شائعة جدًا", confidence="عالية", sources="I1 I4",
    gender="رجل", region="جاوة+")

add(id="ID011", category="C مخاطبة", subcategory="جاوة امرأة", arabic="يا أختي",
    targetLanguage="id", originalText="Mbak", arabicTranslation="يا أخت (جاوي)",
    arabicPronunciation="مْباك", country="إندونيسيا", situation="امرأة",
    register="شعبي", frequency="🔥 شائعة جدًا", confidence="عالية", sources="I4",
    gender="امرأة", region="جاوة+")

add(id="ID012", category="D اكتشاف", subcategory="سؤال حاجة", arabic="شو بدك اليوم؟",
    targetLanguage="id", originalText="Cari apa, Kak?", arabicTranslation="تدور على إيش؟",
    arabicPronunciation="تشاري آبا، كاك", country="إندونيسيا", situation="فتح حديث",
    register="شعبي", frequency="🔥 شائعة جدًا", confidence="عالية", sources="I1")

add(id="ID013", category="D اكتشاف", subcategory="متفرج", arabic="خذ راحتك",
    targetLanguage="id", originalText="Santai aja, lihat dulu",
    arabicTranslation="على راحتك شوف", arabicPronunciation="سانتاي أجا، ليهات دولو",
    country="إندونيسيا", situation="رد المتفرج", register="شعبي",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="I4")

add(id="ID014", category="E عرض", subcategory="طلب", arabic="عليه طلب",
    targetLanguage="id", originalText="Ini yang lagi laku",
    arabicTranslation="هذا اللي ينباع", arabicPronunciation="إيني يانغ لاغي لاكو",
    country="إندونيسيا", situation="إثبات اجتماعي", register="شعبي",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="I4")

add(id="ID015", category="E عرض", subcategory="جودة", arabic="خامة ممتازة",
    targetLanguage="id", originalText="Bahannya bagus, bukan abal-abal",
    arabicTranslation="خامتُه حلوة مو زائفة",
    arabicPronunciation="باهانْنيا باغوس، بوكان أبال-أبال", country="إندونيسيا",
    situation="مدح", register="شعبي", frequency="⭐ شائعة", confidence="عالية", sources="I4")

add(id="ID016", category="H سعر", subcategory="سؤال", arabic="بكم؟",
    targetLanguage="id", originalText="Ini harganya berapa, Kak?",
    arabicTranslation="بكم هذا؟", arabicPronunciation="إيني هارجانيا بيراپا",
    country="إندونيسيا", situation="سؤال سعر", register="شعبي",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="I1")

add(id="ID017", category="H سعر", subcategory="ثابت", arabic="آخر سعر / السعر ثابت",
    targetLanguage="id", originalText="Harga pas", arabicTranslation="السعر ثابت/الصافي",
    arabicPronunciation="هارجا پاس", country="إندونيسيا", situation="عدم المساومة أو السعر الصافي",
    register="شعبي", frequency="🔥 شائعة جدًا", confidence="عالية", sources="I1 I2",
    nodirect="yes", alt="Harga mati")

add(id="ID018", category="H سعر", subcategory="نهائي", arabic="آخر سعر",
    targetLanguage="id", originalText="Sudah paling murah",
    arabicTranslation="هذا أرخص ما عندي", arabicPronunciation="سوداه پالينغ موراه",
    country="إندونيسيا", situation="إغلاق نزول", register="شعبي",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="I1")

add(id="ID019", category="H تفاوض", subcategory="طلب خصم", arabic="في مجال؟",
    targetLanguage="id", originalText="Bisa lebih murah, Kak?",
    arabicTranslation="تقدر أرخص؟", arabicPronunciation="بيسا لبيه موراه",
    country="إندونيسيا", situation="بداية مساومة", register="شعبي",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="I1", alt="Bisa kurang?")

add(id="ID020", category="H تفاوض", subcategory="رفض لطيف", arabic="والله ما أقدر",
    targetLanguage="id", originalText="Wah, rugi saya, Kak",
    arabicTranslation="أتضرر/خسارة عليّ", arabicPronunciation="واه، روغي سايا",
    country="إندونيسيا", situation="رفض خصم كبير", register="شعبي",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="I1", nodirect="yes")

add(id="ID021", category="H خصم", subcategory="شخصي", arabic="عشانك",
    targetLanguage="id", originalText="Khusus Kakak, saya potong",
    arabicTranslation="خصوصًا لك أنزّل", arabicPronunciation="خصوص كاكا، سايا پوتونغ",
    country="إندونيسيا", situation="خصم شخصي", register="شعبي",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="I1")

add(id="ID022", category="H تفاوض", subcategory="اتفاق", arabic="اتفقنا",
    targetLanguage="id", originalText="Deal / oke", arabicTranslation="اتفقنا",
    arabicPronunciation="ديل / أوكي", country="إندونيسيا", situation="إغلاق",
    register="شعبي", frequency="🔥 شائعة جدًا", confidence="عالية", sources="I1")

add(id="ID023", category="G اعتراض", subcategory="غالي", arabic="غالي؟ شوف الجودة",
    targetLanguage="id", originalText="Mahal sih, tapi bahannya beda",
    arabicTranslation="غالي بس الخامة غير", arabicPronunciation="ماهال سي، تاپي باهانْنيا بيدا",
    country="إندونيسيا", situation="رد mahal", register="شعبي",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="I1")

add(id="ID024", category="G اعتراض", subcategory="بديل", arabic="عندي أرخص",
    targetLanguage="id", originalText="Saya tunjukkan yang lebih hemat",
    arabicTranslation="أوريك أوفر", arabicPronunciation="سايا تونجوكّان يانغ لبيه هيمات",
    country="إندونيسيا", situation="تحويل", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="I1")

add(id="ID025", category="I إغلاق", subcategory="تغليف", arabic="نغلفها لك؟",
    targetLanguage="id", originalText="Saya bungkuskan ya?",
    arabicTranslation="أغلفها لك؟", arabicPronunciation="سايا بونغكوسكان يا",
    country="إندونيسيا", situation="إغلاق ناعم", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="I2")

add(id="ID026", category="K وداع", subcategory="عودة", arabic="حياك مرة ثانية",
    targetLanguage="id", originalText="Makasih, mampir lagi ya",
    arabicTranslation="شكرًا، عرّج مرة ثانية", arabicPronunciation="ماكاشيه، مامبير لاغي يا",
    country="إندونيسيا", situation="توديع", register="شعبي",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="I4")

add(id="ID027", category="K دائم", subcategory="تمييز", arabic="يا هلا بالقديم",
    targetLanguage="id", originalText="Wah, langganan datang!",
    arabicTranslation="الزبون الدائم إجا!", arabicPronunciation="واه، لانغّانان داتانغ",
    country="إندونيسيا", situation="زبون دائم", register="عفوي",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="I4", audience="زبون دائم")

add(id="ID028", category="K دائم", subcategory="المعتاد", arabic="إيش نجهز لك",
    targetLanguage="id", originalText="Yang biasa?", arabicTranslation="المعتاد؟",
    arabicPronunciation="يانغ بياسا", country="إندونيسيا", situation="دائم",
    register="عفوي", frequency="🔥 شائعة جدًا", confidence="عالية", sources="I4",
    audience="زبون دائم")

add(id="ID029", category="N غضب", subcategory="اعتذار", arabic="معك حق",
    targetLanguage="id", originalText="Saya dengar, Pak. Maaf sekali",
    arabicTranslation="أسمعك، آسف جدًا", arabicPronunciation="سايا دِنغار، پاك. ماعاف سكالي",
    country="إندونيسيا", situation="غاضب", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="I4")

add(id="ID030", category="J إضافي", subcategory="مكمل", arabic="خذ معها",
    targetLanguage="id", originalText="Sekalian yang ini, nyambung",
    arabicTranslation="خذ هذا معه يكمّل", arabicPronunciation="سكاليان يانغ إيني، نيامبونغ",
    country="إندونيسيا", situation="بيع إضافي", register="شعبي",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="I4")

add(id="ID031", category="H سعر", subcategory="جملة", arabic="سعر جملة",
    targetLanguage="id", originalText="Harga grosir", arabicTranslation="سعر جملة",
    arabicPronunciation="هارجا غروسير", country="إندونيسيا", situation="كمية",
    register="شعبي", frequency="⭐ شائعة", confidence="عالية", sources="I1")

add(id="ID032", category="A جذب", subcategory="عرض", arabic="عندنا عرض",
    targetLanguage="id", originalText="Ada promo hari ini",
    arabicTranslation="عندنا عرض اليوم", arabicPronunciation="آدا پرومو هاري إيني",
    country="إندونيسيا", situation="جذب", register="شعبي",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="I4")

add(id="ID033", category="C مخاطبة", subcategory="تحذير", arabic="يا حبيبتي",
    targetLanguage="id", originalText="Sayang / cantik (نداء)",
    arabicTranslation="يا حبيبي/يا حلوة — لا تُقال لغريبة",
    arabicPronunciation="سايانغ / تشانتيك", country="إندونيسيا",
    situation="⚠️ غريبة", register="حميمي", frequency="⚠️ حساسة",
    confidence="عالية", sources="I4", gender="امرأة")

add(id="ID034", category="I إغلاق", subcategory="دفع", arabic="كاش أو شبكة",
    targetLanguage="id", originalText="Bayar tunai atau qris/kartu?",
    arabicTranslation="نقدًا أو QR/بطاقة؟", arabicPronunciation="بايار توناي أو كريس",
    country="إندونيسيا", situation="دفع", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="I4", nodirect="yes")

add(id="ID035", category="A جذب", subcategory="تصفية", arabic="حراج / تصفية",
    targetLanguage="id", originalText="Cuci gudang!", arabicTranslation="تصفية مستودع",
    arabicPronunciation="تشوتشي غودانغ", country="إندونيسيا", situation="نداء سوق",
    register="شعبي", frequency="⭐ شائعة", confidence="عالية", sources="I4", nodirect="yes")

add(id="ID036", category="K وداع", subcategory="سلامة طريق", arabic="مع السلامة",
    targetLanguage="id", originalText="Hati-hati di jalan",
    arabicTranslation="انتبه في الطريق", arabicPronunciation="هاتي-هاتي دي جالان",
    country="إندونيسيا", situation="توديع", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="I4")

add(id="ID037", category="N إرجاع", subcategory="تبديل", arabic="نبدله",
    targetLanguage="id", originalText="Bisa ditukar", arabicTranslation="يمكن تبديله",
    arabicPronunciation="بيسا ديتوكار", country="إندونيسيا", situation="إرجاع",
    register="محترم وودود", frequency="🔥 شائعة جدًا", confidence="عالية", sources="I4")

add(id="ID038", category="E عرض", subcategory="تجربة", arabic="جرّب",
    targetLanguage="id", originalText="Coba dulu, Kak", arabicTranslation="جرّب أول",
    arabicPronunciation="تشوبا دولو", country="إندونيسيا", situation="ملابس/عطر/أكل",
    register="شعبي", frequency="🔥 شائعة جدًا", confidence="عالية", sources="I1")

add(id="ID039", category="H تفاوض", subcategory="رأس مال", arabic="ما أقدر",
    targetLanguage="id", originalText="Saya belum balik modal",
    arabicTranslation="بعدني ما غطيت رأس المال", arabicPronunciation="سايا بلوم باليك مودال",
    country="إندونيسيا", situation="رفض خصم", register="شعبي",
    frequency="⭐ شائعة", confidence="عالية", sources="I1 I2")

add(id="ID040", category="K غير مشترٍ", subcategory="وجه طيب", arabic="ولا يهمك",
    targetLanguage="id", originalText="Nggak apa-apa, lain kali mampir lagi",
    arabicTranslation="عادي، المرة الجاية تعال", arabicPronunciation="إنغّاك آبا-آبا",
    country="إندونيسيا", situation="لم يشترِ", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="I4")

# ===================== TAJIK =====================
add(id="TJ001", category="B ترحيب", subcategory="ترحيب عام", arabic="يا هلا وسهلا",
    targetLanguage="tg", originalText="Хуш омадед", arabicTranslation="أهلًا وسهلًا",
    lit="جئتم طيبين", arabicPronunciation="خوش آمديد", country="طاجيكستان",
    situation="دخول المحل", register="محترم وودود", frequency="🔥 شائعة جدًا",
    confidence="عالية", sources="J1 J2")

add(id="TJ002", category="B ترحيب", subcategory="دعوة", arabic="تفضل",
    targetLanguage="tg", originalText="Марҳамат", arabicTranslation="تفضل / خذ / ادخل",
    arabicPronunciation="مرحَمَت", country="طاجيكستان", situation="دعوة متعددة الوظائف",
    register="محترم وودود", frequency="🔥 شائعة جدًا", confidence="عالية", sources="J3")

add(id="TJ003", category="B ترحيب", subcategory="إسلامي", arabic="السلام عليكم",
    targetLanguage="tg", originalText="Ассалом алейкум", arabicTranslation="السلام عليكم",
    arabicPronunciation="أسلوم عليكوم", country="طاجيكستان", situation="افتتاح اللقاء",
    register="محترم وودود", frequency="🔥 شائعة جدًا", confidence="عالية", sources="J3")

add(id="TJ004", category="A جذب", subcategory="نداء", arabic="تعال شوف",
    targetLanguage="tg", originalText="Биёед, бинед", arabicTranslation="تعال انظر",
    arabicPronunciation="بيوييد، بينيد", country="طاجيكستان", situation="جذب",
    register="شعبي", frequency="🔥 شائعة جدًا", confidence="عالية", sources="J3")

add(id="TJ005", category="A جذب", subcategory="جديد", arabic="وصل اليوم",
    targetLanguage="tg", originalText="Нав омад", arabicTranslation="وصل جديد",
    arabicPronunciation="نوْ آمد", country="طاجيكستان", situation="نداء حداثة",
    register="شعبي", frequency="🔥 شائعة جدًا", confidence="متوسطة", sources="J3")

add(id="TJ006", category="C مخاطبة", subcategory="رجل", arabic="يا أخوي",
    targetLanguage="tg", originalText="Ака", arabicTranslation="يا أخ (أكبر)",
    arabicPronunciation="أكا", country="طاجيكستان", situation="مخاطبة رجل",
    register="شعبي", frequency="🔥 شائعة جدًا", confidence="عالية", sources="J3",
    gender="رجل", alt="Ҷаноб")

add(id="TJ007", category="C مخاطبة", subcategory="امرأة", arabic="يا أختي / يا أستاذة",
    targetLanguage="tg", originalText="Апа", arabicTranslation="يا أخت (أكبر)",
    arabicPronunciation="أپا", country="طاجيكستان", situation="مخاطبة امرأة",
    register="شعبي", frequency="🔥 شائعة جدًا", confidence="عالية", sources="J3",
    gender="امرأة", alt="Хонум")

add(id="TJ008", category="C مخاطبة", subcategory="رجل مهذب", arabic="يا أستاذ",
    targetLanguage="tg", originalText="Ҷаноб", arabicTranslation="يا جناب",
    arabicPronunciation="جناب", country="طاجيكستان", situation="أدب أعلى",
    register="محترم وودود", frequency="⭐ شائعة", confidence="عالية", sources="J3",
    gender="رجل")

add(id="TJ009", category="C مخاطبة", subcategory="امرأة مهذبة", arabic="يا مدام",
    targetLanguage="tg", originalText="Хонум", arabicTranslation="يا خانم / سيدتي",
    arabicPronunciation="خانم", country="طاجيكستان", situation="أدب أعلى",
    register="محترم وودود", frequency="🔥 شائعة جدًا", confidence="عالية", sources="J3",
    gender="امرأة")

add(id="TJ010", category="L ضيافة", subcategory="شاي", arabic="تفضل شاي؟",
    targetLanguage="tg", originalText="Чой бинӯшед", arabicTranslation="اشرب شاي",
    arabicPronunciation="چوي بينوشيد", country="طاجيكستان", situation="دكان تقليدي/بازار",
    register="شعبي", frequency="⭐ شائعة", confidence="متوسطة", sources="J3")

add(id="TJ011", category="D اكتشاف", subcategory="متفرج", arabic="خذ راحتك",
    targetLanguage="tg", originalText="Марҳамат, озодона бинед",
    arabicTranslation="تفضل انظر بحرية", arabicPronunciation="مرحمت، أزودونا بينيد",
    country="طاجيكستان", situation="رد المتفرج", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="متوسطة", sources="J3")

add(id="TJ012", category="H سعر", subcategory="سؤال", arabic="بكم؟",
    targetLanguage="tg", originalText="Ин чанд пул?", arabicTranslation="بكم هذا؟",
    arabicPronunciation="إن چند پول", country="طاجيكستان", situation="سؤال سعر",
    register="شعبي", frequency="🔥 شائعة جدًا", confidence="عالية", sources="J1",
    alt="Нархаш чанд?|Сколько стоит?")

add(id="TJ013", category="H سعر", subcategory="آخر سعر", arabic="آخر سعر",
    targetLanguage="tg", originalText="Нархи охирин", arabicTranslation="آخر سعر",
    arabicPronunciation="نرخِ آخرين", country="طاجيكستان", situation="تفاوض",
    register="شعبي", frequency="🔥 شائعة جدًا", confidence="متوسطة", sources="J3")

add(id="TJ014", category="G اعتراض", subcategory="غالي", arabic="غالي",
    targetLanguage="tg", originalText="Ин хеле қиммат",
    arabicTranslation="هذا غالي جدًا", arabicPronunciation="إن هيلي قِيمت",
    country="طاجيكستان", situation="اعتراض زبون", register="شعبي",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="J1",
    alt="Ин бисёр ҳам қиммат")

add(id="TJ015", category="G اعتراض", subcategory="رد جودة", arabic="غالي؟ شوف الجودة",
    targetLanguage="tg", originalText="Қиммат не, сифаташ дигар",
    arabicTranslation="مو غالي، جودته غير", arabicPronunciation="قِيمت ني، صفاتش ديغر",
    country="طاجيكستان", situation="رد البائع", register="شعبي",
    frequency="⭐ شائعة", confidence="متوسطة", sources="J3")

add(id="TJ016", category="H خصم", subcategory="شخصي", arabic="عشانك",
    targetLanguage="tg", originalText="Барои шумо нарх медиҳам",
    arabicTranslation="أعطيك سعرًا", arabicPronunciation="براي شومو نرخ مِديهم",
    country="طاجيكستان", situation="خصم شخصي", register="شعبي",
    frequency="⭐ شائعة", confidence="متوسطة", sources="J3")

add(id="TJ017", category="H خصم", subcategory="دخيل روسي", arabic="خصم",
    targetLanguage="tg", originalText="Скидка медиҳам", arabicTranslation="أعطيك خصمًا",
    arabicPronunciation="سكيدكا مديهم", country="طاجيكستان", situation="سوق مختلط",
    register="شعبي", frequency="🔥 شائعة جدًا", confidence="عالية", sources="J4",
    nodirect="yes")

add(id="TJ018", category="H تفاوض", subcategory="كمية", arabic="إذا أخذت اثنين",
    targetLanguage="tg", originalText="Агар дуто гиред, тахфиф мекунам",
    arabicTranslation="إذا أخذت اثنين أخصم", arabicPronunciation="أغر دوتو غيريد، تخفيف ميكنم",
    country="طاجيكستان", situation="خصم مشروط", register="شعبي",
    frequency="🔥 شائعة جدًا", confidence="متوسطة", sources="J3")

add(id="TJ019", category="I إغلاق", subcategory="كيس", arabic="نغلفها / كيس",
    targetLanguage="tg", originalText="Пакет лозим? / Печон?",
    arabicTranslation="تبغي كيس / أغلف؟", arabicPronunciation="پاكت لازِم",
    country="طاجيكستان", situation="إغلاق", register="شعبي",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="J1 J4")

add(id="TJ020", category="K وداع", subcategory="عودة", arabic="حياك مرة ثانية",
    targetLanguage="tg", originalText="Боз биёед", arabicTranslation="تعال مرة ثانية",
    arabicPronunciation="باز بيوييد", country="طاجيكستان", situation="توديع",
    register="محترم وودود", frequency="🔥 شائعة جدًا", confidence="عالية", sources="J3",
    alt="То дидор|Хайр")

add(id="TJ021", category="K وداع", subcategory="شكر", arabic="شكرًا",
    targetLanguage="tg", originalText="Ташаккур / Раҳмат", arabicTranslation="شكرًا",
    arabicPronunciation="تشكور / رحمت", country="طاجيكستان", situation="شكر",
    register="محترم وودود", frequency="🔥 شائعة جدًا", confidence="عالية", sources="J1")

add(id="TJ022", category="E عرض", subcategory="جودة", arabic="جودة ممتازة",
    targetLanguage="tg", originalText="Сифаташ хуб", arabicTranslation="جودته طيبة",
    arabicPronunciation="صفاتش خوب", country="طاجيكستان", situation="مدح",
    register="شعبي", frequency="🔥 شائعة جدًا", confidence="عالية", sources="J3")

add(id="TJ023", category="E عرض", subcategory="أصلي", arabic="أصلي مو تقليد",
    targetLanguage="tg", originalText="Аслӣ, на қалбакӣ", arabicTranslation="أصلي لا مزيف",
    arabicPronunciation="أصلي، نَ قلبكي", country="طاجيكستان", situation="تمييز",
    register="شعبي", frequency="⭐ شائعة", confidence="متوسطة", sources="J3")

add(id="TJ024", category="N غضب", subcategory="اعتذار", arabic="معك حق",
    targetLanguage="tg", originalText="Шумо ҳақ доред. Ман гӯш мекунам",
    arabicTranslation="معك حق أسمعك", arabicPronunciation="شومو حق داريد",
    country="طاجيكستان", situation="غاضب", register="محترم وودود",
    frequency="⭐ شائعة", confidence="متوسطة", sources="J3")

add(id="TJ025", category="N إرجاع", subcategory="تبديل", arabic="نبدله",
    targetLanguage="tg", originalText="Иваз мекунем", arabicTranslation="نبدّل",
    arabicPronunciation="إيوز ميكنيم", country="طاجيكستان", situation="إرجاع",
    register="محترم وودود", frequency="⭐ شائعة", confidence="متوسطة", sources="J3")

add(id="TJ026", category="K دائم", subcategory="غبت", arabic="من زمان ما شفناك",
    targetLanguage="tg", originalText="Кайҳо шуморо надидем",
    arabicTranslation="ما شفناكم من زمان", arabicPronunciation="كايها شومورو نَديديم",
    country="طاجيكستان", situation="دائم", register="عفوي",
    frequency="⭐ شائعة", confidence="متوسطة", sources="J3", audience="زبون دائم")

add(id="TJ027", category="A جذب", subcategory="خصم", arabic="عندنا خصم",
    targetLanguage="tg", originalText="Тахфиф ҳаст", arabicTranslation="في خصم",
    arabicPronunciation="تخفيف هست", country="طاجيكستان", situation="جذب",
    register="شعبي", frequency="⭐ شائعة", confidence="عالية", sources="J3")

add(id="TJ028", category="H سعر", subcategory="عملة", arabic="هذا السعر",
    targetLanguage="tg", originalText="Нархаш … сомонӣ",
    arabicTranslation="سعره … سوموني", arabicPronunciation="نرخَش … سوموني",
    country="طاجيكستان", situation="ذكر السعر", register="شعبي",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="J1", nodirect="yes")

add(id="TJ029", category="L مائدة", subcategory="هنيئًا", arabic="بالعافية",
    targetLanguage="tg", originalText="Нӯш ҷон", arabicTranslation="هنيئًا",
    arabicPronunciation="نوش جان", country="طاجيكستان", situation="طعام",
    register="محترم وودود", frequency="⭐ شائعة", confidence="متوسطة", sources="J3",
    nodirect="yes")

add(id="TJ030", category="C مخاطبة", subcategory="تحذير", arabic="يا حبيبتي",
    targetLanguage="tg", originalText="Ҷонам / азизам",
    arabicTranslation="يا روحي / يا عزيزي — لا تُقال لغريبة",
    arabicPronunciation="جانم / عزيزم", country="طاجيكستان", situation="⚠️ غريبة",
    register="حميمي", frequency="⚠️ حساسة", confidence="عالية", sources="J3",
    gender="امرأة")

add(id="TJ031", category="D اكتشاف", subcategory="حاجة", arabic="شو بدك؟",
    targetLanguage="tg", originalText="Чӣ лозим? / Чӣ меҷӯед?",
    arabicTranslation="إيش لازم / إيش تدور؟", arabicPronunciation="چي لازِم",
    country="طاجيكستان", situation="فتح حديث", register="شعبي",
    frequency="🔥 شائعة جدًا", confidence="متوسطة", sources="J3")

add(id="TJ032", category="G اعتراض", subcategory="بديل", arabic="خيار أرخص",
    targetLanguage="tg", originalText="Яке арзонтар нишон диҳам",
    arabicTranslation="أوريك واحد أرخص", arabicPronunciation="يكى أرزونتر نيشان دِهم",
    country="طاجيكستان", situation="تحويل غالي", register="محترم وودود",
    frequency="⭐ شائعة", confidence="متوسطة", sources="J3")

add(id="TJ033", category="K غير مشترٍ", subcategory="باب مفتوح", arabic="تعال أي وقت",
    targetLanguage="tg", originalText="Харидан шарт нест. Бори дигар биёед",
    arabicTranslation="الشراء مش شرط. تعال مرة ثانية",
    arabicPronunciation="خريدن شرط نيست", country="طاجيكستان", situation="لم يشترِ",
    register="محترم وودود", frequency="⭐ شائعة", confidence="متوسطة", sources="J3")

add(id="TJ034", category="H تفاوض", subcategory="تحت هذا لا", arabic="هذا أقل سعر",
    targetLanguage="tg", originalText="Аз ин поён намешавад",
    arabicTranslation="تحت هذا ما ينزل", arabicPronunciation="أز إن پاين نمى شود",
    country="طاجيكستان", situation="إغلاق نزول", register="شعبي",
    frequency="⭐ شائعة", confidence="متوسطة", sources="J3")

add(id="TJ035", category="J إضافي", subcategory="مكمل", arabic="خذ معها",
    targetLanguage="tg", originalText="Инро ҳам гиред, мувофиқ аст",
    arabicTranslation="خذ هذا أيضًا يناسبه", arabicPronunciation="إنرو هم غيريد",
    country="طاجيكستان", situation="بيع إضافي", register="شعبي",
    frequency="⭐ شائعة", confidence="متوسطة", sources="J3")

# ===================== FRENCH =====================
add(id="FR001", category="B ترحيب", subcategory="إلزام اجتماعي", arabic="أهلًا / السلام عليكم",
    targetLanguage="fr", originalText="Bonjour Monsieur / Madame",
    arabicTranslation="صباح الخير يا سيد/سيدتي", arabicPronunciation="بونجور مسيو / مادام",
    country="فرنسا", situation="أول كلمة عند الدخول", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="F1 F5", nodirect="yes",
    notes="الدخول بلا Bonjour يُعد وقاحة.")

add(id="FR002", category="B ترحيب", subcategory="ترحيب", arabic="أهلًا وسهلًا",
    targetLanguage="fr", originalText="Bienvenue", arabicTranslation="مرحبًا بكم",
    arabicPronunciation="بيانْڤو", country="فرنسا", situation="محل سياحي/فندق",
    register="محترم وودود", frequency="⭐ شائعة", confidence="عالية", sources="F2")

add(id="FR003", category="B ترحيب", subcategory="دعوة", arabic="تفضل",
    targetLanguage="fr", originalText="Je vous en prie",
    arabicTranslation="تفضل / العفو / تفضل ادخل", arabicPronunciation="جو ڤوز آن پري",
    country="فرنسا", situation="متعددة الوظائف", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="F5", nodirect="yes")

add(id="FR004", category="D اكتشاف", subcategory="مساعدة", arabic="كيف أقدر أساعدك؟",
    targetLanguage="fr", originalText="Je peux vous aider ?",
    arabicTranslation="أقدر أساعدكم؟", arabicPronunciation="جو پُو ڤو زيديه",
    country="فرنسا", situation="بعد السلام", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="F2")

add(id="FR005", category="D اكتشاف", subcategory="متفرج", arabic="بس أتفرج",
    targetLanguage="fr", originalText="Je ne fais que regarder",
    arabicTranslation="أتفرج فقط", arabicPronunciation="جو نُ فاي كُ رغارديه",
    country="فرنسا", situation="الزبون يتفرج", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="F2")

add(id="FR006", category="D اكتشاف", subcategory="رد متفرج", arabic="خذ راحتك",
    targetLanguage="fr", originalText="Bien sûr, je vous laisse regarder",
    arabicTranslation="طبعًا أتركك تنظر", arabicPronunciation="بيان سور، جو ڤو ليس رغارديه",
    country="فرنسا", situation="رد البائع", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="F1",
    alt="Prenez votre temps")

add(id="FR007", category="A جذب", subcategory="سوق", arabic="تعال شوف",
    targetLanguage="fr", originalText="Venez voir / Approchez",
    arabicTranslation="تعال انظر / اقترب", arabicPronunciation="ڤنيه ڤوار / آپروشيه",
    country="فرنسا/فرنكوفونية", situation="marché / سوق شعبي", register="شعبي",
    frequency="⭐ شائعة", confidence="عالية", sources="F1")

add(id="FR008", category="A جذب", subcategory="عرض", arabic="عندنا عرض",
    targetLanguage="fr", originalText="C’est soldé / Y a une promo",
    arabicTranslation="عليه تخفيض / في عرض", arabicPronunciation="سي سولديه / يا يون پرومو",
    country="فرنسا", situation="عروض", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="F2")

add(id="FR009", category="C مخاطبة", subcategory="رجل", arabic="يا أستاذ",
    targetLanguage="fr", originalText="Monsieur", arabicTranslation="يا سيد",
    arabicPronunciation="مسيو", country="فرنسا", situation="أي رجل بالغ غريب",
    register="محترم وودود", frequency="🔥 شائعة جدًا", confidence="عالية", sources="F1",
    gender="رجل")

add(id="FR010", category="C مخاطبة", subcategory="امرأة", arabic="يا أستاذة / يا مدام",
    targetLanguage="fr", originalText="Madame", arabicTranslation="يا سيدة",
    arabicPronunciation="مادام", country="فرنسا", situation="أي امرأة بالغة",
    register="محترم وودود", frequency="🔥 شائعة جدًا", confidence="عالية", sources="F1",
    gender="امرأة", notes="Mademoiselle حساسة في فرنسا المعاصرة.")

add(id="FR011", category="H سعر", subcategory="سؤال", arabic="بكم؟",
    targetLanguage="fr", originalText="C’est combien ?", arabicTranslation="بكم؟",
    arabicPronunciation="سي كوميان", country="فرنسا", situation="سؤال سعر",
    register="شعبي", frequency="🔥 شائعة جدًا", confidence="عالية", sources="F1 F2")

add(id="FR012", category="H سعر", subcategory="ثابت", arabic="السعر ثابت",
    targetLanguage="fr", originalText="C’est le prix affiché",
    arabicTranslation="هذا السعر المعلن", arabicPronunciation="سي لُ پري أفيشيه",
    country="فرنسا", situation="متجر حديث", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="F5")

add(id="FR013", category="H خصم", subcategory="لفتة", arabic="عشانك أنزل شوي",
    targetLanguage="fr", originalText="Je vous fais un geste",
    arabicTranslation="أعمل لك لفتة (خصم صغير)", arabicPronunciation="جو ڤو فاي أون جيست",
    country="فرنسا", situation="خصم مسموح", register="محترم وودود",
    frequency="⭐ شائعة", confidence="عالية", sources="F5", nodirect="yes")

add(id="FR014", category="H خصم", subcategory="سعر خاص", arabic="عشانك",
    targetLanguage="fr", originalText="Je vous fais un prix",
    arabicTranslation="أعطيك سعرًا", arabicPronunciation="جو ڤو فاي أون پري",
    country="فرنسا/المغرب/غرب أفريقيا", situation="مساومة", register="شعبي",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="F5")

add(id="FR015", category="H سعر", subcategory="آخر سعر", arabic="آخر سعر",
    targetLanguage="fr", originalText="C’est mon dernier prix",
    arabicTranslation="هذا آخر سعر", arabicPronunciation="سي مون ديرنيه پري",
    country="أسواق/puces/مغرب", situation="تفاوض", register="شعبي",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="F1")

add(id="FR016", category="H تفاوض", subcategory="نتوسط", arabic="خلينا نتفق",
    targetLanguage="fr", originalText="On coupe la poire en deux",
    arabicTranslation="نتوسط الفرق", lit="نقطع الإجاصة نصفين",
    arabicPronunciation="أون كوپ لا پوار آن دُ", country="فرنسا", situation="مساومة مهذبة",
    register="شعبي", frequency="⭐ شائعة", confidence="عالية", sources="F5", nodirect="yes")

add(id="FR017", category="H خصم", subcategory="هدية/تقريب", arabic="زيادة / على الحساب",
    targetLanguage="fr", originalText="C’est cadeau",
    arabicTranslation="هدية / على الحساب / السعر تافه", arabicPronunciation="سي كادو",
    country="فرنسا + فرنكوفونية", situation="تقريب أو زيادة أو وصف سعر",
    register="شعبي", frequency="🔥 شائعة جدًا", confidence="عالية", sources="F3",
    nodirect="yes")

add(id="FR018", category="G اعتراض", subcategory="غالي", arabic="غالي",
    targetLanguage="fr", originalText="C’est un peu cher",
    arabicTranslation="شوي غالي", arabicPronunciation="سي أون پُ شير",
    country="فرنسا", situation="اعتراض مهذب", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="F2",
    alt="C’est trop cher")

add(id="FR019", category="G اعتراض", subcategory="رد جودة", arabic="غالي؟ شوف الجودة",
    targetLanguage="fr", originalText="C’est le prix de la qualité",
    arabicTranslation="هذا سعر الجودة", arabicPronunciation="سي لُ پري دُ لا كاليتيه",
    country="فرنسا", situation="رد", register="محترم وودود",
    frequency="⭐ شائعة", confidence="عالية", sources="F5")

add(id="FR020", category="G اعتراض", subcategory="بديل", arabic="خيار أرخص",
    targetLanguage="fr", originalText="Je vous montre une gamme plus douce",
    arabicTranslation="أوريك شريحة ألطف سعرًا", arabicPronunciation="جو ڤو مونتر يون غام پلو دوس",
    country="فرنسا", situation="تحويل", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="F5")

add(id="FR021", category="I إغلاق", subcategory="تغليف", arabic="نغلفها لك؟",
    targetLanguage="fr", originalText="Je vous l’emballe ?",
    arabicTranslation="أغلفها لكم؟", arabicPronunciation="جو ڤو لومبال",
    country="فرنسا", situation="إغلاق ناعم", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="F2")

add(id="FR022", category="I إغلاق", subcategory="دفع", arabic="كاش أو بطاقة",
    targetLanguage="fr", originalText="Carte ou espèces ?",
    arabicTranslation="بطاقة ولا نقد؟", arabicPronunciation="كارت أو إسپيس",
    country="فرنسا", situation="دفع", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="F2")

add(id="FR023", category="K وداع", subcategory="وداع كامل", arabic="مع السلامة نورتنا",
    targetLanguage="fr", originalText="Merci, au revoir, bonne journée",
    arabicTranslation="شكرًا مع السلامة يوم سعيد",
    arabicPronunciation="ميرسي، أورڤوار، بون جورنيه", country="فرنسا", situation="توديع",
    register="محترم وودود", frequency="🔥 شائعة جدًا", confidence="عالية", sources="F1 F5")

add(id="FR024", category="K وداع", subcategory="عودة", arabic="حياك مرة ثانية",
    targetLanguage="fr", originalText="À bientôt / Au plaisir de vous revoir",
    arabicTranslation="إلى اللقاء", arabicPronunciation="آ بيانْتو",
    country="فرنسا", situation="توديع", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="F5")

add(id="FR025", category="K دائم", subcategory="المعتاد", arabic="إيش نجهز لك",
    targetLanguage="fr", originalText="Comme d’habitude ?", arabicTranslation="كالعادة؟",
    arabicPronunciation="كوم داديتود", country="فرنسا", situation="زبون دائم",
    register="عفوي", frequency="🔥 شائعة جدًا", confidence="عالية", sources="F5",
    audience="زبون دائم")

add(id="FR026", category="N غضب", subcategory="استماع", arabic="معك حق",
    targetLanguage="fr", originalText="Je vous écoute / Vous avez raison",
    arabicTranslation="أسمعكم / معكم حق", arabicPronunciation="جو ڤو زكوت",
    country="فرنسا", situation="غاضب", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="F5",
    notes="تجنّب Calmez-vous.")

add(id="FR027", category="N إرجاع", subcategory="حل", arabic="نبدله أو نرجّع",
    targetLanguage="fr", originalText="On échange ou on rembourse",
    arabicTranslation="نبدّل أو نرجّع المبلغ", arabicPronunciation="أون إشانج أو أون رنبورس",
    country="فرنسا", situation="شكوى", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="F2")

add(id="FR028", category="J إضافي", subcategory="مكمل", arabic="خذ معها",
    targetLanguage="fr", originalText="Je vous montre ce qui va avec",
    arabicTranslation="أوريك اللي يمشي معه", arabicPronunciation="جو ڤو مونتر سُ كي ڤا أڤيك",
    country="فرنسا", situation="بيع إضافي", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="F5")

add(id="FR029", category="C مخاطبة", subcategory="تحذير", arabic="يا حبيبتي",
    targetLanguage="fr", originalText="Chérie / ma belle",
    arabicTranslation="يا حبيبتي / يا جميلة — خط أحمر",
    arabicPronunciation="شيري / ما بيل", country="فرنسا", situation="⚠️ غريبة",
    register="حميمي", frequency="⚠️ حساسة", confidence="عالية", sources="F4 F5",
    gender="امرأة")

add(id="FR030", category="C مخاطبة", subcategory="تحذير tu", arabic="ألفة زائدة",
    targetLanguage="fr", originalText="Tutoiement فجائي (tu)",
    arabicTranslation="مخاطبة بـأنت بدل vous", arabicPronunciation="تو",
    country="فرنسا", situation="زبون غريب في محل", register="حميمي",
    frequency="⚠️ حساسة", confidence="عالية", sources="F4")

add(id="FR031", category="E عرض", subcategory="جديد", arabic="وصل اليوم",
    targetLanguage="fr", originalText="C’est tout juste arrivé",
    arabicTranslation="وصل توّه", arabicPronunciation="سي تو جوست أريڤيه",
    country="فرنسا", situation="عرض", register="محترم وودود",
    frequency="⭐ شائعة", confidence="عالية", sources="F5")

add(id="FR032", category="E عرض", subcategory="الأكثر مبيعًا", arabic="عليه طلب",
    targetLanguage="fr", originalText="C’est notre best-seller",
    arabicTranslation="هذا الأكثر مبيعًا", arabicPronunciation="سي نوتر بيست سيلر",
    country="فرنسا", situation="إثبات اجتماعي", register="محترم وودود",
    frequency="⭐ شائعة", confidence="عالية", sources="F5")

add(id="FR033", category="E عرض", subcategory="يليق", arabic="يليق عليك",
    targetLanguage="fr", originalText="Ça vous va très bien",
    arabicTranslation="يليق عليك جدًا", arabicPronunciation="سا ڤو ڤا تري بيان",
    country="فرنسا", situation="أمام المرآة", register="محترم وودود",
    frequency="⭐ شائعة", confidence="عالية", sources="F2")

add(id="FR034", category="A جذب", subcategory="سوق غذاء", arabic="زيادة مني",
    targetLanguage="fr", originalText="Je vous mets un peu plus, c’est cadeau",
    arabicTranslation="أزودك شوي، هدية", arabicPronunciation="جو ڤو مي أون پُ پلو، سي كادو",
    country="فرنسا", situation="سوق خضار/جبن", register="شعبي",
    frequency="⭐ شائعة", confidence="عالية", sources="F3 F5")

add(id="FR035", category="I إغلاق", subcategory="طعام", arabic="خلاص؟",
    targetLanguage="fr", originalText="Ce sera tout ?", arabicTranslation="هذا كل شيء؟",
    arabicPronunciation="سُ سرا تو", country="فرنسا", situation="مخبز/مقهى/كاشير",
    register="محترم وودود", frequency="🔥 شائعة جدًا", confidence="عالية", sources="F5",
    nodirect="yes")

add(id="FR036", category="K غير مشترٍ", subcategory="وجه طيب", arabic="ولا يهمك",
    targetLanguage="fr", originalText="Pas de souci. Revenez quand vous voulez",
    arabicTranslation="ما في مشكلة. ارجع متى ما حبيت",
    arabicPronunciation="پا دُ سوسي", country="فرنسا", situation="لم يشترِ",
    register="محترم وودود", frequency="🔥 شائعة جدًا", confidence="عالية", sources="F1")

add(id="FR037", category="H تفاوض", subcategory="كمية", arabic="إذا أخذت اثنين",
    targetLanguage="fr", originalText="Si vous en prenez deux, je fais un effort",
    arabicTranslation="إذا أخذت اثنين أبذل جهدًا",
    arabicPronunciation="سي ڤو زان پرنيه دُ", country="فرنسا/أسواق", situation="خصم مشروط",
    register="شعبي", frequency="⭐ شائعة", confidence="عالية", sources="F5")

add(id="FR038", category="L مغرب", subcategory="حرارة سوق", arabic="عشانك",
    targetLanguage="fr", originalText="C’est bon prix",
    arabicTranslation="سعر طيب", arabicPronunciation="سي بون پري",
    country="المغرب/تونس/الجزائر", situation="مساومة", register="شعبي",
    frequency="🔥 شائعة جدًا", confidence="متوسطة", sources="F5", region="مغرب")

add(id="FR039", category="N إرجاع", subcategory="فاتورة", arabic="معك الفاتورة؟",
    targetLanguage="fr", originalText="Vous avez le ticket ?",
    arabicTranslation="معكم الإيصال؟", arabicPronunciation="ڤو زاڤيه لُ تيكيه",
    country="فرنسا", situation="إرجاع", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="F2")

add(id="FR040", category="E عرض", subcategory="تجربة", arabic="جرّب",
    targetLanguage="fr", originalText="Je vous le fais essayer",
    arabicTranslation="أخليك تجربه", arabicPronunciation="جو ڤو لُ فاي إيسييه",
    country="فرنسا", situation="ملابس/عطر", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="F2")

# ===================== ENGLISH =====================
add(id="EN001", category="B ترحيب", subcategory="ترحيب عام", arabic="يا هلا وسهلا",
    targetLanguage="en", originalText="Hi there / Welcome in",
    arabicTranslation="أهلًا / تفضل ادخل", arabicPronunciation="هاي ذير / وِلكم إن",
    country="UK/US", situation="ترحيب عند الدخول", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="E1 E5",
    notes="لا مقابل حرفي لـ«نورتونا». للدائم: Good to see you.")

add(id="EN002", category="B ترحيب", subcategory="دعوة", arabic="تفضل",
    targetLanguage="en", originalText="Come on in",
    arabicTranslation="ادخل / تفضل", arabicPronunciation="كَم أون إن",
    country="UK/US", situation="دعوة الدخول", register="شعبي",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="E5",
    alt="Go ahead|After you")

add(id="EN003", category="D اكتشاف", subcategory="متفرج", arabic="بس أتفرج",
    targetLanguage="en", originalText="Just browsing / just looking",
    arabicTranslation="بس أتفرج", arabicPronunciation="جَست براوزِنغ",
    country="UK/US", situation="الزبون يرفض المساعدة بلطف", register="شعبي",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="E1 E2",
    nodirect="yes", notes="جملة ثقافية: غالبًا تعني اتركني. ليست مجرد ترجمة «أتفرج».")

add(id="EN004", category="D اكتشاف", subcategory="رد متفرج", arabic="خذ راحتك أنا موجود",
    targetLanguage="en", originalText="I'll be right here if you need me",
    arabicTranslation="أنا هنا إذا احتجتني", arabicPronunciation="آيل بي رايت هير إف يو نيد مي",
    country="UK/US", situation="رد على just browsing", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="E2 E5",
    alt="Take your time|No problem")

add(id="EN005", category="A جذب", subcategory="مساعدة UK", arabic="محتاج شيء؟",
    targetLanguage="en", originalText="You all right there?",
    arabicTranslation="محتاج مساعدة؟ (ليست سؤال صحة)", lit="هل أنت بخير هناك؟",
    arabicPronunciation="يو أول رايت ذير", country="المملكة المتحدة",
    situation="اقتراب من زبون في محل بريطاني", register="شعبي",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="E5",
    nodirect="yes", region="بريطانيا")

add(id="EN006", category="A جذب", subcategory="بلا التزام", arabic="بس شوف ما بتخسر شيء",
    targetLanguage="en", originalText="Have a look, no obligation",
    arabicTranslation="شوف، بلا التزام", arabicPronunciation="هاف أ لوك، نو أوبليغيشن",
    country="UK/US", situation="سوق أو بسطة", register="شعبي",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="E3 E5")

add(id="EN007", category="A جذب", subcategory="منتج", arabic="جديد وصل اليوم",
    targetLanguage="en", originalText="This just came in",
    arabicTranslation="هذا وصل توّه", arabicPronunciation="ذِس جَست كيم إن",
    country="UK/US", situation="عرض حداثة", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="E5")

add(id="EN008", category="C مخاطبة", subcategory="رجل مهذب", arabic="يا أستاذ",
    targetLanguage="en", originalText="Sir",
    arabicTranslation="يا سيد — قليلًا أو بلا لقب", arabicPronunciation="سَر",
    country="UK/US", situation="مخاطبة رجل", register="محترم وودود",
    frequency="⭐ شائعة", confidence="عالية", sources="E5",
    gender="رجل", notes="الإنجليزية تبيع غالبًا بلا لقب.")

add(id="EN009", category="C مخاطبة", subcategory="امرأة مهذبة", arabic="يا أستاذة",
    targetLanguage="en", originalText="Ma'am / (بلا لقب)",
    arabicTranslation="يا سيدتي أو بلا نداء", arabicPronunciation="مام",
    country="الولايات المتحدة", situation="مخاطبة امرأة", register="محترم وودود",
    frequency="⭐ شائعة", confidence="عالية", sources="E5",
    gender="امرأة", notes="بعض النساء يكرهن Ma'am.")

add(id="EN010", category="C مخاطبة", subcategory="تحذير", arabic="يا حبيبتي (ممنوع)",
    targetLanguage="en", originalText="Babe / gorgeous / honey",
    arabicTranslation="يا حلوة / يا عسل — خط أحمر مع غريبة",
    arabicPronunciation="بيب / غورجَس / هاني", country="UK/US",
    situation="⚠️ لا تُقال لامرأة غريبة", register="حميمي",
    frequency="⚠️ حساسة", confidence="عالية", sources="E5", gender="امرأة")

add(id="EN011", category="D اكتشاف", subcategory="تفرج أم طلب",
    arabic="بتدور على شيء ولا بتتفرج؟", targetLanguage="en",
    originalText="Looking for anything in particular?",
    arabicTranslation="تدور على شيء معيّن؟",
    arabicPronunciation="لوكِنغ فور إني ثِنغ إن بِرتِكيولَر",
    country="UK/US", situation="فتح حديث", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="E1")

add(id="EN012", category="E عرض", subcategory="تقديم", arabic="شوف هذا",
    targetLanguage="en", originalText="Have a look at this one",
    arabicTranslation="شوف هذا", arabicPronunciation="هاف أ لوك أت ذِس وَن",
    country="UK/US", situation="عرض منتج", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="E5")

add(id="EN013", category="E عرض", subcategory="طلب", arabic="عليه طلب",
    targetLanguage="en", originalText="It's one of our bestsellers",
    arabicTranslation="من الأكثر مبيعًا", arabicPronunciation="بِست سيلرز",
    country="UK/US", situation="إثبات اجتماعي", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="E5")

add(id="EN014", category="E عرض", subcategory="جودة", arabic="شغل نظيف",
    targetLanguage="en", originalText="It's well made — it'll last",
    arabicTranslation="شغل متقن ويعيش", arabicPronunciation="وِل ميد — إتِل لاست",
    country="UK/US", situation="مدح", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="E5")

add(id="EN015", category="E عرض", subcategory="يليق", arabic="يليق عليك",
    targetLanguage="en", originalText="It really suits you",
    arabicTranslation="يليق عليك", arabicPronunciation="إِت ريلي سووتس يو",
    country="UK/US", situation="أمام المرآة", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="E5",
    notes="نبرة مهنية لا غزل.", alt="It looks great on you")

add(id="EN016", category="H سعر", subcategory="سؤال", arabic="بكم؟",
    targetLanguage="en", originalText="How much is this?",
    arabicTranslation="بكم هذا؟", arabicPronunciation="هاو مَتش إز ذِس",
    country="UK/US", situation="سؤال سعر", register="شعبي",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="E1 E3")

add(id="EN017", category="H سعر", subcategory="ثابت", arabic="السعر ثابت",
    targetLanguage="en", originalText="That's the ticket price",
    arabicTranslation="هذا سعر البطاقة", arabicPronunciation="تيكِت پرايس",
    country="UK/US", situation="متجر حديث", register="محترم وودود",
    frequency="⭐ شائعة", confidence="عالية", sources="E4 E5",
    alt="That's the marked price")

add(id="EN018", category="H سعر", subcategory="آخر سعر", arabic="آخر سعر",
    targetLanguage="en", originalText="That's as low as I can go",
    arabicTranslation="هذا أقل سعر أقدر عليه", arabicPronunciation="ذات آز لو آز آي كان غو",
    country="UK/US أسواق", situation="مساومة في سوق لا هاي ستريت", register="شعبي",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="E3",
    alt="Best I can do is…")

add(id="EN019", category="H خصم", subcategory="شخصي", arabic="عشانك نضبطها",
    targetLanguage="en", originalText="I can do a bit better",
    arabicTranslation="أقدر أحسّن السعر شوي", arabicPronunciation="آي كان دو أ بِت بِتَر",
    country="أسواق/تحف/سيارات", situation="خصم إن كان مسموحًا", register="شعبي",
    frequency="⭐ شائعة", confidence="عالية", sources="E3",
    alt="I can knock a bit off")

add(id="EN020", category="H تفاوض", subcategory="هدية بدل خصم", arabic="زيادة مني",
    targetLanguage="en", originalText="I'll throw that in",
    arabicTranslation="أضيف لك هذا", arabicPronunciation="آيل ثرو ذات إن",
    country="أسواق", situation="إضافة بدل إنزال الرقم", register="شعبي",
    frequency="⭐ شائعة", confidence="عالية", sources="E3 E5", nodirect="yes")

add(id="EN021", category="H تفاوض", subcategory="نتوسط", arabic="خلينا نتفق",
    targetLanguage="en", originalText="Let's split the difference",
    arabicTranslation="نتوسط الفرق", lit="نقسم الفرق",
    arabicPronunciation="سبْلِت ذَ دِفْرَنس", country="أسواق/سيارات",
    situation="مساومة", register="شعبي", frequency="⭐ شائعة", confidence="عالية",
    sources="E3", nodirect="yes")

add(id="EN022", category="H تفاوض", subcategory="اتفاق", arabic="اتفقنا",
    targetLanguage="en", originalText="You've got a deal",
    arabicTranslation="اتفقنا", arabicPronunciation="يوڤ غوت أ ديل",
    country="UK/US", situation="إغلاق مساومة", register="شعبي",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="E3")

add(id="EN023", category="G اعتراض", subcategory="غالي", arabic="غالي",
    targetLanguage="en", originalText="That's a bit pricey / a bit steep",
    arabicTranslation="شوي غالي", arabicPronunciation="أ بِت پرايسي / ستيب",
    country="UK/US", situation="اعتراض زبون", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="E3 E5")

add(id="EN024", category="G اعتراض", subcategory="رد جودة", arabic="غالي؟ شوف الجودة",
    targetLanguage="en", originalText="It's a bit more, but the quality's there",
    arabicTranslation="أغلى شوي بس الجودة ظاهرة",
    arabicPronunciation="أ بِت مور بَت ذَ كوولِتي ذير", country="UK/US",
    situation="رد على pricey", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="E5")

add(id="EN025", category="G اعتراض", subcategory="بديل", arabic="عندي خيار أرخص",
    targetLanguage="en", originalText="Let me show you something in a different price range",
    arabicTranslation="أوريك شي في شريحة سعر ثانية",
    arabicPronunciation="دِفْرَنت پرايس رينج", country="UK/US",
    situation="محل حديث بلا مساومة", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="E5")

add(id="EN026", category="I إغلاق", subcategory="تغليف", arabic="نغلفها لك؟",
    targetLanguage="en", originalText="Shall I wrap that for you?",
    arabicTranslation="أغلفها لك؟", arabicPronunciation="شال آي راپ ذات",
    country="UK/US", situation="إغلاق ناعم", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="E5")

add(id="EN027", category="I إغلاق", subcategory="زيادة بيع", arabic="شيء ثاني؟",
    targetLanguage="en", originalText="Anything else today?",
    arabicTranslation="شيء ثاني اليوم؟", arabicPronunciation="إني ثِنغ إلس تُدي",
    country="UK/US", situation="قبل الدفع", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="E5",
    alt="Will that be all?")

add(id="EN028", category="I إغلاق", subcategory="دفع", arabic="كاش أو بطاقة",
    targetLanguage="en", originalText="Card or cash?",
    arabicTranslation="بطاقة ولا نقد؟", arabicPronunciation="كارد أور كاش",
    country="UK/US", situation="دفع", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="E5")

add(id="EN029", category="I إغلاق", subcategory="جاهز US", arabic="(لا مقابل مباشر)",
    targetLanguage="en", originalText="You're all set",
    arabicTranslation="صرت جاهز / خلصت العملية", arabicPronunciation="يور أول سِت",
    country="الولايات المتحدة", situation="بعد الدفع", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="E5", nodirect="yes")

add(id="EN030", category="K وداع", subcategory="وداع US", arabic="مع السلامة نورتنا",
    targetLanguage="en", originalText="Have a nice day",
    arabicTranslation="يوم سعيد", arabicPronunciation="هاف أ نايس دي",
    country="الولايات المتحدة", situation="توديع", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="E5",
    nodirect="yes", alt="Have a good one|Take care")

add(id="EN031", category="K وداع", subcategory="عودة", arabic="حياك مرة ثانية",
    targetLanguage="en", originalText="Thanks for coming in",
    arabicTranslation="شكرًا على الزيارة", arabicPronunciation="ثنكس فور كَمِنغ إن",
    country="UK/US", situation="توديع", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="E1 E5",
    alt="Pop back anytime (UK)")

add(id="EN032", category="K دائم", subcategory="المعتاد", arabic="إيش نجهز لك اليوم؟",
    targetLanguage="en", originalText="The usual?",
    arabicTranslation="المعتاد؟", arabicPronunciation="ذَ يوجوول",
    country="UK/US", situation="زبون دائم", register="عفوي",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="E5",
    audience="زبون دائم")

add(id="EN033", category="K دائم", subcategory="تمييز", arabic="يا هلا بالقديم",
    targetLanguage="en", originalText="Good to see you again",
    arabicTranslation="سررت برؤيتك مرة ثانية", arabicPronunciation="غود تو سي يو أغين",
    country="UK/US", situation="دائم رجع", register="عفوي",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="E5",
    audience="زبون دائم")

add(id="EN034", category="N غضب", subcategory="اعتذار", arabic="معك حق",
    targetLanguage="en", originalText="I'm sorry about that. Tell me what happened",
    arabicTranslation="آسف. قل لي ماذا صار", arabicPronunciation="آيم سوري أباوت ذات",
    country="UK/US", situation="غاضب", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="E5",
    notes="تجنّب Calm down.")

add(id="EN035", category="N إرجاع", subcategory="حل", arabic="نبدله أو نرجّع",
    targetLanguage="en", originalText="We can exchange it or refund you",
    arabicTranslation="نبدّل أو نرجّع المبلغ", arabicPronunciation="إكسشينج أور ريفاَند",
    country="UK/US", situation="إرجاع", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="E5")

add(id="EN036", category="N إرجاع", subcategory="فاتورة", arabic="معك الفاتورة؟",
    targetLanguage="en", originalText="Have you got the receipt? / Do you have the receipt?",
    arabicTranslation="معك الإيصال؟", arabicPronunciation="رِسيت",
    country="UK/US", situation="إرجاع", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="E5",
    notes="UK: have you got. US: do you have.")

add(id="EN037", category="J إضافي", subcategory="مكمل", arabic="خذ معها",
    targetLanguage="en", originalText="This goes really well with it",
    arabicTranslation="هذا يمشي معه", arabicPronunciation="غوز ريلي وِل وِث إِت",
    country="UK/US", situation="بيع إضافي", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="E5")

add(id="EN038", category="H سعر", subcategory="سياسة سلسلة", arabic="(لا مقابل مباشر سوقي عام)",
    targetLanguage="en", originalText="We can price-match",
    arabicTranslation="نساوي سعر المنافس", arabicPronunciation="پرايس ماتش",
    country="UK/US سلاسل", situation="اعتراض أرخص عند غيرنا", register="محترم وودود",
    frequency="⭐ شائعة", confidence="عالية", sources="E4", nodirect="yes")

add(id="EN039", category="L طعام", subcategory="سفري", arabic="سفري ولا هنا؟",
    targetLanguage="en", originalText="For here or to go? / Eat in or takeaway?",
    arabicTranslation="أكل هنا أم سفري؟", arabicPronunciation="فور هير أور تو غو / إيت إن أور تيكأوي",
    country="US / UK", situation="مقهى/وجبات", register="شعبي",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="E5", nodirect="yes",
    notes="US الأولى، UK الثانية.")

add(id="EN040", category="K غير مشترٍ", subcategory="وجه طيب", arabic="ولا يهمك",
    targetLanguage="en", originalText="No worries at all. Thanks for stopping by",
    arabicTranslation="أبدًا ما في مشكلة. شكرًا على المرور",
    arabicPronunciation="نو وَريز · ستوپِنغ باي", country="UK/US",
    situation="لم يشترِ", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="E5")

add(id="EN041", category="H تفاوض", subcategory="كمية", arabic="إذا أخذت اثنين",
    targetLanguage="en", originalText="If you take two I can do a bit more",
    arabicTranslation="إذا أخذت اثنين أقدر أنزّل أكثر",
    arabicPronunciation="إف يو تيك تو", country="أسواق", situation="خصم مشروط",
    register="شعبي", frequency="⭐ شائعة", confidence="عالية", sources="E3")

add(id="EN042", category="A جذب", subcategory="عرض", arabic="عندنا عرض",
    targetLanguage="en", originalText="It's on sale / it's in the sale",
    arabicTranslation="عليه تخفيض", arabicPronunciation="أون سيل / إن ذَ سيل",
    country="US / UK", situation="عروض", register="محترم وودود",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="E5",
    notes="US: on sale. UK كثيرًا: in the sale.")

add(id="EN043", category="D اكتشاف", subcategory="حجز", arabic="أحجزها لك",
    targetLanguage="en", originalText="I can put it aside / put it on hold",
    arabicTranslation="أحجزها لك", arabicPronunciation="پوت إِت أسايد / أون هولد",
    country="UK/US", situation="زبون متردد", register="محترم وودود",
    frequency="⭐ شائعة", confidence="عالية", sources="E5")

add(id="EN044", category="E عرض", subcategory="مثل قيمة", arabic="غالي مرة ولا رخيص مرتين",
    targetLanguage="en", originalText="Buy cheap, buy twice",
    arabicTranslation="اشترِ الرخيص تشتري مرتين", arabicPronunciation="باي تشيب باي توايس",
    country="UK/US", situation="إقناع بالجودة", register="شعبي",
    frequency="⭐ شائعة", confidence="عالية", sources="E5",
    notes="مثل لا جملة يومية لكل بائع.", alt="You get what you pay for")

add(id="EN045", category="K وداع", subcategory="UK خفيف", arabic="شكرًا / مع السلامة",
    targetLanguage="en", originalText="Cheers",
    arabicTranslation="شكرًا / سلام خفيف", arabicPronunciation="تشيرز",
    country="المملكة المتحدة", situation="شكر أو وداع غير رسمي", register="عفوي",
    frequency="🔥 شائعة جدًا", confidence="عالية", sources="E5",
    nodirect="yes", notes="ليست نخبًا هنا.")

assert len(rows) == len({x["id"] for x in rows}), "duplicate ids"
with open(path, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    w.writerows(rows)
print("wrote", len(rows), "rows to", path)
from collections import Counter
print(Counter(x["targetLanguage"] for x in rows))
print("noDirect", sum(1 for x in rows if x["noDirectArabic"] == "yes"))
