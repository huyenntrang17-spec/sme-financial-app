import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="AI Financial Dashboard for SMEs", layout="wide")

st.markdown("""
    <div style="text-align: center; color: #0D47A1; margin-bottom: 20px;">
        <h1>📊 HỆ THỐNG TRỢ LÝ ẢO AI PHÂN TÍCH TÀI CHÍNH & CẢNH BÁO DÒNG TIỀN</h1>
        <h3>Giải pháp hỗ trợ quản trị tài chính tinh gọn cho Doanh nghiệp Siêu nhỏ (SMEs)</h3>
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
        status_text = "🟢 AN TOÀN - DÒNG TIỀN ỔN ĐỊNH"

        if r["OCF Margin (%)"] < 5:
            reasons.append("⚠️ Biên dòng tiền hoạt động kinh doanh mỏng (< 5%).")
            status = "YELLOW"
            status_text = "🟡 CẢNH BÁO - NGUY CƠ THIẾU HỤT DÒNG TIỀN NGHẾN MẠCH"

        if r["Quick Ratio"] < 0.8:
            reasons.append("🚨 Hệ số thanh toán nhanh thấp (< 0.8), nguy cơ vỡ nợ ngắn hạn cao.")
            status = "RED"
            status_text = "🔴 BÁO ĐỘNG ĐỎ - RỦI RO THANH KHOẢN TRẦM TRỌNG"

        return {"status": status, "status_text": status_text, "reasons": reasons}

    def forecast_cashflow(self):
        ocfs = [self.metrics[p]["OCF Value"] for p in self.periods]
        if len(ocfs) < 2:
            return {"possible": False, "msg": "Không đủ kỳ dữ liệu để dự báo."}
        
        x = np.arange(len(ocfs))
        y = np.array(ocfs)
        slope, intercept = np.polyfit(x, y, 1)
        next_val = slope * len(ocfs) + intercept
        trend = "TĂNG TRƯỞNG" if slope > 0 else "GIẢM"
        return {"possible": True, "forecast_value": round(next_val, 2), "trend": trend, "slope": round(slope, 2)}

uploaded_file = st.file_uploader("📥 Tải lên Báo cáo Tài chính (.xlsx)", type=["xlsx"])

if uploaded_file is not None:
    try:
        analyzer = FinancialAnalyzerStreamlit(uploaded_file)
        ratios = analyzer.compute_financial_ratios()
        risk = analyzer.evaluate_risk_level()
        forecast = analyzer.forecast_cashflow()

        st.success("✅ Xử lý dữ liệu thành công!")

        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown("### 📌 Cảnh báo Rủi ro")
            status_color = "#D32F2F" if risk["status"] == "RED" else ("#FBC02D" if risk["status"] == "YELLOW" else "#388E3C")
            st.markdown(f"""
            <div style="background-color: {status_color}; color: white; padding: 12px; border-radius: 8px; font-weight: bold; text-align: center;">
                {risk['status_text']}
            </div>
            """, unsafe_allow_html=True)
            
            if risk['reasons']:
                st.markdown("**Chi tiết nguy cơ:**")
                for r in risk['reasons']:
                    st.write(r)
            else:
                st.write("Không phát hiện dấu hiệu rủi ro nghiêm trọng.")

        with col2:
            st.markdown("### 📈 Dự báo Dòng tiền kỳ tiếp theo")
            if forecast["possible"]:
                st.metric(label="Dòng tiền OCF Dự báo (Triệu VNĐ)", value=f"{forecast['forecast_value']:,}", delta=forecast['trend'])
            else:
                st.info(forecast["msg"])

        st.markdown("---")
        st.markdown("### 📊 Trực quan hóa Xu hướng Dòng tiền & Thanh khoản")
        periods = analyzer.periods
        ocfs = [ratios[p]["OCF Value"] for p in periods]

        fig = go.Figure()
        fig.add_trace(go.Bar(x=periods, y=ocfs, name="Dòng tiền OCF (Triệu VNĐ)", marker_color='#1E88E5'))
        fig.update_layout(title="Xu hướng Dòng tiền OCF qua các kỳ", template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### 📋 Bảng Chi tiết các Chỉ số Tài chính")
        df_res = pd.DataFrame(ratios)
        st.dataframe(df_res, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Lỗi đọc file: {str(e)}")
else:
    st.info("👈 Vui lòng tải lên tệp Excel báo cáo tài chính mẫu (`bao_cao_tai_chinh_mau_multi.xlsx`) để bắt đầu phân tích.")
