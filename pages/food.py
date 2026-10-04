import streamlit as st
from content import FOOD_EN, FOOD_FA, FOOD_IMAGE_URL
from utils import bilingual_header, submission_form
from approved_content import render_approved_content, admin_editor
st.markdown("<h1>Food, Fruits & Local Products<br><span class=\"rtl\">(غذا، میوه‌ها و محصولات محلی)</span></h1>", unsafe_allow_html=True)
left, center, right = st.columns([1, 2, 1])
with center:
    st.image(FOOD_IMAGE_URL, width=500)
st.write(FOOD_EN); st.markdown(f"<p class='rtl'>{FOOD_FA}</p>", unsafe_allow_html=True)

st.markdown("### Fruits & foods / میوه‌ها و غذاها")
for en,fa in [("Apples","سیب"),("Grapes","انگور"),("Apricots","زردآلو"),("Mulberries","توت"),("Walnuts","چهارمغز"),("Almonds","بادام"),("Rice and wheat foods","غذاهای برنجی و گندمی"),("Dairy products","لبنیات")]:
    st.markdown(f"<span class='badge'>{en} / {fa}</span>", unsafe_allow_html=True)

submission_form("community", "food", "food")

render_approved_content("food", "Approved community food contributions", "مطالب غذایی تأییدشده مردم")


admin_editor("food", "Food, Fruits & Local Products", "غذا، میوه‌ها و محصولات محلی")
