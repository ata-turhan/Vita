import base64
from datetime import datetime

import pandas as pd
import streamlit as st


@st.cache_data
def add_bg_from_local(background_img_path, sidebar_background_img_path):
    with open(background_img_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    with open(sidebar_background_img_path, "rb") as image_file:
        sidebar_encoded_string = base64.b64encode(image_file.read())

    return f"""<style>
        .stApp {{
            background-image: url(data:image/png;base64,{encoded_string.decode()});
            background-size: cover;
        }}

        section[data-testid="stSidebar"] {{
            background-image: url(data:image/png;base64,{sidebar_encoded_string.decode()});
            background-size: cover;
        }}
    </style>"""


def set_page_config():
    st.set_page_config(
        page_title="Vita Toolbox",
        page_icon="🧰",
        # layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            "Get Help": "https://github.com/invictus-21/Vita/blob/main/README.md",
            "Report a bug": "https://github.com/invictus-21/Vita/issues",
            "About": """Welcome to the Vita (β) Toolbox! This repository serves as a collection of various
             mini tools designed to simplify and enhance different tasks and processes. Whether you're a developer,
              data scientist, or just someone looking to streamline everyday tasks, you'll find something useful here.""",
        },
    )


def local_css(file_name=None):
    if file_name:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    # st.markdown(style, unsafe_allow_html=True)
    st.markdown(
        """
        <style>
            section[data-testid="stSidebar"] {
                width: 300px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
