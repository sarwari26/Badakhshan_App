import pandas as pd
import streamlit as st
from content import ICON_URL
from db import (
    pending_submissions, update_submission, update_submission_path, rows, audit,
    approve_upload, reject_upload, read_upload, upload_url,
)
from security import check_admin, admin_credentials_configured
from utils import bilingual_header

bilingual_header("Admin", "گرداننده", 1)
left, center, right = st.columns([1, 2, 1])
with center:
    st.image(ICON_URL, use_container_width=True)

# Authentication is handled with a form so the page never shows an
# "incorrect password" error before the administrator has submitted anything.
if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

if not admin_credentials_configured():
    st.error(
        "Admin setup is incomplete. Add ADMIN_USERNAME and ADMIN_PASSWORD to .streamlit/secrets.toml for local use, "
        "or to Streamlit Cloud Secrets for deployment. / تنظیمات گرداننده کامل نیست. "
        "ADMIN_USERNAME و ADMIN_PASSWORD را در .streamlit/secrets.toml برای استفاده محلی یا در Secrets استریم‌لیت برای استقرار اضافه کنید."
    )
    st.stop()

if not st.session_state.admin_authenticated:
    st.markdown(
        "<div class='admin-login-card'><h2>Administrator Login / ورود گرداننده</h2>"
        "<p>Enter your administrator credentials to open the management area.</p>"
        "<p class='rtl'>برای ورود به بخش مدیریت، نام کاربری و رمز گرداننده را وارد کنید.</p></div>",
        unsafe_allow_html=True,
    )
    with st.form("admin_login_form", clear_on_submit=False):
        username = st.text_input("Username / نام کاربری", autocomplete="username")
        password = st.text_input("Password / رمز", type="password", autocomplete="current-password")
        submitted = st.form_submit_button("🔐 Sign in / ورود", use_container_width=True)

    if submitted:
        if not username.strip() or not password:
            st.warning("Please enter both username and password. / لطفاً نام کاربری و رمز را وارد کنید.")
        elif check_admin(username.strip(), password):
            st.session_state.admin_authenticated = True
            st.rerun()
        else:
            st.error("Incorrect administrator username or password. / نام کاربری یا رمز گرداننده نادرست است.")
    st.stop()

# Authenticated state: the administrator can now use the full management area.
login_col, action_col = st.columns([4, 1])
with login_col:
    st.success("Admin access enabled / دسترسی گرداننده فعال است")
with action_col:
    if st.button("Log out / خروج", use_container_width=True):
        st.session_state.admin_authenticated = False
        st.rerun()

bilingual_header("Approval queue", "صف تأیید محتوا", 2)
pending = pending_submissions()
if not pending:
    st.info("No pending submissions. / هیچ مطلب در انتظار تأیید وجود ندارد.")

for p in pending:
    with st.expander(f"#{p['id']} • {p['kind']} • {p.get('title_en') or p.get('title_fa') or p.get('filename') or 'Untitled'}"):
        if p.get("body_en"):
            st.write(p["body_en"])
        if p.get("body_fa"):
            st.markdown(f"<p class='rtl'>{p['body_fa']}</p>", unsafe_allow_html=True)
        stored = p.get("stored_path") or ""
        filename = p.get("filename") or ""
        suffix = filename.lower()
        if stored:
            if suffix.endswith((".jpg", ".jpeg", ".png")):
                url = upload_url(stored)
                if url:
                    st.image(url, use_container_width=True)
                else:
                    try:
                        st.image(read_upload(stored), use_container_width=True)
                    except Exception:
                        st.warning("Could not preview the image. / پیش‌نمایش تصویر ممکن نیست.")
            else:
                try:
                    st.download_button(
                        "Download file / دریافت فایل",
                        read_upload(stored),
                        filename=filename or "attachment",
                        key=f"pre{p['id']}",
                    )
                except Exception as exc:
                    st.warning(f"Could not prepare download: {exc}")
        c1, c2 = st.columns(2)
        if c1.button("Approve / تأیید", key=f"app{p['id']}", use_container_width=True):
            try:
                new_path = approve_upload(stored)
                if new_path != stored:
                    update_submission_path(p["id"], new_path)
                update_submission(p["id"], "approved")
                audit("approve", f"submission {p['id']}")
                st.success("Approved / تأیید شد")
                st.rerun()
            except Exception as exc:
                st.error(f"Approval failed / تأیید ناموفق بود: {exc}")
        if c2.button("Reject / رد", key=f"rej{p['id']}", use_container_width=True):
            try:
                reject_upload(stored)
                update_submission(p["id"], "rejected")
                audit("reject", f"submission {p['id']}")
                st.success("Rejected / رد شد")
                st.rerun()
            except Exception as exc:
                st.error(f"Rejection failed / رد ناموفق بود: {exc}")

st.markdown("---")
bilingual_header("Registrations & Contacts", "ثبت‌نام‌ها و تماس‌ها", 2)
for table, title in [("registrations", "Registrations / ثبت‌نام‌ها"), ("contacts", "Contacts / تماس‌ها")]:
    data = rows(table)
    st.subheader(title)
    if data:
        st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)
        st.download_button(
            "Download CSV / دانلود CSV",
            pd.DataFrame(data).to_csv(index=False).encode("utf-8-sig"),
            f"badakhshan_{table}.csv",
            "text/csv",
            key=f"csv_{table}",
        )
    else:
        st.info("No records yet / هنوز رکوردی وجود ندارد")

bilingual_header("Approved content", "محتوای تأییدشده", 2)
data = rows("submissions")
if data:
    st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)
else:
    st.info("No submissions yet / هنوز مطلبی وجود ندارد")
