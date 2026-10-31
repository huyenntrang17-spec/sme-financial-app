import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Cấu hình trang rộng
st.set_page_config(page_title="Hệ thống trợ lý ảo AI phân tích tài chính cảnh báo dòng tiền", layout="wide")

# --- GIAO DIỆN CSS: KHÔNG GIAN AI & ROBOT CÔNG NGHỆ ---
st.markdown("""
    <style>
    .stApp {
        background-color: #050b1a;
        background-image: radial-gradient(circle at 50% 20%, #102650 0%, #050b1a 80%);
        color: #ffffff !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    p, span, label, div, .streamlit-expanderHeader, .stMarkdown {
        color: #e0f2fe !important;
    }
    
    .hero-container {
        background: rgba(13, 37, 78, 0.75);
        border: 2px solid #00f2fe;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 0 25px rgba(0, 242, 254, 0.5);
        margin-bottom: 25px;
        backdrop-filter: blur(10px);
    }

    .hero-title {
        background: linear-gradient(90deg, #00f2fe 0%, #70e1f5 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        font-size: 24px;
        text-transform: uppercase;
        margin-bottom: 8px;
        text-shadow: 0 0 10px rgba(0, 242, 254, 0.3);
    }

    .hero-subtitle {
        color: #93c5fd !important;
        font-size: 14px;
        font-weight: 600;
        letter-spacing: 0.5px;
    }

    .stButton>button {
        background: linear-gradient(45deg, #00f2fe, #3b82f6);
        color: #050b1a !important;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        box-shadow: 0 0 10px rgba(0, 242, 254, 0.5);
    }
    </style>
""", unsafe_allow_html=True)

# Tiêu đề & Slogan chuẩn theo yêu cầu
st.markdown("""
    <div class="hero-container">
        <div class="hero-title">🤖 HỆ THỐNG TRỢ LÝ ẢO AI PHÂN TÍCH TÀI CHÍNH & CẢNH BÁO DÒNG TIỀN</div>
        <div class="hero-subtitle">Giải pháp hỗ trợ quản lý tài chính tinh gọn cho doanh nghiệp nhỏ</div>
    </div>
""", unsafe_allow_html=True)

class FinancialAnalyzerStreamlit:
    def __init__(self, file_path):
        self.df = pd.read_excel(file_path)
        self.periods = [str(col) for col in self.df.columns[1:]]
        self.metrics = self.compute_financial_ratios()

    def get_val(self, row_name, col_idx):
        try:
            val = self.df.iloc[row_name, col_idx + 1]
            return float(val) if pd.notnull(val) else 0.0
        except:
            return 0.0

    def compute_financial_ratios(self):
        ratios = {}
        for i, p in enumerate(self.periods):
            cash = self.get_val(0, i)
            receivable = self.get_val(1, i)
            inventory = self.get_val(2, i)
            total_assets = self.get_val(3, i)
            current_liabilities = self.get_val(4, i)
            ocf = self.get_val(5, i)
            revenue = self.get_val(6, i)

            quick_ratio = (cash + receivable) / current_liabilities if current_liabilities > 0 else 0
            ocf_margin = (ocf / revenue) * 100 if revenue > 0 else 0

            ratios[p] = {
                "Quick Ratio": round(quick_ratio, 2),
                "OCF Margin (%)": round(ocf_margin, 2),
                "OCF Value": ocf
            }
        return ratios

    def evaluate_risk_level(self):
        latest_p = self.periods[-1]
        r = self.metrics[latest_p]
        reasons = []
        status = "GREEN"
        status_text = "🟢 [AN TOÀN] - HỆ THỐNG DÒNG TIỀN ỔN ĐỊNH"

        if r["OCF Margin (%)"] < 5:
            reasons.append("⚠️ Cảnh báo: Biên dòng tiền hoạt động kinh doanh mỏng (< 5%).")
            status = "YELLOW"
            status_text = "🟡 [CẢNH BÁO] - NGUY CƠ NGHẼN MẠCH THANH KHOẢN"

        if r["Quick Ratio"] < 0.8:
            reasons.append("🚨 Báo động: Hệ số thanh toán nhanh thấp (< 0.8), áp lực nợ ngắn hạn cao.")
            status = "RED"
            status_text = "🔴 [NGUY HIỂM] - RỦI RO VỠ NỢ NGẮN HẠN TRẦM TRỌNG"

        return {"status": status, "status_text": status_text, "reasons": reasons}

    def forecast_cashflow(self):
        ocfs = [self.metrics[p]["OCF Value"] for p in self.periods]
        if len(ocfs) < 2:
            return {"possible": False, "msg": "Dữ liệu không đủ để AI dự báo."}
        
        x = np.arange(len(ocfs))
        y = np.array(ocfs)
        slope, intercept = np
