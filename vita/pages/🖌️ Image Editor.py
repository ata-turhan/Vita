import os

import streamlit as st
from modules.utils import add_bg_from_local, local_css, set_page_config
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
from PIL.ImageFilter import (
    CONTOUR,
    DETAIL,
    EDGE_ENHANCE,
    EDGE_ENHANCE_MORE,
    EMBOSS,
    FIND_EDGES,
    SHARPEN,
    SMOOTH,
    SMOOTH_MORE,
)
from removebg import RemoveBg


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

        sharp_value = st.slider("Sharpness", 0.0, 2.0, 1.0)
        color_value = st.slider("Color")
        brightness_value = st.slider("Brightness", 0.0, 5.0, 1.0)
        contrast_value = st.slider("Contrast", 0.0, 2.0, 1.0)
        rotate_value = st.slider(
            "Rotate",
            0,
            360,
        )
        resize_value = st.slider(
            "Resize (px)",
            50,
            500,
        )
        flip_image_value = st.sidebar.selectbox(
            "Flip Image",
            options=("Original", "Top->Bottom", "Left->Right", "Both"),
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

            edited_img = edited_img.rotate(rotate_value)

            edited_img = edited_img.resize((resize_value, resize_value))

            if flip_image_value == "Top->Bottom":
                edited_img = edited_img.transpose(Image.FLIP_TOP_BOTTOM)
            elif flip_image_value == "Left->Right":
                edited_img = edited_img.transpose(Image.FLIP_LEFT_RIGHT)
            elif flip_image_value == "Both":
                edited_img = edited_img.transpose(Image.FLIP_TOP_BOTTOM)
                edited_img = edited_img.transpose(Image.FLIP_LEFT_RIGHT)

            st.sidebar.header("Filters")
            if st.sidebar.checkbox("Contour"):
                edited_img = edited_img.filter(CONTOUR)
            if st.sidebar.checkbox("Detail"):
                edited_img = edited_img.filter(DETAIL)
            if st.sidebar.checkbox("Edge Enhance"):
                edited_img = edited_img.filter(EDGE_ENHANCE)
            if st.sidebar.checkbox("Edge enhance more"):
                edited_img = edited_img.filter(EDGE_ENHANCE_MORE)
            if st.sidebar.checkbox("Emboss"):
                edited_img = edited_img.filter(EMBOSS)
            if st.sidebar.checkbox("Find edges"):
                edited_img = edited_img.filter(FIND_EDGES)
            if st.sidebar.checkbox("Grayscale"):
                edited_img = ImageOps.grayscale(edited_img)
            if st.sidebar.checkbox("Invert colors"):
                edited_img = ImageOps.invert(edited_img)
            if st.sidebar.checkbox("Smooth"):
                edited_img = edited_img.filter(SMOOTH)
            if st.sidebar.checkbox("Smooth more"):
                edited_img = edited_img.filter(SMOOTH_MORE)
            if st.sidebar.checkbox("Sharpen"):
                edited_img = edited_img.filter(SHARPEN)

            filter_blur = st.sidebar.checkbox("Blur")

            if filter_blur:
                filter_blur_strength = st.sidebar.slider(
                    "Select Blur strength"
                )

            if filter_blur:
                if filter_blur_strength:
                    edited_img = edited_img.filter(
                        ImageFilter.GaussianBlur(filter_blur_strength)
                    )

            st.sidebar.header("Background")
            if st.sidebar.checkbox("Remove background"):
                rmbg = RemoveBg(st.secrets["removebg_api_key"], "error.log")
                edited_img.save("input.jpg")
                rmbg.remove_background_from_img_file(
                    img_file_path="input.jpg",
                )
                edited_img = Image.open("input.jpg_no_bg.png")
    if img is not None:
        col1, col2 = st.columns(2, gap="large")
        col1.subheader("Before")
        col1.image(
            img,
            width=450,
        )
        col2.subheader("After")
        col2.image(
            edited_img,
            width=450,
        )


if __name__ == "__main__":
    main()
