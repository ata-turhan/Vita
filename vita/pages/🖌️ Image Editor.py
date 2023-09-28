import os

import cv2
import numpy as np
import streamlit as st
from modules.utils import add_bg_from_local, local_css, set_page_config
from PIL import Image, ImageEnhance, ImageFilter


def main():
    set_page_config()

    local_css()

    background_img_path = os.path.join(
        "static", "background", "Toolbox Logo.png"
    )
    sidebar_background_img_path = os.path.join(
        "static", "background", "Lila Gradient.png"
    )
    page_markdown = add_bg_from_local(
        background_img_path=background_img_path,
        sidebar_background_img_path=sidebar_background_img_path,
    )
    st.markdown(page_markdown, unsafe_allow_html=True)

    st.markdown(
        """<h1 style='text-align: center; color: black; font-size: 40px;'> Welcome to Image Editor 🖌️ </h1> \
        <br>""",
        unsafe_allow_html=True,
    )

    image = st.file_uploader(
        "Choose a image to edit",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=False,
    )
    if image is None:
        return

    img = Image.open(image)
    edited_img = img

    with st.sidebar:
        _, center_col, _ = st.sidebar.columns(3)
        center_col.header("Settings")
        option = st.selectbox(
            "Options",
            [
                "<Select>",
                "Filters",
                "Image Corrections",
            ],
        )
        if option == "Filters":
            filter_choice = st.selectbox(
                "Filters",
                ["Original", "Grayscale", "Sepia", "Contour", "Sketch"],
            )
            if filter_choice == "Grayscale":
                img_convert = np.array(img.convert("RGB"))
                gray_image = cv2.cvtColor(img_convert, cv2.COLOR_RGB2GRAY)
                edited_img = gray_image
            elif filter_choice == "Sepia":
                img_convert = np.array(img.convert("RGB"))
                img_convert = cv2.cvtColor(img_convert, cv2.COLOR_RGB2BGR)
                kernel = np.array(
                    [
                        [0.272, 0.534, 0.131],
                        [0.349, 0.686, 0.168],
                        [0.393, 0.769, 0.189],
                    ]
                )
                sepia_image = cv2.filter2D(img_convert, -1, kernel)
                edited_img = sepia_image
            elif filter_choice == "Contour":
                img_convert = np.array(img.convert("RGB"))
                img_convert = cv2.cvtColor(img_convert, cv2.COLOR_RGB2BGR)
                blur_image = cv2.GaussianBlur(img_convert, (11, 11), 0)
                canny_image = cv2.Canny(blur_image, 100, 150)
                edited_img = canny_image
            elif filter_choice == "Sketch":
                img_convert = np.array(img.convert("RGB"))
                gray_image = cv2.cvtColor(img_convert, cv2.COLOR_RGB2GRAY)
                inv_gray = 255 - gray_image
                blur_image = cv2.GaussianBlur(inv_gray, (25, 25), 0, 0)
                sketch_image = cv2.divide(
                    gray_image, 255 - blur_image, scale=256
                )
                edited_img = sketch_image

        elif option == "Image Corrections":
            sharp_value = st.slider("Sharpness", 0.0, 2.0, 1.0)
            color_value = st.slider("Color")
            brightness_value = st.slider("Brightness", 0.0, 5.0, 1.0)
            contrast_value = st.slider("Contrast", 0.0, 2.0, 1.0)
            flip_image_value = st.sidebar.selectbox(
                "Flip Image",
                options=("Original", "Top->Bottom", "Left->Right", "Both"),
            )

            st.sidebar.write("Filters")
            filter_black_and_white = st.sidebar.checkbox("Black and white")
            filter_blur = st.sidebar.checkbox("Blur")

            if filter_blur:
                filter_blur_strength = st.sidebar.slider(
                    "Select Blur strength"
                )

            if not color_value:
                color_value = 1
            if not brightness_value:
                brightness_value = 1
            if not contrast_value:
                contrast_value = 1

            if img is not None:
                sharp = ImageEnhance.Sharpness(edited_img)
                edited_img = sharp.enhance(sharp_value)

                color = ImageEnhance.Color(edited_img)
                edited_img = color.enhance(color_value)

                brightness = ImageEnhance.Brightness(edited_img)
                edited_img = brightness.enhance(brightness_value)

                contrast = ImageEnhance.Contrast(edited_img)
                edited_img = contrast.enhance(contrast_value)

                if flip_image_value == "Top->Bottom":
                    edited_img = edited_img.transpose(Image.FLIP_TOP_BOTTOM)
                elif flip_image_value == "Left->Right":
                    edited_img = edited_img.transpose(Image.FLIP_LEFT_RIGHT)
                elif flip_image_value == "Both":
                    edited_img = edited_img.transpose(Image.FLIP_TOP_BOTTOM)
                    edited_img = edited_img.transpose(Image.FLIP_LEFT_RIGHT)

                if filter_black_and_white:
                    edited_img = edited_img.convert(mode="L")

                if filter_blur:
                    if filter_blur_strength:
                        edited_img = edited_img.filter(
                            ImageFilter.GaussianBlur(filter_blur_strength)
                        )
    if img is not None:
        col1, col2 = st.columns(2, gap="large")
        col1.subheader("Before")
        col1.image(
            img,
            width=350,
        )
        col2.subheader("After")
        col2.image(
            edited_img,
            width=350,
        )


if __name__ == "__main__":
    main()
