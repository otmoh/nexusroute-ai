import streamlit as st
import math
import io
import pandas as pd
import altair as alt  # مكتبة الرسوم البيانية المتقدمة والأنيقة

# إعدادات الصفحة
st.set_page_config(page_title="Project X Engine", layout="wide")

# قاموس اللغات لترجمة الموقع ديناميكياً
translations = {
    "العربية": {
        "title": "🤖 المشروع إكس - محرك تحسين الخدمات اللوجستية العالمية",
        "subtitle": "تحسين أساليب الشحن البحري وتقليل الهدر المالي لحظياً",
        "sidebar_title": "📦 مواصفات الشحنة ومدخلاتها",
        "slider_label": "اختر وزن الشحنة الإجمالي (بالطن):",
        "analysis_title": "📊 تحليل التحسين في الوقت الفعلي لـ {} طن:",
        "chart_title": "📈 مقارنة بصرية ديناميكية لإجمالي التكاليف الاقتصادية للموانئ ($)",
        "footer": "💡 خوارزمية المشروع إكس تقوم بتحديث هذه البيانات تلقائياً بناءً على حركة الموانئ والطقس.",
        "status_safe": "🟢 مسار آمن وناجح",
        "status_mid": "🟡 ازدحام مروري متوسط",
        "status_danger": "🚨 خطر كبير! تحذير من رسوم التأخير",
        "congestion": "نسبة الازدحام",
        "cost": "التكلفة الإجمالية",
        "time": "الوقت المتوقع",
        "days_unit": "أيام",
        "pdf_btn": "📥 تحميل تقرير الوفورات المالي (PDF)",
        "align": "right", "dir": "rtl"
    },
    "English": {
        "title": "🤖 Project X - Global Logistics Optimization Engine",
        "subtitle": "Real-time maritime route optimization and maritime cost reduction",
        "sidebar_title": "📦 Cargo Specifications & Input",
        "slider_label": "Select Total Cargo Weight (Tons):",
        "analysis_title": "📊 Real-Time Optimization Analysis for {} Tons:",
        "chart_title": "📈 Dynamic Visual Comparison of Total Port Economic Costs ($)",
        "footer": "💡 Project X algorithm automatically updates this data based on port movement and weather.",
        "status_safe": "🟢 Safe Path & Optimal Efficiency",
        "status_mid": "🟡 Moderate Congestion Predicted",
        "status_danger": "🚨 High Risk! Demurrage Warning Issued",
        "congestion": "Congestion Rate",
        "cost": "Total Economic Cost",
        "time": "Estimated Time",
        "days_unit": "Days",
        "pdf_btn": "📥 Download PDF Financial Savings Report",
        "align": "left", "dir": "ltr"
    }
}

# اختيار اللغة من القائمة الجانبية
st.sidebar.markdown("### 🌐 Language / اللغة")
lang = st.sidebar.selectbox("Choose System Language:", ["English", "العربية"])
t = translations[lang]

# تطبيق التنسيق والاتجاهات
st.markdown(f"<style>h1, h3, h4, p, div {{ text-align: {t['align']}; direction: {t['dir']}; font-family: 'Segoe UI', sans-serif; }}</style>", unsafe_allow_html=True)

st.title(t["title"])
st.markdown(f"### {t['subtitle']}")
st.write("---")

st.sidebar.markdown(f"<h3 style='text-align:{t['align']};'>{t['sidebar_title']}</h3>", unsafe_allow_html=True)
cargo_size = st.sidebar.slider(t["slider_label"], min_value=50, max_value=20000, value=500, step=50)

# قاعدة بيانات الموانئ
ports_data = {
    "Algiers": {"congestion": 0.20, "base_cost": 2000, "ar": "الجزائر"},
    "Valencia": {"congestion": 0.15, "base_cost": 3500, "ar": "فالنسيا"},
    "Marseille": {"congestion": 0.45, "base_cost": 4000, "ar": "مارسيليا"},
    "Genoa": {"congestion": 0.80, "base_cost": 3800, "ar": "جنوة"}
}

# دالة توليد ملف PDF
def generate_pdf_report(cargo_weight):
    import io
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    story = []
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=22, textColor=colors.HexColor("#2c3e50"), spaceAfter=15)
    text_style = ParagraphStyle('TextStyle', parent=styles['Normal'], fontSize=11, leading=14, spaceAfter=10)
    
    story.append(Paragraph("PROJECT X - GLOBAL LOGISTICS OPTIMIZATION REPORT", title_style))
    story.append(Paragraph(f"<b>Target Cargo Weight:</b> {cargo_weight:,} Tons", text_style))
    story.append(Spacer(1, 15))
    
    table_data = [["Port Destination", "Congestion Rate", "Estimated Time", "Total Economic Cost"]]
    for port, info in ports_data.items():
        penalty = math.exp(info["congestion"] * 2) * 600
        cost = (cargo_weight * 15) + info["base_cost"] + penalty
        days = round(3 + (info["congestion"] * 12), 1)
        table_data.append([port, f"{info['congestion']*100}%", f"{days} Days", f"${cost:,.2f}"])
        
    t_table = Table(table_data, colWidths=[130, 100, 100, 130])
    t_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2c3e50")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#f8f9fa")),
        ('GRID', (0,0), (-1,-1), 1, colors.HexColor("#e2e8f0")),
    ]))
    story.append(t_table)
    doc.build(story)
    buffer.seek(0)
    return buffer

# زر الـ PDF الجانبي
pdf_data = generate_pdf_report(cargo_size)
st.sidebar.download_button(label=t["pdf_btn"], data=pdf_data, file_name=f"Project_X_Report_{cargo_size}Tons.pdf", mime="application/pdf")

# عرض البطاقات على الشاشة وتجميع البيانات
st.markdown(f"<h3>{t['analysis_title'].format(f'{cargo_size:,}')}</h3>", unsafe_allow_html=True)
cols = st.columns(4)

chart_records = []

for i, (port, info) in enumerate(ports_data.items()):
    congestion_penalty = math.exp(info["congestion"] * 2) * 600
    total_cost = (cargo_size * 15) + info["base_cost"] + congestion_penalty
    estimated_days = round(3 + (info["congestion"] * 12), 1)
    
    display_name = info["ar"] if lang == "العربية" else port
    
    # تحديد اللون والحالة بناء على الازدحام
    if info["congestion"] < 0.3:
        status_text, bg_card, border_color = t["status_safe"], "rgba(46, 204, 113, 0.15)", "#2ecc71"
        color_hex = "#2ecc71"  # أخضر للمسار الآمن
    elif info["congestion"] < 0.6:
        status_text, bg_card, border_color = t["status_mid"], "rgba(241, 196, 15, 0.15)", "#f1c40f"
        color_hex = "#f1c40f"  # أصفر للازدحام المتوسط
    else:
        status_text, bg_card, border_color = t["status_danger"], "rgba(231, 76, 60, 0.15)", "#e74c3c"
        color_hex = "#e74c3c"  # أحمر للخطر المالي
        
    chart_records.append({"Port": display_name, "Cost ($)": total_cost, "Color": color_hex})
    
    with cols[i]:
        st.markdown(f"""
        <div style="background-color: {bg_card}; padding: 25px; border-radius: 12px; border: 2px solid {border_color}; text-align: {t['align']}; direction: {t['dir']};">
            <h3 style="margin-top:0; color:#fff;">🚢 {display_name}</h3>
            <hr style="border-color: #444; margin: 15px 0;">
            <p><b>{t['congestion']}:</b> {info['congestion']*100}%</p>
            <p><b>{t['cost']}:</b> <span style="font-size: 1.2em; color: #2ecc71; font-weight: bold;">${total_cost:,.2f}</span></p>
            <p><b>{t['time']}:</b> {estimated_days} {t['days_unit']}</p>
            <p style="font-weight: bold; margin-bottom:0;">{status_text}</p>
        </div>
        """, unsafe_allow_html=True)

st.write("---")

# 📊 قسم الرسم البياني الاحترافي المطور (أعمدة رشيقة وبألوان متباينة)
st.markdown(f"<h3>{t['chart_title']}</h3>", unsafe_allow_html=True)
df_chart = pd.DataFrame(chart_records)

# بناء الرسم البياني الأنيق عبر Altair لتنحيف الأعمدة وتلوينها ديناميكياً
chart = alt.Chart(df_chart).mark_bar(size=45, cornerRadiusTopLeft=5, cornerRadiusTopRight=5).encode(
    x=alt.X('Port:N', axis=alt.Axis(labelAngle=0, title=None)),
    y=alt.Y('Cost ($):Q', axis=alt.Axis(title='Total Cost ($)')),
    color=alt.Color('Color:N', scale=alt.Scale(identity='property'), legend=None)
).properties(
    height=400
).configure_view(
    strokeWidth=0
)

st.altair_chart(chart, use_container_width=True)

st.write("---")
st.markdown(f"<p style='text-align:center; color:#777;'>{t['footer']}</p>", unsafe_allow_html=True)


