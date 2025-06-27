"""
Utility functions for Streamlit applications.
This module provides functions to set a background image for the Streamlit app
and to convert an image file to a base64 encoded string.
"""
import streamlit as st
import base64

def get_base64_image(image_path):
    """
    Convert an image file to a base64 encoded string.
    Args:
        image_path (str): Path to the image file.
    Returns:
        str: Base64 encoded string of the image.
    """
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    return encoded

def set_background(image_path):
    """
    Set the background image for the Streamlit app.
    Args:
        image_path (str): Path to the background image file.
    This function applies the background image using CSS.
    It also styles the title box with a semi-transparent background.
    It ensures the background covers the entire app area and is centered.
    """
    encoded_image = get_base64_image(image_path)
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded_image}");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
    }}
    .title-box {{
        background-color: rgba(255, 255, 255, 0.85);
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-top: 1rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }}
    .title-box h1 {{
        font-size: 2rem;
        margin: 0;
        color: #333333;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)