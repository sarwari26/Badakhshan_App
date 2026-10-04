from pathlib import Path
import html
import streamlit as st
from db import insert_submission, store_upload

ROOT = Path(__file__).resolve().parent
ALLOWED = {"docx", "doc", "txt", "csv", "xls", "xlsx", "jpg", "jpeg", "png"}


def save_uploaded(uploaded):
    suffix = uploaded.name.rsplit('.', 1)[-1].lower() if '.' in uploaded.name else ''
    if suffix not in ALLOWED:
        raise ValueError(f"Unsupported file type: {suffix}")
    return store_upload(uploaded.getvalue(), uploaded.name)


def bilingual_header(en, fa, level=1):
    st.markdown(f"<h{level}>{html.escape(en)} <span class='rtl'>({html.escape(fa)})</span></h{level}>", unsafe_allow_html=True)


def card(en_title, fa_title, en_body, fa_body, image_url=None):
    if image_url:
        st.image(image_url, use_container_width=True)
    st.markdown(f"<div class='card'><h3>{html.escape(en_title)} <span class='rtl'>({html.escape(fa_title)})</span></h3><p>{html.escape(en_body)}</p><p class='rtl'>{html.escape(fa_body)}</p></div>", unsafe_allow_html=True)


def submission_form(kind, category, key_prefix="sub"):
    with st.form(f"{key_prefix}_{kind}_{category}"):
        c1, c2 = st.columns(2)
        with c1:
            title_en = st.text_input("Title (English) عنوان (انگلیسی)")
            body_en = st.text_area("Text (English) متن (انگلیسی)", height=180)
        with c2:
            title_fa = st.text_input("Title (Farsi) عنوان (فارسی)")
            body_fa = st.text_area("Text (Farsi) متن (فارسی)", height=180)
        uploaded = st.file_uploader(
            "Attachment / فایل پیوست",
            type=sorted(ALLOWED),
            key=f"file_{key_prefix}_{kind}_{category}",
            help="DOCX, DOC, TXT, CSV, XLS, XLSX, JPG or PNG",
        )
        submit = st.form_submit_button("Submit for approval / ارسال برای تأیید")
    if submit:
        if not any([title_en.strip(), title_fa.strip(), body_en.strip(), body_fa.strip(), uploaded]):
            st.error("Please add text or an attachment. / لطفاً متن یا فایل پیوست اضافه کنید.")
            return
        path = ""
        filename = ""
        if uploaded:
            try:
                path = save_uploaded(uploaded)
                filename = Path(uploaded.name).name
            except Exception as exc:
                st.error(f"Upload failed / بارگذاری ناموفق بود: {exc}")
                return
        try:
            sid = insert_submission((kind, category, title_en, title_fa, body_en, body_fa, filename, path, "public user"))
            st.success(f"Submitted #{sid}. It will appear after admin approval. | مطلب شما با شماره {sid} پس از تأیید گرداننده نشر می‌شود.")
        except Exception as exc:
            st.error(f"Could not save submission / ذخیره مطلب ناموفق بود: {exc}")
