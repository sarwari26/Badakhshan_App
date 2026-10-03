# Badakhshan (بدخشان) — GitHub + Streamlit Community Cloud Edition

A bilingual English/Farsi Streamlit information portal for Badakhshan.

## Included

- Home / خانه
- About / درباره بدخشان
- Geography / جغرافیا
- Districts / ولسوالی‌ها
- Culture / فرهنگ
- Food / غذا
- Clothing / پوشاک
- Minerals / معادن
- Blog / وبلاگ
- Registration / ثبت‌نام
- Contact / تماس
- ChatBadaksh / چت‌بدخش
- Admin / گرداننده

The Resources and Windows Deployment pages are intentionally removed.

## Important cloud-storage change

The app supports two modes:

1. **Cloud mode (recommended for Streamlit Community Cloud):** Supabase stores registrations, contact messages, submissions, audit records and uploaded files.
2. **Local fallback:** SQLite and local folders are used when Supabase secrets are not configured. This is useful for local VS Code testing, but local file storage is not guaranteed to persist on Streamlit Community Cloud.

Streamlit Community Cloud does not guarantee persistence of local file storage, so use Supabase for the public deployment.

## 1. Local VS Code setup

Use Python 3.12 for the deployment environment and, ideally, for local testing.

```powershell
cd Badakhshan_App
py -3.12 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

If your Windows machine only has another supported Python release, you can use it for local testing, but select the same supported version in Streamlit Community Cloud.

## 2. Create the Supabase database

1. Create a Supabase project.
2. Open **SQL Editor**.
3. Open `cloud_schema.sql` from this project.
4. Run the complete SQL script.
5. In Supabase Project Settings/API, copy:
   - Project URL
   - Service Role Key
6. Keep the service-role key private. It must never be committed to GitHub or displayed in the app.

The bucket created by the SQL script is private: `badakhshan-uploads`.

## 3. Local secrets (optional but recommended for testing cloud mode)

Create:

```text
.streamlit/secrets.toml
```

using `.streamlit/secrets.toml.example` as the template.

Example:

```toml
SUPABASE_URL = "https://YOUR-PROJECT.supabase.co"
SUPABASE_SERVICE_ROLE_KEY = "YOUR-SERVICE-ROLE-KEY"
SUPABASE_BUCKET = "badakhshan-uploads"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "use-a-long-random-password"
```

Never commit `secrets.toml`.

## 4. Test cloud mode locally

Start Streamlit:

```powershell
streamlit run app.py
```

The sidebar should show:

`Cloud database connected / دیتابیس ابری وصل است`

Test all of these before deployment:

- Registration submission
- Contact submission
- Blog text submission
- Blog image upload
- DOCX/TXT/CSV/XLS/XLSX upload
- Admin login
- Admin approval
- Admin rejection
- Approved blog display
- ChatBadaksh
- District search/download

## 5. GitHub

Create a new repository, for example:

`Badakhshan-App`

Upload the contents of this folder, not the ZIP file itself.

Do **not** upload:

- `.streamlit/secrets.toml`
- `.venv/`
- local SQLite databases
- local pending/approved upload files

The included `.gitignore` already excludes these.

A clean repository should look similar to:

```text
Badakhshan-App/
├── app.py
├── content.py
├── db.py
├── security.py
├── utils.py
├── cloud_schema.sql
├── requirements.txt
├── README.md
├── .gitignore
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml.example
├── assets/
├── data/
│   └── districts.csv
└── pages/
    ├── home.py
    ├── about.py
    ├── geography.py
    ├── districts.py
    ├── culture.py
    ├── food.py
    ├── clothing.py
    ├── minerals.py
    ├── blog.py
    ├── registration.py
    ├── contact.py
    ├── chatbot.py
    └── admin.py
```

## 6. Streamlit Community Cloud

1. Sign in to Streamlit Community Cloud with GitHub.
2. Click **Create app**.
3. Select your GitHub repository.
4. Select branch `main`.
5. Set the main file to:

```text
app.py
```

6. Open **Advanced settings**.
7. Select Python **3.12**.
8. Paste the contents of your real `secrets.toml` into the **Secrets** field.
9. Deploy.

After deployment, Streamlit provides a public `streamlit.app` URL.

## 7. Admin login

For local VS Code testing, this updated package includes `.streamlit/secrets.toml` and it is excluded by `.gitignore`.
The local test credentials are:

```text
Username: admin
Password: Badakhshan@Admin2026
```

Change them before any public deployment.

For the deployed app, use the credentials stored in Streamlit Secrets:

```toml
ADMIN_USERNAME = "..."
ADMIN_PASSWORD = "..."
```

Change the password before making the application public.

## 8. Image sources

The application keeps the image URLs supplied for this project, including the Badakhshan icon, Badakhshan map, culture, food, clothing and minerals images. These images require Internet access when the app is viewed.

For long-term reliability, replace externally hosted image URLs with locally stored images for which you have permission to use them. The application can then reference files in `assets/`.

## 9. Data and privacy

Registration and contact forms collect personal information. Before public launch, publish a privacy notice appropriate to your intended audience and jurisdiction, collect only information you actually need, protect administrator credentials, and restrict database access.

The Supabase service-role key is server-side only and must never be exposed to visitors.

## 10. Updating the app

After deployment, commit changes to GitHub. Community Cloud detects repository changes and updates the app.

For dependency changes, Community Cloud will reinstall dependencies from `requirements.txt`.
