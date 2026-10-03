import streamlit as st
from content import CLOTHING_EN, CLOTHING_FA, ICON_URL
from utils import bilingual_header, submission_form
st.markdown("<h1>Clothing & Handicrafts<br><span class=\"rtl\">(پوشاک و صنایع دستی)</span></h1>", unsafe_allow_html=True)
from content import CLOTHING_IMAGE_URL
left, center, right = st.columns([1, 2, 1])
with center:
    st.image(CLOTHING_IMAGE_URL, width=500)
st.write(CLOTHING_EN); st.markdown(f"<p class='rtl'>{CLOTHING_FA}</p>", unsafe_allow_html=True)
for en,fa in [("Wool textiles","بافته‌های پشمی"),("Embroidery","گلدوزی"),("Local caps and headwear","کلاه‌ها و سربندهای محلی"),("Mountain clothing layers","پوشاک چندلایه کوهستانی"),("Handmade textiles","پارچه‌های دست‌ساز")]:
    st.markdown(f"<span class='badge'>{en} / {fa}</span>", unsafe_allow_html=True)
submission_form("community", "clothing", "clothing")
