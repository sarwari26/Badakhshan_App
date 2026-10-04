import html
import streamlit as st
from db import approved_submissions, read_upload, upload_url, upload_entries, delete_submission
from security import check_admin, admin_credentials_configured


def _admin_logged_in() -> bool:
    return bool(st.session_state.get("admin_authenticated", False))


def render_approved_content(category: str, heading_en: str = "Community contributions", heading_fa: str = "مشارکت مردم"):
    posts = approved_submissions(category)
    if not posts:
        return
    st.markdown(f"<h2>{html.escape(heading_en)} <span class='rtl'>({html.escape(heading_fa)})</span></h2>", unsafe_allow_html=True)
    st.caption("Published after administrator approval / پس از تأیید گرداننده نشر شده است")
    for p in posts:
        title_en = html.escape(p.get('title_en') or '')
        title_fa = html.escape(p.get('title_fa') or '')
        body_en = html.escape(p.get('body_en') or '').replace('\n', '<br>')
        body_fa = html.escape(p.get('body_fa') or '').replace('\n', '<br>')
        st.markdown(
            f"<div class='card'><h3>{title_en} <span class='rtl'>({title_fa})</span></h3>"
            f"<p>{body_en}</p><p class='rtl'>{body_fa}</p>"
            f"<small>Published after admin approval • {html.escape(str(p.get('created_at','')))}</small></div>",
            unsafe_allow_html=True,
        )
        entries = upload_entries(p.get('stored_path') or '', p.get('filename') or '')
        if entries:
            for idx, (stored, filename) in enumerate(entries, 1):
                try:
                    if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                        url = upload_url(stored)
                        if url:
                            st.image(url, use_container_width=True, caption=f"Image {idx} / تصویر {idx}")
                        else:
                            st.image(read_upload(stored), use_container_width=True, caption=f"Image {idx} / تصویر {idx}")
                    else:
                        st.download_button(
                            "Download attachment / دریافت فایل",
                            read_upload(stored),
                            filename or 'attachment',
                            key=f"approved_{category}_{p['id']}_{idx}",
                        )
                except Exception:
                    st.warning("Attachment is currently unavailable. / فایل پیوست فعلاً در دسترس نیست.")
        if _admin_logged_in():
            if st.button(
                f"🗑️ Delete this post and its images / حذف این مطلب و تصاویر — #{p['id']}",
                key=f"delete_approved_{category}_{p['id']}",
                use_container_width=True,
            ):
                try:
                    delete_submission(p['id'])
                    st.success("Post and attached images deleted. / مطلب و تصاویر پیوست‌شده حذف شد.")
                    st.rerun()
                except Exception as exc:
                    st.error(f"Delete failed / حذف ناموفق بود: {exc}")


def admin_editor(category: str, page_name_en: str, page_name_fa: str):
    """Admin-only editor shown directly on content pages.

    Posts are deliberately sent through the same approval queue as community
    submissions, so the administrator can review/publish them from Admin.
    """
    st.markdown("---")
    st.markdown(f"<h2>Admin content manager — {html.escape(page_name_en)} <span class='rtl'>({html.escape(page_name_fa)})</span></h2>", unsafe_allow_html=True)

    if not admin_credentials_configured():
        st.warning("Admin credentials are not configured. / تنظیمات گرداننده کامل نیست.")
        return

    if not _admin_logged_in():
        with st.expander("🔐 Admin sign-in / ورود گرداننده", expanded=False):
            with st.form(f"page_admin_login_{category}"):
                username = st.text_input("Username / نام کاربری", key=f"page_admin_user_{category}")
                password = st.text_input("Password / رمز", type="password", key=f"page_admin_pass_{category}")
                login = st.form_submit_button("Sign in / ورود", use_container_width=True)
            if login:
                if check_admin(username.strip(), password):
                    st.session_state.admin_authenticated = True
                    st.rerun()
                else:
                    st.error("Incorrect administrator credentials. / نام کاربری یا رمز نادرست است.")
        return

    st.success("Admin editing is enabled. New posts go to Admin → Content Approval before publication. / ویرایش گرداننده فعال است. مطالب جدید برای تأیید به بخش گرداننده می‌روند.")
    with st.form(f"admin_post_form_{category}", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            title_en = st.text_input("Title (English) / عنوان انگلیسی")
            body_en = st.text_area("Text (English) / متن انگلیسی", height=180)
        with c2:
            title_fa = st.text_input("Title (Farsi) / عنوان فارسی")
            body_fa = st.text_area("Text (Farsi) / متن فارسی", height=180)
        images = st.file_uploader(
            "Upload 1 or 2 images / بارگذاری ۱ یا ۲ تصویر",
            type=["jpg", "jpeg", "png", "webp"],
            accept_multiple_files=True,
            key=f"admin_images_{category}",
            help="You can select one or two images without opening VS Code.",
        )
        post = st.form_submit_button("📤 Post for approval / ارسال برای تأیید", type="primary", use_container_width=True)
    if post:
        if len(images or []) > 2:
            st.error("Please select no more than two images. / لطفاً بیشتر از دو تصویر انتخاب نکنید.")
            return
        if not any([title_en.strip(), title_fa.strip(), body_en.strip(), body_fa.strip(), images]):
            st.error("Add text or at least one image. / متن یا حداقل یک تصویر اضافه کنید.")
            return
        try:
            from db import create_admin_submission
            sid = create_admin_submission(category, title_en.strip(), title_fa.strip(), body_en.strip(), body_fa.strip(), images or [])
            st.success(f"Post #{sid} was sent to Content Approval. / مطلب شماره {sid} برای تأیید ارسال شد.")
        except Exception as exc:
            st.error(f"Could not save post / ذخیره مطلب ناموفق بود: {exc}")
