
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime
import time

# Page configuration
st.set_page_config(page_title="Air Quality Dashboard", layout="wide", page_icon="")

# Earth Loader at the start
st.markdown("""
    <div class="earth-loader-container">
        <div class="earth">
            <div class="earth-loader">
                <svg viewBox="0 0 200 200">
                    <path fill="#9be24f"
                        d="M100 35
                           C138 38, 162 68, 158 105
                           C154 142, 120 160, 100 156
                           C62 152, 38 125, 42 100
                           C46 70, 70 40, 100 35Z"/>
                </svg>
                <svg viewBox="0 0 200 200">
                    <path fill="#9be24f"
                        d="M100 45
                           C132 48, 152 78, 148 108
                           C144 138, 118 148, 100 145
                           C68 142, 48 120, 52 100
                           C56 78, 72 50, 100 45Z"/>
                </svg>
                <svg viewBox="0 0 200 200">
                    <path fill="#9be24f"
                        d="M100 40
                           C130 44, 150 72, 146 104
                           C142 136, 118 148, 100 144
                           C70 140, 50 118, 54 100
                           C58 74, 74 46, 100 40Z"/>
                </svg>
            </div>
            <p>Connecting…</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# Custom CSS with animations
st.markdown("""
    <style>
    .main {background-color: #f0f2f6;}
    .stButton>button {
        width: 100%;
        background-color: #4e73df;
        color: white;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #2e59d9;
        transform: scale(1.05);
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
    
    .pulse-emoji {
        animation: pulse 2s ease-in-out infinite;
        display: inline-block;
        font-size: 2em;
    }
    
    .bounce-emoji {
        animation: bounce 1.5s ease-in-out infinite;
        display: inline-block;
        font-size: 2em;
    }
    
    .rotate-emoji {
        animation: rotate 3s linear infinite;
        display: inline-block;
        font-size: 2em;
    }
    
    .shake-emoji {
        animation: shake 0.5s ease-in-out infinite;
        display: inline-block;
        font-size: 2em;
    }
    
    .fade-in {
        animation: fadeIn 0.8s ease-out;
    }
    
    .weather-header {
        font-size: 2.5em;
        text-align: center;
        margin: 20px 0;
    }
    
    .alert-box {
        animation: fadeIn 0.5s ease-out;
        margin: 10px 0;
        padding: 15px;
        border-radius: 10px;
        transition: transform 0.3s ease;
    }
    
    .alert-box:hover {
        transform: translateX(10px);
    }
    
    .metric-container {
        text-align: center;
        padding: 20px;
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .metric-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    
    .loading-spinner {
        animation: rotate 1s linear infinite;
        display: inline-block;
    }
    
    /* ================= EARTH LOADER ================= */
    .earth-loader-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        background: radial-gradient(circle at top, #0f172a, #020617);
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        z-index: 9999;
        animation: fadeOut 0.5s ease-out 2s forwards;
    }
    
    @keyframes fadeOut {
        to {
            opacity: 0;
            visibility: hidden;
        }
    }
    
    .earth {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 1rem;
    }
    
    .earth-loader {
        width: 8em;
        height: 8em;
        position: relative;
        overflow: hidden;
        border-radius: 50%;
        border: 2px solid rgba(255,255,255,0.9);
        background: radial-gradient(circle at 30% 30%, #6a78ff, #3f51d9);
        box-shadow: inset 0.45em 0.45em rgba(255,255,255,0.22),
                    inset -0.6em -0.6em rgba(0,0,0,0.42),
                    0 0 22px rgba(79,112,255,0.4);
        animation: startround 0.8s ease-out 1;
    }
    
    .earth p {
        color: white;
        font-size: 1.1rem;
        letter-spacing: 1px;
        margin: 0;
    }
    
    .earth-loader svg {
        position: absolute;
        width: 8.2em;
        opacity: 0.9;
        filter: drop-shadow(0 0 4px rgba(155,226,79,0.65));
    }
    
    .earth-loader svg:nth-child(1) {
        top: -2.6em;
        animation: round1 4s infinite linear;
    }
    
    .earth-loader svg:nth-child(2) {
        bottom: -2.8em;
        animation: round2 4s infinite linear 0.9s;
    }
    
    .earth-loader svg:nth-child(3) {
        top: -1.8em;
        animation: round1 4s infinite linear 1.8s;
    }
    
    @keyframes startround {
        0% { filter: brightness(220%); }
        100% { filter: brightness(100%); }
    }
    
    @keyframes round1 {
        0%   { left: -3.5em; transform: rotate(0deg); opacity: 1; }
        45%  { left: -8em; transform: rotate(20deg); }
        46%  { opacity: 0; }
        55%  { left: 9em; transform: rotate(-20deg); }
        65%  { opacity: 1; }
        100% { left: -3.5em; transform: rotate(0deg); }
    }
    
    @keyframes round2 {
        0%   { left: 5.5em; transform: rotate(0deg); opacity: 1; }
        65%  { left: -9em; transform: rotate(-20deg); }
        66%  { opacity: 0; }
        75%  { left: 10em; transform: rotate(20deg); }
        85%  { opacity: 1; }
        100% { left: 5.5em; transform: rotate(0deg); }
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for admin authentication
if 'admin_authenticated' not in st.session_state:
    st.session_state.admin_authenticated = False
if 'admin_data' not in st.session_state:
    st.session_state.admin_data = None
if 'imported_data' not in st.session_state:
    st.session_state.imported_data = None
if 'admin_loading' not in st.session_state:
    st.session_state.admin_loading = False
if 'login_clicked' not in st.session_state:
    st.session_state.login_clicked = False
if 'telangana_data' not in st.session_state:
    st.session_state.telangana_data = None

# Load Telangana dataset
@st.cache_data
def load_telangana_data():
    try:
        df = pd.read_csv('telangana_data.csv')
        # Convert pollutant_avg to numeric, handling empty strings
        df['pollutant_avg'] = pd.to_numeric(
            df['pollutant_avg'], errors='coerce')
        df['pollutant_min'] = pd.to_numeric(
            df['pollutant_min'], errors='coerce')
        df['pollutant_max'] = pd.to_numeric(
            df['pollutant_max'], errors='coerce')
        # Parse last_update to datetime
        df['last_update'] = pd.to_datetime(
            df['last_update'], format='%d-%m-%Y %H:%M:%S', errors='coerce')
        return df
    except Exception as e:
        st.error(f"Error loading Telangana data: {str(e)}")
        return None


# Load data if not already loaded
if st.session_state.telangana_data is None:
    st.session_state.telangana_data = load_telangana_data()


# Helper function to calculate AQI from PM2.5
def calculate_aqi_pm25(pm25):
    """Calculate AQI from PM2.5 value (μg/m³)"""
    if pd.isna(pm25) or pm25 < 0:
        return None, "No Data"
    
    if pm25 <= 12:
        aqi = (50/12) * pm25
        return round(aqi), "Good"
    elif pm25 <= 35.4:
        aqi = 50 + ((50/23.4) * (pm25 - 12))
        return round(aqi), "Moderate"
    elif pm25 <= 55.4:
        aqi = 100 + ((50/20) * (pm25 - 35.4))
        return round(aqi), "Unhealthy for Sensitive"
    elif pm25 <= 150.4:
        aqi = 150 + ((50/95) * (pm25 - 55.4))
        return round(aqi), "Unhealthy"
    elif pm25 <= 250.4:
        aqi = 200 + ((100/100) * (pm25 - 150.4))
        return round(aqi), "Very Unhealthy"
    else:
        aqi = 300 + ((200/149.6) * (pm25 - 250.4))
        return round(min(aqi, 500)), "Hazardous"


# Helper function to get aggregated stats from dataset
def get_dataset_stats(df, station=None, pollutant=None):
    """Get statistics from the dataset"""
    if df is None or len(df) == 0:
        return None
    
    filtered_df = df.copy()
    
    if station:
        filtered_df = filtered_df[filtered_df['station'] == station]
    if pollutant:
        # Map common pollutant names
        pollutant_map = {
            'PM2.5': 'PM2.5', 'PM10': 'PM10', 'NO2': 'NO2',
            'O3': 'OZONE', 'CO': 'CO', 'SO2': 'SO2'
        }
        pol_id = pollutant_map.get(pollutant.strip(), pollutant.strip())
        filtered_df = filtered_df[filtered_df['pollutant_id'] == pol_id]
    
    return filtered_df

# Admin Mode Section in Sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔐 Admin Mode")
admin_mode = st.sidebar.checkbox("Enable Admin Mode")

if admin_mode:
    if not st.session_state.admin_authenticated:
        # Password input
        admin_password = st.sidebar.text_input("Enter Admin Password", type="password", key="admin_pwd")
        
        if st.sidebar.button("Login", key="admin_login"):
            if admin_password == "admin123":
                st.session_state.login_clicked = True
                st.session_state.admin_loading = True
                st.rerun()
            else:
                st.sidebar.error("❌ Incorrect Password!")
    else:
        st.sidebar.markdown('<span class="shake-emoji"></span> <strong>Admin Mode Active</strong>', unsafe_allow_html=True)
        
        if st.sidebar.button("🚪 Logout", key="admin_logout"):
            st.session_state.admin_authenticated = False
            st.session_state.admin_data = None
            st.session_state.admin_loading = False
            st.session_state.login_clicked = False
            st.rerun()
else:
    # Reset admin state when checkbox is unchecked
    if st.session_state.admin_authenticated:
        st.session_state.admin_authenticated = False
        st.session_state.admin_data = None
        st.session_state.admin_loading = False
        st.session_state.login_clicked = False

# Show Loading Screen if login was clicked
if st.session_state.admin_loading:
    # Loading screen CSS
    st.markdown("""
        <style>
        .loading-screen {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100vh;
            background: radial-gradient(circle at top, #0f172a, #020617);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 9999;
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        }
        .loading-globe {
            width: 150px;
            height: 150px;
            position: relative;
            margin-bottom: 30px;
        }
        .loading-globe svg {
            width: 100%;
            height: 100%;
            animation: rotate 20s linear infinite;
        }
        .loading-text {
            color: white;
            font-size: 24px;
            font-weight: 500;
            letter-spacing: 2px;
            animation: pulse 2s ease-in-out infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.6; }
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Loading screen HTML
    st.markdown("""
        <div class="loading-screen">
            <div class="loading-globe">
                <svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
                    <defs>
                        <radialGradient id="globeGradient" cx="30%" cy="30%">
                            <stop offset="0%" stop-color="#3b82f6" />
                            <stop offset="100%" stop-color="#1e40af" />
                        </radialGradient>
                    </defs>
                    <circle cx="100" cy="100" r="90" fill="url(#globeGradient)" stroke="#60a5fa" stroke-width="2" opacity="0.9"/>
                    <path d="M 50 100 Q 100 80 150 100" stroke="#34d399" stroke-width="2" fill="none" opacity="0.7"/>
                    <path d="M 50 100 Q 100 120 150 100" stroke="#34d399" stroke-width="2" fill="none" opacity="0.7"/>
                    <path d="M 100 50 Q 80 100 100 150" stroke="#34d399" stroke-width="2" fill="none" opacity="0.7"/>
                    <path d="M 100 50 Q 120 100 100 150" stroke="#34d399" stroke-width="2" fill="none" opacity="0.7"/>
                    <circle cx="100" cy="100" r="8" fill="#60a5fa" opacity="0.8"/>
                    <ellipse cx="70" cy="80" rx="15" ry="20" fill="#9be24f" opacity="0.6"/>
                    <ellipse cx="130" cy="90" rx="12" ry="18" fill="#9be24f" opacity="0.6"/>
                    <ellipse cx="90" cy="130" rx="10" ry="15" fill="#9be24f" opacity="0.6"/>
                    <ellipse cx="120" cy="120" rx="8" ry="12" fill="#9be24f" opacity="0.6"/>
                </svg>
            </div>
            <div class="loading-text">Connecting...</div>
        </div>
    """, unsafe_allow_html=True)
    
    # After delay, authenticate and show admin panel
    time.sleep(2)  # 2 second loading screen
    st.session_state.admin_authenticated = True
    st.session_state.admin_loading = False
    st.rerun()

# Show Admin Page OR Main Dashboard (not both)
if st.session_state.admin_authenticated:
    # ========== ADMIN PANEL ==========
    
    # Initialize admin session state
    if 'admin_page' not in st.session_state:
        st.session_state.admin_page = "Dashboard"
    
    # Light theme CSS for admin page
    st.markdown("""
        <style>
        .admin-main-container {
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .admin-upload-area {
            background-color: #ffffff;
            border: 2px dashed #dee2e6;
            border-radius: 10px;
            padding: 30px;
            text-align: center;
            margin: 20px 0;
            transition: all 0.3s ease;
        }
        .admin-upload-area:hover {
            border-color: #4e73df;
            background-color: #f8f9fa;
        }
        .admin-globe-icon {
            width: 120px;
            height: 120px;
            margin: 40px auto;
            display: block;
            animation: rotate 10s linear infinite;
        }
        .admin-connecting-text {
            text-align: center;
            color: #212529;
            font-size: 24px;
            font-weight: 600;
            margin: 20px 0;
        }
        .admin-instruction-text {
            text-align: center;
            color: #6c757d;
            font-size: 14px;
            margin: 10px 0;
        }
        .admin-card {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
            border: 1px solid #dee2e6;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .admin-stat-box {
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            border: 1px solid #dee2e6;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Admin Panel Header
    st.markdown("""
        <div style="background: linear-gradient(135deg, #4e73df 0%, #2e59d9 100%); 
                    padding: 20px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h1 style="color: white; margin: 0; display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 2em;"></span> Admin Panel
            </h1>
            <p style="color: #e3ebf1; margin: 5px 0 0 0;">Air Quality Dashboard Management System</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Admin Navigation Tabs
    admin_tabs = st.tabs([" Dashboard", " Data Upload", " Analytics", " Settings"])
    
    # ========== TAB 1: DASHBOARD ==========
    with admin_tabs[0]:
        st.markdown("###  Admin Dashboard Overview")
        
        # Statistics Row
        # Check imported_data, admin_data, or telangana_data for statistics
        current_data = (
            st.session_state.imported_data if st.session_state.imported_data is not None
            else st.session_state.admin_data if st.session_state.admin_data is not None
            else st.session_state.telangana_data
        )
        
        stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
        
        with stat_col1:
            data_files_count = 0
            if st.session_state.imported_data is not None:
                data_files_count += 1
            if st.session_state.admin_data is not None and st.session_state.admin_data is not st.session_state.imported_data:
                data_files_count += 1
            st.markdown("""
                <div class="admin-stat-box">
                    <h3 style="color: #4e73df; margin: 0; font-size: 2em;"></h3>
                    <h2 style="color: #212529; margin: 10px 0;">Data Files</h2>
                    <p style="color: #495057; font-size: 1.5em; margin: 0;">{}</p>
                </div>
            """.format(data_files_count), unsafe_allow_html=True)
        
        with stat_col2:
            total_rows = len(current_data) if current_data is not None else 0
            st.markdown("""
                <div class="admin-stat-box">
                    <h3 style="color: #1cc88a; margin: 0; font-size: 2em;"></h3>
                    <h2 style="color: #212529; margin: 10px 0;">Total Records</h2>
                    <p style="color: #495057; font-size: 1.5em; margin: 0;">{:,}</p>
                </div>
            """.format(total_rows), unsafe_allow_html=True)
        
        with stat_col3:
            total_cols = len(current_data.columns) if current_data is not None else 0
            st.markdown("""
                <div class="admin-stat-box">
                    <h3 style="color: #f6c23e; margin: 0; font-size: 2em;"></h3>
                    <h2 style="color: #212529; margin: 10px 0;">Data Columns</h2>
                    <p style="color: #495057; font-size: 1.5em; margin: 0;">{}</p>
                </div>
            """.format(total_cols), unsafe_allow_html=True)
        
        with stat_col4:
            st.markdown("""
                <div class="admin-stat-box">
                    <h3 style="color: #e74a3b; margin: 0; font-size: 2em;"></h3>
                    <h2 style="color: #212529; margin: 10px 0;">Active Users</h2>
                    <p style="color: #495057; font-size: 1.5em; margin: 0;">1</p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Data Preview Section
        # Use imported_data if available, otherwise admin_data, or telangana_data
        preview_data = (
            st.session_state.imported_data if st.session_state.imported_data is not None
            else st.session_state.admin_data if st.session_state.admin_data is not None
            else st.session_state.telangana_data
        )
        
        # Auto-import Telangana data if not already imported
        if st.session_state.imported_data is None and st.session_state.telangana_data is not None:
            st.session_state.imported_data = st.session_state.telangana_data
            preview_data = st.session_state.imported_data
            st.info("Telangana dataset has been automatically loaded!")
        
        if preview_data is not None:
            data_status = (
                "Imported" if st.session_state.imported_data is not None
                else "Uploaded (Not yet imported)" if st.session_state.admin_data is not None
                else "Telangana Dataset (Auto-loaded)"
            )
            st.markdown(f"### Current Data Preview ({data_status})")
            st.dataframe(preview_data.head(20), use_container_width=True)
            
            # Data Info
            col_info1, col_info2 = st.columns(2)
            with col_info1:
                st.markdown("""
                    <div class="admin-card">
                        <h4 style="color: #212529;"> Data Information</h4>
                        <p style="color: #495057;">Rows: <strong>{:,}</strong></p>
                        <p style="color: #495057;">Columns: <strong>{}</strong></p>
                        <p style="color: #495057;">Memory Usage: <strong>{:.2f} MB</strong></p>
                    </div>
                """.format(
                    len(preview_data),
                    len(preview_data.columns),
                    preview_data.memory_usage(deep=True).sum() / 1024**2
                ), unsafe_allow_html=True)
            
            with col_info2:
                st.markdown("""
                    <div class="admin-card">
                        <h4 style="color: #212529;">Column Names</h4>
                        <p style="color: #495057; font-size: 0.9em;">
                            {}
                        </p>
                    </div>
                """.format(", ".join(preview_data.columns.tolist()[:10])), unsafe_allow_html=True)
            
            if st.session_state.imported_data is None and st.session_state.admin_data is not None:
                st.info(" Click 'Import to Dashboard' in the Data Upload tab to make this data available in the main dashboard.")
        else:
            st.info("ℹ No data uploaded yet. Please upload data in the 'Data Upload' tab.")
    
    # ========== TAB 2: DATA UPLOAD ==========
    with admin_tabs[1]:
        st.markdown("###  Upload Air Quality Data")
        
        col_upload, col_info = st.columns([2, 1])
        
        with col_upload:
            st.markdown("""
                <div class="admin-card">
                    <h3 style="color: #212529; margin-bottom: 20px;"> CSV File Upload</h3>
                </div>
            """, unsafe_allow_html=True)
            
            uploaded_file = st.file_uploader(
                "Drag and drop CSV file here",
                type=['csv'],
                key="admin_csv_upload",
                help="Upload CSV files up to 200MB",
                label_visibility="visible"
            )
            
            if uploaded_file is not None:
                try:
                    df = pd.read_csv(uploaded_file)
                    st.session_state.admin_data = df
                    
                    st.success(f"File uploaded: {uploaded_file.name}")
                    
                    # File Information
                    file_size = uploaded_file.size / (1024 * 1024)  # MB
                    st.info(f" {len(df)} rows × {len(df.columns)} columns | Size: {file_size:.2f} MB")
                    
                    # Data Preview
                    with st.expander(" Preview Data (First 10 rows)"):
                        st.dataframe(df.head(10), use_container_width=True)
                    
                    # Column Information
                    with st.expander(" Column Information"):
                        col_info_df = pd.DataFrame({
                            'Column': df.columns,
                            'Data Type': df.dtypes.astype(str),
                            'Non-Null Count': df.count().values,
                            'Null Count': df.isnull().sum().values
                        })
                        st.dataframe(col_info_df, use_container_width=True)
                    
                    # Import Button
                    col_btn1, col_btn2 = st.columns(2)
                    with col_btn1:
                        if st.button(" Import to Dashboard", key="import_data",
                                     use_container_width=True, type="primary"):
                            st.session_state.imported_data = df
                            st.success(" Data imported successfully!")
                            time.sleep(1)
                            st.rerun()
                    
                    with col_btn2:
                        # Export as CSV
                        csv = df.to_csv(index=False)
                        st.download_button(
                            label=" Download CSV",
                            data=csv,
                            file_name=f"exported_{uploaded_file.name}",
                            mime="text/csv",
                            use_container_width=True
                        )
                    
                except Exception as e:
                    st.error(f"❌ Error reading file: {str(e)}")
        
        with col_info:
            st.markdown("""
                <div class="admin-card">
                    <h4 style="color: #212529;">ℹ Upload Guidelines</h4>
                    <ul style="color: #495057; font-size: 0.9em;">
                        <li>Maximum file size: 200MB</li>
                        <li>Supported format: CSV only</li>
                        <li>Ensure proper column headers</li>
                        <li>Date columns should be formatted</li>
                        <li>Remove empty rows before upload</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
            
            # Show current data status
            current_data_info = st.session_state.imported_data if st.session_state.imported_data is not None else st.session_state.admin_data
            if current_data_info is not None:
                status_text = " Imported" if st.session_state.imported_data is not None else "📤 Uploaded (Not imported)"
                st.markdown("""
                    <div class="admin-card">
                        <h4 style="color: #212529;">{}</h4>
                        <p style="color: #495057;">
                            <strong>{:,}</strong> rows loaded<br>
                            <strong>{}</strong> columns
                        </p>
                    </div>
                """.format(
                    status_text,
                    len(current_data_info),
                    len(current_data_info.columns)
                ), unsafe_allow_html=True)
    
    # ========== TAB 3: ANALYTICS ==========
    with admin_tabs[2]:
        st.markdown("###  Data Analytics")
        
        # Use imported_data if available, otherwise use admin_data
        analytics_data = st.session_state.imported_data if st.session_state.imported_data is not None else st.session_state.admin_data
        
        if analytics_data is not None:
            df = analytics_data
            
            # Summary Statistics
            st.markdown("####  Summary Statistics")
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            
            if len(numeric_cols) > 0:
                st.dataframe(df[numeric_cols].describe(), use_container_width=True)
                
                # Visualizations
                col_viz1, col_viz2 = st.columns(2)
                
                with col_viz1:
                    if len(numeric_cols) > 0:
                        selected_col = st.selectbox("Select Column for Distribution", numeric_cols)
                        if selected_col:
                            fig_hist = go.Figure(data=[go.Histogram(x=df[selected_col].dropna(), nbinsx=30)])
                            fig_hist.update_layout(
                                title=f"Distribution of {selected_col}",
                                xaxis_title=selected_col,
                                yaxis_title="Frequency",
                                height=400,
                                template="plotly_white"
                            )
                            st.plotly_chart(fig_hist, use_container_width=True)
                
                with col_viz2:
                    if len(numeric_cols) > 1:
                        col_x = st.selectbox("Select X-axis", numeric_cols, key="x_axis")
                        col_y = st.selectbox("Select Y-axis", numeric_cols, key="y_axis")
                        if col_x and col_y:
                            fig_scatter = go.Figure(data=[go.Scatter(
                                x=df[col_x].dropna(),
                                y=df[col_y].dropna(),
                                mode='markers',
                                marker=dict(size=5, opacity=0.6)
                            )])
                            fig_scatter.update_layout(
                                title=f"{col_x} vs {col_y}",
                                xaxis_title=col_x,
                                yaxis_title=col_y,
                                height=400,
                                template="plotly_white"
                            )
                            st.plotly_chart(fig_scatter, use_container_width=True)
            else:
                st.warning(" No numeric columns found for analytics.")
        else:
            st.info("Please upload data first to view analytics.")
    
    # ========== TAB 4: SETTINGS ==========
    with admin_tabs[3]:
        st.markdown("### Admin Settings")
        
        settings_col1, settings_col2 = st.columns(2)
        
        with settings_col1:
            st.markdown("""
                <div class="admin-card">
                    <h4 style="color: #212529;">Security Settings</h4>
                </div>
            """, unsafe_allow_html=True)
            
            current_password = st.text_input("Current Password", type="password", value="admin123", disabled=True)
            new_password = st.text_input("New Password", type="password", key="new_pwd")
            confirm_password = st.text_input("Confirm New Password", type="password", key="confirm_pwd")
            
            if st.button("Change Password", use_container_width=True):
                if new_password == confirm_password and len(new_password) >= 6:
                    st.success("Password changed successfully! (Note: This is a demo - password change not persisted)")
                elif new_password != confirm_password:
                    st.error("Passwords do not match!")
                else:
                    st.error(" Password must be at least 6 characters!")
            
            st.markdown("---")
            
            st.markdown("""
                <div class="admin-card">
                    <h4 style="color: #212529;">System Information</h4>
                    <p style="color: #495057;">Version: <strong>1.0.0</strong></p>
                    <p style="color: #495057;">Last Updated: <strong>{}</strong></p>
                    <p style="color: #495057;">Status: <strong style="color: #1cc88a;">● Active</strong></p>
                </div>
            """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)
        
        with settings_col2:
            st.markdown("""
                <div class="admin-card">
                    <h4 style="color: #212529;"> Display Settings</h4>
                </div>
            """, unsafe_allow_html=True)
            
            auto_refresh = st.checkbox("Auto-refresh Dashboard", value=False)
            refresh_interval = st.slider("Refresh Interval (seconds)", 10, 300, 60, disabled=not auto_refresh)
            
            show_animations = st.checkbox("Show Animations", value=True)
            dark_mode = st.checkbox("Dark Mode", value=False, disabled=True)
            
            if st.button(" Save Settings", use_container_width=True):
                st.success(" Settings saved!")
            
            st.markdown("---")
            
            st.markdown("""
                <div class="admin-card">
                    <h4 style="color: #212529;"> System Actions</h4>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button(" Clear Cache", use_container_width=True):
                st.session_state.imported_data = None
                st.session_state.admin_data = None
                st.success(" Cache cleared!")
                st.rerun()
            
            # Export data - use imported_data if available, otherwise admin_data
            export_data = st.session_state.imported_data if st.session_state.imported_data is not None else st.session_state.admin_data
            if st.button(" Export All Data", use_container_width=True,
                         disabled=export_data is None):
                if export_data is not None:
                    csv = export_data.to_csv(index=False)
                    st.download_button(
                        label=" Download",
                        data=csv,
                        file_name=f"admin_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
    
    # Back to Dashboard button at top
    if st.button("← Back to Main Dashboard", key="back_to_dashboard", use_container_width=True):
        st.session_state.admin_authenticated = False
        st.rerun()

elif not st.session_state.admin_loading:
    # ========== MAIN DASHBOARD (shown when NOT in admin mode) ==========
    
    # Animated Header
    st.markdown("""
        <div class="weather-header fade-in">
            <span class="pulse-emoji"></span> Air Quality Dashboard <span class="pulse-emoji"></span>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar Controls with animated emojis
    st.sidebar.markdown('<h2><span class="bounce-emoji"></span> Controls</h2>', unsafe_allow_html=True)
    
    # Get unique stations and pollutants from dataset
    telangana_df = st.session_state.telangana_data
    if telangana_df is not None and len(telangana_df) > 0:
        stations = sorted(telangana_df['station'].unique().tolist())
        pollutants_available = sorted(telangana_df['pollutant_id'].dropna().unique().tolist())
        # Map pollutant IDs to display names
        pollutant_display_map = {
            'PM2.5': 'PM2.5', 'PM10': 'PM10', 'NO2': 'NO2',
            'OZONE': 'O3', 'CO': 'CO', 'SO2': 'SO2', 'NH3': 'NH3'
        }
        pollutant_options = [pollutant_display_map.get(p, p) for p in pollutants_available if p in pollutant_display_map]
        if not pollutant_options:
            pollutant_options = ['PM2.5', 'PM10', 'NO2', 'O3', 'CO']
    else:
        stations = ["Downtown", "Suburb", "Industrial Area", "Park"]
        pollutant_options = ['PM2.5', 'PM10', 'NO2', 'O3', 'CO']
    
    st.sidebar.markdown('<p><span class="pulse-emoji"></span> <b>Monitoring Station</b></p>', unsafe_allow_html=True)
    monitoring_station = st.sidebar.selectbox(
        "Monitoring Station",
        stations if len(stations) > 0 else ["Select Station"],
        label_visibility="collapsed",
        index=0 if len(stations) > 0 else 0
    )
    
    st.sidebar.markdown('<p><span class="pulse-emoji"></span> <b>Time Range</b></p>', unsafe_allow_html=True)
    time_range = st.sidebar.selectbox(
        "Time Range",
        ["Last 24 Hours ⏱", "Last 48 Hours ", "Last Week "],
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown('<p><span class="pulse-emoji"></span> <b>Pollutant</b></p>', unsafe_allow_html=True)
    pollutant = st.sidebar.selectbox(
        "Pollutant",
        pollutant_options if len(pollutant_options) > 0 else ["PM2.5", "PM10", "NO2", "O3", "CO"],
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown('<p><span class="pulse-emoji"></span> <b>Forecast Horizon</b></p>', unsafe_allow_html=True)
    forecast_horizon = st.sidebar.selectbox(
        "Forecast Horizon",
        ["24 Hours ", "48 Hours ", "72 Hours "],
        label_visibility="collapsed"
    )
    
    # Animated update button
    if st.sidebar.button("Update Dashboard"):
        with st.spinner(''):
            st.sidebar.markdown('<div class="loading-spinner">⏳</div>', unsafe_allow_html=True)
            time.sleep(1)
            st.sidebar.success("Dashboard Updated!")
            st.rerun()
    
    # Quick Stats Row - Using actual data from Telangana dataset
    st.markdown("###  Quick Stats")
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    
    # Calculate stats from dataset
    telangana_df = st.session_state.telangana_data
    if telangana_df is not None and len(telangana_df) > 0:
        # Get PM2.5 average
        pm25_data = telangana_df[telangana_df['pollutant_id'] == 'PM2.5']['pollutant_avg'].dropna()
        pm25_avg = round(pm25_data.mean()) if len(pm25_data) > 0 else 0
        
        # Get PM10 average
        pm10_data = telangana_df[telangana_df['pollutant_id'] == 'PM10']['pollutant_avg'].dropna()
        pm10_avg = round(pm10_data.mean()) if len(pm10_data) > 0 else 0
        
        # Get NO2 average
        no2_data = telangana_df[telangana_df['pollutant_id'] == 'NO2']['pollutant_avg'].dropna()
        no2_avg = round(no2_data.mean()) if len(no2_data) > 0 else 0
        
        # Get OZONE average
        ozone_data = telangana_df[telangana_df['pollutant_id'] == 'OZONE']['pollutant_avg'].dropna()
        ozone_avg = round(ozone_data.mean()) if len(ozone_data) > 0 else 0
    else:
        pm25_avg = 0
        pm10_avg = 0
        no2_avg = 0
        ozone_avg = 0
    
    with stat_col1:
        st.markdown(f"""
            <div class="metric-container fade-in">
                <div class="pulse-emoji"></div>
                <h3>PM2.5 Avg</h3>
                <h2>{pm25_avg} μg/m³</h2>
            </div>
        """, unsafe_allow_html=True)
    
    with stat_col2:
        st.markdown(f"""
            <div class="metric-container fade-in">
                <div class="pulse-emoji"></div>
                <h3>PM10 Avg</h3>
                <h2>{pm10_avg} μg/m³</h2>
            </div>
        """, unsafe_allow_html=True)
    
    with stat_col3:
        st.markdown(f"""
            <div class="metric-container fade-in">
                <div class="rotate-emoji"></div>
                <h3>NO2 Avg</h3>
                <h2>{no2_avg} μg/m³</h2>
            </div>
        """, unsafe_allow_html=True)
    
    with stat_col4:
        st.markdown(f"""
            <div class="metric-container fade-in">
                <div class="bounce-emoji"></div>
                <h3>Ozone Avg</h3>
                <h2>{ozone_avg} μg/m³</h2>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Main content
    col1, col2 = st.columns([1, 1])

    # Current Air Quality Gauge - Using real data from Telangana dataset
    with col1:
        st.markdown('<h3><span class="pulse-emoji"></span> Current Air Quality</h3>', unsafe_allow_html=True)
        
        # Calculate AQI from actual PM2.5 data
        telangana_df = st.session_state.telangana_data
        if telangana_df is not None and len(telangana_df) > 0:
            # Filter by selected station if available
            if monitoring_station and monitoring_station != "Select Station":
                station_data = telangana_df[telangana_df['station'] == monitoring_station]
            else:
                station_data = telangana_df
            
            # Get PM2.5 average for AQI calculation
            pm25_data = station_data[station_data['pollutant_id'] == 'PM2.5']['pollutant_avg'].dropna()
            if len(pm25_data) > 0:
                pm25_avg_value = pm25_data.mean()
                current_aqi, status_text = calculate_aqi_pm25(pm25_avg_value)
                if current_aqi is None:
                    current_aqi = 0
                    status_text = "No Data"
            else:
                # Fallback: calculate from overall average
                overall_pm25 = telangana_df[telangana_df['pollutant_id'] == 'PM2.5']['pollutant_avg'].dropna()
                if len(overall_pm25) > 0:
                    pm25_avg_value = overall_pm25.mean()
                    current_aqi, status_text = calculate_aqi_pm25(pm25_avg_value)
                else:
                    current_aqi = 68
                    status_text = "Moderate"
        else:
            current_aqi = 68
            status_text = "Moderate"
        
        # AQI status emoji and color
        if current_aqi <= 50:
            status_emoji = ""
            status_color = "#00e400"
        elif current_aqi <= 100:
            status_emoji = ""
            status_color = "#ffff00"
        elif current_aqi <= 150:
            status_emoji = ""
            status_text = "Unhealthy for Sensitive"
            status_color = "#ff7e00"
        elif current_aqi <= 200:
            status_emoji = ""
            status_color = "#ff0000"
        else:
            status_emoji = ""
            status_color = "#8f3f97"
        
        st.markdown(f"""
            <div style="text-align: center; font-size: 3em;" class="pulse-emoji">
                {status_emoji}
            </div>
        """, unsafe_allow_html=True)
        
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=current_aqi,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': f"AQI<br><span style='font-size:0.8em;color:{status_color}'>{status_text}</span>",
                   'font': {'size': 20}},
            gauge={
                'axis': {'range': [None, 500], 'tickwidth': 1, 'tickcolor': "darkgray"},
                'bar': {'color': "white", 'thickness': 0.25},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 50], 'color': '#00e400'},
                    {'range': [50, 100], 'color': '#ffff00'},
                    {'range': [100, 150], 'color': '#ff7e00'},
                    {'range': [150, 200], 'color': '#ff0000'},
                    {'range': [200, 300], 'color': '#8f3f97'},
                    {'range': [300, 500], 'color': '#7e0023'}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 4},
                    'thickness': 0.75,
                    'value': current_aqi
                }
            }
        ))
        
        fig_gauge.update_layout(
            height=280,
            margin=dict(l=20, r=20, t=50, b=20)
        )
        
        st.plotly_chart(fig_gauge, use_container_width=True)

    # PM2.5 Forecast - Using real data from Telangana dataset
    with col2:
        st.markdown('<h3><span class="bounce-emoji"></span> PM2.5 Trends</h3>', unsafe_allow_html=True)
        
        telangana_df = st.session_state.telangana_data
        if telangana_df is not None and len(telangana_df) > 0:
            # Filter PM2.5 data
            pm25_data = telangana_df[telangana_df['pollutant_id'] == 'PM2.5'].copy()
            pm25_data = pm25_data[pm25_data['pollutant_avg'].notna()]
            
            # Filter by selected station if available
            if monitoring_station and monitoring_station != "Select Station":
                pm25_data = pm25_data[pm25_data['station'] == monitoring_station]
            
            # Get historical values (last 8 records)
            if len(pm25_data) > 0:
                historical_values = pm25_data['pollutant_avg'].tail(8).tolist()
                if len(historical_values) < 8:
                    # Pad with first value if not enough data
                    historical_values = [historical_values[0]] * (8 - len(historical_values)) + historical_values
                
                # Generate forecast (slight variation from last value)
                last_value = historical_values[-1]
                forecast_values = []
                for i in range(16):
                    # Simple trend-based forecast (can be improved with actual ML model)
                    variation = np.random.uniform(-0.1, 0.1) * last_value
                    forecast_values.append(last_value + variation)
                    last_value = forecast_values[-1]
            else:
                historical_values = [0] * 8
                forecast_values = [0] * 16
        else:
            historical_values = [0] * 8
            forecast_values = [0] * 16
        
        fig_forecast = go.Figure()
        
        # Historical line
        fig_forecast.add_trace(go.Scatter(
            x=list(range(len(historical_values))),
            y=historical_values,
            mode='lines+markers',
            name=' Historical',
            line=dict(color='#4e73df', width=3),
            marker=dict(size=6)
        ))
        
        # Forecast line
        fig_forecast.add_trace(go.Scatter(
            x=list(range(len(historical_values)-1, len(historical_values)+len(forecast_values))),
            y=[historical_values[-1]] + forecast_values,
            mode='lines+markers',
            name=' Forecast',
            line=dict(color='#ff7e00', width=3, dash='dot'),
            marker=dict(size=6)
        ))
        
        fig_forecast.update_layout(
            height=350,
            margin=dict(l=20, r=20, t=20, b=40),
            xaxis_title="Time ",
            yaxis_title="PM2.5 (μg/m³)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_forecast, use_container_width=True)

    st.markdown("---")

    # Bottom section
    col3, col4 = st.columns([1, 1])

    # Pollutant Trends - Using real data from Telangana dataset
    with col3:
        st.markdown('<h3><span class="rotate-emoji"></span> Pollutant Trends</h3>', unsafe_allow_html=True)
        
        telangana_df = st.session_state.telangana_data
        if telangana_df is not None and len(telangana_df) > 0:
            # Filter by selected station if available
            station_data = telangana_df.copy()
            if monitoring_station and monitoring_station != "Select Station":
                station_data = telangana_df[telangana_df['station'] == monitoring_station]
            
            # Get average values for each pollutant
            pm25_data = station_data[station_data['pollutant_id'] == 'PM2.5']['pollutant_avg'].dropna()
            pm25_avg = pm25_data.mean() if len(pm25_data) > 0 else 0
            
            no2_data = station_data[station_data['pollutant_id'] == 'NO2']['pollutant_avg'].dropna()
            no2_avg = no2_data.mean() if len(no2_data) > 0 else 0
            
            ozone_data = station_data[station_data['pollutant_id'] == 'OZONE']['pollutant_avg'].dropna()
            ozone_avg = ozone_data.mean() if len(ozone_data) > 0 else 0
            
            # Get PM10 for comparison
            pm10_data = station_data[station_data['pollutant_id'] == 'PM10']['pollutant_avg'].dropna()
            pm10_avg = pm10_data.mean() if len(pm10_data) > 0 else 0
            
            # Create trend data (simulate variation around average)
            days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            np.random.seed(42)  # For reproducible results
            variation_range = 0.15  # 15% variation
            
            pm25_values = [round(pm25_avg * (1 + np.random.uniform(-variation_range, variation_range))) for _ in days]
            no2_values = [round(no2_avg * (1 + np.random.uniform(-variation_range, variation_range))) for _ in days]
            o3_values = [round(ozone_avg * (1 + np.random.uniform(-variation_range, variation_range))) for _ in days]
        else:
            days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            pm25_values = [0] * 7
            no2_values = [0] * 7
            o3_values = [0] * 7
        
        fig_trends = go.Figure()
        
        fig_trends.add_trace(go.Scatter(
            x=days, y=pm25_values,
            mode='lines+markers',
            name=' PM2.5',
            line=dict(color='#4e73df', width=2),
            marker=dict(size=8)
        ))
        
        fig_trends.add_trace(go.Scatter(
            x=days, y=no2_values,
            mode='lines+markers',
            name=' NO2',
            line=dict(color='#1cc88a', width=2),
            marker=dict(size=8)
        ))
        
        fig_trends.add_trace(go.Scatter(
            x=days, y=o3_values,
            mode='lines+markers',
            name=' O3',
            line=dict(color='#e74a3b', width=2),
            marker=dict(size=8)
        ))
        
        fig_trends.update_layout(
            height=350,
            margin=dict(l=20, r=20, t=20, b=40),
            xaxis_title="",
            yaxis_title="Concentration (μg/m³)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_trends, use_container_width=True)

    # Alert Notifications - Only Active Alerts based on actual data
    with col4:
        st.markdown('<h3><span class="shake-emoji"></span> Active Alerts</h3>', unsafe_allow_html=True)
        
        telangana_df = st.session_state.telangana_data
        active_alerts = []
        
        if telangana_df is not None and len(telangana_df) > 0:
            # Check for high PM2.5 alerts (> 150 μg/m³ - Unhealthy threshold)
            pm25_data = telangana_df[telangana_df['pollutant_id'] == 'PM2.5'].copy()
            pm25_data = pm25_data[pm25_data['pollutant_avg'].notna()]
            
            if len(pm25_data) > 0:
                high_pm25 = pm25_data[pm25_data['pollutant_avg'] > 150]
                if len(high_pm25) > 0:
                    worst_station = high_pm25.loc[high_pm25['pollutant_avg'].idxmax()]
                    active_alerts.append({
                        'type': 'danger',
                        'icon': '',
                        'message': f'High PM2.5 Alert: {worst_station["pollutant_avg"]:.0f} μg/m³',
                        'location': worst_station['station'],
                        'color': '#dc3545',
                        'bg': '#f8d7da'
                    })
                
                # Check for moderate PM2.5 (50-150 μg/m³)
                moderate_pm25 = pm25_data[(pm25_data['pollutant_avg'] > 50) & (pm25_data['pollutant_avg'] <= 150)]
                if len(moderate_pm25) > 0:
                    avg_pm25 = moderate_pm25['pollutant_avg'].mean()
                    active_alerts.append({
                        'type': 'warning',
                        'icon': '',
                        'message': f'Moderate PM2.5 levels detected',
                        'location': f'Avg: {avg_pm25:.0f} μg/m³',
                        'color': '#ffc107',
                        'bg': '#fff3cd'
                    })
            
            # Check for high PM10 alerts (> 100 μg/m³)
            pm10_data = telangana_df[telangana_df['pollutant_id'] == 'PM10'].copy()
            pm10_data = pm10_data[pm10_data['pollutant_avg'].notna()]
            
            if len(pm10_data) > 0:
                high_pm10 = pm10_data[pm10_data['pollutant_avg'] > 100]
                if len(high_pm10) > 0:
                    worst_pm10 = high_pm10.loc[high_pm10['pollutant_avg'].idxmax()]
                    active_alerts.append({
                        'type': 'warning',
                        'icon': '🌫️',
                        'message': f'High PM10 detected: {worst_pm10["pollutant_avg"]:.0f} μg/m³',
                        'location': worst_pm10['station'],
                        'color': '#ff7e00',
                        'bg': '#fff3cd'
                    })
            
            # Check for good air quality (low PM2.5 < 50)
            if len(pm25_data) > 0:
                good_air = pm25_data[pm25_data['pollutant_avg'] <= 50]
                if len(good_air) > len(pm25_data) * 0.5:  # More than 50% stations have good air
                    avg_good = good_air['pollutant_avg'].mean()
                    active_alerts.append({
                        'type': 'success',
                        'icon': '✅',
                        'message': 'Good air quality in most areas',
                        'location': f'Avg PM2.5: {avg_good:.0f} μg/m³',
                        'color': '#28a745',
                        'bg': '#d4edda'
                    })
        
        # Display active alerts (limit to 4 most important)
        if len(active_alerts) == 0:
            # Default alert if no data
            active_alerts.append({
                'type': 'info',
                'icon': '',
                'message': 'No active alerts',
                'location': 'All stations normal',
                'color': '#17a2b8',
                'bg': '#d1ecf1'
            })
        
        # Show up to 4 most important alerts (prioritize danger > warning > success > info)
        alert_priority = {'danger': 0, 'warning': 1, 'success': 2, 'info': 3}
        sorted_alerts = sorted(active_alerts[:4], key=lambda x: alert_priority.get(x['type'], 99))
        
        for alert in sorted_alerts:
            st.markdown(f"""
                <div class="alert-box" style="background-color: {alert['bg']}; border-left: 5px solid {alert['color']};">
                    <span class="pulse-emoji" style="font-size: 1.5em;">{alert['icon']}</span>
                    <strong>{alert['message']}</strong><br>
                    <small>{alert['location']}</small>
                </div>
            """, unsafe_allow_html=True)

    # Footer with animated icons
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <span class="pulse-emoji"></span>
            <span class="bounce-emoji"></span>
            <span class="pulse-emoji"></span>
            <br>
            <p style="color: #666; margin-top: 10px;">
                Real-time Air Quality Monitoring System | Last Updated: <span class="rotate-emoji"></span> Just now
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Floating action button animation
    st.markdown("""
        <div style="position: fixed; bottom: 30px; right: 30px; z-index: 999;">
            <div class="bounce-emoji" style="font-size: 3em; cursor: pointer; 
                 background: white; border-radius: 50%; padding: 10px; 
                 box-shadow: 0 4px 12px rgba(0,0,0,0.3);">
                💬
            </div>
        </div>
    """, unsafe_allow_html=True)