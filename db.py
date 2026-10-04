from __future__ import annotations

import os
import sqlite3
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import streamlit as st

ROOT = Path(__file__).resolve().parent
LOCAL_DB = ROOT / "database" / "badakhshan.db"
LOCAL_PENDING = ROOT / "uploads" / "pending"
LOCAL_APPROVED = ROOT / "uploads" / "approved"
DEFAULT_BUCKET = "badakhshan-uploads"


def _secret(name: str, default: str = "") -> str:
    try:
        value = st.secrets.get(name, default)
    except Exception:
        value = os.getenv(name, default)
    return str(value or default)


def cloud_enabled() -> bool:
    return bool(_secret("SUPABASE_URL") and _secret("SUPABASE_SERVICE_ROLE_KEY"))


def _supabase():
    from supabase import create_client
    return create_client(_secret("SUPABASE_URL"), _secret("SUPABASE_SERVICE_ROLE_KEY"))


def bucket_name() -> str:
    return _secret("SUPABASE_BUCKET", DEFAULT_BUCKET)


def connect():
    LOCAL_DB.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(LOCAL_DB, check_same_thread=False)
    con.row_factory = sqlite3.Row
    return con


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def init_db():
    if cloud_enabled():
        return
    LOCAL_PENDING.mkdir(parents=True, exist_ok=True)
    LOCAL_APPROVED.mkdir(parents=True, exist_ok=True)
    con = connect()
    con.executescript(
        """
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            district TEXT,
            occupation TEXT,
            phone TEXT,
            email TEXT,
            message TEXT,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            district TEXT,
            occupation TEXT,
            phone TEXT,
            email TEXT,
            subject TEXT,
            message TEXT,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kind TEXT NOT NULL,
            category TEXT,
            title_en TEXT,
            title_fa TEXT,
            body_en TEXT,
            body_fa TEXT,
            filename TEXT,
            stored_path TEXT,
            status TEXT NOT NULL DEFAULT 'pending',
            submitted_by TEXT,
            created_at TEXT NOT NULL,
            reviewed_at TEXT
        );
        CREATE TABLE IF NOT EXISTS audit (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT,
            detail TEXT,
            created_at TEXT NOT NULL
        );
        """
    )
    con.commit()
    con.close()


def _cloud_insert(table: str, payload: dict[str, Any]):
    return _supabase().table(table).insert(payload).execute()


def insert_registration(data):
    keys = ["name", "district", "occupation", "phone", "email", "message"]
    payload = dict(zip(keys, data))
    payload["created_at"] = now()
    if cloud_enabled():
        _cloud_insert("registrations", payload)
        return
    con = connect()
    con.execute(
        "INSERT INTO registrations(name,district,occupation,phone,email,message,created_at) VALUES (?,?,?,?,?,?,?)",
        (*data, payload["created_at"]),
    )
    con.commit(); con.close()


def insert_contact(data):
    keys = ["name", "district", "occupation", "phone", "email", "subject", "message"]
    payload = dict(zip(keys, data))
    payload["created_at"] = now()
    if cloud_enabled():
        _cloud_insert("contacts", payload)
        return
    con = connect()
    con.execute(
        "INSERT INTO contacts(name,district,occupation,phone,email,subject,message,created_at) VALUES (?,?,?,?,?,?,?,?)",
        (*data, payload["created_at"]),
    )
    con.commit(); con.close()


def insert_submission(data):
    keys = [
        "kind", "category", "title_en", "title_fa", "body_en", "body_fa",
        "filename", "stored_path", "submitted_by"
    ]
    payload = dict(zip(keys, data))
    payload.update({"status": "pending", "created_at": now()})
    if cloud_enabled():
        response = _cloud_insert("submissions", payload)
        return response.data[0]["id"] if response.data else None
    con = connect()
    cur = con.execute(
        "INSERT INTO submissions(kind,category,title_en,title_fa,body_en,body_fa,filename,stored_path,status,submitted_by,created_at) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
        (*data, "pending", payload["created_at"]),
    )
    con.commit(); sid = cur.lastrowid; con.close(); return sid


def rows(table):
    allowed = {"registrations", "contacts", "submissions", "audit"}
    if table not in allowed:
        raise ValueError("Invalid table")
    if cloud_enabled():
        response = _supabase().table(table).select("*").order("id", desc=True).execute()
        return response.data or []
    con = connect(); out = [dict(r) for r in con.execute(f"SELECT * FROM {table} ORDER BY id DESC").fetchall()]; con.close(); return out


def pending_submissions():
    """Return every submission that still needs editorial review.

    Older local/cloud records may contain slightly different status spelling
    (or a blank status). Treat those legacy values as pending so received
    content cannot disappear from the administrator's queue.
    """
    review_statuses = {"", "pending", "awaiting", "submitted", "received"}
    if cloud_enabled():
        response = _supabase().table("submissions").select("*").order("id", desc=True).execute()
        rows = response.data or []
        return [r for r in rows if str(r.get("status") or "").strip().lower() in review_statuses]
    con = connect()
    out = [dict(r) for r in con.execute("SELECT * FROM submissions ORDER BY id DESC").fetchall()]
    con.close()
    return [r for r in out if str(r.get("status") or "").strip().lower() in review_statuses]


def approved_submissions(category=None):
    """Return only approved submissions, optionally for one portal category."""
    if cloud_enabled():
        query = _supabase().table("submissions").select("*").eq("status", "approved")
        if category:
            query = query.eq("category", category)
        response = query.order("id", desc=True).execute()
        return response.data or []
    con = connect()
    if category:
        out = [dict(r) for r in con.execute("SELECT * FROM submissions WHERE status='approved' AND category=? ORDER BY id DESC", (category,)).fetchall()]
    else:
        out = [dict(r) for r in con.execute("SELECT * FROM submissions WHERE status='approved' ORDER BY id DESC").fetchall()]
    con.close(); return out


def update_submission(sid, status):
    reviewed = now()
    if cloud_enabled():
        _supabase().table("submissions").update({"status": status, "reviewed_at": reviewed}).eq("id", sid).execute()
        return
    con = connect(); con.execute("UPDATE submissions SET status=?, reviewed_at=? WHERE id=?", (status, reviewed, sid)); con.commit(); con.close()


def update_submission_path(sid, stored_path):
    if cloud_enabled():
        _supabase().table("submissions").update({"stored_path": stored_path}).eq("id", sid).execute()
        return
    con = connect(); con.execute("UPDATE submissions SET stored_path=? WHERE id=?", (stored_path, sid)); con.commit(); con.close()


def audit(action, detail):
    payload = {"action": action, "detail": detail, "created_at": now()}
    if cloud_enabled():
        _cloud_insert("audit", payload)
        return
    con = connect(); con.execute("INSERT INTO audit(action,detail,created_at) VALUES (?,?,?)", (action, detail, payload["created_at"])); con.commit(); con.close()


def store_upload(file_bytes: bytes, filename: str) -> str:
    safe_name = Path(filename).name.replace(" ", "_")
    unique = f"{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}_{safe_name}"
    if cloud_enabled():
        path = f"pending/{unique}"
        _supabase().storage.from_(bucket_name()).upload(path, file_bytes, {"upsert": "false", "content-type": "application/octet-stream"})
        return path
    LOCAL_PENDING.mkdir(parents=True, exist_ok=True)
    path = LOCAL_PENDING / unique
    path.write_bytes(file_bytes)
    return str(path)


def read_upload(stored_path: str) -> bytes:
    if cloud_enabled():
        return _supabase().storage.from_(bucket_name()).download(stored_path)
    return Path(stored_path).read_bytes()


def upload_url(stored_path: str, expires: int = 3600) -> str | None:
    if not stored_path:
        return None
    if cloud_enabled():
        result = _supabase().storage.from_(bucket_name()).create_signed_url(stored_path, expires)
        if isinstance(result, dict):
            return result.get("signedURL") or result.get("signedUrl")
        return None
    return None



def upload_entries(stored_path: str, filename: str = "") -> list[tuple[str, str]]:
    """Normalize one or two stored uploads, including legacy single-file rows."""
    if not stored_path:
        return []
    try:
        paths = json.loads(stored_path)
        if not isinstance(paths, list):
            paths = [stored_path]
    except Exception:
        paths = [stored_path]
    try:
        names = json.loads(filename) if filename else []
        if not isinstance(names, list):
            names = [filename]
    except Exception:
        names = [filename] if filename else []
    return [(str(path), str(names[i]) if i < len(names) else Path(str(path)).name) for i, path in enumerate(paths) if path]


def pack_uploads(entries: list[tuple[str, str]]) -> tuple[str, str]:
    if not entries:
        return "", ""
    if len(entries) == 1:
        return entries[0][0], entries[0][1]
    return json.dumps([p for p, _ in entries]), json.dumps([n for _, n in entries])


def delete_submission(sid: int):
    """Delete a submission and all of its stored images/files."""
    if cloud_enabled():
        existing = _supabase().table("submissions").select("stored_path,filename").eq("id", sid).execute()
        row = (existing.data or [None])[0]
        if row:
            for path, _ in upload_entries(row.get("stored_path") or "", row.get("filename") or ""):
                try:
                    _supabase().storage.from_(bucket_name()).remove([path])
                except Exception:
                    pass
        _supabase().table("submissions").delete().eq("id", sid).execute()
        return
    con = connect()
    row = con.execute("SELECT stored_path, filename FROM submissions WHERE id=?", (sid,)).fetchone()
    if row:
        for path, _ in upload_entries(row[0] or "", row[1] or ""):
            try:
                Path(path).unlink(missing_ok=True)
            except Exception:
                pass
    con.execute("DELETE FROM submissions WHERE id=?", (sid,))
    con.commit(); con.close()


def create_admin_submission(category, title_en, title_fa, body_en, body_fa, uploads):
    """Create an administrator-authored post in the normal approval queue."""
    entries = []
    for uploaded in uploads or []:
        path = store_upload(uploaded.getvalue(), uploaded.name)
        entries.append((path, Path(uploaded.name).name))
    stored_path, filename = pack_uploads(entries)
    return insert_submission(("admin_post", category, title_en, title_fa, body_en, body_fa, filename, stored_path, "admin"))


def approve_submission(sid: int):
    """Move every attached file to approved storage and mark the post approved."""
    if cloud_enabled():
        response = _supabase().table("submissions").select("stored_path,filename").eq("id", sid).execute()
        row = (response.data or [None])[0]
    else:
        con = connect(); row = con.execute("SELECT stored_path, filename FROM submissions WHERE id=?", (sid,)).fetchone(); con.close()
        row = dict(row) if row else None
    if not row:
        raise ValueError("Submission not found")
    entries = upload_entries(row.get("stored_path") or "", row.get("filename") or "") if isinstance(row, dict) else upload_entries(row[0] or "", row[1] or "")
    moved = [(approve_upload(path), name) for path, name in entries]
    new_path, _ = pack_uploads(moved)
    if new_path != (row.get("stored_path") if isinstance(row, dict) else row[0]):
        update_submission_path(sid, new_path)
    update_submission(sid, "approved")
    return moved

def approve_upload(stored_path: str) -> str:
    if not stored_path:
        return stored_path
    if cloud_enabled():
        if stored_path.startswith("pending/"):
            new_path = stored_path.replace("pending/", "approved/", 1)
            _supabase().storage.from_(bucket_name()).move(stored_path, new_path)
            return new_path
        return stored_path
    src = Path(stored_path)
    if src.exists():
        LOCAL_APPROVED.mkdir(parents=True, exist_ok=True)
        dest = LOCAL_APPROVED / src.name
        src.replace(dest)
        return str(dest)
    return stored_path


def reject_upload(stored_path: str):
    if not stored_path:
        return
    if cloud_enabled():
        try:
            _supabase().storage.from_(bucket_name()).remove([stored_path])
        except Exception:
            pass
    else:
        try:
            Path(stored_path).unlink(missing_ok=True)
        except Exception:
            pass
