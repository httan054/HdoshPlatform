import streamlit as st

st.set_page_config(page_title="📈 الرسم البياني", layout="wide")
st.title("📈 عرض الرسم البياني المباشر - منصة هدوش")

# ✅ قائمة عملات جاهزة
symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", "DOGEUSDT"]

# ✅ اختيار العملة
selected_symbol = st.selectbox("🔍 اختر العملة:", symbols)

# ✅ اختيار الفريم الزمني
timeframes = {
    "1 دقيقة": "1",
    "15 دقيقة": "15",
    "1 ساعة": "60",
    "4 ساعات": "240",
    "يومي": "D"
}
selected_tf_label = st.selectbox("⏱️ اختر الفريم:", list(timeframes.keys()))
selected_tf = timeframes[selected_tf_label]

# ✅ زر عرض الرسم البياني
if st.button("📊 عرض الرسم البياني"):
    tv_symbol = selected_symbol.replace("USDT", "USD")
    st.markdown(f"### الرسم البياني لـ {selected_symbol} - فريم: {selected_tf_label}")

    # ✅ عرض الرسم البياني من TradingView مع مؤشرات RSI و MACD
    st.components.v1.html(f"""
        <div class="tradingview-widget-container">
            <iframe src="https://s.tradingview.com/widgetembed/?symbol=BINANCE%3A{tv_symbol}&interval={selected_tf}&hidesidetoolbar=1&theme=dark&style=1&studies=RSI%40tv-basicstudies%2CMACD%40tv-basicstudies&toolbarbg=f1f3f6&withdateranges=1&hideideas=1&locale=ar"
                width="100%" height="600" frameborder="0" allowtransparency="true" scrolling="no">
            </iframe>
        </div>
    """, height=600)

    st.success("✅ تم عرض الرسم البياني بنجاح!")

    # ✅ ملاحظة مستقبلية: نقدر نضيف لقطة أو حفظ صورة أو تحليل شمعة تلقائي لاحقًا
