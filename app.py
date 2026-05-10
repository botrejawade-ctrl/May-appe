import streamlit as st
import google.generativeai as genai
import PIL.Image

# إعداد الواجهة
st.set_page_config(page_title="AI Fashion Coach", layout="wide")
st.title("👓 مستشارك الشخصي المتكامل")

# المدخلات
st.sidebar.header("📋 بياناتك الشخصية")
api_key = st.sidebar.text_input("ادخل مفتاح API الخاص بك", type="password")
height = st.sidebar.number_input("الطول (سم)", min_value=100, max_value=250, value=164)
weight = st.sidebar.number_input("الوزن (كجم)", min_value=30, max_value=200, value=64)

if api_key:
    # إعداد الذكاء الاصطناعي بالمكتبة المستقرة
    genai.configure(api_key=api_key)
    
    st.subheader("📸 ارفع صورتك")
    uploaded_file = st.file_uploader("اختر صورة...", type=["jpg", "jpeg", "png"])

    if uploaded_file and st.button("ابدأ التحليل"):
        with st.spinner('جاري التحليل...'):
            try:
                # استخدام الموديل الأكثر شهرة واستقراراً
                model = genai.GenerativeModel('gemini-1.5-flash')
                image = PIL.Image.open(uploaded_file)
                
                prompt = f"أنت خبير ستايل وتغذية. الطول: {height}سم، الوزن: {weight}كجم. حلل الصورة وقدم نصائح باللغة العربية."
                
                response = model.generate_content([prompt, image])
                st.markdown("---")
                st.write(response.text)
            except Exception as e:
                st.error(f"حدث خطأ: {e}")
else:
    st.warning("👈 أدخل مفتاح API في القائمة الجانبية")
