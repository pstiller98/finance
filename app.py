import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page Config
st.set_page_config(
    page_title="WealthVision Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS für Mobile
st.markdown("""
<style>
    .stApp {
        max-width: 100%;
        padding: 0;
    }
    .big-font {
        font-size: 32px !important;
        font-weight: 800;
    }
    .medium-font {
        font-size: 24px !important;
        font-weight: 700;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 24px;
        border-radius: 16px;
        color: white;
        margin-bottom: 16px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 12px 20px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Daten
positions = pd.DataFrame([
    {'Name': 'Allianz', 'Shares': 12, 'BuyPrice': 219.77, 'CurrentPrice': 383.00, 'Broker': 'Consorsbank'},
    {'Name': 'BASF', 'Shares': 29, 'BuyPrice': 67.16, 'CurrentPrice': 52.77, 'Broker': 'Consorsbank'},
    {'Name': 'Deutsche Telekom', 'Shares': 326, 'BuyPrice': 19.48, 'CurrentPrice': 29.19, 'Broker': 'Consorsbank'},
    {'Name': 'SAP', 'Shares': 32.65, 'BuyPrice': 144.12, 'CurrentPrice': 156.30, 'Broker': 'Trade Republic'},
    {'Name': 'NVIDIA', 'Shares': 8, 'BuyPrice': 115.00, 'CurrentPrice': 189.58, 'Broker': 'Consorsbank'},
    {'Name': 'Core MSCI World', 'Shares': 82.41, 'BuyPrice': 60.50, 'CurrentPrice': 73.57, 'Broker': 'Trade Republic'}
])

# Berechnungen
positions['CurrentValue'] = positions['Shares'] * positions['CurrentPrice']
positions['Invested'] = positions['Shares'] * positions['BuyPrice']
positions['Profit'] = positions['CurrentValue'] - positions['Invested']
positions['ProfitPercent'] = (positions['Profit'] / positions['Invested']) * 100

# Stats
total_value = positions['CurrentValue'].sum()
total_profit = positions['Profit'].sum()
crypto_value = 2735.66
cash = 2767
total_assets = total_value + crypto_value + cash

# Header
st.markdown('<h1 style="text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 36px; font-weight: 800;">📊 WealthVision Pro</h1>', unsafe_allow_html=True)

# Hero Card
st.markdown(f"""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 32px; border-radius: 20px; color: white; text-align: center; margin: 16px 0;">
    <div style="font-size: 14px; opacity: 0.9; margin-bottom: 8px;">Gesamtvermögen</div>
    <div style="font-size: 48px; font-weight: 800; margin-bottom: 16px;">{total_assets:,.0f} €</div>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; font-size: 14px;">
        <div>
            <div style="opacity: 0.8;">Portfolio</div>
            <div style="font-size: 20px; font-weight: 700;">{total_value:,.0f} €</div>
        </div>
        <div>
            <div style="opacity: 0.8;">Gewinn</div>
            <div style="font-size: 20px; font-weight: 700;">{total_profit:,.0f} €</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "💼 Portfolio", "🐷 Sparpläne", "📈 Prognose"])

with tab1:
    # Quick Stats
    col1, col2 = st.columns(2)
    with col1:
        st.metric("💶 Cash", f"{cash:,.0f} €")
        st.metric("📊 Positionen", len(positions))
    with col2:
        st.metric("₿ Krypto", f"{crypto_value:,.0f} €")
        st.metric("📈 Rendite", f"{(total_profit/total_value*100):.1f}%")
    
    # Asset Allocation
    st.subheader("Asset Verteilung")
    allocation_data = pd.DataFrame({
        'Asset': ['Portfolio', 'Krypto', 'Cash'],
        'Wert': [total_value, crypto_value, cash]
    })
    fig_pie = px.pie(allocation_data, values='Wert', names='Asset', 
                     color_discrete_sequence=['#667eea', '#f59e0b', '#3b82f6'])
    fig_pie.update_layout(height=300)
    st.plotly_chart(fig_pie, use_container_width=True)
    
    # Top Positionen
    st.subheader("Top 3 Performer")
    top_positions = positions.nlargest(3, 'ProfitPercent')[['Name', 'CurrentValue', 'ProfitPercent']]
    for idx, row in top_positions.iterrows():
        col1, col2, col3 = st.columns([3, 2, 2])
        with col1:
            st.write(f"**{row['Name']}**")
        with col2:
            st.write(f"{row['CurrentValue']:,.0f} €")
        with col3:
            color = "green" if row['ProfitPercent'] >= 0 else "red"
            st.markdown(f"<span style='color: {color}; font-weight: 700;'>{row['ProfitPercent']:.1f}%</span>", unsafe_allow_html=True)

with tab2:
    st.subheader("Alle Positionen")
    
    # DataFrame mit Styling
    display_df = positions[['Name', 'Broker', 'CurrentValue', 'Profit', 'ProfitPercent']].copy()
    display_df.columns = ['Aktie', 'Broker', 'Wert (€)', 'Gewinn (€)', 'Rendite (%)']
    display_df['Wert (€)'] = display_df['Wert (€)'].round(0)
    display_df['Gewinn (€)'] = display_df['Gewinn (€)'].round(0)
    display_df['Rendite (%)'] = display_df['Rendite (%)'].round(1)
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Rendite (%)": st.column_config.NumberColumn(
                format="%.1f%%"
            )
        }
    )
    
    # Performance Chart
    st.subheader("Performance Übersicht")
    fig_bar = px.bar(positions, x='Name', y='ProfitPercent', 
                     color='ProfitPercent',
                     color_continuous_scale=['red', 'yellow', 'green'],
                     labels={'ProfitPercent': 'Rendite (%)', 'Name': 'Position'})
    fig_bar.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_bar, use_container_width=True)

with tab3:
    st.subheader("Aktive Sparpläne")
    
    savings = pd.DataFrame([
        {'Name': 'Core MSCI World', 'Betrag': 700, 'Aktiv': True},
        {'Name': 'MSCI EM', 'Betrag': 300, 'Aktiv': True},
        {'Name': 'Deutsche Telekom', 'Betrag': 250, 'Aktiv': True},
        {'Name': 'Allianz', 'Betrag': 100, 'Aktiv': True}
    ])
    
    total_savings = savings[savings['Aktiv']]['Betrag'].sum()
    st.metric("💰 Monatliche Sparrate", f"{total_savings:,.0f} €")
    
    for idx, row in savings.iterrows():
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            st.write(f"**{row['Name']}**")
        with col2:
            st.write(f"{row['Betrag']} € / Monat")
        with col3:
            if row['Aktiv']:
                st.success("✓")
            else:
                st.warning("⏸")

with tab4:
    st.subheader("Portfolio-Prognose")
    
    col1, col2 = st.columns(2)
    with col1:
        years = st.slider("Zeitraum (Jahre)", 1, 30, 10)
    with col2:
        return_rate = st.slider("Erwartete Rendite (%)", 0, 15, 7)
    
    # Berechnung
    monthly_savings = 1450  # Summe der Sparpläne
    monthly_rate = return_rate / 100 / 12
    months = years * 12
    
    projection = []
    current_val = total_value
    for month in range(0, months + 1):
        if month > 0:
            current_val = current_val * (1 + monthly_rate) + monthly_savings
        if month % 12 == 0:
            year = month / 12
            invested = total_value + (monthly_savings * month)
            projection.append({
                'Jahr': year,
                'Wert': current_val,
                'Investiert': invested,
                'Gewinn': current_val - invested
            })
    
    proj_df = pd.DataFrame(projection)
    
    # Ergebnis
    end_value = proj_df.iloc[-1]['Wert']
    end_invested = proj_df.iloc[-1]['Investiert']
    end_profit = proj_df.iloc[-1]['Gewinn']
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🎯 Endwert", f"{end_value:,.0f} €")
    with col2:
        st.metric("💰 Investiert", f"{end_invested:,.0f} €")
    with col3:
        st.metric("📈 Gewinn", f"{end_profit:,.0f} €")
    
    # Chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=proj_df['Jahr'], y=proj_df['Investiert'], 
                            fill='tonexty', name='Investiert',
                            line=dict(color='#94a3b8')))
    fig.add_trace(go.Scatter(x=proj_df['Jahr'], y=proj_df['Wert'], 
                            fill='tonexty', name='Gesamtwert',
                            line=dict(color='#10b981')))
    fig.update_layout(height=400, hovermode='x unified')
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #64748b; font-size: 12px;'>WealthVision Pro • Mobile Edition 📱</div>", unsafe_allow_html=True)


