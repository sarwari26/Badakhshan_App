import pandas as pd
import streamlit as st
from content import ICON_URL
from db import (
    pending_submissions, update_submission, update_submission_path, rows, audit,
    approve_upload, approve_submission, reject_upload, read_upload, upload_url, upload_entries,
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

queue_title_col, queue_action_col = st.columns([4, 1])
with queue_title_col:
    bilingual_header("Content approval & publishing", "تأیید و نشر محتوا", 2)
with queue_action_col:
    if st.button("🔄 Refresh / تازه‌سازی", use_container_width=True, key="refresh_approval_queue"):
        st.rerun()

pending = pending_submissions()
st.info(
    f"Pending submissions: {len(pending)} / مطالب در انتظار تأیید: {len(pending)}"
)
if pending:
    st.caption(
        "Approve & Publish sends approved content to the related portal page automatically. "
        "For example: Blog → Blog, Culture → Culture, Food → Food, Clothing → Clothing, Minerals → Minerals."
    )
else:
    st.warning(
        "No pending submissions. If a submission was just received, use Refresh / "
        "تازه‌سازی را بزنید. / هیچ مطلب در انتظار تأیید وجود ندارد."
    )

for p in pending:
    category = (p.get("category") or p.get("kind") or "blog").strip().lower()
    publish_target = {
        "blog": "Blog / وبلاگ",
        "culture": "Culture / فرهنگ",
        "food": "Food / غذا",
        "clothing": "Clothing / پوشاک",
        "minerals": "Minerals / معادن",
    }.get(category, f"{category.title()} / صفحه مرتبط")
    title = p.get('title_en') or p.get('title_fa') or p.get('filename') or 'Untitled / بدون عنوان'
    with st.container(border=True):
        st.markdown(
            f"<h3 style='margin-top:0'>#{p['id']} • {title}</h3>",
            unsafe_allow_html=True,
        )
        meta1, meta2, meta3 = st.columns(3)
        meta1.markdown(f"**Type:** {p.get('kind') or '-'}")
        meta2.markdown(f"**Category:** {category}")
        meta3.markdown(f"**Publish to:** {publish_target}")
        if p.get("body_en"):
            st.markdown("**English content**")
            st.write(p["body_en"])
        if p.get("body_fa"):
            st.markdown("**محتوای فارسی**")
            st.markdown(f"<p class='rtl'>{p['body_fa']}</p>", unsafe_allow_html=True)
        entries = upload_entries(p.get("stored_path") or "", p.get("filename") or "")
        if entries:
            for idx, (stored, filename) in enumerate(entries, 1):
                suffix = filename.lower()
                if suffix.endswith((".jpg", ".jpeg", ".png", ".webp")):
                    url = upload_url(stored)
                    try:
                        if url:
                            st.image(url, use_container_width=True, caption=f"Image {idx} / تصویر {idx}")
                        else:
                            st.image(read_upload(stored), use_container_width=True, caption=f"Image {idx} / تصویر {idx}")
                    except Exception:
                        st.warning("Could not preview the image. / پیش‌نمایش تصویر ممکن نیست.")
                else:
                    try:
                        st.download_button(
                            "Download file / دریافت فایل", read_upload(stored),
                            filename=filename or "attachment", key=f"pre{p['id']}_{idx}",
                        )
                    except Exception as exc:
                        st.warning(f"Could not prepare download: {exc}")

        st.markdown(
            "<div style='margin:.6rem 0 .35rem 0'><b>Review action / اقدام بررسی</b></div>",
            unsafe_allow_html=True,
        )
        c1, c2 = st.columns(2)
        if c1.button(
            f"✅ Approve & Publish to {publish_target}",
            key=f"approve_publish_{p['id']}",
            use_container_width=True,
            type="primary",
        ):
            try:
                approve_submission(p["id"])
                audit("approve_publish", f"submission {p['id']} -> {publish_target}")
                st.success(
                    f"Approved and published to {publish_target}. / تأیید و در {publish_target} نشر شد."
                )
                st.rerun()
            except Exception as exc:
                st.error(f"Approval/publishing failed / تأیید و نشر ناموفق بود: {exc}")
        if c2.button(
            "❌ Reject / رد",
            key=f"reject_{p['id']}",
            use_container_width=True,
        ):
            try:
                for stored_path, _ in entries:
                    reject_upload(stored_path)
                update_submission(p["id"], "rejected")
                audit("reject", f"submission {p['id']}")
                st.success("Rejected / رد شد")
                st.rerun()
            except Exception as exc:
                st.error(f"Rejection failed / رد ناموفق بود: {exc}")

st.markdown("---")
bilingual_header("Published community content", "محتوای منتشرشده مردم", 2)
approved = rows("submissions")
approved = [r for r in approved if str(r.get("status") or "").strip().lower() == "approved"]
if approved:
    st.dataframe(pd.DataFrame(approved), use_container_width=True, hide_index=True)
else:
    st.info("No approved submissions yet / هنوز مطلب تأییدشده‌ای وجود ندارد")

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

bilingual_header("Approved content & approval actions", "محتوای تأییدشده و گزینه تأیید", 2)
all_content = rows("submissions")
if all_content:
    for item in all_content:
        status = str(item.get("status") or "pending").lower()
        title = item.get("title_en") or item.get("title_fa") or item.get("filename") or "Untitled / بدون عنوان"
        st.markdown(f"**#{item['id']} — {title}**  \nStatus: `{status}` | Category: `{item.get('category') or '-'}`")
        if status != "approved":
            a1, a2 = st.columns(2)
            if a1.button("✅ Approve & Publish / تأیید و نشر", key=f"approve_all_{item['id']}", use_container_width=True, type="primary"):
                try:
                    approve_submission(item["id"])
                    audit("approve_publish", f"submission {item['id']} -> {item.get('category') or 'related page'}")
                    st.success("Approved and published. / تأیید و نشر شد.")
                    st.rerun()
                except Exception as exc:
                    st.error(f"Approval failed / تأیید ناموفق بود: {exc}")
            if a2.button("❌ Reject / رد", key=f"reject_all_{item['id']}", use_container_width=True):
                try:
                    for stored_path, _ in upload_entries(item.get("stored_path") or "", item.get("filename") or ""):
                        reject_upload(stored_path)
                    update_submission(item["id"], "rejected")
                    audit("reject", f"submission {item['id']}")
                    st.success("Rejected. / رد شد.")
                    st.rerun()
                except Exception as exc:
                    st.error(f"Rejection failed / رد ناموفق بود: {exc}")
    st.dataframe(pd.DataFrame(all_content), use_container_width=True, hide_index=True)
else:
    st.info("No submissions yet / هنوز مطلبی وجود ندارد")
