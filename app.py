import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# --- إعدادات الصفحة الواجهة ---
st.set_page_config(page_title="منصة الكلاف الذكية", layout="wide", initial_sidebar_state="expanded")

# --- وظائف قاعدة البيانات ---
def init_db():
    conn = sqlite3.connect('kallaf_system.db', check_same_thread=False)
    cursor = conn.cursor()
    # جدول طلبات الخدمة
    cursor.execute('''CREATE TABLE IF NOT EXISTS service_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT, phone TEXT, vin TEXT, service_type TEXT,
        status TEXT DEFAULT 'قيد الانتظار', created_at TEXT)''')
    # جدول تسجيل الكلافين
    cursor.execute('''CREATE TABLE IF NOT EXISTS kallaf_reg (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, experience TEXT, city TEXT, phone TEXT, specialty TEXT)''')
    conn.commit()
    return conn

conn = init_db()

# --- القائمة الجانبية ---
st.sidebar.title("📂 القائمة الرئيسية")
choice = st.sidebar.radio("اختر الوجهة:", ["الرئيسية", "طلب كلاف جديد", "التسجيل كـ كلاف", "لوحة تحكم الإدارة"])

# --- الصفحة الرئيسية ---
if choice == "الرئيسية":
    st.title("🚀 مرحباً بك في منصة الكلاف")
    st.write("المنصة الأسرع لطلب خدمات الكلاف أو الانضمام لفريق المحترفين.")

# --- لوحة تحكم الإدارة (مع حماية بكلمة سر) ---
elif choice == "لوحة تحكم الإدارة":
    st.title("🔐 منطقة الإدارة")
    
    # كلمة سر قوية مقترحة: K@llaf_Admin_2026!
    password = st.text_input("أدخل كلمة المرور للدخول", type="password")
    
    if password == "K@llaf_Admin_2026!":
        st.success("تم تسجيل الدخول بنجاح")
        st.subheader("📋 طلبات الخدمة الحالية")
        df_requests = pd.read_sql_query("SELECT * FROM service_requests", conn)
        st.dataframe(df_requests)
        
        st.subheader("👷 الكلافين المسجلين")
        df_kallaf = pd.read_sql_query("SELECT * FROM kallaf_reg", conn)
        st.dataframe(df_kallaf)
    elif password != "":
        st.error("كلمة المرور غير صحيحة، حاول مرة أخرى.")

# (بقية الصفحات "طلب كلاف" و "تسجيل" تظل كما هي في كودك الأصلي)
