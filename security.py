import hmac
import os
import streamlit as st


def secret(name: str, default: str = "") -> str:
    try:
        value = st.secrets.get(name, default)
    except Exception:
        value = os.getenv(name, default)
    return str(value or default)


def admin_credentials_configured() -> bool:
    return bool(secret("ADMIN_USERNAME") and secret("ADMIN_PASSWORD"))


def check_admin(username: str, password: str) -> bool:
    expected_user = secret("ADMIN_USERNAME")
    expected_password = secret("ADMIN_PASSWORD")
    return (
        bool(expected_user and expected_password and username and password)
        and hmac.compare_digest(username, expected_user)
        and hmac.compare_digest(password, expected_password)
    )
