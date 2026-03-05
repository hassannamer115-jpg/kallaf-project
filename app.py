import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# --- إعدادات الصفحة ---
st.set_page_config(page_title="منصة الكلاف الذكية", layout="wide")

# --- وظائف قاعدة البيانات ---
def init_db():
    conn = sqlite3.connect('kallaf_system.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS service_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT, customer_name TEXT, phone TEXT, service_type TEXT, created_at TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS kallaf_reg (
        id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, specialty TEXT, phone TEXT, city TEXT)''')
    conn.commit()
    return conn

conn = init_db()

# --- القائمة الجانبية ---
st.sidebar.title("📂 القائمة الرئيسية")
choice = st.sidebar.radio("اختر الوجهة:", ["الرئيسية", "طلب كلاف جديد", "التسجيل كـ كلاف", "لوحة تحكم الإدارة"])

# 1. الصفحة الرئيسية
if choice == "الرئيسية":
    st.title("🚀 مرحباً بك في منصة الكلاف")
    st.write("المنصة الأسرع لطلب خدمات الكلاف أو الانضمام لفريق المحترفين.")

# 2. صفحة طلب كلاف جديد (الحل للمشكلة)
elif choice == "طلب كلاف جديد":
    st.title("📝 نموذج طلب خدمة")
    with st.form("request_form"):
        name = st.text_input("اسم العميل")
        phone = st.text_input("رقم الهاتف")
        service = st.selectbox("نوع الخدمة", ["كلاف خيل", "كلاف ماشية", "أخرى"])
        submitted = st.form_submit_button("إرسال الطلب")
        if submitted:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO service_requests (customer_name, phone, service_type, created_at) VALUES (?, ?, ?, ?)", 
                           (name, phone, service, datetime.now().strftime("%Y-%m-%d %H:%M")))
            conn.commit()
            st.success("تم إرسال طلبك بنجاح!")

# 3. صفحة التسجيل كـ كلاف (الحل للمشكلة)
elif choice == "التسجيل كـ كلاف":
    st.title("👷 انضم إلينا كـ محترف")
    with st.form("kallaf_form"):
        k_name = st.text_input("الاسم بالكامل")
        k_specialty = st.text_input("التخصص")
        k_phone = st.text_input("رقم التواصل")
        k_city = st.text_input("المدينة")
        k_submitted = st.form_submit_button("تسجيل")
        if k_submitted:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO kallaf_reg (name, specialty, phone, city) VALUES (?, ?, ?, ?)", 
                           (k_name, k_specialty, k_phone, k_city))
            conn.commit()
            st.success("تم تسجيل بياناتك بنجاح!")

# 4. لوحة تحكم الإدارة
elif choice == "لوحة تحكم الإدارة":
    st.title("🔐 منطقة الإدارة")
    password = st.text_input("أدخل كلمة المرور للدخول", type="password")
    if password == "K@llaf_Admin_2026!":
        st.success("تم تسجيل الدخول بنجاح")
        st.subheader("📋 طلبات الخدمة")
        df_req = pd.read_sql_query("SELECT * FROM service_requests", conn)
        st.dataframe(df_req)
        st.subheader("👷 الكلافين المسجلين")
        df_kal = pd.read_sql_query("SELECT * FROM kallaf_reg", conn)
        st.dataframe(df_kal)
    elif password != "":
        st.error("كلمة المرور غير صحيحة!")
