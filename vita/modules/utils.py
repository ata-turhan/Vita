import base64

import streamlit as st


@st.cache_data
def add_bg_from_local(
    background_img_path: str, sidebar_background_img_path: str
) -> str:
    """
    Generate CSS code to set background images for Streamlit application elements.

    Args:
        background_img_path (str): The file path to the background image for the main application.
        sidebar_background_img_path (str): The file path to the background image for the sidebar.

    Returns:
        str: A string containing CSS code to set background images for the main application and sidebar.
    """
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


def set_page_config() -> None:
    """
    Configure Streamlit's page settings including title, icon, sidebar state, and menu items.

    Args:
        None

    Returns:
        None
    """
    st.set_page_config(
        page_title="Vita Toolbox",
        page_icon="🧰",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            "Get Help": "https://github.com/invictus-21/Vita/blob/main/README.md",
            "Report a bug": "https://github.com/invictus-21/Vita/issues",
            "About": """Welcome to the Vita (β) Toolbox! This repository serves as a collection of various
             mini tools designed to simplify and enhance different tasks and processes. Whether you're a developer,
              data scientist, or just someone looking to streamline everyday tasks, you'll find something useful here.""",
        },
    )


def local_css(file_name: str = None) -> None:
    """
    Add custom CSS styles to a Streamlit application, either by providing a file name or using inline CSS.

    Args:
        file_name (str, optional): The name or path of a CSS file to include. If provided, the function reads
        the CSS content from the file and adds it to the application. If not provided, default CSS for adjusting
        the sidebar width is added.

    Returns:
        None
    """
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
