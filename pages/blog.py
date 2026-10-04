import streamlit as st
from content import ICON_URL
from utils import bilingual_header, submission_form
from approved_content import render_approved_content, admin_editor

st.markdown('<h1>Blog & Community Stories<br><span class="rtl">(وبلاگ و داستان‌های مردمی)</span></h1>', unsafe_allow_html=True)
left, center, right = st.columns([1, 2, 1])
with center:
    st.image(ICON_URL, width=500)
st.write("Approved community posts appear here. Users can paste bilingual text or upload DOCX, DOC, TXT, CSV, XLS/XLSX or JPG/PNG files for admin review.")
st.markdown("<p class='rtl'>مطالب تأییدشده مردم در این بخش نمایش داده می‌شود. کاربران می‌توانند متن دوزبانه را وارد کرده یا فایل‌های DOCX، DOC، TXT، CSV، XLS/XLSX یا JPG/PNG را برای بررسی گرداننده ارسال کنند.</p>", unsafe_allow_html=True)

submission_form("blog", "blog", "blog")
st.markdown("---")
render_approved_content("blog", "Published community stories", "داستان‌های منتشرشده مردم")


admin_editor("blog", "Blog", "وبلاگ")
