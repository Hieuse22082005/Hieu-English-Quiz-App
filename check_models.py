import google.generativeai as genai
import streamlit as st

# Cấu hình Key từ secrets của em
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.write("### Danh sách Model khả dụng với Key của bạn:")

try:
    # Lấy danh sách các model hỗ trợ tạo nội dung
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    if available_models:
        for model_name in available_models:
            st.code(model_name)
            # Nếu thấy tên nào có dạng 'models/gemini-1.5-flash', 
            # hãy copy nguyên văn để dùng.
    else:
        st.error("Không tìm thấy model nào hỗ trợ generateContent.")
except Exception as e:
    st.error(f"Lỗi khi truy vấn danh sách: {e}")