from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
ICON_URL = "https://revayataf.com/wp-content/uploads/2025/03/photo_2025-03-18_09-29-14-1.jpg"
ABOUT_IMAGE_URL = "https://thumb.wikimedia.org/wikipedia/commons/thumb/5/53/Badakhshan_in_Afghanistan.svg/250px-Badakhshan_in_Afghanistan.svg.png?utm_source=en.wikipedia.org&utm_campaign=parser&utm_content=thumbnail"
GEOGRAPHY_IMAGE_URL = "https://www.d-maps.com/m/asia/afghanistan/badakhshan/badakhshan17.gif"
CULTURE_IMAGE_URL = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSWuWgvLdEwnWiSUMGCnYymgZ3p7KlSW4PXDWV-ri7_bQ&s=10"
FOOD_IMAGE_URL = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTj-0FPMeaHG7lyPEyUJtaXmu9D3MkZnaDQrOK9BwNqiA&s=10"
CLOTHING_IMAGE_URL = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQJoC3uvSpnCuI6JE6slPSQU3Qm_Ll2F7l96kP_49qKi_Wmv3F_w5VxsASh&s=10"
MINERALS_IMAGE_URL = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSWKwrXFpumgfUmMF5wUJUKG7spmcUavBPgU-BRztjJPA&s=10"

FACTS = {
    "population": "1,054,087 (2020 estimate)",
    "population_fa": "۱٬۰۵۴٬۰۸۷ نفر (برآورد سال ۲۰۲۰)",
    "area": "44,836 km²",
    "area_fa": "۴۴٬۸۳۶ کیلومتر مربع",
    "capital": "Fayzabad / فیض‌آباد",
    "languages": "Dari, Pamiri languages, Pashto and other local languages",
    "languages_fa": "دری، زبان‌های پامیری، پشتو و زبان‌های محلی دیگر",
    "countries": ["Tajikistan / تاجیکستان", "China / چین", "Pakistan / پاکستان"],
    "provinces": ["Takhar / تخار", "Panjshir / پنجشیر", "Nuristan / نورستان"],
}

INTRO_EN = """Badakhshan is a mountainous province in northeastern Afghanistan, centered on Fayzabad. It contains parts of the Hindu Kush and Pamir mountain systems and the Wakhan Corridor, giving Afghanistan a narrow land connection with China. Its rivers, valleys, high mountain settlements and border position have shaped its economy, mobility and cultural diversity."""
INTRO_FA = """بدخشان یکی از ولایت‌های کوهستانی شمال‌شرق افغانستان است و مرکز آن فیض‌آباد می‌باشد. این ولایت بخش‌هایی از رشته‌کوه‌های هندوکش و پامیر و همچنین دهلیز واخان را دربر می‌گیرد. موقعیت مرزی، دره‌ها، رودخانه‌ها و ارتفاعات بلند، بر اقتصاد، رفت‌وآمد و تنوع فرهنگی مردم بدخشان اثر گذاشته است."""

CULTURE_EN = """Badakhshan has a diverse cultural landscape with Tajik, Uzbek, Pamiri and Sheghnani communities and, besides Farsi, several local languages. Traditional life includes agriculture, livestock raising, handicrafts, religious and social gatherings, hospitality, music, and local and seasonal entertainment. Pamiri areas preserve distinctive languages, clothing styles, foodways and musical traditions. Cultural practices vary by district, so the portal treats community-submitted material as a valuable source that requires editorial approval."""
CULTURE_FA = """بدخشان دارای چشم‌انداز فرهنگی متنوعی است که جوامع تاجیک، ازبیک، پامیری شغنانی و در کنار زبان فارسی، زبان‌های محلی گوناگون را دربر می‌گیرد. زندگی سنتی در بسیاری از مناطق با زراعت، مالداری، صنایع دستی، مهمان‌نوازی، گردهمایی‌های مذهبی و اجتماعی، موسیقی و سرگرمی‌های محلی و فصلی پیوند دارد. در مناطق پامیری، زبان‌ها، پوشاک، غذاها و موسیقی‌های ویژه حفظ شده‌اند. رسوم در ولسوالی‌های مختلف تفاوت دارد؛ به همین دلیل مطالب ارسالی مردم پس از بررسی گرداننده نشر می‌شود."""

FOOD_EN = """Local food varies with altitude and available crops. Common ingredients and products include wheat, rice, dairy products, meat, legumes, walnuts, almonds, dried fruits and fresh orchard fruits. Community recipes may include local breads, dumplings, soups and rice dishes. Users can upload family recipes and photographs for publication after admin review."""
FOOD_FA = """غذاهای محلی بدخشان با توجه به ارتفاع، آب‌وهوا و محصولات هر منطقه متفاوت است. گندم، برنج، لبنیات، گوشت، حبوبات، چهارمغز، بادام، میوه‌های تازه و خشک از مواد و محصولات مهم غذایی هستند. در خانواده‌ها انواع نان‌های محلی، آش‌ها، غذاهای خمیری و غذاهای برنجی تهیه می‌شود. کاربران می‌توانند دستورهای غذایی و تصاویر خانوادگی را برای نشر پس از تأیید گرداننده ارسال کنند."""

CLOTHING_EN = """Traditional clothing in Badakhshan varies by community, altitude and local heritage. In Pamiri areas, distinctive dress and textile traditions are important cultural expressions. Local garments may use wool, cotton, embroidery, patterned fabrics and practical mountain layers. The portal encourages users to document clothing respectfully by district and community, with captions and dates."""
CLOTHING_FA = """پوشاک سنتی در بدخشان بر اساس جامعه، ارتفاع، اقلیم و میراث محلی تفاوت دارد. در مناطق پامیری، لباس‌ها و بافته‌های ویژه بخشی از بیان فرهنگی مردم است. در پوشاک محلی از پشم، پنبه، گلدوزی، پارچه‌های نقش‌دار و لایه‌های مناسب هوای کوهستان استفاده می‌شود. پورتال از کاربران می‌خواهد تصاویر پوشاک را با ذکر ولسوالی، جامعه و زمان به شکل محترمانه ثبت و ارسال کنند."""

MINERALS_EN = """Badakhshan is internationally associated with lapis lazuli from Sar-i-Sang in the Kokcha valley. Afghanistan's Ministry of Mines and Petroleum describes Badakhshan lapis as a major source and notes the Sary-Sang deposit. Historical and geological sources also discuss other gemstones and mineral occurrences, including ruby/spinel, gold, marble and salt. Mining information should be treated as location- and time-specific because production and access change."""
MINERALS_FA = """بدخشان در سطح بین‌المللی با لاجورد سَرِسنگ در دره کوکچه شناخته می‌شود. وزارت معادن و پترولیم افغانستان، بدخشان را یکی از منابع مهم لاجورد معرفی کرده و از ذخیره سَرِسنگ یاد می‌کند. منابع تاریخی و زمین‌شناسی همچنین از یاقوت/اسپینل، طلا، مرمر، نمک و برخی سنگ‌های نیمه‌قیمتی نام می‌برند. اطلاعات مربوط به استخراج باید با ذکر زمان و محل ارائه شود، زیرا میزان استخراج و دسترسی در دوره‌های مختلف تغییر می‌کند."""

GEOGRAPHY_EN = """Badakhshan borders Tajikistan, China and Pakistan internationally. Within Afghanistan it borders Takhar, Panjshir and Nuristan. The province is dominated by mountainous terrain, with the Hindu Kush and Pamirs, and includes the Wakhan Corridor. Major river systems include the Kokcha and Panj/Amu Darya system."""
GEOGRAPHY_FA = """بدخشان از سمت شمال و شرق با تاجیکستان، از سمت شرق با چین و از سمت جنوب‌شرق با پاکستان مرز بین‌المللی دارد. در داخل افغانستان با ولایت‌های تخار، پنجشیر و نورستان هم‌مرز است. بخش بزرگی از بدخشان را کوهستان‌های هندوکش و پامیر تشکیل می‌دهد و دهلیز واخان نیز در این ولایت قرار دارد. رودخانه‌های کوکچه و پنج و حوزه آمودریا از عناصر مهم جغرافیایی آن هستند."""

USER_SEARCH_LINKS = [
    ("Local food / غذاهای محلی بدخشان", "https://www.google.com/search?q=%D8%BA%D8%B0%D8%A7%D9%87%D8%A7%DB%8C+%D9%85%D8%AD%D9%84%DB%8C+%D8%A8%D8%AF%D8%AE%D8%B4%D8%A7%D9%86"),
    ("Local clothing / لباس‌های محلی بدخشان", "https://www.google.com/search?q=%D9%84%D8%A8%D8%A7%D8%B3+%D9%87%D8%A7%DB%8C+%D9%85%D8%AD%D9%84%DB%8C+%D8%A8%D8%AF%D8%AE%D8%B4%D8%A7%D9%86"),
    ("Minerals and gemstones / معادن و سنگ‌های قیمتی", "https://www.google.com/search?q=%D9%85%D8%B9%D8%A7%D8%AF%D9%86+%D9%88+%D8%B3%D9%86%DA%AF+%D9%87%D8%A7%DB%8C+%D9%82%DB%8C%D9%85%D8%AA%DB%8C+%D8%A8%D8%AF%D8%AE%D8%B4%D8%A7%D9%86"),
    ("Badakhshan people / مردم بدخشان", "https://www.google.com/search?q=%D9%85%D8%B1%D8%AF%D9%85+%D8%A8%D8%AF%D8%AE%D8%B4%D8%A7%D9%86"),
    ("Culture and traditions / فرهنگ و عنعنات", "https://www.google.com/search?q=%D9%81%D8%B1%D9%87%D9%86%DA%AF+%D9%88+%D8%B9%D9%86%D8%B9%D9%86%D8%A7%D8%AA+%D9%85%D8%B1%D8%AF%D9%85+%D8%A8%D8%AF%D8%AE%D8%B4%D8%A7%D9%86"),
    ("Population and districts / نفوس بدخشان و ولسوالی‌ها", "https://www.google.com/search?q=%D9%86%D9%81%D9%88%D8%B3+%D8%A8%D8%AF%D8%AE%D8%B4%D8%A7%D9%86+%D9%88+%D9%86%D9%81%D9%88%D8%B3+%D9%87%D8%B1+%D9%88%D9%84%D8%B3%D9%88%D8%A7%D9%84%DB%8C+%D8%A2%D9%86"),
    ("Farsi Wikipedia district category / رده ولسوالی‌های بدخشان در ویکی‌پدیای فارسی", "https://fa.wikipedia.org/wiki/%D8%B1%D8%AF%D9%87:%D9%88%D9%84%D8%B3%D9%88%D8%A7%D9%84%DB%8C%E2%80%8C%D9%87%D8%A7%DB%8C_%D9%88%D9%84%D8%A7%DB%8C%D8%AA_%D8%A8%D8%AF%D8%AE%D8%B4%D8%A7%D9%86"),
]

SOURCE_NOTES = [
    ("Population / جمعیت", "Districts of Afghanistan table, 2020 estimates", "https://en.wikipedia.org/wiki/Districts_of_Afghanistan"),
    ("Geography / جغرافیا", "EASO/European Union country-of-origin information report, Badakhshan section", "https://www.ecoi.net/en/file/local/2010329/Afghanistan_security_situation_2019.pdf"),
    ("Minerals / معادن", "Afghanistan Ministry of Mines and Petroleum, Mineral Resources in Afghanistan", "https://momp.gov.af/sites/default/files/stg-008_afghanistan_momp_mining_booklet.pdf"),
    ("Culture / فرهنگ", "Australian National University research on Badakhshan social and cultural context", "https://openresearch-repository.anu.edu.au/handle/1885/9198"),
    ("User-provided image / تصویر ارائه‌شده", "Revayat Af image supplied by the user", ICON_URL),
]
