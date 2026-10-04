import streamlit as st
from content import CULTURE_EN, CULTURE_FA, CULTURE_IMAGE_URL
from utils import bilingual_header, submission_form
from approved_content import render_approved_content, admin_editor
bilingual_header("Culture & Traditions", "فرهنگ و عنعنات", 1)
left, center, right = st.columns([1, 2, 1])
with center:
    st.image(CULTURE_IMAGE_URL, width=500)
st.write(CULTURE_EN); st.markdown(f"<p class='rtl'>{CULTURE_FA}</p>", unsafe_allow_html=True)

st.markdown("### Community contributions / مشارکت مردم")
st.write("Upload a story, tradition, song description, clothing photo, craft description or festival note. It is published only after admin approval.")
st.markdown("<p class='rtl'>داستان، رسم، شرح موسیقی، تصویر لباس، صنایع دستی یا معلومات جشن‌ها را ارسال کنید. نشر محتوا فقط پس از تأیید گرداننده انجام می‌شود.</p>", unsafe_allow_html=True)
submission_form("community", "culture", "culture")

render_approved_content("culture", "Approved community culture contributions", "مطالب فرهنگی تأییدشده مردم")


admin_editor("culture", "Culture & Traditions", "فرهنگ و عنعنات")
