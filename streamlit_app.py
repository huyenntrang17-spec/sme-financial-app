import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Cấu hình trang với giao diện rộng
st.set_page_config(page_title="AI Cybernetic CFO - SME Financial", layout="wide")

# --- GIAO DIỆN CSS PHONG CÁCH ROBOT CÔNG NGHỆ (SCI-FI / CYBERPUNK) ---
st.markdown("""
    <style>
    /* Màu nền tổng thể tối đậm chất công nghệ */
    .stApp {
        background-color: #0b0f19;
        color: #00ffcc;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* Tiêu đề phong cách bảng mạch / Hologram */
    .hero-title {
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-weight: 900;
        font-size: 28px;
        text-shadow: 0px 0px 20px rgba(0, 242, 254, 0.5);
        border-bottom: 2px solid #00f2fe;
        padding-bottom: 15px;
        margin-bottom: 25px;
    }

    /* Khung panel thông tin phong cách trạm AI */
    .cyber-card {
        background-color: #131c31;
        border: 1px solid #00f2fe;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 0 15px rgba(0, 242, 254, 0.2);
        margin-bottom: 20px;
    }

    /* Tùy chỉnh các nút bấm */
    .stButton>button {
        background: linear-gradient(45deg, #00f2fe, #4facfe);
        color: #0b0f19;
        font-weight: bold;
        border: none;
        border-radius: 5px;
        box-shadow: 0 0 10px rgba(0, 242, 254, 0.4);
    }
    .stButton>button:hover {
        background: linear-gradient(45deg, #4facfe, #00f2fe);
        color: #ffffff;
        box-shadow: 0 0 20px rgba(0, 242, 254, 0.8);
    }
    
    /* Chữ hiển thị nhãn */
    label, .streamlit-expanderHeader {
        color: #00f2fe !important;
    }
    </style>
""", unsafe_allow_html=True)

# Tiêu đề ứng dụng
st.markdown('<div class="hero-title">🤖 [SYSTEM AI] - TRỢ LÝ CFO & CẢNH BÁO RỦI RO DÒNG TIỀN (SME)</div>', unsafe_allow_html=True)

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
        slope, intercept = np.polyfit(x, y, 1)
        next_val = slope * len(ocfs) + intercept
        trend = "TĂNG TRƯỞNG" / 1 if slope > 0 else "SUY GIẢM"
        return {"possible": True, "forecast_value": round(next_val, 2), "trend": "TĂNG TRƯỞNG" if slope > 0 else "SUY GIẢM", "slope": round(slope, 2)}

# Khung tải file đầu vào
st.markdown("### 📥 MODULE KẾT NỐI DỮ LIỆU TÀI CHÍNH")
uploaded_file = st.file_uploader("Tải lên tệp báo cáo tài chính (.xlsx)", type=["xlsx"])

if uploaded_file is not None:
    try:
        analyzer = FinancialAnalyzerStreamlit(uploaded_file)
        ratios = analyzer.compute_financial_ratios()
        risk = analyzer.evaluate_risk_level()
        forecast = analyzer.forecast_cashflow()

        st.success("⚡ [AI CORE]: Đã quét và phân tích dữ liệu thành công!")

        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown("### 🛡️ TRẠM KIỂM SOÁT RỦI RO")
            status_color = "#ff3366" if risk["status"] == "RED" else ("#ffcc00" if risk["status"] == "YELLOW" else "#00ffcc")
            st.markdown(f"""
            <div style="background-color: #131c31; border: 2px solid {status_color}; color: {status_color}; padding: 15px; border-radius: 8px; font-weight: bold; text-align: center; box-shadow: 0 0 10px {status_color};">
                {risk['status_text']}
            </div>
            """, unsafe_allow_html=True)
            
            if risk['reasons']:
                st.markdown("<br>**Chi tiết phân tích lỗi:**", unsafe_allow_html=True)
                for r in risk['reasons']:
                    st.write(r)
            else:
                st.write("Không phát hiện bất thường trong hệ thống tài chính.")

        with col2:
            st.markdown("### 📈 MÔ HÌNH AI DỰ BÁO DÒNG TIỀN")
            if forecast["possible"]:
                st.metric(label="Dự báo OCF kỳ tiếp theo (Triệu VNĐ)", value=f"{forecast['forecast_value']:,}", delta=forecast['trend'])
            else:
                st.info(forecast["msg"])

        st.markdown("---")
        st.markdown("### 📊 GIAO DIỆN TRỰC QUAN HÓA DÒNG TIỀN OCF")
        periods = analyzer.periods
        ocfs = [ratios[p]["OCF Value"] for p in periods]

        fig = go.Figure()
        fig.add_trace(go.Bar(x=periods, y=ocfs, name="Dòng tiền OCF (Triệu VNĐ)", marker_color='#00f2fe'))
        fig.update_layout(
            title="Biểu đồ dao động Dòng tiền thuần từ HĐKD", 
            template="plotly_dark",
            paper_bgcolor="#131c31",
            plot_bgcolor="#131c31"
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### 📋 BẢNG THÔNG SỐ CHỈ SỐ TÀI CHÍNH CHI TIẾT")
        df_res = pd.DataFrame(ratios)
        st.dataframe(df_res, use_container_width=True)

    except Exception as e:
        st.error(f"❌ [LỖI HỆ THỐNG]: {str(e)}")
else:
    st.info("👈 Vui lòng tải lên tệp Excel báo cáo tài chính mẫu để khởi động hệ thống AI phân tích.")
