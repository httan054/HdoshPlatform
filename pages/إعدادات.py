import streamlit as st
import json
import os

st.title("⚙️ إعدادات منصة هدوش الذكية")

# ملف الإعدادات
settings_file = "hdosh_settings.json"

# كل الفريمات الممكنة
available_timeframes = ["1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w"]

# كل المؤشرات
available_indicators = [
    "RSI",
    "MACD",
    "MA50",
    "MA100",
    "MA200",
    "الاتجاه العام (Trend)",
    "الفوليوم (Volume)",
    "الدعم والمقاومة"
]

# تحميل الإعدادات الحالية أو إعداد افتراضي
if os.path.exists(settings_file):
    with open(settings_file, "r", encoding="utf-8") as f:
        settings = json.load(f)
else:
    settings = {
        "timeframes": ["4h", "1d"],
        "indicators": ["RSI", "MACD", "MA200"],
        "max_symbols": 20
    }

# واجهة المستخدم
st.subheader("🕒 اختر الفريمات الزمنية للتحليل:")
timeframes = st.multiselect("الفريمات المتاحة:", available_timeframes, default=settings["timeframes"])

st.subheader("📊 المؤشرات التي تريد استخدامها:")
indicators = st.multiselect("المؤشرات:", available_indicators, default=settings["indicators"])

st.subheader("🔢 عدد العملات التي سيتم تحليلها:")
max_symbols = st.slider("كم عملة تبغى تحلل؟", 5, 200, value=settings["max_symbols"])

# حفظ الإعدادات
if st.button("💾 حفظ الإعدادات"):
    settings = {
        "timeframes": timeframes,
        "indicators": indicators,
        "max_symbols": max_symbols
    }
    with open(settings_file, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False)
    st.success("✅ تم حفظ الإعدادات بنجاح!")

# عرض الإعدادات الحالية
with st.expander("📂 عرض الإعدادات الحالية"):
    st.json(settings)
