import streamlit as st
import pandas as pd
import numpy as np
import requests
import os
import csv
from datetime import datetime

st.title("📊 تحليل العملات - منصة هدوش")

TIMEFRAMES = ['4h', '1d']

@st.cache_data(ttl=3600)
def get_symbols():
    url = "https://api.binance.com/api/v3/exchangeInfo"
    res = requests.get(url).json()
    return [s['symbol'] for s in res['symbols'] if s['quoteAsset'] == 'USDT' and s['status'] == 'TRADING']

@st.cache_data(ttl=3600)
def get_klines(symbol, interval, limit=150):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    res = requests.get(url)
    if res.status_code != 200:
        return None
    return res.json()

def analyze(symbol, tf):
    try:
        data = get_klines(symbol, tf)
        if not data:
            return None

        df = pd.DataFrame(data, columns=["time", "open", "high", "low", "close", "volume",
                                         "close_time", "qav", "num_trades", "taker_base_vol",
                                         "taker_quote_vol", "ignore"])
        df['close'] = df['close'].astype(float)
        df['high'] = df['high'].astype(float)
        df['low'] = df['low'].astype(float)
        df['volume'] = df['volume'].astype(float)

        delta = df['close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(14).mean()
        avg_loss = loss.rolling(14).mean()
        rs = avg_gain / avg_loss
        df['RSI'] = 100 - (100 / (1 + rs))

        exp1 = df['close'].ewm(span=12, adjust=False).mean()
        exp2 = df['close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = exp1 - exp2
        df['MA200'] = df['close'].rolling(200).mean()
        df['MA50'] = df['close'].rolling(50).mean()

        support = df['low'].tail(20).min()
        resistance = df['high'].tail(20).max()

        last = df.iloc[-1]

        score = 0
        reasons = []

        if last['RSI'] < 30:
            score += 1
            reasons.append("RSI منخفض")
        if last['MACD'] > 0:
            score += 1
            reasons.append("MACD إيجابي")
        if last['close'] > last['MA200']:
            score += 1
            reasons.append("السعر فوق MA200")
        if last['volume'] > df['volume'].mean():
            score += 1
            reasons.append("حجم تداول مرتفع")
        if last['close'] > last['MA50']:
            score += 1
            reasons.append("السعر فوق MA50")

        signal = "❌ لا توصية"
        if score >= 4:
            signal = "🔥 دخول قوي"
        elif score == 3:
            signal = "👀 مراقبة"

        return {
            'العملة': symbol,
            'الفريم': tf,
            'RSI': round(last['RSI'], 2),
            'MACD': round(last['MACD'], 4),
            'MA200': round(last['MA200'], 2) if not np.isnan(last['MA200']) else '-',
            'MA50': round(last['MA50'], 2) if not np.isnan(last['MA50']) else '-',
            'الدعم': round(support, 4),
            'المقاومة': round(resistance, 4),
            'الحجم': round(last['volume'], 2),
            'TradingView': f"https://www.tradingview.com/symbols/{symbol.replace('USDT','')}USDT/",
            '📊 التوصية': signal,
            '📌 الأسباب': ", ".join(reasons)
        }
    except:
        return None

symbols = get_symbols()
selected = st.multiselect("🔎 اختر العملات للتحليل:", symbols, default=symbols[:20])

فلتر_قوي = st.checkbox("📊 عرض التوصيات القوية فقط 🔥")

if st.button("🚀 تحليل الآن"):
    results = []
    with st.spinner("🤖 يعمل نظام هدوش على التحليل..."):
        for symbol in selected:
            for tf in TIMEFRAMES:
                result = analyze(symbol, tf)
                if result:
                    results.append(result)

                    if result["📊 التوصية"] == "🔥 دخول قوي":
                        # ✅ تنبيه صوتي
                        st.markdown("""
                            <audio autoplay>
                            <source src="https://www.soundjay.com/buttons/sounds/button-3.mp3" type="audio/mpeg">
                            </audio>
                        """, unsafe_allow_html=True)

                        # ✅ حفظ في سجل التوصيات
                        log_file = "recommendation_log.csv"
                        save_data = result.copy()
                        save_data["🕒 التاريخ"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                        if os.path.exists(log_file):
                            with open(log_file, "a", newline="", encoding="utf-8") as f:
                                writer = csv.DictWriter(f, fieldnames=save_data.keys())
                                writer.writerow(save_data)
                        else:
                            with open(log_file, "w", newline="", encoding="utf-8") as f:
                                writer = csv.DictWriter(f, fieldnames=save_data.keys())
                                writer.writeheader()
                                writer.writerow(save_data)

    if results:
        df = pd.DataFrame(results)

        if فلتر_قوي:
            df = df[df["📊 التوصية"] == "🔥 دخول قوي"]

        df['TradingView'] = df['TradingView'].apply(lambda x: f"[رابط]({x})")
        st.success(f"✅ تم تحليل {len(df)} عملة بعد الفلترة")
        st.dataframe(df, use_container_width=True)

        with st.expander("📥 تحميل النتائج كملف Excel"):
            st.download_button(
                label="📤 تحميل ملف Excel",
                data=df.to_csv(index=False).encode("utf-8-sig"),
                file_name="تحليل_هدوش.xlsx",
                mime="text/csv"
            )
    else:
        st.warning("⚠️ لا توجد نتائج حالياً.")
