import re
from pathlib import Path

import pandas as pd
import streamlit as st

from content import (
    ICON_URL, FACTS, INTRO_EN, INTRO_FA,
    GEOGRAPHY_EN, GEOGRAPHY_FA,
    CULTURE_EN, CULTURE_FA,
    FOOD_EN, FOOD_FA,
    CLOTHING_EN, CLOTHING_FA,
    MINERALS_EN, MINERALS_FA,
)
from db import approved_submissions
from utils import bilingual_header


bilingual_header("ChatBadaksh", "چت‌بدخش", 1)

left, center, right = st.columns([1, 2, 1])
with center:
    st.markdown("<div class='chatbot-icon'>🤖</div>", unsafe_allow_html=True)
left, center, right = st.columns([1, 2, 1])
with center:
    st.image(ICON_URL, width=360)

st.write(
    "Ask ChatBadaksh in English or Farsi/Dari. It answers from the information published in this portal, including districts, geography, culture, food, fruits, clothing, minerals, Fayzabad and approved community content."
)
st.markdown(
    "<p class='rtl'>از چت‌بدخش به زبان انگلیسی یا فارسی/دری سؤال کنید. "
    "چت‌بدخش بر اساس معلومات منتشرشده در پورتال، از جمله ولسوالی‌ها، جغرافیا، فرهنگ، غذا، میوه‌ها، پوشاک، معادن، فیض‌آباد و مطالب تأییدشده مردم پاسخ می‌دهد.</p>",
    unsafe_allow_html=True,
)


@st.cache_data
def districts():
    return pd.read_csv(Path(__file__).resolve().parent.parent / "data" / "districts.csv")


df = districts()


def norm(text: str) -> str:
    """Normalize common Persian/Arabic and spacing variations for matching."""
    s = str(text or "").strip().lower()
    replacements = {
        "ي": "ی", "ى": "ی", "ك": "ک",
        "ۀ": "ه", "ة": "ه",
        "‌": " ", "ـ": "",
        "ؤ": "و", "ئ": "ی",
    }
    for a, b in replacements.items():
        s = s.replace(a, b)
    s = re.sub(r"\s+", " ", s)
    return s


def bilingual(en: str, fa: str) -> str:
    return f"English: {en}\n\nفارسی: {fa}"


def district_count_answer() -> str:
    n = len(df)
    names_en = "، ".join(df["district_en"].tolist())
    names_fa = "، ".join(df["district_fa"].tolist())
    return bilingual(
        f"Badakhshan has {n} districts in this portal's district table.",
        f"بدخشان در جدول معلوماتی این پورتال {n} ولسوالی دارد.",
    ) + f"\n\nEnglish district names: {names_en}\n\nنام ولسوالی‌ها: {names_fa}"


def district_answer(qn: str):
    for _, r in df.iterrows():
        en = norm(r.district_en)
        fa = norm(r.district_fa)
        cap_en = norm(r.capital_en)
        cap_fa = norm(r.capital_fa)
        if (en and en in qn) or (fa and fa in qn) or (cap_en and cap_en in qn) or (cap_fa and cap_fa in qn):
            return bilingual(
                f"{r.district_en} district has an estimated 2020 population of {int(r.population_2020):,} and an area of {int(r.area_km2):,} km².",
                f"ولسوالی {r.district_fa} بر اساس برآورد سال ۲۰۲۰ حدود {int(r.population_2020):,} نفر جمعیت و {int(r.area_km2):,} کیلومتر مربع مساحت دارد.",
            )
    return None


def approved_content_answer(qn: str):
    try:
        posts = approved_submissions()
    except Exception:
        posts = []
    for p in posts:
        text = " ".join([
            p.get("title_en") or "", p.get("title_fa") or "",
            p.get("body_en") or "", p.get("body_fa") or "",
        ])
        tokens = [t for t in re.findall(r"[\w\u0600-\u06ff]+", qn) if len(t) > 2]
        nt = norm(text)
        if tokens and any(norm(tok) in nt for tok in tokens):
            en = p.get("body_en") or ""
            fa = p.get("body_fa") or ""
            if en or fa:
                return bilingual(en or "See the approved Farsi content below.", fa or "مطلب تأییدشده در پورتال موجود است.")
    return None


def answer(q: str) -> str:
    qn = norm(q)

    # Districts / ولسوالی‌ها
    district_words = [
        "district", "districts", "wuleswali", "wuleswaliha",
        "ولسوالی", "ولسوالی ها", "ولسوالی‌های", "تعداد ولسوالی",
        "چند ولسوالی", "چند تا ولسوالی", "تعداد", "فهرست ولسوالی",
        "لیست ولسوالی",
    ]
    if any(norm(x) in qn for x in district_words) and any(
        x in qn for x in ["badakhshan", "بدخشان", "ولایت"]
    ):
        return district_count_answer()

    # General introduction / identity
    if any(x in qn for x in [
        "what is badakhshan", "about badakhshan", "بدخشان چیست",
        "درباره بدخشان", "معلومات بدخشان", "معرفی بدخشان",
    ]):
        return bilingual(INTRO_EN, INTRO_FA)

    # Population
    if any(x in qn for x in ["population", "people", "نفوس", "جمعیت", "چند نفر"]):
        return bilingual(
            f"Badakhshan's portal fact sheet gives a population of {FACTS['population']}.",
            f"در برگه معلوماتی پورتال، جمعیت بدخشان {FACTS['population_fa']} ذکر شده است.",
        )

    # Area
    if any(x in qn for x in ["area", "size", "مساحت", "وسعت", "کیلومتر مربع"]):
        return bilingual(
            f"The area listed in the portal is {FACTS['area']}.",
            f"مساحت درج‌شده در پورتال {FACTS['area_fa']} است.",
        )

    # Capital / Fayzabad
    if any(x in qn for x in ["capital", "fayzabad", "فیض آباد", "فیض‌آباد", "مرکز ولایت", "مرکز بدخشان"]):
        return bilingual(
            "Fayzabad is the capital of Badakhshan province.",
            "فیض‌آباد مرکز ولایت بدخشان است.",
        )

    # Borders / neighbours
    if any(x in qn for x in ["border", "borders", "neighbor", "neighbour", "neighbours", "همسایه", "همسایگان", "مرز"]):
        return bilingual(
            "Badakhshan borders Tajikistan, China and Pakistan internationally, and Takhar, Panjshir and Nuristan within Afghanistan.",
            "بدخشان با تاجیکستان، چین و پاکستان مرز بین‌المللی دارد و در داخل افغانستان با تخار، پنجشیر و نورستان هم‌مرز است.",
        )

    # Geography
    if any(x in qn for x in ["geography", "mountain", "mountains", "pamir", "hindu kush", "wakhan", "kokcha", "جغرافیا", "کوه", "کوهستان", "پامیر", "هندوکش", "واخان", "کوکچه"]):
        return bilingual(GEOGRAPHY_EN, GEOGRAPHY_FA)

    # Culture
    if any(x in qn for x in ["culture", "tradition", "traditions", "music", "cultural", "فرهنگ", "عنعنات", "عننات", "سنت", "موسیقی"]):
        return bilingual(CULTURE_EN, CULTURE_FA)

    # Food / fruits
    if any(x in qn for x in ["food", "foods", "fruit", "fruits", "apple", "grape", "apricot", "mulberry", "walnut", "almond",
                              "غذا", "غذاها", "میوه", "میوه ها", "میوه‌های", "سیب", "انگور", "زردآلو", "توت", "چهارمغز", "گردو", "بادام"]):
        food_fa = FOOD_FA.replace("گردو", "چهارمغز")
        return bilingual(
            FOOD_EN + " The portal lists apples, grapes, apricots, mulberries, fourmaghz (walnuts), almonds, rice and wheat foods, and dairy products among its food and fruit topics.",
            food_fa + " در فهرست پورتال، سیب، انگور، زردآلو، توت، چهارمغز، بادام، غذاهای برنجی و گندمی و لبنیات آمده است.",
        )

    # Clothing
    if any(x in qn for x in ["clothing", "dress", "clothes", "textile", "embroidery", "پوشاک", "لباس", "بافته", "گلدوزی", "کلاه"]):
        return bilingual(CLOTHING_EN, CLOTHING_FA)

    # Minerals
    if any(x in qn for x in ["mineral", "minerals", "gemstone", "gemstones", "lapis", "ruby", "spinel", "gold", "marble", "salt",
                              "معدن", "معادن", "سنگ", "سنگ قیمتی", "لاجورد", "یاقوت", "اسپینل", "طلا", "مرمر", "نمک"]):
        return bilingual(MINERALS_EN, MINERALS_FA)

    # Try a specific district after broad intents
    specific = district_answer(qn)
    if specific:
        return specific

    # Approved community content
    approved = approved_content_answer(qn)
    if approved:
        return approved

    return bilingual(
        "I could not match that question to the portal's current knowledge. Try asking about Badakhshan's population, area, capital/Fayzabad, number or names of districts, a specific district, borders, geography, culture, food, fruits, clothing, minerals, or approved community posts.",
        "این پرسش را در معلومات فعلی پورتال پیدا نکردم. می‌توانید درباره جمعیت، مساحت، مرکز/فیض‌آباد، تعداد یا نام ولسوالی‌ها، یک ولسوالی مشخص، مرزها، جغرافیا، فرهنگ، غذا، میوه‌ها، پوشاک، معادن یا مطالب تأییدشده مردم سؤال کنید.",
    )


if "chat" not in st.session_state:
    st.session_state.chat = []

for role, msg in st.session_state.chat:
    with st.chat_message(role):
        st.markdown(msg)

q = st.chat_input("Ask ChatBadaksh / از چت‌بدخش بپرسید...")
if q:
    st.session_state.chat.append(("user", q))
    st.chat_message("user").write(q)
    a = answer(q)
    st.session_state.chat.append(("assistant", a))
    st.chat_message("assistant").write(a)
