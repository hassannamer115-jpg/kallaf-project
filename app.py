import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# --- إعدادات الصفحة الواجهة ---
st.set_page_config(page_title="منصة الكلاف الذكية", layout="wide", initial_sidebar_state="expanded")

# --- وظائف قاعدة البيانات (تأمين الحماية) ---
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

# --- تنسيق الواجهة (CSS ليدعم العربية RTL) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: RTL;
        text-align: right;
    }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- القائمة الجانبية ---
st.sidebar.title("🗂️ القائمة الرئيسية")
choice = st.sidebar.radio("اختر الوجهة:", ["الرئيسية", "طلب كلاف جديد", "التسجيل كـ كلاف", "لوحة تحكم الإدارة"])

# --- الصفحة الرئيسية ---
if choice == "الرئيسية":
    st.title("🚀 مرحباً بك في منصة الكلاف")
    st.write("المنصة الأسرع لطلب خدمات الكلاف أو الانضمام لفريق المحترفين.")
    

# --- نموذج طلب خدمة ---
elif choice == "طلب كلاف جديد":
    st.header("📝 تقديم طلب خدمة كلاف")
    with st.form("service_form"):
        c_name = st.text_input("اسم العميل")
        c_phone = st.text_input("رقم الجوال")
        c_vin = st.text_input("رقم الشاسية للمركبة (إن وجد)")
        c_service = st.selectbox("نوع الخدمة المطلوبة", ["فحص دوري", "كلاف محرك", "صيانة هيكل", "أخرى"])
        
        submitted = st.form_submit_button("إرسال الطلب")
        if submitted:
            if c_name and c_phone:
                now = datetime.now().strftime("%Y-%m-%d %H:%M")
                cursor = conn.cursor()
                cursor.execute("INSERT INTO service_requests (customer_name, phone, vin, service_type, created_at) VALUES (?,?,?,?,?)", 
                               (c_name, c_phone, c_vin, c_service, now))
                conn.commit()
                st.success("✅ تم استلام طلبك بنجاح، سيتواصل معك الكلاف المختص.")
            else:
                st.error("⚠️ يرجى ملء الحقول الأساسية (الاسم والجوال).")

# --- نموذج تسجيل كلاف جديد ---
elif choice == "التسجيل كـ كلاف":
    st.header("👷 انضم إلينا كـ كلاف محترف")
    with st.form("kallaf_form"):
        k_name = st.text_input("اسم الكلاف بالكامل")
        k_specialty = st.text_input("التخصص (مثلاً: محركات، كهرباء)")
        k_exp = st.selectbox("سنوات الخبرة", ["1-3 سنوات", "4-7 سنوات", "أكثر من 7 سنوات"])
        k_city = st.text_input("المدينة")
        k_phone = st.text_input("رقم التواصل")
        
        k_submitted = st.form_submit_button("تسجيل البيانات")
        if k_submitted:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO kallaf_reg (name, experience, city, phone, specialty) VALUES (?,?,?,?,?)", 
                           (k_name, k_exp, k_city, k_phone, k_specialty))
            conn.commit()
            st.success("🎊 شكراً لانضمامك! تم تسجيل بياناتك بنجاح.")

# --- لوحة التحكم (Admin Dashboard) ---
elif choice == "لوحة تحكم الإدارة":
    st.header("📊 إدارة الطلبات والمسجلين")
    
    tab1, tab2 = st.tabs(["طلبات الخدمات", "قائمة الكلافين"])
    
    with tab1:
        df_orders = pd.read_sql_query("SELECT * FROM service_requests", conn)
        if not df_orders.empty:
            st.dataframe(df_orders, use_container_width=True)
            
            # عمليات الإدارة (تعديل/حذف)
            order_id = st.number_input("أدخل رقم الطلب للإدارة", min_value=1, step=1)
            col1, col2 = st.columns(2)
            if col1.button("تحديث الحالة إلى (مكتمل)"):
                conn.cursor().execute("UPDATE service_requests SET status='مكتمل' WHERE id=?", (order_id,))
                conn.commit()
                st.rerun()
            if col2.button("حذف الطلب نهائياً"):
                conn.cursor().execute("DELETE FROM service_requests WHERE id=?", (order_id,))
                conn.commit()
                st.rerun()
        else:
            st.info("لا توجد طلبات حالياً.")

    with tab2:
        df_kallaf = pd.read_sql_query("SELECT * FROM kallaf_reg", conn)
        if not df_kallaf.empty:
            st.table(df_kallaf)
        else:
            st.info("لا يوجد كلافين مسجلين بعد.")