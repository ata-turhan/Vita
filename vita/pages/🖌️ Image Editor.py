import os

import streamlit as st
from modules.utils import add_bg_from_local, local_css, set_page_config
from PIL import Image


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

    image = st.file_uploader("Choose a image to edit")
    if image is not None:
        st.image(image)
        Image.open(image)


if __name__ == "__main__":
    main()
