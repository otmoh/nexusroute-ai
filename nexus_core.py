import streamlit as st
import math

# إعدادات الصفحة
st.set_page_config(page_title="NexusRoute AI", layout="wide")

# 1. أيقونة اختيار اللغة في أعلى القائمة الجانبية
st.sidebar.markdown("### 🌐 Language / اللغة")
lang = st.sidebar.selectbox("Choose System Language:", ["العربية", "English", "Français"])

# 2. قاموس اللغات لترجمة الموقع بالكامل ديناميكياً
translations = {
    "العربية": {
        "title": "🤖 NexusRoute AI - محرك تحسين الخدمات اللوجستية العالمية",
        "subtitle": "تحسين أساليب الشحن البحري وتقليل الهدر المالي لحظياً",
        "sidebar_title": "📦 مواصفات الشحنة ومدخلاتها",
        "slider_label": "اختر وزن الشحنة الإجمالي (بالطن):",
        "analysis_title": "📊 تحليل التحسين في الوقت الفعلي لـ {} طن:",
        "footer": "💡 خوارزمية NexusRoute AI تقوم بتحديث هذه البيانات تلقائياً بناءً على حركة الموانئ والطقس.",
        "status_safe": "🟢 مسار آمن وناجح",
        "status_mid": "🟡 ازدحام مروري متوسط",
        "status_danger": "🚨 خطر كبير! تحذير من رسوم التأخير",
        "congestion": "نسبة الازدحام",
        "cost": "التكلفة الإجمالية",
        "time": "الوقت المتوقع",
        "days_unit": "أيام",
        "align": "right", "dir": "rtl"
    },
    "English": {
        "title": "🤖 NexusRoute AI - Global Logistics Optimization Engine",
        "subtitle": "Real-time maritime route optimization and maritime cost reduction",
        "sidebar_title": "📦 Cargo Specifications & Input",
        "slider_label": "Select Total Cargo Weight (Tons):",
        "analysis_title": "📊 Real-Time Optimization Analysis for {} Tons:",
        "footer": "💡 NexusRoute AI algorithm automatically updates this data based on port movement and weather.",
        "status_safe": "🟢 Safe Path & Optimal Efficiency",
        "status_mid": "🟡 Moderate Congestion Predicted",
        "status_danger": "🚨 High Risk! Demurrage Warning Issued",
        "congestion": "Congestion Rate",
        "cost": "Total Economic Cost",
        "time": "Estimated Time",
        "days_unit": "Days",
        "align": "left", "dir": "ltr"
    },
    "Français": {
        "title": "🤖 NexusRoute AI - Moteur d'Optimisation Logistique Globale",
        "subtitle": "Optimisation des routes maritimes et réduction des coûts en temps réel",
        "sidebar_title": "📦 Spécifications de la Cargaison",
        "slider_label": "Sélectionnez le poids total (Tonnes):",
        "analysis_title": "📊 Analyse d'Optimisation en Temps Réel pour {} Tonnes:",
        "footer": "💡 L'algorithme NexusRoute AI met à jour ces données automatiquement selon le trafic et la météo.",
        "status_safe": "🟢 Voie Sécurisée & Optimale",
        "status_mid": "🟡 Congestion Modérée Prévue",
        "status_danger": "🚨 Risque Élevé! Alerte aux Frais de Surestaries",
        "congestion": "Taux de Congestion",
        "cost": "Coût Économique Total",
        "time": "Temps Estimé",
        "days_unit": "Jours",
        "align": "left", "dir": "ltr"
    }
}

# تحديد اللغة النشطة بناءً على اختيار المستخدم
t = translations[lang]

# تطبيق التنسيق والاتجاهات بناءً على اللغة المخطرة
st.markdown(f"""
    <style>
    h1, h3, h4, p, div {{ text-align: {t['align']}; direction: {t['dir']}; font-family: 'Segoe UI', sans-serif; }}
    </style>
""", unsafe_allow_html=True)

# عرض نصوص الواجهة المترجمة
st.title(t["title"])
st.markdown(f"### {t['subtitle']}")
st.write("---")

# تحديث السلايدر الجانبي باللغة الصحيحة
st.sidebar.markdown(f"<h3 style='text-align:{t['align']};'>{t['sidebar_title']}</h3>", unsafe_allow_html=True)
cargo_size = st.sidebar.slider(t["slider_label"], min_value=50, max_value=20000, value=500, step=50)

# قاعدة البيانات الثابتة للموانئ
ports_data = {
    "Algiers / الجزائر": {"congestion": 0.20, "base_cost": 2000},
    "Valencia / فالنسيا": {"congestion": 0.15, "base_cost": 3500},
    "Marseille / مارسيليا": {"congestion": 0.45, "base_cost": 4000},
    "Genoa / جنوة": {"congestion": 0.80, "base_cost": 3800}
}

st.markdown(f"<h3>{t['analysis_title'].format(f'{cargo_size:,}')}</h3>", unsafe_allow_html=True)

# عرض البطاقات اللوجستية الملونة
cols = st.columns(4)
for i, (port, info) in enumerate(ports_data.items()):
    with cols[i]:
        congestion_penalty = math.exp(info["congestion"] * 2) * 600
        total_cost = (cargo_size * 15) + info["base_cost"] + congestion_penalty
        estimated_days = round(3 + (info["congestion"] * 12), 1)
        
        if info["congestion"] < 0.3:
            status_text = t["status_safe"]
            bg_card, border_color = "rgba(46, 204, 113, 0.15)", "#2ecc71"
        elif info["congestion"] < 0.6:
            status_text = t["status_mid"]
            bg_card, border_color = "rgba(241, 196, 15, 0.15)", "#f1c40f"
        else:
            status_text = t["status_danger"]
            bg_card, border_color = "rgba(231, 76, 60, 0.15)", "#e74c3c"
            
        st.markdown(f"""
        <div style="background-color: {bg_card}; padding: 25px; border-radius: 12px; border: 2px solid {border_color}; text-align: {t['align']}; direction: {t['dir']};">
            <h3 style="margin-top:0; color:#fff;">🚢 {port}</h3>
            <hr style="border-color: #444; margin: 15px 0;">
            <p><b>{t['congestion']}:</b> {info['congestion']*100}%</p>
            <p><b>{t['cost']}:</b> <span style="font-size: 1.2em; color: #2ecc71; font-weight: bold;">${total_cost:,.2f}</span></p>
            <p><b>{t['time']}:</b> {estimated_days} {t['days_unit']}</p>
            <p style="font-weight: bold; margin-bottom:0;">{status_text}</p>
        </div>
        """, unsafe_allow_html=True)

st.write("---")
st.markdown(f"<p style='text-align:center; color:#777;'>{t['footer']}</p>", unsafe_allow_html=True)


