import streamlit as st
from content import ICON_URL
from db import insert_contact
from utils import bilingual_header
bilingual_header("Contact", "تماس", 1)
left, center, right = st.columns([1, 2, 1])
with center:
    st.image(ICON_URL, width=500)
st.write("Send a message to the portal team. Contact records are stored for administrator review.")
st.markdown("<p class='rtl'>پیام خود را به تیم پورتال ارسال کنید. پیام‌ها برای بررسی گرداننده ذخیره می‌شوند.</p>", unsafe_allow_html=True)
with st.form("contact"):
    name=st.text_input("Name / نام *")
    district=st.text_input("District / ولسوالی")
    occupation=st.text_input("Job / Occupation / وظیفه یا شغل")
    phone=st.text_input("Phone / شماره تماس")
    email=st.text_input("Email / ایمیل")
    subject=st.text_input("Subject / موضوع")
    message=st.text_area("Message / پیام", height=180)
    ok=st.form_submit_button("Send / ارسال")
if ok:
    if not name.strip() or not message.strip(): st.error("Name and message are required / نام و پیام الزامی است")
    else:
        try:
            insert_contact((name,district,occupation,phone,email,subject,message))
            st.success("Message sent and stored for admin review. / پیام ارسال و برای بررسی گرداننده ذخیره شد.")
        except Exception as exc:
            st.error(f"Message could not be saved / پیام ذخیره نشد: {exc}")
