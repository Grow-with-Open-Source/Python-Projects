import streamlit as st
from PIL import Image
import os
from utils.watermark import add_text_watermark, add_logo_watermark

st.set_page_config(page_title=" Image Watermarking Tool", layout="wide")

st.title(" Image Watermarking Tool")
st.write("Upload an image, add a text or logo watermark, and download the result.")

os.makedirs("output", exist_ok=True)

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Original Image", use_container_width=True)

    st.sidebar.header(" Settings")
    wm_type = st.sidebar.radio("Watermark Type", ["Text", "Logo"])

    position = st.sidebar.selectbox("Position", ["Top-Left", "Top-Right", "Bottom-Left", "Bottom-Right", "Center"])
    opacity = st.sidebar.slider("Opacity", 0.0, 1.0, 0.5)

    if wm_type == "Text":
        text = st.sidebar.text_input("Enter Watermark Text", "© MyBrand")
        font_size = st.sidebar.slider("Font Size", 20, 100, 40)

        if st.sidebar.button("Apply Text Watermark"):
            result = add_text_watermark(image, text, position, opacity, font_size)
            output_path = os.path.join("output", "watermarked_text.jpg")
            result.save(output_path)
            st.image(result, caption="Watermarked Image", use_container_width=True)
            st.download_button("Download Image", data=open(output_path, "rb"), file_name="watermarked_text.jpg")

    elif wm_type == "Logo":
        logo_file = st.sidebar.file_uploader("Upload Logo (PNG preferred)", type=["png"])
        scale = st.sidebar.slider("Logo Scale", 0.05, 0.5, 0.2)

        if st.sidebar.button("Apply Logo Watermark"):
            if logo_file:
                logo_path = os.path.join("assets", "temp_logo.png")
                os.makedirs("assets", exist_ok=True)
                with open(logo_path, "wb") as f:
                    f.write(logo_file.getbuffer())

                result = add_logo_watermark(image, logo_path, position, opacity, scale)
                output_path = os.path.join("output", "watermarked_logo.jpg")
                result.save(output_path)
                st.image(result, caption="Watermarked Image", use_container_width=True)
                st.download_button("Download Image", data=open(output_path, "rb"), file_name="watermarked_logo.jpg")
            else:
                st.warning("Please upload a logo image.")
