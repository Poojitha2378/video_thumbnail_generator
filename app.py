import tempfile
from pathlib import Path
from typing import List

import cv2
import streamlit as st
from PIL import Image
from transformers import pipeline


def extract_frames(video_path: str, interval: float = 1.0) -> List[Image.Image]:
    """Extract frames from the given video at the specified second interval."""
    video = cv2.VideoCapture(video_path)
    frames: List[Image.Image] = []

    fps = video.get(cv2.CAP_PROP_FPS) or 1
    frame_interval = max(int(interval * fps), 1)

    frame_index = 0
    while True:
        ret, frame = video.read()
        if not ret:
            break

        if frame_index % frame_interval == 0:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(Image.fromarray(rgb_frame))

        frame_index += 1

    video.release()
    return frames


@st.cache_resource(show_spinner=False)
def load_captioner(model_name: str = "Salesforce/blip-image-captioning-base"):
    """Load the BLIP captioning pipeline once per session."""
    return pipeline("image-to-text", model=model_name)


def run_captioner(captioner, frames: List[Image.Image], limit: int = 3) -> List[str]:
    captions: List[str] = []
    for frame in frames[:limit]:
        result = captioner(frame)[0]["generated_text"]
        captions.append(result)
    return captions


st.set_page_config(page_title="Video Thumbnail & Copy Generator", layout="wide")
st.title("Video Thumbnail & Copy Generator")

st.write(
    "Upload a short video to automatically extract thumbnail candidates and generate "
    "social-ready captions using BLIP image captioning."
)

with st.sidebar:
    st.header("Controls")
    interval = st.slider("Frame extraction interval (seconds)", min_value=1, max_value=10, value=2)
    caption_count = st.slider("Caption how many frames?", min_value=1, max_value=5, value=3)
    st.caption("Captions are generated from the earliest frames first.")

video_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi", "mkv"])

if video_file:
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_video_path = Path(temp_dir) / "upload_video"

        with open(temp_video_path, "wb") as f:
            f.write(video_file.read())

        with st.spinner("Extracting frames..."):
            frames = extract_frames(str(temp_video_path), interval=interval)

    if frames:
        st.success(f"Captured {len(frames)} frame(s). Showing the first 5 below.")
        cols = st.columns(min(5, len(frames)))
        for idx, frame in enumerate(frames[:5]):
            cols[idx % len(cols)].image(frame, caption=f"Frame {idx}")

        with st.spinner("Loading BLIP captioner (first run may download weights)..."):
            captioner = load_captioner()

        with st.spinner("Generating social copy suggestions..."):
            captions = run_captioner(captioner, frames, limit=caption_count)

        st.subheader("Suggested Captions")
        for idx, caption in enumerate(captions):
            st.write(f"{idx + 1}. {caption}")

        st.download_button(
            "Download captions as text",
            data="\n".join(captions),
            file_name="captions.txt",
            mime="text/plain",
        )
    else:
        st.warning("No frames could be extracted from this video. Please try another file.")
else:
    st.info("Upload a video to generate thumbnails and captions.")
