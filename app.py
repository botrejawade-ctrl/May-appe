import streamlit as st
from google import genai
import PIL.Image

# إعداد واجهة التطبيق
st.set_page_config(page_title="AI Fashion & Fitness Coach", layout="wide")
st.title("👓 مستشارك الشخصي المتكامل")
st.write("!حلل ستايلك، جسمك، ونظامك الغذائي في مكان واحد")

# القائمة الجانبية للمدخلات
st.sidebar.header("📋 بياناتك الشخصية")
api_key = st.sidebar.text_input("ادخل مفتاح API الخاص بك", type="password")
height = st.sidebar.number_input("الطول (سم)", min_value=100, max_value=250, value=164)
weight = st.sidebar.number_input("الوزن (كجم)", min_value=30, max_value=200, value=64)
budget = st.sidebar.selectbox("الميزانية اليومية للأكل", ["غير محددة", "متوسطة", "محدودة جداً"])

if api_key:
    try:
        client = genai.Client(api_key=api_key)

        st.subheader("📸 ارفع صورتك لتحليل الستايل")
        uploaded_file = st.file_uploader("اختر صورة تظهر جسمك بوضوح...", type=["jpg", "jpeg", "png"])

        if uploaded_file is not None:
            image = PIL.Image.open(uploaded_file)
            st.image(image, caption='الصورة المرفوعة', width=400)

            if st.button("ابدأ التحليل الشامل"):
                with st.spinner('...جاري معالجة البيانات'):
                    prompt = f"""
                    أنت خبير محترف في الموضة واللياقة البدنية. بناءً على الصورة المرفقة والبيانات التالية:
                    - الطول: {height} سم.
                    - الوزن: {weight} كجم.
                    - الميزانية الغذائية: {budget}.

                    يرجى تقديم تحليل لنوع الجسم، نصائح للموضة، وبرنامج غذائي باللغة العربية.
                    """
                    
                    # محاولة استخدام أسماء مختلفة للموديل لتجنب خطأ 404
                    model_names = ["gemini-1.5-flash", "gemini-1.5-flash-001", "gemini-1.5-flash-002"]
                    success = False
                    
                    for m_name in model_names:
                        try:
                            response = client.models.generate_content(model=m_name, contents=[prompt, image])
                            st.markdown("---")
                            st.write(response.text)
                            success = True
                            break # إذا نجح، توقف عن المحاولة
                        except:
                            continue # إذا فشل، جرب الاسم التالي
                    
                    if not success:
                        st.error("عذراً، لم نتمكن من الاتصال بالموديل. تأكد من صلاحية مفتاح API الخاص بك.")
                        
    except Exception as e:
        st.error(f"حدث خطأ في النظام: {e}")
else:
    st.warning("👈 في القائمة الجانبية يرجى إدخال مفتاح Gemini API.")
