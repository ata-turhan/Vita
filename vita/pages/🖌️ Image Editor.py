import os
import re
import streamlit as st
from modules.utils import add_bg_from_local, set_page_config, local_css


def main():
    set_page_config()

    local_css()

    background_img_path = os.path.join("static", "background", "Toolbox Logo.png")
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


if __name__ == "__main__":
    main()
