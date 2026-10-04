import streamlit as st
from content import *
from utils import bilingual_header
from approved_content import render_approved_content, admin_editor

bilingual_header("About Badakhshan", "درباره بدخشان", 1)
left, center, right = st.columns([1, 2, 1])
with center:
    st.image(ABOUT_IMAGE_URL, width=500)
st.write(INTRO_EN); st.markdown(f"<p class='rtl'>{INTRO_FA}</p>", unsafe_allow_html=True)

bilingual_header("Key facts", "معلومات اساسی", 2)
for en,fa,enval,faval in [("Location","موقعیت","Northeastern Afghanistan","شمال‌شرق افغانستان"),("Capital","مرکز ولایت","Fayzabad","فیض‌آباد"),("Area","مساحت",FACTS['area'],FACTS['area_fa']),("Population","جمعیت",FACTS['population'],FACTS['population_fa'])]:
    st.markdown(f"<div class='card'><b>{en} / {fa}</b><br>{enval}<br><span class='rtl'>{faval}</span></div>", unsafe_allow_html=True)



admin_editor("about", "About Badakhshan", "درباره بدخشان")
render_approved_content("about", "Approved community About content", "مطالب تأییدشده درباره بدخشان")
