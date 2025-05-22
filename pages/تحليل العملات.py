import streamlit as st
import pandas as pd
import requests
import numpy as np

st.set_page_config(page_title="📊 تحليل العملات - منصة هدوش", layout="wide")
st.title("📊 تحليل العملات - منصة هدوش")

# ✅ الدالة المعدلة لحماية الاتصال بـ Binance
@st.cache_data(ttl=3600)
def get_symbols():
    try:
        url = "https://api.binance.com/api/v3/exchangeInfo"
        res = requests.get(url).json()

        if 'symbols' not in res:
            st.error("⚠️ فشل في جلب العملات من Binance – احتمال حظر أو خلل مؤقت.")
            return []

        return [s['symbol'] for s in res['symbols'] if s['quoteAsset'] == 'USDT' and s['status'] == 'TRADING']

    except Exception as e:
        st.error(f"❌ خطأ أثناء الاتصال بـ Binance:\n{e}")
        return []

# 🧠 تحليل العملة
def analyze_symbol(symbol):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1h&limit=150"
    res = requests.get(url)
    if res.status_code != 200:
        return None

    data = res.json()
    df = pd.DataFrame(data, columns=["time", "open", "high", "low", "close", "volume",
                                     "close_time", "qav", "num_trades", "taker_base_vol",
                                     "taker_quote_vol", "ignore"])
    df["close"] = df["close"].astype(float)
    df["high"] = df["high"].astype(float)
    df["low"] = df["low"].astype(float)
    df["volume"] = df["volume"].astype(float)

    # RSI
    delta = df["close"].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()
    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))

    # MACD
    exp1 = df["close"].ewm(span=12, adjust=False).mean()
    exp2 = df["close"].ewm(span=26, adjust=False).mean()
    df["MACD"] = exp1 - exp2

    # MA
    df["MA200"] = df["close"].rolling(200).mean()

    support = df["low"].tail(20).min()
    resistance = df["high"].tail(20).max()

    last = df.iloc[-1]

    signal = "❌ لا توصية"
    score = 0
    if last["RSI"] < 30:
        score += 1
    if last["MACD"] > 0:
        score += 1
    if last["close"] > last["MA200"]:
        score += 1
    if last["volume"] > df["volume"].mean():
        score += 1
    if score >= 3:
        signal = "🔥 دخول قوي"
    elif score == 2:
        signal = "👀 مراقبة"

    return {
        "العملة": symbol,
        "RSI": round(last["RSI"], 2),
        "MACD": round(last["MACD"], 4),
        "MA200": round(last["MA200"], 2) if not np.isnan(last["MA200"]) else "-",
        "الدعم": round(support, 4),
        "المقاومة": round(resistance, 4),
        "الحجم": round(last["volume"], 2),
        "📊 التوصية": signal
    }

# 🔍 عرض التحليل
symbols = get_symbols()

if symbols:
    اختيار = st.multiselect("اختر العملات التي تريد تحليلها:", symbols[:50])  # عرض أول 50 عملة فقط لتسريع الصفحة

    if st.button("🔎 بدء التحليل"):
        النتائج = []
        for sym in اختيار:
            result = analyze_symbol(sym)
            if result:
                النتائج.append(result)

        if النتائج:
            df = pd.DataFrame(النتائج)
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("❗ لم يتم العثور على نتائج تحليل.")
else:
    st.stop()
