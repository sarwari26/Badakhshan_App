import streamlit as st
from content import ICON_URL
from db import approved_submissions, read_upload, upload_url
from utils import bilingual_header, submission_form

st.markdown("<h1>Blog & Community Stories<br><span class=\"rtl\">(وبلاگ و داستان‌های مردمی)</span></h1>", unsafe_allow_html=True)
left, center, right = st.columns([1, 2, 1])
with center:
    st.image(ICON_URL, width=500)
st.write("Approved community posts appear here. Users can paste bilingual text or upload DOCX, DOC, TXT, CSV, XLS/XLSX or JPG/PNG files for admin review.")
st.markdown("<p class='rtl'>مطالب تأییدشده مردم در این بخش نمایش داده می‌شود. کاربران می‌توانند متن دوزبانه را وارد کرده یا فایل‌های DOCX، DOC، TXT، CSV، XLS/XLSX یا JPG/PNG را برای بررسی گرداننده ارسال کنند.</p>", unsafe_allow_html=True)

submission_form("blog", "blog", "blog")

st.markdown("---")
posts = approved_submissions("blog")
if not posts:
    st.info("No approved posts yet. / هنوز مطلب تأییدشده‌ای وجود ندارد.")
for p in posts:
    st.markdown(f"<div class='card'><h3>{p.get('title_en') or ''} <span class='rtl'>({p.get('title_fa') or ''})</span></h3><p>{p.get('body_en') or ''}</p><p class='rtl'>{p.get('body_fa') or ''}</p><small>Published after admin approval • {p.get('created_at','')}</small></div>", unsafe_allow_html=True)
    stored = p.get("stored_path") or ""
    filename = p.get("filename") or ""
    if stored:
        try:
            if filename.lower().endswith((".jpg", ".jpeg", ".png")):
                url = upload_url(stored)
                if url:
                    st.image(url, use_container_width=True)
                else:
                    st.image(read_upload(stored), use_container_width=True)
            else:
                st.download_button("Download attachment / دریافت فایل", read_upload(stored), filename or "attachment", key=f"dl{p['id']}")
        except Exception:
            st.warning("Attachment is currently unavailable. / فایل پیوست فعلاً در دسترس نیست.")
