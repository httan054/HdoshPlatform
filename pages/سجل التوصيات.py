import streamlit as st
import pandas as pd
import os

st.title("🗂️ سجل التوصيات - منصة هدوش الذكية")

# اسم ملف السجل
log_file = "recommendation_log.csv"

# عرض السجل لو موجود
if os.path.exists(log_file):
    df = pd.read_csv(log_file)
    st.success(f"📈 تم العثور على {len(df)} توصية محفوظة")
    st.dataframe(df, use_container_width=True)
    with st.expander("📥 تحميل السجل"):
        st.download_button("📤 تحميل Excel", data=df.to_csv(index=False), file_name="سجل_التوصيات.csv")
else:
    st.warning("⚠️ لا يوجد سجل توصيات محفوظ حتى الآن.")
