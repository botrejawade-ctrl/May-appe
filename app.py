import streamlit as st
from google import genai
import PIL.Image

st.set_page_config(page_title="AI Fashion & Fitness Coach", layout="wide")
st.title("👓 مستشارك الشخصي المتكامل")
st.write("!حلل ستايلك، جسمك، ونظامك الغذائي في مكان واحد")

st.sidebar.header("📋 بياناتك الشخصية")
api_key = st.sidebar.text_input("ادخل مفتاح API الخاص بك", type="password")
height = st.sidebar.number_input("الطول (سم)", min_value=100, max_value=250, value=164)
weight = st.sidebar.number_input("الوزن (كجم)", min_value=30, max_value=200, value=64)
budget = st.sidebar.selectbox("الميزانية اليومية للأكل", ["متوسطة", "محدودة جداً", "غير محددة"])

if api_key:
    try:
        client = genai.Client(api_key=api_key)
        st.subheader("📸 ارفع صورتك لتحليل الستايل")
        uploaded_file = st.file_uploader("اختر صورة...", type=["jpg", "jpeg", "png"])

        if uploaded_file and st.button("ابدأ التحليل الشامل"):
            with st.spinner('...جاري التحليل'):
                image = PIL.Image.open(uploaded_file)
                prompt = f"أنت خبير ستايل وتغذية. الطول: {height}سم، الوزن: {weight}كجم، الميزانية: {budget}. حلل الصورة وقدم نصائح للموضة وبرنامج غذائي باللغة العربية."
                
                # تجربة الموديل المستقر مباشرة
                response = client.models.generate_content(model="gemini-1.5-flash", contents=[prompt, image])
                st.markdown("---")
                st.write(response.text)
    except Exception as e:
        st.error(f"حدث خطأ: {e}")
        st.info("نصيحة: تأكد أن مفتاح API صحيح تماماً وجرب مرة أخرى بعد دقيقة.")
else:
    st.warning("👈 يرجى إدخال مفتاح API في القائمة الجانبية.")
