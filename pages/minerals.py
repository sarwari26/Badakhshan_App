import streamlit as st
from content import MINERALS_EN, MINERALS_FA, MINERALS_IMAGE_URL
from utils import bilingual_header, submission_form
st.markdown("<h1>Minerals & Gemstones<br><span class=\"rtl\">(معادن و سنگ‌های قیمتی)</span></h1>", unsafe_allow_html=True)
left, center, right = st.columns([1, 2, 1])
with center:
    st.image(MINERALS_IMAGE_URL, width=500)
st.write(MINERALS_EN); st.markdown(f"<p class='rtl'>{MINERALS_FA}</p>", unsafe_allow_html=True)
for en,fa in [("Lapis lazuli","لاجورد"),("Ruby / spinel","یاقوت / اسپینل"),("Gold","طلا"),("Marble","مرمر"),("Salt","نمک"),("Other semi-precious stones","سنگ‌های نیمه‌قیمتی دیگر")]:
    st.markdown(f"<span class='badge'>{en} / {fa}</span>", unsafe_allow_html=True)
st.markdown("### Submit mineral information / ارسال معلومات معادن")
submission_form("community", "minerals", "minerals")
