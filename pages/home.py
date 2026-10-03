import streamlit as st
from content import ICON_URL, FACTS, INTRO_EN, INTRO_FA
from utils import bilingual_header

st.markdown("""<div class='hero home-hero'>
<h1>Badakhshan (بدخشان)</h1>
<p>A bilingual digital portal about the people, districts, geography, culture, food, minerals, stories and community information of Badakhshan.</p>
<p class='rtl'>پورتال معلوماتی دوزبانه درباره مردم، ولسوالی‌ها، جغرافیا، فرهنگ، غذا، معادن، مطالب و معلومات اجتماعی بدخشان.</p>
</div>""", unsafe_allow_html=True)
st.markdown("<div class='home-icon-wrap'>", unsafe_allow_html=True)
st.image(ICON_URL, caption="Badakhshan / بدخشان", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

c1,c2,c3,c4=st.columns(4)
c1.metric("Population / جمعیت", FACTS["population"])
c2.metric("Area / مساحت", FACTS["area"])
c3.metric("Districts / ولسوالی‌ها", "29")
c4.metric("Capital / مرکز", "Fayzabad / فیض‌آباد")

bilingual_header("About Badakhshan", "درباره بدخشان", 2)
st.write(INTRO_EN)
st.markdown(f"<p class='rtl'>{INTRO_FA}</p>", unsafe_allow_html=True)

bilingual_header("Explore the portal", "بخش‌های پورتال", 2)
items=[
    ("🗺️ Geography", "جغرافیا", "pages/geography.py"),
    ("📍 Districts", "ولسوالی‌ها", "pages/districts.py"),
    ("🧵 Culture", "فرهنگ", "pages/culture.py"),
    ("🍲 Food", "غذا", "pages/food.py"),
    ("🧥 Clothing", "پوشاک", "pages/clothing.py"),
    ("💎 Minerals", "معادن", "pages/minerals.py"),
    ("📝 Blog", "وبلاگ", "pages/blog.py"),
    ("🧾 Registration", "ثبت‌نام", "pages/registration.py"),
    ("✉️ Contact", "تماس", "pages/contact.py"),
    ("🤖 ChatBadaksh", "چت‌بدخش", "pages/chatbot.py"),
    ("🔐 Admin", "گرداننده", "pages/admin.py"),
]
cols=st.columns(3)
for i,(en,fa,path) in enumerate(items):
    with cols[i%3]:
        card_class = "card portal-card chatbot-card" if "ChatBadaksh" in en else "card portal-card"
        st.markdown(f"<div class='{card_class}'><h3>{en}</h3><p class='rtl'>{fa}</p></div>", unsafe_allow_html=True)
        if st.button(f"Open / مشاهده", key=f"home_nav_{i}", use_container_width=True):
            st.switch_page(path)
