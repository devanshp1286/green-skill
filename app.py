import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Energy Consumption Calculator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #ff6b6b, #ee5a24);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin: 10px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .energy-result {
        background: linear-gradient(135deg, #00b894, #00a085);
        color: white;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
    }
    
    .section-header {
        background: linear-gradient(90deg, #667eea, #764ba2);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 20px 0 10px 0;
        text-align: center;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .info-box {
        background: linear-gradient(135deg, #fdcb6e, #e17055);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #e17055;
    }
    
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
    }
    
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
    }
    
    .stRadio > div {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Title and header
st.markdown("""
<div style="text-align: center; margin-bottom: 30px;">
    <h1 style="color: white; font-size: 3rem; margin-bottom: 10px;">⚡ Energy Consumption Calculator</h1>
    <p style="color: rgba(255, 255, 255, 0.8); font-size: 1.2rem;">Calculate your home's energy consumption with our smart calculator</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'calculated' not in st.session_state:
    st.session_state.calculated = False
if 'energy_data' not in st.session_state:
    st.session_state.energy_data = {}

# Sidebar for navigation
st.sidebar.markdown("""
<div class="section-header">
    <h3>📊 Navigation</h3>
</div>
""", unsafe_allow_html=True)

page = st.sidebar.selectbox(
    "Choose a section:",
    ["🏠 Home Calculator", "📈 Energy Analysis", "💡 Tips & Info"],
    index=0
)

if page == "🏠 Home Calculator":
    # Main calculator interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Personal Information Section
        st.markdown("""
        <div class="section-header">
            <h3>👤 Personal Information</h3>
        </div>
        """, unsafe_allow_html=True)
        
        with st.container():
            name = st.text_input("🏷️ Your Name", placeholder="Enter your full name")
            
            col_age, col_city = st.columns(2)
            with col_age:
                age = st.number_input("🎂 Age", min_value=1, max_value=120, value=25)
            with col_city:
                city = st.text_input("🏙️ City", placeholder="Enter your city")
            
            area = st.text_input("📍 Area/Locality", placeholder="Enter your area name")
        
        # Housing Information Section
        st.markdown("""
        <div class="section-header">
            <h3>🏠 Housing Information</h3>
        </div>
        """, unsafe_allow_html=True)
        
        with st.container():
            flat_tenament = st.radio(
                "🏠 Type of Residence:",
                ["Flat", "Tenement"],
                horizontal=True
            )
            
            facility = st.selectbox(
                "🏡 Number of Bedrooms:",
                ["1BHK", "2BHK", "3BHK"],
                index=0
            )
        
        # Appliances Section
        st.markdown("""
        <div class="section-header">
            <h3>🔌 Appliances</h3>
        </div>
        """, unsafe_allow_html=True)
        
        with st.container():
            col_ac, col_fridge, col_wm = st.columns(3)
            
            with col_ac:
                ac = st.checkbox("❄️ Air Conditioner", value=False)
            with col_fridge:
                fridge = st.checkbox("🧊 Refrigerator", value=True)
            with col_wm:
                wm = st.checkbox("🧺 Washing Machine", value=False)
        
        # Calculate button
        if st.button("⚡ Calculate Energy Consumption", type="primary", use_container_width=True):
            if name and city and area:
                # Energy calculation logic
                cal_energy = 0
                
                # Base consumption based on BHK
                if facility == "1BHK":
                    cal_energy += 2 * 0.4 + 2 * 0.8  # 2.4 kW
                elif facility == "2BHK":
                    cal_energy += 3 * 0.4 + 3 * 0.8  # 3.6 kW
                elif facility == "3BHK":
                    cal_energy += 4 * 0.4 + 4 * 0.8  # 4.8 kW
                
                # Additional appliances
                if ac:
                    cal_energy += 3
                if fridge:
                    cal_energy += 3
                if wm:
                    cal_energy += 3
                
                # Store results in session state
                st.session_state.calculated = True
                st.session_state.energy_data = {
                    'name': name,
                    'age': age,
                    'city': city,
                    'area': area,
                    'residence_type': flat_tenament,
                    'facility': facility,
                    'ac': ac,
                    'fridge': fridge,
                    'washing_machine': wm,
                    'total_energy': cal_energy,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                st.success("✅ Energy consumption calculated successfully!")
            else:
                st.error("⚠️ Please fill in all required fields (Name, City, Area)")
    
    with col2:
        # Information panel
        st.markdown("""
        <div class="info-box">
            <h4>💡 How it works</h4>
            <p>Our calculator estimates your home's energy consumption based on:</p>
            <ul>
                <li>Number of bedrooms</li>
                <li>Major appliances usage</li>
                <li>Standard consumption patterns</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick stats
        if st.session_state.calculated:
            data = st.session_state.energy_data
            st.markdown(f"""
            <div class="metric-card">
                <h3>📊 Your Profile</h3>
                <p><strong>Name:</strong> {data['name']}</p>
                <p><strong>Location:</strong> {data['city']}, {data['area']}</p>
                <p><strong>Home:</strong> {data['facility']} {data['residence_type']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Results section
    if st.session_state.calculated:
        data = st.session_state.energy_data
        
        st.markdown("---")
        st.markdown("""
        <div class="section-header">
            <h3>⚡ Energy Consumption Results</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Main result display
        st.markdown(f"""
        <div class="energy-result">
            <h2>🏠 Total Energy Consumption</h2>
            <h1 style="font-size: 4rem; margin: 20px 0;">{data['total_energy']:.1f} kW</h1>
            <p>Estimated daily consumption for your {data['facility']} home</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Breakdown
        col1, col2, col3, col4 = st.columns(4)
        
        base_energy = 2.4 if data['facility'] == "1BHK" else 3.6 if data['facility'] == "2BHK" else 4.8
        
        with col1:
            st.metric("🏠 Base Consumption", f"{base_energy} kW", f"{data['facility']}")
        with col2:
            st.metric("❄️ AC", f"{3 if data['ac'] else 0} kW", "Active" if data['ac'] else "Inactive")
        with col3:
            st.metric("🧊 Fridge", f"{3 if data['fridge'] else 0} kW", "Active" if data['fridge'] else "Inactive")
        with col4:
            st.metric("🧺 Washing Machine", f"{3 if data['wm'] else 0} kW", "Active" if data['wm'] else "Inactive")

elif page == "📈 Energy Analysis":
    st.markdown("""
    <div class="section-header">
        <h3>📈 Energy Analysis Dashboard</h3>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.calculated:
        data = st.session_state.energy_data
        
        # Create visualization
        col1, col2 = st.columns(2)
        
        with col1:
            # Pie chart for energy breakdown
            labels = ['Base Consumption']
            values = [2.4 if data['facility'] == "1BHK" else 3.6 if data['facility'] == "2BHK" else 4.8]
            colors = ['#667eea']
            
            if data['ac']:
                labels.append('Air Conditioner')
                values.append(3)
                colors.append('#ff6b6b')
            if data['fridge']:
                labels.append('Refrigerator')
                values.append(3)
                colors.append('#4ecdc4')
            if data['washing_machine']:
                labels.append('Washing Machine')
                values.append(3)
                colors.append('#45b7d1')
            
            fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3)])
            fig_pie.update_traces(marker=dict(colors=colors))
            fig_pie.update_layout(
                title="Energy Consumption Breakdown",
                showlegend=True,
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Monthly projection
            daily_consumption = data['total_energy']
            monthly_data = {
                'Period': ['Daily', 'Weekly', 'Monthly', 'Yearly'],
                'Consumption (kW)': [daily_consumption, daily_consumption * 7, daily_consumption * 30, daily_consumption * 365],
                'Estimated Cost (₹)': [daily_consumption * 5, daily_consumption * 7 * 5, daily_consumption * 30 * 5, daily_consumption * 365 * 5]
            }
            
            fig_bar = px.bar(
                x=monthly_data['Period'],
                y=monthly_data['Consumption (kW)'],
                title="Energy Consumption Projection",
                color=monthly_data['Consumption (kW)'],
                color_continuous_scale='viridis'
            )
            fig_bar.update_layout(
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Cost estimation table
        st.markdown("""
        <div class="section-header">
            <h3>💰 Cost Estimation</h3>
        </div>
        """, unsafe_allow_html=True)
        
        df = pd.DataFrame(monthly_data)
        st.dataframe(df, use_container_width=True)
        
    else:
        st.info("📊 Please calculate your energy consumption first to view the analysis.")

elif page == "💡 Tips & Info":
    st.markdown("""
    <div class="section-header">
        <h3>💡 Energy Saving Tips & Information</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="info-box">
            <h4>🏠 Home Energy Tips</h4>
            <ul>
                <li>Use LED bulbs to reduce lighting consumption</li>
                <li>Set AC temperature to 24°C for optimal efficiency</li>
                <li>Unplug electronics when not in use</li>
                <li>Use natural light during daytime</li>
                <li>Regular maintenance of appliances</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box">
            <h4>❄️ AC Efficiency Tips</h4>
            <ul>
                <li>Clean filters regularly</li>
                <li>Use ceiling fans to circulate air</li>
                <li>Seal doors and windows properly</li>
                <li>Use timer function wisely</li>
                <li>Consider inverter AC for better efficiency</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-box">
            <h4>🧊 Refrigerator Tips</h4>
            <ul>
                <li>Keep refrigerator at 37-40°F</li>
                <li>Don't overfill or underfill</li>
                <li>Check door seals regularly</li>
                <li>Allow hot food to cool before storing</li>
                <li>Clean coils periodically</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box">
            <h4>📊 Understanding Your Bill</h4>
            <ul>
                <li>1 kW = 1000 watts</li>
                <li>Average cost: ₹5-8 per kWh</li>
                <li>Peak hours typically cost more</li>
                <li>Solar panels can reduce bills by 70-90%</li>
                <li>Energy-efficient appliances save money long-term</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: rgba(255, 255, 255, 0.6); margin-top: 30px;">
    <p>⚡ Energy Consumption Calculator | Built with Streamlit | © 2024</p>
    <p>💡 Save energy, save money, save the planet!</p>
</div>
""", unsafe_allow_html=True)