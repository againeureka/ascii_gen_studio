#------------------------------------------------------------------------------
# Ascii Generation Studio ver2025
# againeureka, Sep. 2025
#------------------------------------------------------------------------------

import streamlit as st
from PIL import Image, ImageEnhance
import numpy as np
import pyfiglet

# --- 함수 정의 ---

# 1. 텍스트를 아스키 아트로 변환하는 함수
def text_to_ascii_art(text, font, width):
    fig = pyfiglet.Figlet(font=font, width=width) # pyfiglet width 매개변수 활용
    return fig.renderText(text)

# 2. 이미지를 아스키/이모지 아트로 변환하는 함수
def image_to_char_art(image, width_chars, char_set, brightness_factor, contrast_factor, maintain_aspect=True, char_richness_level=10):
    # 이미지 전처리 (밝기, 대비)
    enhancer_bright = ImageEnhance.Brightness(image)
    image = enhancer_bright.enhance(brightness_factor)
    enhancer_contrast = ImageEnhance.Contrast(image)
    image = enhancer_contrast.enhance(contrast_factor)

    # 흑백으로 변환
    image = image.convert('L') # 'L' for grayscale

    # 가로/세로 비율 계산 및 크기 조절
    aspect_ratio = image.width / image.height
    
    if maintain_aspect:
        height_chars = int(width_chars / aspect_ratio / (0.5 if ' ' in char_set else 1)) # 문자의 세로 비율 보정
        # 문자의 세로 폭이 가로 폭보다 좁으므로, height_chars를 늘려줘야 함 (대략 2배)
        height_chars = int(height_chars * 0.55) # 대략적인 문자 비율 보정
    else:
        # 사용자가 직접 높이도 조절할 수 있게 하려면 여기에 다른 로직 추가
        height_chars = int(width_chars / aspect_ratio) # 임시값, 실제 구현에서는 사용자 입력 반영

    image = image.resize((width_chars, height_chars))
    
    pixels = np.array(image)

    # 문자 셋 정의 및 밝기 매핑 (char_set과 char_richness_level 반영)
    if not char_set:
        char_set = " .:-=+*#%@" # 기본 아스키 문자
    
    # char_richness_level에 따라 사용될 문자 셋을 조절
    # 예를 들어, char_richness_level이 낮으면 char_set의 앞부분만 사용
    effective_char_set_len = max(1, int(len(char_set) * (char_richness_level / 10.0)))
    effective_char_set = char_set[:effective_char_set_len]

    # 밝기에 따라 문자를 매핑
    # 0 (가장 어두움) -> char_set[0], 255 (가장 밝음) -> char_set[-1]
    output_chars = []
    for row in pixels:
        row_chars = []
        for pixel_value in row:
            # 픽셀 값을 effective_char_set의 인덱스로 매핑
            index = int(pixel_value / 256 * len(effective_char_set))
            row_chars.append(effective_char_set[min(index, len(effective_char_set) - 1)])
        output_chars.append("".join(row_chars))
    
    return "\n".join(output_chars)


# --- Streamlit UI 구성 ---

st.set_page_config(layout="wide", page_title="AsciiGen Studio 2025")

st.title("✨ AsciiGen Studio 2025 ✨")
st.markdown("옛 콘솔 감성의 텍스트/이미지 아트를 만들어보세요! (againeureka@gmail.com)")

# 사이드바 (제어 옵션)
with st.sidebar:
    st.header("⚙️ 제어판")
    
    output_type = st.radio("출력 형식 선택:", ("텍스트 아트", "이미지 아트"))

    st.subheader("텍스트 아트 설정")
    f = pyfiglet.Figlet()
    available_fonts = f.getFonts() 
    text_font = st.selectbox("폰트 선택:", available_fonts, index=available_fonts.index('standard'))
    text_width = st.slider("텍스트 아트 가로 길이 (문자 수):", min_value=40, max_value=120, value=80)

    st.subheader("이미지 아트 설정")
    img_char_type = st.radio("문자/이모지 타입:", ("아스키 문자", "이모지", "사용자 정의"), key="char_type")
    
    if img_char_type == "아스키 문자":
        img_char_set = st.text_input("사용할 아스키 문자:", " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$", key="ascii_chars")
    elif img_char_type == "이모지":
        img_char_set = st.text_input("사용할 이모지 (밝은->어두운 순):", "🤍🖤", key="emoji_chars")
    else: # 사용자 정의
        img_char_set = st.text_input("사용할 문자열 (밝은->어두운 순):", ".,:;!*#@", key="custom_chars")

    img_width_chars = st.slider("이미지 아트 가로 길이 (문자 수):", min_value=30, max_value=200, value=100)
    maintain_aspect_ratio = st.checkbox("원본 비율 유지", value=True)
    # maintain_aspect_ratio가 False일 경우, height_chars 슬라이더 추가 가능

    img_brightness = st.slider("밝기 조절:", min_value=0.5, max_value=2.0, value=1.0, step=0.1)
    img_contrast = st.slider("선명도 조절:", min_value=0.5, max_value=2.0, value=1.0, step=0.1)
    img_char_richness = st.slider("문자 다양성 (디테일):", min_value=1, max_value=10, value=7, help="낮을수록 단순, 높을수록 복잡한 문자 사용")

    # 목표 연령대/스타일 프리셋
    st.subheader("스타일 프리셋 (베타)")
    target_style = st.selectbox(
        "스타일 프리셋 선택:",
        ["사용자 정의", "어린이 친화적", "복고풍 흑백", "고대비 모던"],
        index=0
    )

    if target_style == "어린이 친화적":
        # 값 자동 설정 (예시)
        img_char_set = "👶👧👦🎉🎈✨🌈💖"
        img_brightness = 1.5
        img_contrast = 0.8
        img_char_richness = 5
        # 텍스트 아트 폰트도 변경 가능
    elif target_style == "복고풍 흑백":
        img_char_set = " .:-=+*#%@"
        img_brightness = 0.8
        img_contrast = 1.2
        img_char_richness = 8
    # ... 다른 프리셋들도 추가

# --- 메인 콘텐츠 ---

if output_type == "텍스트 아트":
    st.header("📝 텍스트 아트 생성")
    user_text = st.text_area("변환할 텍스트를 입력하세요:", "Hello World !")
    
    if st.button("텍스트 아트 생성"):
        if user_text:
            st.subheader("생성된 텍스트 아트:")
            ascii_output = text_to_ascii_art(user_text, text_font, text_width)
            st.code(ascii_output, language='text')
            
            # 다운로드 버튼
            st.download_button(
                label="텍스트 아트 다운로드",
                data=ascii_output,
                file_name="text_art.txt",
                mime="text/plain"
            )
        else:
            st.warning("텍스트를 입력해주세요.")

else: # 이미지 아트
    st.header("🖼️ 이미지 아트 생성")
    uploaded_file = st.file_uploader("이미지 파일을 업로드하세요.", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='원본 이미지', use_container_width=True)
        
        if st.button("이미지 아트 생성"):
            st.subheader("생성된 이미지 아트:")
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

            # 다운로드 버튼
            st.download_button(
                label="이미지 아트 다운로드",
                data=char_art_output,
                file_name="image_art.txt",
                mime="text/plain"
            )
    else:
        st.info("이미지 파일을 업로드하여 아트로 변환해보세요.")

#------------------------------------------------------------------------------
# End of this file
#------------------------------------------------------------------------------