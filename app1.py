import streamlit as st
import qrcode
from PIL import Image, ImageOps
import io
import img2pdf

# Set Page Config
st.set_page_config(
    page_title="QR Code Designer", 
    page_icon="🚀",
    layout="centered"
)

# Custom CSS for Professional UI
st.markdown("""
    <style>
    .block-container {
        padding-top: 2rem;
    }
    /* Professional Image Styling */
    [data-testid="stImage"] img {
        max-width: 300px;
        margin: 0 auto;
        display: block;
        border-radius: 8px; /* Softer corners for the frame */
        box-shadow: 0px 10px 30px rgba(0,0,0,0.1); /* Deeper shadow */
    }
    .stAlert {
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 QR Code Designer")
st.write("Generate High-Quality, Original QR codes within Seconds.")

# --- Sidebar Inputs ---
with st.sidebar:
    st.header("Customize")
    data = st.text_input("URL or Text", placeholder="https://google.com")
    color = st.color_picker("QR Code Color", "#000000")
    logo_file = st.file_uploader("Upload Center Logo (Optional)", type=['png', 'jpg', 'jpeg'])
    fmt = st.selectbox("Export Format", ["PNG", "JPG", "PDF"])

# --- QR Generation Logic ---
if data:
    # 1. Generate QR
    qr = qrcode.QRCode(
        version=None, 
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=2 # Reduced internal border to let the custom frame shine
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    # 2. Apply Style
    qr_img = qr.make_image(fill_color=color, back_color="white").convert('RGB')

    # 3. Add Professional Thin Border (The Frame)
    # This adds a 2-pixel light grey border around the white area
    img = ImageOps.expand(qr_img, border=2, fill='#E5E7EB')

    # 4. Process Logo
    if logo_file:
        logo = Image.open(logo_file)
        qr_w, qr_h = img.size
        logo_size = qr_w // 5
        logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
        pos = ((qr_w - logo_size) // 2, (qr_h - logo_size) // 2)
        img.paste(logo, pos)

    # 5. Display Result
    st.image(img, caption="Scan Me,QR Generated Successfully")
   
    # 6. Handle Downloads
    buf = io.BytesIO()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if fmt == "PDF":
            temp_buf = io.BytesIO()
            img.save(temp_buf, format="PNG")
            temp_buf.seek(0)
            pdf_bytes = img2pdf.convert(temp_buf)
            st.download_button("Download PDF", data=pdf_bytes, file_name="qrcode.pdf", mime="application/pdf", use_container_width=True)
        else:
            save_fmt = "PNG" if fmt == "PNG" else "JPEG"
            img.save(buf, format=save_fmt)
            st.download_button(f"Download {fmt}", data=buf.getvalue(), file_name=f"qrcode.{fmt.lower()}", mime=f"image/{fmt.lower()}", use_container_width=True)
else:
    st.info("👋 Enter a URL or text in the sidebar to generate your QR code.")