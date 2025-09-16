#------------------------------------------------------------------------------
# Ascii Generation Studio ver2025
# againeureka, Sep. 2025
#------------------------------------------------------------------------------

import streamlit as st
from PIL import Image, ImageEnhance
import numpy as np
import pyfiglet

# --- Function Definitions ---

# 1. Function to convert text to ASCII art
def text_to_ascii_art(text, font, width):
    # Use pyfiglet's width parameter to control the output width
    fig = pyfiglet.Figlet(font=font, width=width)
    return fig.renderText(text)

# 2. Function to convert an image to ASCII/Emoji art
def image_to_char_art(image, width_chars, char_set, brightness_factor, contrast_factor, maintain_aspect=True, char_richness_level=10):
    # Image preprocessing (brightness, contrast)
    enhancer_bright = ImageEnhance.Brightness(image)
    image = enhancer_bright.enhance(brightness_factor)
    enhancer_contrast = ImageEnhance.Contrast(image)
    image = enhancer_contrast.enhance(contrast_factor)

    # Convert to grayscale
    image = image.convert('L') # 'L' for grayscale

    # Calculate aspect ratio and resize the image
    aspect_ratio = image.width / image.height
    
    if maintain_aspect:
        # Adjust vertical ratio for monospaced fonts, which are taller than they are wide.
        height_chars = int(width_chars / aspect_ratio / (0.5 if ' ' in char_set else 1)) 
        # Since character height is roughly half the width, increase height_chars to compensate.
        height_chars = int(height_chars * 0.55)
    else:
        # Add logic here if you want to allow the user to manually adjust the height as well.
        height_chars = int(width_chars / aspect_ratio) # Temporary value, would be replaced by user input

    image = image.resize((width_chars, height_chars))
    
    pixels = np.array(image)

    # Define character set and map them based on brightness (reflecting char_set and char_richness_level)
    if not char_set:
        char_set = " .:-=+*#%@" # Default ASCII characters
    
    # Adjust the character set based on the char_richness_level
    # For example, a lower richness level uses only the first few characters of the set.
    effective_char_set_len = max(1, int(len(char_set) * (char_richness_level / 10.0)))
    effective_char_set = char_set[:effective_char_set_len]

    # Map pixels to characters based on brightness
    # 0 (darkest) -> char_set[0], 255 (brightest) -> char_set[-1]
    output_chars = []
    for row in pixels:
        row_chars = []
        for pixel_value in row:
            # Map the pixel value to an index in effective_char_set
            index = int(pixel_value / 256 * len(effective_char_set))
            row_chars.append(effective_char_set[min(index, len(effective_char_set) - 1)])
        output_chars.append("".join(row_chars))
    
    return "\n".join(output_chars)


# --- Streamlit UI Configuration ---

st.set_page_config(layout="wide", page_title="AsciiGen Studio 2025")

st.title("✨ AsciiGen Studio 2025 ✨")
st.markdown("Create text and image art with a retro console vibe! (againeureka@gmail.com)")

# Sidebar (Control Panel)
with st.sidebar:
    st.header("⚙️ Control Panel")
    
    output_type = st.radio("Select Output Type:", ("Text Art", "Image Art"))

    st.subheader("Text Art Settings")
    f = pyfiglet.Figlet()
    available_fonts = f.getFonts()
    text_font = st.selectbox("Select Font:", available_fonts, index=available_fonts.index('standard'))
    text_width = st.slider("Text Art Width (characters):", min_value=40, max_value=120, value=80)

    st.subheader("Image Art Settings")
    img_char_type = st.radio("Character/Emoji Type:", ("ASCII Characters", "Emojis", "Custom"), key="char_type")
    
    if img_char_type == "ASCII Characters":
        img_char_set = st.text_input("ASCII Characters to Use:", " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$", key="ascii_chars")
    elif img_char_type == "Emojis":
        img_char_set = st.text_input("Emojis to Use (lightest to darkest):", "🤍🖤", key="emoji_chars")
    else: # Custom
        img_char_set = st.text_input("Custom String (lightest to darkest):", ".,:;!*#@", key="custom_chars")

    img_width_chars = st.slider("Image Art Width (characters):", min_value=30, max_value=200, value=100)
    maintain_aspect_ratio = st.checkbox("Maintain Original Aspect Ratio", value=True)
    # If maintain_aspect_ratio is False, a slider for height_chars could be added here.

    img_brightness = st.slider("Brightness Adjustment:", min_value=0.5, max_value=2.0, value=1.0, step=0.1)
    img_contrast = st.slider("Contrast Adjustment:", min_value=0.5, max_value=2.0, value=1.0, step=0.1)
    img_char_richness = st.slider("Character Richness (Detail):", min_value=1, max_value=10, value=7, help="Lower value means simpler characters; higher value means more complex characters are used.")

    # Target Age Group/Style Presets
    st.subheader("Style Presets (Beta)")
    target_style = st.selectbox(
        "Select a Style Preset:",
        ["Custom", "Kid-Friendly", "Retro Black and White", "High-Contrast Modern"],
        index=0
    )

    if target_style == "Kid-Friendly":
        # Automatically set values (example)
        img_char_set = "👶👧👦🎉🎈✨🌈💖"
        img_brightness = 1.5
        img_contrast = 0.8
        img_char_richness = 5
        # Can also change text art font here
    elif target_style == "Retro Black and White":
        img_char_set = " .:-=+*#%@"
        img_brightness = 0.8
        img_contrast = 1.2
        img_char_richness = 8
    # ... add other presets here

# --- Main Content ---

if output_type == "Text Art":
    st.header("📝 Generate Text Art")
    user_text = st.text_area("Enter text to convert:", "Hello World !")
    
    if st.button("Generate Text Art"):
        if user_text:
            st.subheader("Generated Text Art:")
            ascii_output = text_to_ascii_art(user_text, text_font, text_width)
            st.code(ascii_output, language='text')
            
            # Download button
            st.download_button(
                label="Download Text Art",
                data=ascii_output,
                file_name="text_art.txt",
                mime="text/plain"
            )
        else:
            st.warning("Please enter some text.")

else: # Image Art
    st.header("🖼️ Generate Image Art")
    uploaded_file = st.file_uploader("Upload an image file.", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Original Image', use_container_width=True)
        
        if st.button("Generate Image Art"):
            st.subheader("Generated Image Art:")
            char_art_output = image_to_char_art(
                image, 
                img_width_chars, 
                img_char_set, 
                img_brightness, 
                img_contrast, 
                maintain_aspect=maintain_aspect_ratio,
                char_richness_level=img_char_richness
            )
            st.code(char_art_output, language='text')

            # Download button
            st.download_button(
                label="Download Image Art",
                data=char_art_output,
                file_name="image_art.txt",
                mime="text/plain"
            )
    else:
        st.info("Upload an image file to convert it to art.")

#------------------------------------------------------------------------------
# End of this file
#------------------------------------------------------------------------------