import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Cấu hình trang rộng
st.set_page_config(page_title="AI Cybernetic CFO - SME Financial", layout="wide")

# --- GIAO DIỆN CSS: NỀN TỐI CÔNG NGHỆ NHƯNG CHỮ SÁNG RÕ NÉT ---
st.markdown("""
    <style>
    /* Màu nền tổng thể tối và đổi toàn bộ chữ mặc định thành màu trắng sáng */
    .stApp {
        background-color: #0b0f19;
        color: #ffffff !important;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* Ép tất cả các văn bản, nhãn, chữ thường thành màu trắng sáng */
    p, span, label, div, .streamlit-expanderHeader, .stMarkdown {
        color: #f0f6fc !important;
    }
    
    /* Tiêu đề phong cách Hologram */
    .hero-title {
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-weight: 900;
        font-size: 26px;
        text-shadow: 0px 0px 15px rgba(0, 242, 254, 0.4);
        border-bottom: 2px solid #00f2fe;
        padding-bottom: 12px;
        margin-bottom: 20px;
    }

    /* Khung panel thông tin */
    .cyber-card {
        background-color: #131c31;
        border: 1px solid #00f2fe;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 0 10px rgba(0, 242, 254, 0.2);
        margin-bottom: 15px;
    }

    /* Tùy chỉnh các nút bấm */
    .stButton>button {
        background: linear-gradient(45deg, #00f2fe, #4facfe);
        color: #0b0f19 !important;
        font-weight: bold;
        border: none;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Tiêu đề ứng dụng
st.markdown('<div class="hero-title">🤖 [SYSTEM AI] - TRỢ LÝ CFO & CẢNH BÁO RỦI RO DÒNG TIỀN (SME)</div>', unsafe_allow_html=True)

class FinancialAnalyzerStreamlit:
    def __init__(self, file_path):
        self.df = pd.read_excel(file_path)
