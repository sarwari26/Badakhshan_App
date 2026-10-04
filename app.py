import streamlit as st
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ICON_URL = "https://revayataf.com/wp-content/uploads/2025/03/photo_2025-03-18_09-29-14-1.jpg"

st.set_page_config(
    page_title="Badakhshan (بدخشان)",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="expanded",
)

from db import init_db, cloud_enabled
init_db()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Naskh+Arabic:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: Inter, "Noto Naskh Arabic", sans-serif; }
.rtl { direction: rtl; text-align: right; font-family: "Noto Naskh Arabic", serif; }
.hero { padding: .45rem 1.8rem; border-radius: 20px; background: linear-gradient(135deg, #0B5C8E 0%, #176B87 52%, #C99A2E 150%); color: white; margin-bottom: 1.15rem; text-align:center; box-shadow: 0 10px 30px rgba(11,92,142,.16); border: 1px solid rgba(201,154,46,.38); }
.hero h1, .hero p { text-align:center; }
.home-hero h1 { font-size: 36px !important; margin-bottom: .18rem; color: #FFFFFF !important; text-shadow: 0 1px 2px rgba(0,0,0,.18); }
.home-hero p { max-width: 1050px; margin: .12rem auto; line-height: 1.25; color: #FFD966 !important; font-size: 1rem; font-weight: 600; text-shadow: 0 1px 1px rgba(0,0,0,.16); }
.home-icon-wrap { width:100%; max-width:1050px; margin:0 auto 1.15rem auto; user-select:none; }
.home-icon-crop { width:100%; aspect-ratio: 16 / 9; overflow:hidden; border-radius:18px; box-shadow:0 10px 26px rgba(11,92,142,.15); border:2px solid rgba(201,154,46,.35); background:#eee; }
.home-icon-crop img { width:112%; height:100%; object-fit:cover; object-position:left center; display:block; -webkit-user-drag:none; user-drag:none; user-select:none; pointer-events:none; }
.home-icon-caption { text-align:center; font-size:.78rem; color:#666; margin-top:.25rem; }
.admin-login-card { max-width:760px; margin:0 auto 1rem auto; padding:1.2rem 1.4rem; border-radius:18px; background:linear-gradient(135deg, rgba(11,92,142,.08), rgba(201,154,46,.10)); border:1px solid rgba(11,92,142,.16); }
.admin-login-card h2 { color:#0B5C8E; margin-bottom:.45rem; }

.page-image { display:block; margin:0 auto 1rem auto; }
.chatbot-icon { text-align:center; font-size:2.6rem; margin:.15rem 0; }
.portal-card { padding:.75rem !important; margin-bottom:.45rem !important; }
.portal-card h3 { font-size:1.02rem; margin:.2rem 0; }
.portal-card p { font-size:.88rem; margin:.15rem 0; }
.chatbot-card { padding:.9rem !important; }
.chatbot-card h3 { font-size:1.12rem; }
.card { padding: 1rem; border: 1px solid rgba(120,120,120,.18); border-radius: 16px; background: rgba(255,255,255,.04); margin-bottom: .8rem; }
.small { color: #666; font-size: .82rem; }
.badge { display:inline-block; padding:.25rem .55rem; border-radius:999px; background:#e8f3ef; margin:.15rem; }
h1, h2, h3 { text-align: center; }
h1 { font-size: 25px !important; }
h2, h3 { font-size: 20px !important; }
[data-testid="stMetricValue"] { font-size: 1.25rem !important; line-height: 1.15 !important; }
[data-testid="stMetricLabel"] { font-size: .78rem !important; line-height: 1.1 !important; }
[data-testid="stMetricDelta"] { font-size: .72rem !important; }
img, [data-testid="stImage"] img { -webkit-user-drag:none !important; user-drag:none !important; user-select:none !important; }
button, input, textarea, select, [role="button"] { user-select:none !important; }
.stApp { scroll-behavior:smooth; }
footer { visibility: hidden; }
.app-footer { text-align:center; color:#777; font-size:.65rem; margin-top:2rem; padding: .5rem 0 1rem; }
.sidebar-title { text-align:center; font-weight:700; font-size:1.1rem; }
.sidebar-note { text-align:center; font-size:.76rem; color:#666; }
</style>
""", unsafe_allow_html=True)

pages = {
    "Badakhshan (بدخشان)": [
        st.Page("pages/home.py", title="Home خانه", icon="🏠", default=True),
        st.Page("pages/chatbot.py", title="ChatBadaksh چت‌بدخش", icon="🧸"),
        st.Page("pages/contact.py", title="Contact تماس", icon="✉️"),
        st.Page("pages/registration.py", title="Registration ثبت‌نام", icon="🧾"),
        st.Page("pages/blog.py", title="Blog وبلاگ", icon="📝"),
        st.Page("pages/about.py", title="About درباره بدخشان", icon="ℹ️"),
        st.Page("pages/geography.py", title="Location موقعیت", icon="🗺️"),
        st.Page("pages/districts.py", title="Districts ولسوالی‌ها", icon="📍"),
        st.Page("pages/culture.py", title="Culture فرهنگ", icon="🧵"),
        st.Page("pages/food.py", title="Food غذا", icon="🍲"),
        st.Page("pages/clothing.py", title="Clothing پوشاک", icon="🧥"),
        st.Page("pages/minerals.py", title="Minerals معادن", icon="💎"),
        st.Page("pages/admin.py", title="Admin گرداننده", icon="🔐"),
    ]
}

with st.sidebar:
    st.image(ICON_URL, width=150)
    st.markdown("<div class='sidebar-title'>Badakhshan (بدخشان)</div>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-note'>Bilingual information portal | پورتال معلوماتی دوزبانه</div>", unsafe_allow_html=True)
    st.markdown("---")
    if st.button("🏠 Home خانه", use_container_width=True, key="sidebar_home"):
        st.switch_page("pages/home.py")
    if cloud_enabled():
        st.success("Cloud database connected / دیتابیس ابری وصل است")
    else:
        st.warning("Local storage mode / حالت ذخیره‌سازی محلی")

pg = st.navigation(pages)
pg.run()

st.markdown("<div class='app-footer'>Created by Dr. A. Q. Sarwari &nbsp;|&nbsp; ساخته شده توسط دکتر سروری</div>", unsafe_allow_html=True)
