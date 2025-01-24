import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import requests
from io import BytesIO

# Page config
st.set_page_config(
    page_title="👻 GHOST",
    page_icon="👻",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 0rem;
    }
    .element-container img {
        max-width: 200px;
    }
    .logo-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Header with logo and title
col1, col2 = st.columns([1, 4])
with col1:
    response = requests.get('https://gamprodcdn.azureedge.net/ui-kit/2025-01-15-c1006d08/resources/img/logo-groupama.svg')
    st.markdown(f'<div class="logo-container" style="width: 200px">{response.text}</div>', unsafe_allow_html=True)
with col2:
    st.title("👻 GHOST (GAM HOsting Streamlit Test)")
    st.markdown("*Your Interactive Excel Data Explorer*")

# File uploader
uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

if uploaded_file is not None:
    # Load the data
    df = pd.read_excel(uploaded_file)
    
    # Basic info about the dataset
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(f"📊 Rows: {df.shape[0]}")
    with col2:
        st.info(f"📈 Columns: {df.shape[1]}")
    with col3:
        st.info(f"🔢 Total cells: {df.size}")

    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Data Explorer", "📊 Statistics", "📈 Visualizations", "⚙️ Data Processing"])
    
    with tab1:
        # Data Explorer
        st.subheader("Interactive Data Table")
        
        # Column selector
        selected_columns = st.multiselect(
            "Select columns to display",
            options=list(df.columns),
            default=list(df.columns)
        )
        
        # Search functionality
        search_term = st.text_input("🔍 Search in data")
        
        # Filter data based on search
        if search_term:
            filtered_df = df[df.astype(str).apply(lambda x: x.str.contains(search_term, case=False)).any(axis=1)]
        else:
            filtered_df = df
            
        # Display filtered data with selected columns
        st.dataframe(
            filtered_df[selected_columns],
            use_container_width=True,
            hide_index=True
        )

    with tab2:
        # Statistics
        st.subheader("Data Statistics")
        
        # Select numerical columns
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        if len(numeric_cols) > 0:
            st.write("📊 Numerical Columns Statistics")
            st.dataframe(df[numeric_cols].describe(), use_container_width=True)
        
        # Display info about missing values
        st.write("⚠️ Missing Values Analysis")
        missing_data = pd.DataFrame({
            'Column': df.columns,
            'Missing Values': df.isnull().sum(),
            'Percentage': (df.isnull().sum() / len(df) * 100).round(2)
        })
        st.dataframe(missing_data, use_container_width=True)

    with tab3:
        # Visualizations
        st.subheader("Data Visualizations")
        
        # Only show visualization options if there are numeric columns
        if len(numeric_cols) > 0:
            # Column selections for visualization
            x_col = st.selectbox("Select X-axis", numeric_cols)
            y_col = st.selectbox("Select Y-axis", numeric_cols)
            
            # Chart type selector
            chart_type = st.selectbox(
                "Select chart type",
                ["Scatter Plot", "Line Plot", "Bar Chart", "Box Plot"]
            )
            
            # Create the selected plot
            if chart_type == "Scatter Plot":
                fig = px.scatter(df, x=x_col, y=y_col, title=f"{x_col} vs {y_col}")
            elif chart_type == "Line Plot":
                fig = px.line(df, x=x_col, y=y_col, title=f"{x_col} vs {y_col}")
            elif chart_type == "Bar Chart":
                fig = px.bar(df, x=x_col, y=y_col, title=f"{x_col} vs {y_col}")
            else:
                fig = px.box(df, y=y_col, title=f"Box Plot of {y_col}")
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No numerical columns available for visualization")

    with tab4:
        # Data Processing
        st.subheader("Data Processing Options")
        
        # Handle missing values
        if st.checkbox("Handle Missing Values"):
            method = st.radio(
                "Select method",
                ["Drop rows with missing values", "Fill with mean", "Fill with median", "Fill with zero"]
            )
            
            if st.button("Process"):
                if method == "Drop rows with missing values":
                    df = df.dropna()
                elif method == "Fill with mean":
                    df = df.fillna(df.mean())
                elif method == "Fill with median":
                    df = df.fillna(df.median())
                else:
                    df = df.fillna(0)
                st.success("Missing values processed!")
                st.dataframe(df, use_container_width=True)
        
        # Download processed data
        if st.download_button(
            label="Download processed data as CSV",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name='processed_data.csv',
            mime='text/csv',
        ):
            st.success("Data downloaded successfully!")

else:
    # Display welcome message when no file is uploaded
    st.info("👋 Welcome! Please upload an Excel file to get started.")
    
    # Example features list
    st.markdown("""
    ### Available Features:
    - 📊 Interactive data exploration
    - 📈 Dynamic visualizations
    - 📋 Basic statistics and insights
    - 🔍 Search and filter capabilities
    - ⚙️ Data processing tools
    - 💾 Export processed data
    """)

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit")
