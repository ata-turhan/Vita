import os
import re
import streamlit as st
from pytube import YouTube
from modules.utils import add_bg_from_local, set_page_config, local_css

if "progress_bar" not in st.session_state:
    st.session_state.progress_bar = None


def show_percent_progress(stream, chunk, bytes_remaining):
    file_size = stream.filesize
    percent = (file_size - bytes_remaining) / file_size
    st.session_state.progress_bar.progress(percent, text="YouTube video is downloaded")


def check_youtube_link(link: str):
    return re.match("^https://www.youtube.com/(watch|shorts)", link)


def download_video(link: str, path: str = "", choice: int = 2):
    st.session_state.progress_bar = st.progress(0, text="YouTube video is downloaded")
    yt = YouTube(
        link,
        on_progress_callback=show_percent_progress,
        # use_oauth=True,
        # allow_oauth_cache=True,
    )
    stream = ""
    if choice == 1:
        stream = yt.streams.filter(only_audio=True).first()
    elif choice == 2:
        stream = yt.streams.filter(file_extension="mp4").first()
    path = stream.download(output_path=path)
    st.session_state.progress_bar.progress(1.0, text="YouTube video downloaded")
    st.balloons()
    st.write("Your video downloaded here: ", path)


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
        """<h1 style='text-align: center; color: black; font-size: 40px;'> Welcome to YouTube Downloader 📥 </h1> \
        <br>""",
        unsafe_allow_html=True,
    )
    _, center_col, _ = st.columns([1, 5, 1])

    with center_col:
        youtube_link = st.text_input("Enter Youtube video link: ")
        if check_youtube_link(youtube_link):
            st.video(youtube_link)
        if st.button("Download the video"):
            if not check_youtube_link(youtube_link):
                st.write("Please write a valid Youtube link")
                return
            path = ""
            choice = 2
            download_video(youtube_link, path, choice)


if __name__ == "__main__":
    main()
