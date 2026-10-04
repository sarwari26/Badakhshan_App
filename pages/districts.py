import streamlit as st
import pandas as pd
from pathlib import Path
from content import ICON_URL
from utils import bilingual_header

df = pd.read_csv(Path(__file__).resolve().parent.parent / "data" / "districts.csv")

bilingual_header("Districts", "ولسوالی‌ها", 1)

# Center the Badakhshan image
left, center, right = st.columns([1, 2, 1])
with center:
    st.image(ICON_URL, width=300)

st.caption("Population figures below are 2020 estimates from the cited district table; administrative lists and boundaries can change.")
st.caption("ارقام جمعیت زیر برآورد سال ۲۰۲۰ از منبع ذکرشده است؛ فهرست و حدود اداری ممکن است تغییر کند.")

st.info(f"Badakhshan has {len(df)} districts in this portal's district table. / در جدول معلوماتی این پورتال، بدخشان {len(df)} ولسوالی دارد.")

q = st.text_input("Search / جستجو")
if q:
    qn = q.strip().lower()
    df = df[df.apply(
        lambda r: qn in str(r.district_en).lower()
        or q.strip() in str(r.district_fa)
        or qn in str(r.capital_en).lower()
        or q.strip() in str(r.capital_fa),
        axis=1,
    )]

display = df.rename(columns={
    "district_en": "District / ولسوالی",
    "district_fa": "نام فارسی",
    "capital_en": "Capital / مرکز",
    "population_2020": "Population 2020 / جمعیت ۲۰۲۰",
    "area_km2": "Area km² / مساحت",
})
st.dataframe(
    display[["District / ولسوالی", "نام فارسی", "Capital / مرکز", "Population 2020 / جمعیت ۲۰۲۰", "Area km² / مساحت"]],
    use_container_width=True,
    hide_index=True,
)
st.download_button(
    "Download district data / دانلود معلومات ولسوالی‌ها",
    df.to_csv(index=False).encode("utf-8-sig"),
    "badakhshan_districts.csv",
    "text/csv",
)
