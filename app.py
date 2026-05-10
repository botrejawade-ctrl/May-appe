import streamlit as st
from google import genai
import PIL.Image

# إعداد واجهة التطبيق
st.set_page_config(page_title="AI Fashion & Fitness Coach", layout="wide")
st.title("🕶️ مستشارك الشخصي المتكامل")
st.write("حلل ستايلك، جسمك، ونظامك الغذائي في مكان واحد!")

# القائمة الجانبية للمدخلات
st.sidebar.header("📋 بياناتك الشخصية")
api_key = st.sidebar.text_input("ادخل مفتاح API الخاص بك", type="password")
height = st.sidebar.number_input("الطول (سم)", min_value=100, max_value=250, value=164)
weight = st.sidebar.number_input("الوزن (كجم)", min_value=30, max_value=200, value=70)
budget = st.sidebar.selectbox("الميزانية اليومية للأكل", ["محدودة جداً", "متوسطة", "غير محددة"])

if api_key:
    client = genai.Client(api_key=api_key)
    
    st.subheader("📸 ارفع صورتك لتحليل الستايل")
    uploaded_file = st.file_uploader("اختر صورة تظهر جسمك بوضوح...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = PIL.Image.open(uploaded_file)
        st.image(image, caption='الصورة المرفوعة', width=400)
        
        if st.button("ابدأ التحليل الشامل"):
            with st.spinner('جاري معالجة البيانات...'):
                prompt = f"""
                أنت خبير محترف في الموضة واللياقة البدنية. بناءً على الصورة المرفقة والبيانات التالية:
                - الطول: {height} سم.
                - الوزن: {weight} كجم.
                - الميزانية الغذائية: {budget}.
                
                يرجى تقديم:
                1. تحليل لنوع الجسم والتناسق.
                2. نصائح دقيقة للموضة تزيد من جاذبية الشخص وتجعله يبدو أكثر هيبة.
                3. برنامج غذائي اقتصادي بمصادر بروتين رخيصة.
                اجعل الأسلوب باللغة العربية ومحفزاً.
                """
                response = client.models.generate_content(model="gemini-2.0-flash", contents=[prompt, image])
                st.markdown("---")
                st.write(response.text)
else:
    st.warning("👈 يرجى إدخال مفتاح Gemini API في القائمة الجانبية.")
