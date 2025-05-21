import streamlit as st
import pandas as pd
import os

st.title("📊 تقرير التحليل التلقائي - منصة هدوش")

file_name = "تحليل_هدوش_تلقائي.xlsx"

if os.path.exists(file_name):
    df = pd.read_excel(file_name)
    st.success(f"✅ تم تحميل الملف: {file_name}")

    # فلتر عرض العملات ذات التوصية القوية فقط
    فقط_توصيات = st.checkbox("📌 عرض العملات ذات التوصية 🔥 فقط")

    if فقط_توصيات:
        df = df[df['📊 التوصية'] == '🔥 دخول قوي']

    st.dataframe(df, use_container_width=True)

    with st.expander("📥 تحميل التقرير كملف Excel"):
        st.download_button(
            label="📤 تحميل التقرير",
            data=df.to_csv(index=False).encode("utf-8-sig"),
            file_name="تقرير_هدوش.csv",
            mime="text/csv"
        )
else:
    st.warning("⚠️ لم يتم العثور على ملف التحليل التلقائي بعد. تأكد من تشغيل السكربت التلقائي أولاً.")
