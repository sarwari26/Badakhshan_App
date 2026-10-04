import streamlit as st
from content import *
from utils import bilingual_header

bilingual_header("Location", "موقعیت", 1)
left, center, right = st.columns([1, 2, 1])
with center:
    st.image(GEOGRAPHY_IMAGE_URL, width=500)
st.write(GEOGRAPHY_EN); st.markdown(f"<p class='rtl'>{GEOGRAPHY_FA}</p>", unsafe_allow_html=True)

c1,c2=st.columns(2)
with c1:
    st.subheader("International neighbours / همسایگان بین‌المللی")
    for x in FACTS['countries']: st.markdown(f"- {x}")
with c2:
    st.subheader("Afghan provinces / ولایت‌های همجوار")
    for x in FACTS['provinces']: st.markdown(f"- {x}")

st.markdown("### Major geographic features / ویژگی‌های جغرافیایی")
for en,fa in [("Hindu Kush and Pamirs","هندوکش و پامیر"),("Wakhan Corridor","دهلیز واخان"),("Kokcha River","رودخانه کوکچه"),("Panj River / Amu Darya system","رودخانه پنج / حوزه آمودریا")]:
    st.markdown(f"<span class='badge'>{en} / {fa}</span>", unsafe_allow_html=True)
