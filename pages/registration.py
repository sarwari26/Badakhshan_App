import streamlit as st
from content import ICON_URL
from db import insert_registration
from utils import bilingual_header
bilingual_header("Registration", "ثبت‌نام", 1)
left, center, right = st.columns([1, 2, 1])
with center:
    st.image(ICON_URL, width=500)
st.write("Register as a community member, contributor, learner, researcher or partner.")
st.markdown("<p class='rtl'>برای عضویت، مشارکت، پژوهش یا همکاری ثبت‌نام کنید.</p>", unsafe_allow_html=True)
with st.form("registration"):
    name=st.text_input("Full name / نام و تخلص *")
    district=st.text_input("District / ولسوالی")
    occupation=st.text_input("Job / Occupation / وظیفه یا شغل")
    phone=st.text_input("Phone / شماره تماس")
    email=st.text_input("Email / ایمیل")
    message=st.text_area("Message / پیام")
    ok=st.form_submit_button("Register / ثبت‌نام")
if ok:
    if not name.strip(): st.error("Name is required / نام الزامی است")
    else:
        try:
            insert_registration((name,district,occupation,phone,email,message))
            st.success("Registration received. / ثبت‌نام شما دریافت شد.")
        except Exception as exc:
            st.error(f"Registration could not be saved / ثبت‌نام ذخیره نشد: {exc}")
