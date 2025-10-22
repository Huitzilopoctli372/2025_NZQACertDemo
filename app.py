"""
NZQA Certificate Generator - Local Demo Version
Run this locally to demonstrate how to use streamlit (in Snowflake Apps) without the need for Snowflake
Note: Modify and integrate as an App within Snowflake - you will need to connect Pipeline/Tables from a data warehouse.
"""

import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import io
from datetime import datetime, date

# === FILE PATH CORRECTION ===
# Template path must now match the structure defined in your Dockerfile and the file name you provided.
TEMPLATE_PATH = "images/before.png"
FONT_PATH = "fonts/BOD_B.TTF"

# App Configuration
st.set_page_config(page_title="NZQA Certificate Generator - Demo", page_icon="🎓", layout="wide")

# Custom CSS for NZQA branding
st.markdown("""
<style>
    .main-header {
        color: #c41e3a;
        font-size: 2.5rem;
        font-weight: bold;
    }
    .stButton>button[kind="primary"] {
        background-color: #c41e3a;
        color: white;
    }
    .stButton>button[kind="primary"]:hover {
        background-color: #9a1829;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🎓 NZQA Certificate Generator</h1>', unsafe_allow_html=True)
st.markdown("**New Zealand Qualifications Authority** | Mana Tohu Mātai Ranga O Aotearoa")
st.markdown("**DEMO VERSION** - Demonstrates certificate generation capabilities")

# Create sample data (simulating Snowflake database)
@st.cache_data
def load_sample_data():
    return pd.DataFrame({
        'STUDENT_ID': ['S001', 'S002', 'S003', 'S004', 'S005'],
        'STUDENT_NAME': [
            'Emma Wilson',
            'James Patterson',
            'Aroha Te Kanawa',
            'Liam Chen',
            'Sophie Anderson'
        ],
        'QUALIFICATION_NAME': [
            'New Zealand Certificate in Business (Administration and Technology) Level 4',
            'New Zealand Diploma in Engineering (Civil) Level 6',
            'New Zealand Certificate in Health and Wellbeing (Support Work) Level 3',
            'New Zealand Certificate in Information Technology (Technical Support) Level 5',
            'New Zealand Certificate in Hospitality (Food and Beverage Service) Level 4'
        ],
        'QUALIFICATION_LEVEL': [4, 6, 3, 5, 4],
        'RESULT': [
            'Achieved with Excellence',
            'Achieved with Merit',
            'Achieved',
            'Achieved with Excellence',
            'Achieved with Merit'
        ],
        'COMPLETION_DATE': [
            date(2025, 10, 15),
            date(2025, 10, 12),
            date(2025, 10, 10),
            date(2025, 10, 8),
            date(2025, 10, 5)
        ],
        'CREDITS': [120, 240, 60, 180, 120],
        'PROVIDER_NAME': [
            'Auckland Institute of Technology',
            'Wellington Polytechnic',
            'Christchurch Health Academy',
            'Digital Skills New Zealand',
            'Culinary Arts College NZ'
        ],
        'STATUS': ['COMPLETED'] * 5
    })

# Load data
df = load_sample_data()


# Helper Functions
def generate_nzqa_certificate(name, qualification, result, date, level, credits, provider):
    """
    Generate an NZQA certificate by loading the template and adding dynamic text.
    """
    
    # === CORRECTED: Load the template image ===
    try:
        # Load the template image from the specified path
        img = Image.open(TEMPLATE_PATH)
    except FileNotFoundError:
        st.error(f"FATAL: Template file not found. Ensure '{TEMPLATE_PATH}' exists and is copied into your Docker container.")
        return None
        
    width, height = img.size 
    draw = ImageDraw.Draw(img)
    
    # --- Font Loading ---
    # NOTE: You MUST ensure 'arial.ttf' or your preferred font (like Bodoni MT) 
    # is available in the 'fonts/' directory of your project AND copied into the container.
    try:
        # If you have a font file, use its relative path (e.g., "fonts/BodoniMT.ttf")
        # For a safer demo, we'll try 'arial.ttf' or a standard system font.
        # font_path = "arial.ttf" # Replace with your actual font file if provided
        
        # Font Sizes (Adjusted for a standard high-res template)
        name_font = ImageFont.truetype(FONT_PATH, 70)
        body_font = ImageFont.truetype(FONT_PATH, 55)
        qual_font = ImageFont.truetype(FONT_PATH, 30)
        subtitle_font = ImageFont.truetype(FONT_PATH, 20)
        
    except Exception:
        # Fall back to default font if TrueType font is not found in the container
        body_font = name_font = qual_font = subtitle_font = ImageFont.load_default()
    
    
    # === TEXT DRAWING LOGIC (Coordinates Adjusted for Template) ===
    # We are drawing text onto the pre-existing template.
    draw.text((width//2, 250), "Certificate of Achievement", fill='#2C3E50', anchor="mm", font=body_font) 
              
    # "This is to certify that" 
    draw.text((width//2, 300), "This is to certify that", fill='#555555', anchor="mm", font=subtitle_font) 
    
    # Student name 
    draw.text((width//2, 350), name, fill='#1A1A1A', anchor="mm", font=name_font) 
    
    # Has successfully completed 
    draw.text((width//2, 425), "has successfully completed", fill='#555555', anchor="mm", font=subtitle_font) 
    
    # Qualification name 
    draw.text((width//2, 450), qualification, fill='#1A1A1A', anchor="mm", font=qual_font) 
    
    # Level and credits (Adjusted Y)
    draw.text((width//2, 500), f"NZQA Level {level}", fill='#1A1A1A', anchor="mm", font=qual_font) 
    draw.text((width//2, 550), f"{credits} Credits", fill='#555555', anchor="mm", font=qual_font)
    
    # Results and date
    draw.text((width//2, 600), f"Result: {result}", fill='#c41e3a', anchor="mm", font=qual_font)
    draw.text((width//2, 650), f"Issuing Date: {date}", fill='#555555', anchor="mm", font=qual_font) 
    draw.text((width//2, 700), f"Awarded through: {provider}", fill='#888888', anchor="mm", font=subtitle_font)
    draw.text((width//2, 750), "This certificate is awarded under the authority of the New Zealand Qualifications Authority", fill='#AAAAAA', anchor="mm", font=subtitle_font)
    draw.text((width//2, 800), "Te Tari Tarakehi Matauranga o Aotearoa", fill='#AAAAAA', anchor="mm", font=subtitle_font)
    
    # Convert to bytes
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG', quality=95, dpi=(300, 300))
    img_byte_arr.seek(0)
    
    return img_byte_arr.getvalue()

def wrap_text(text, max_chars):
    """Wrap text to multiple lines"""
    words = text.split()
    lines = []
    current_line = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) + 1 <= max_chars:
            current_line.append(word)
            current_length += len(word) + 1
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
            current_length = len(word)
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines

def convert_to_pdf(image_bytes, student_name, qualification):
    """Convert PNG certificate to PDF"""
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.pdfgen import canvas as pdf_canvas
    from reportlab.lib.utils import ImageReader
    
    buffer = io.BytesIO()
    c = pdf_canvas.Canvas(buffer, pagesize=landscape(A4))
    width, height = landscape(A4)
    
    # Add image
    img = ImageReader(io.BytesIO(image_bytes))
    c.drawImage(img, 0, 0, width, height, preserveAspectRatio=True)
    
    # Add metadata
    c.setTitle(f"NZQA Certificate - {student_name}")
    c.setSubject(qualification)
    c.setAuthor("New Zealand Qualifications Authority")
    
    c.showPage()
    c.save()
    
    buffer.seek(0)
    return buffer.getvalue()


# Sidebar
with st.sidebar:
    st.header("ℹ️ Demo Information")
    st.info("""
    This is a **demonstration version** running locally.
    
    In production, this connects to:
    - Your Snowflake database
    - Student records table
    - NZQA logo assets
    - Certificate templates
    """)
    
    st.markdown("---")
    st.markdown("### 🎯 Features Demonstrated")
    st.markdown("""
    ✅ NZQA-compliant certificates  
    ✅ Student data integration  
    ✅ Customizable templates  
    ✅ Bulk generation  
    ✅ PDF export  
    ✅ High-resolution output
    """)
    
    st.markdown("---")
    st.success("💡 **Tip:** Try generating certificates for different students to see customization options")


# Main tabs
tab1, tab2, tab3 = st.tabs(["📄 Single Certificate", "📦 Bulk Generation", "📊 Sample Data"])
with tab1:
    st.header("Generate Single Certificate")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_student = st.selectbox(
            "Select Student",
            options=df['STUDENT_NAME'].tolist(),
            help="Choose a student from the sample database"
        )
    
    if selected_student:
        student_data = df[df['STUDENT_NAME'] == selected_student].iloc[0]
        
        with col2:
            st.metric("Level", f"Level {student_data['QUALIFICATION_LEVEL']}")
            st.metric("Credits", student_data['CREDITS'])
        
        # Display student information
        st.markdown("### Student Information")
        info_col1, info_col2, info_col3 = st.columns(3)
        
        with info_col1:
            st.info(f"**ID:** {student_data['STUDENT_ID']}")
        with info_col2:
            st.success(f"**Result:** {student_data['RESULT']}")
        with info_col3:
            st.info(f"**Provider:** {student_data['PROVIDER_NAME']}")
        
        # Qualification details
        st.markdown("#### Qualification")
        st.write(student_data['QUALIFICATION_NAME'])
        st.caption(f"Completed: {student_data['COMPLETION_DATE']}")
        
        # Certificate customization
        st.markdown("---")
        st.markdown("### Customize Certificate")
        
        with st.expander("📝 Edit Certificate Details", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                cert_name = st.text_input("Name on Certificate", value=student_data['STUDENT_NAME'])
                cert_qualification = st.text_area(
                    "Qualification Name", 
                    value=student_data['QUALIFICATION_NAME'],
                    height=100
                )
            with col2:
                cert_result = st.selectbox(
                    "Result", 
                    ["Achieved", "Achieved with Merit", "Achieved with Excellence"],
                    index=["Achieved", "Achieved with Merit", "Achieved with Excellence"].index(student_data['RESULT'])
                )
                cert_date = st.date_input("Completion Date", value=student_data['COMPLETION_DATE'])
            
            col1, col2 = st.columns(2)
            with col1:
                cert_provider = st.text_input("Provider Name", value=student_data['PROVIDER_NAME'])
            with col2:
                cert_credits = st.number_input("Total Credits", value=int(student_data['CREDITS']), min_value=0)
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🎓 Generate Certificate", type="primary", use_container_width=True):
                with st.spinner("Generating NZQA certificate..."):
                    # Generate certificate
                    certificate_bytes = generate_nzqa_certificate(
                        name=cert_name,
                        qualification=cert_qualification,
                        result=cert_result,
                        date=str(cert_date),
                        level=student_data['QUALIFICATION_LEVEL'],
                        credits=cert_credits,
                        provider=cert_provider
                    )
                    
                    if certificate_bytes:
                        # Display certificate
                        st.markdown("### 🎉 Generated Certificate")
                        st.image(certificate_bytes, caption="NZQA Certificate Preview")
                        
                        # Action buttons
                        st.markdown("### Download Options")
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.download_button(
                                label="📥 Download PNG",
                                data=certificate_bytes,
                                file_name=f"NZQA_certificate_{cert_name.replace(' ', '_')}.png",
                                mime="image/png",
                                use_container_width=True
                            )
                        
                        with col2:
                            # Generate PDF version
                            pdf_bytes = convert_to_pdf(certificate_bytes, cert_name, cert_qualification)
                            st.download_button(
                                label="📄 Download PDF",
                                data=pdf_bytes,
                                file_name=f"NZQA_certificate_{cert_name.replace(' ', '_')}.pdf",
                                mime="application/pdf",
                                use_container_width=True
                            )
                        
                        with col3:
                            st.success("✅ Ready for Distribution")
                        
                        st.info("💡 In production, certificates are automatically saved to Snowflake stages")

with tab2:
    st.header("Bulk Certificate Generation")
    
    st.markdown("""
    Generate certificates for multiple students simultaneously. Perfect for graduation ceremonies or course completions.
    """)
    
    # Filter options
    st.markdown("### Filter Criteria")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        result_filter = st.multiselect(
            "Results",
            ["Achieved", "Achieved with Merit", "Achieved with Excellence"],
            default=["Achieved", "Achieved with Merit", "Achieved with Excellence"]
        )
    with col2:
        level_filter = st.multiselect(
            "Levels",
            [3, 4, 5, 6],
            default=[3, 4, 5, 6]
        )
    with col3:
        provider_filter = st.multiselect(
            "Providers",
            df['PROVIDER_NAME'].unique().tolist(),
            default=df['PROVIDER_NAME'].unique().tolist()
        )
    
    # Filter dataframe
    filtered_df = df[
        (df['RESULT'].isin(result_filter)) &
        (df['QUALIFICATION_LEVEL'].isin(level_filter)) &
        (df['PROVIDER_NAME'].isin(provider_filter))
    ]
    
    st.markdown(f"### Selected Students: {len(filtered_df)}")
    st.dataframe(filtered_df[['STUDENT_NAME', 'QUALIFICATION_NAME', 'RESULT', 'COMPLETION_DATE']], 
                 use_container_width=True)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button(f"🚀 Generate {len(filtered_df)} Certificates", type="primary", use_container_width=True):
            if len(filtered_df) > 0:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                certificates = []
                
                for idx, (_, row) in enumerate(filtered_df.iterrows()):
                    status_text.text(f"Processing: {row['STUDENT_NAME']} ({idx + 1}/{len(filtered_df)})")
                    
                    cert_bytes = generate_nzqa_certificate(
                        name=row['STUDENT_NAME'],
                        qualification=row['QUALIFICATION_NAME'],
                        result=row['RESULT'],
                        date=str(row['COMPLETION_DATE']),
                        level=row['QUALIFICATION_LEVEL'],
                        credits=row['CREDITS'],
                        provider=row['PROVIDER_NAME']
                    )
                    
                    if cert_bytes:
                        certificates.append({
                            'student_id': row['STUDENT_ID'],
                            'name': row['STUDENT_NAME'],
                            'data': cert_bytes
                        })
                    
                    progress_bar.progress((idx + 1) / len(filtered_df))
                
                status_text.empty()
                progress_bar.empty()
                
                st.success(f"✅ Successfully generated {len(certificates)} certificates!")
                
                # Show download options
                st.markdown("### Download All Certificates")
                st.info("💡 In production, all certificates are saved to Snowflake stages for distribution")
                
                # Display first certificate as preview
                if certificates:
                    st.markdown("#### Preview (First Certificate)")
                    st.image(certificates[0]['data'], width=600)
            else:
                st.warning("⚠️ No students match the selected criteria")

with tab3:
    st.header("📊 Sample Data Overview")
    
    st.markdown("""
    This demo uses sample student data to illustrate the system. In production, this connects directly
    to your Snowflake database containing actual student records.
    """)
    
    # Statistics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Students", len(df))
    col2.metric("Qualifications", df['QUALIFICATION_NAME'].nunique())
    col3.metric("Providers", df['PROVIDER_NAME'].nunique())
    col4.metric("Avg Level", f"{df['QUALIFICATION_LEVEL'].mean():.1f}")
    
    st.markdown("---")
    
    # Full data table
    st.markdown("### Complete Student Records")
    st.dataframe(df, use_container_width=True)
    
    st.markdown("---")
    
    # Results distribution
    st.markdown("### Results Distribution")
    result_counts = df['RESULT'].value_counts()
    st.bar_chart(result_counts)
    
    st.markdown("---")
    
    # Database schema
    st.markdown("### Production Database Schema")
    st.code("""
CREATE TABLE EDUCATION_DB.PUBLIC.STUDENTS (
    STUDENT_ID VARCHAR(50) PRIMARY KEY,
    STUDENT_NAME VARCHAR(200) NOT NULL,
    QUALIFICATION_NAME VARCHAR(300) NOT NULL,
    QUALIFICATION_LEVEL INTEGER NOT NULL,
    RESULT VARCHAR(50) NOT NULL,
    COMPLETION_DATE DATE NOT NULL,
    CREDITS INTEGER NOT NULL,
    PROVIDER_NAME VARCHAR(200),
    STATUS VARCHAR(20),
    EMAIL VARCHAR(200),
    PHONE VARCHAR(50),
    CERTIFICATE_ISSUED_DATE TIMESTAMP,
    CERTIFICATE_NUMBER VARCHAR(50)
);
    """, language="sql")


# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888888; padding: 20px;'>
    <p><strong>NZQA Certificate Generator - Demo Version</strong></p>
    <p>This demonstration shows the capabilities of the full Snowflake-integrated solution</p>
    <p style='font-size: 0.9em; margin-top: 10px;'>
        Production version includes:<br>
        ✓ Direct Snowflake database integration<br>
        ✓ Automated bulk processing<br>
        ✓ Email distribution<br>
        ✓ Certificate verification system<br>
        ✓ Audit logging and compliance tracking
    </p>
</div>
""", unsafe_allow_html=True)