import re
import streamlit as st
from pytube import YouTube

if "progress_bar" not in st.session_state:
    st.session_state.progress_bar = None


def show_percent_progress(stream, chunk, bytes_remaining):
    file_size = stream.filesize
    percent = (file_size - bytes_remaining) / file_size
    st.session_state.progress_bar.progress(percent, text="YouTube video is downloaded")


def check_youtube_link(link: str):
    return re.match("^https://www.youtube.com/watch?.+", link)


def download_video(link: str, path: str = "", choice: int = 2):
    st.session_state.progress_bar = st.progress(0, text="YouTube video is downloaded")
    yt = YouTube(link, on_progress_callback=show_percent_progress)
    stream = ""
    if choice == 1:
        stream = yt.streams.filter(only_audio=True).first()
    elif choice == 2:
        stream = yt.streams.filter(file_extension="mp4").first()
    path = stream.download(output_path=path)
    st.balloons()
    st.write("Your video downloaded here: ", path)


def main():
    youtube_link = st.text_input("Enter Youtube video link: ")
    if st.button("Download the video"):
        if not check_youtube_link(youtube_link):
            st.write("Please write a valid Youtube link")
            return
        st.video(youtube_link)
        path = ""
        choice = 2
        download_video(youtube_link, path, choice)


if __name__ == "__main__":
    main()
