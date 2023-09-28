import os

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

    _, center_col, _ = st.sidebar.columns(3)
    center_col.header("Settings")
    sharp_value = st.sidebar.slider("Sharpness")
    color_value = st.sidebar.slider("Color")
    brightness_value = st.sidebar.slider("Brightness")
    contrast_value = st.sidebar.slider("Contrast")
    flip_image_value = st.sidebar.selectbox(
        "Flip Image",
        options=("Original", "Top->Bottom", "Left->Right", "Both"),
    )

    st.sidebar.write("Filters")
    filter_black_and_white = st.sidebar.checkbox("Black and white")
    filter_blur = st.sidebar.checkbox("Blur")

    if filter_blur:
        filter_blur_strength = st.sidebar.slider("Select Blur strength")

    # checking color
    if not color_value:
        color_value = 1
    if not brightness_value:
        brightness_value = 1
    if not contrast_value:
        contrast_value = 1

    image = st.file_uploader(
        "Choose a image to edit",
        type=["png", "jpg"],
        accept_multiple_files=False,
    )
    if image is not None:
        img = Image.open(image)
        sharp = ImageEnhance.Sharpness(img)
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
        _, center_col, _ = st.columns(3)
        center_col.image(
            edited_img,
        )


if __name__ == "__main__":
    main()
