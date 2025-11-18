import tempfile
from io import BytesIO
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import cv2
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
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


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    """Attempt to load a DejaVu font, falling back to default if unavailable."""
    font_name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    try:
        return ImageFont.truetype(font_name, size=size)
    except OSError:
        return ImageFont.load_default()


def build_overlay(size: Tuple[int, int], palette: Sequence[Tuple[int, int, int]], opacity: float) -> Image.Image:
    """Create a soft overlay inspired by polished thumbnail makers."""
    width, height = size
    alpha = int(255 * opacity)
    overlay = Image.new("RGBA", (width, height), palette[0] + (alpha,))

    if len(palette) > 1:
        draw = ImageDraw.Draw(overlay)
        band_height = max(height // (len(palette) + 1), 1)
        for i, color in enumerate(palette[1:], start=1):
            y0 = height - band_height * (len(palette) - i + 1)
            y1 = y0 + band_height
            draw.rectangle([(0, y0), (width, y1)], fill=color + (alpha,))

    return overlay


def stylize_thumbnail(
    base_image: Image.Image,
    title: str,
    subtitle: str,
    palette: Sequence[Tuple[int, int, int]],
    opacity: float = 0.65,
) -> Image.Image:
    """Apply overlay + headline text to mimic polished Canva-style thumbnails."""

    image = base_image.convert("RGBA")
    overlay = build_overlay(image.size, palette, opacity)
    composed = Image.alpha_composite(image, overlay)

    draw = ImageDraw.Draw(composed)
    width, height = composed.size

    title_font = load_font(size=max(height // 12, 28), bold=True)
    subtitle_font = load_font(size=max(height // 22, 16), bold=False)

    padding = 32
    title_y = height - int(height * 0.32)
    subtitle_y = title_y + int(title_font.size * 1.25)

    draw.text((padding, title_y), title, fill=(255, 255, 255, 255), font=title_font)
    if subtitle:
        draw.text((padding, subtitle_y), subtitle, fill=(240, 240, 240, 255), font=subtitle_font)

    return composed.convert("RGB")


def to_bytes(image: Image.Image) -> bytes:
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


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


PALETTES: Dict[str, Tuple[Tuple[int, int, int], ...]] = {
    "Vibrant coral": ((255, 94, 98), (255, 138, 101), (255, 198, 114)),
    "Creator neon": ((58, 12, 163), (90, 24, 220), (244, 67, 54)),
    "Minimal slate": ((26, 26, 36), (64, 64, 80), (92, 92, 112)),
    "Fresh mint": ((0, 150, 136), (0, 191, 165), (118, 255, 230)),
}


st.set_page_config(page_title="Video Thumbnail & Copy Generator", layout="wide")
st.title("Creator-grade Thumbnail & Copy Studio")

st.write(
    "A streamlined Canva-inspired workspace for pulling the best frame, layering an on-brand overlay, "
    "and exporting thumbnails + social hooks for your next post."
)

with st.sidebar:
    st.header("Brand style")
    palette_name = st.selectbox("Palette", list(PALETTES.keys()), index=0)
    overlay_opacity = st.slider("Overlay strength", 0.3, 0.9, 0.65, step=0.05)
    st.caption("Palettes and overlays help text pop regardless of the underlying frame.")

    st.header("Frame & caption controls")
    interval = st.slider("Frame extraction interval (seconds)", min_value=1, max_value=10, value=2)
    caption_count = st.slider("Caption how many frames?", min_value=1, max_value=5, value=3)
    st.caption("Captions drive suggested headlines and hooks.")

tabs = st.tabs(["Video to thumbnails", "Single image to thumbnail"])

with tabs[0]:
    st.subheader("Upload a video")
    video_file = st.file_uploader("Video file", type=["mp4", "mov", "avi", "mkv"], key="video-upload")

    if video_file:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_video_path = Path(temp_dir) / "upload_video"

            with open(temp_video_path, "wb") as f:
                f.write(video_file.read())

            with st.spinner("Extracting frames..."):
                frames = extract_frames(str(temp_video_path), interval=interval)

        if frames:
            st.success(f"Captured {len(frames)} frame(s). Choose one to style.")
            cols = st.columns(min(5, len(frames)))
            selected_idx = st.radio(
                "Select the hero frame", options=list(range(min(5, len(frames)))), format_func=lambda i: f"Frame {i}", horizontal=True
            )
            for idx, frame in enumerate(frames[:5]):
                cols[idx % len(cols)].image(frame, caption=f"Frame {idx}")

            with st.spinner("Loading BLIP captioner (first run may download weights)..."):
                captioner = load_captioner()

            with st.spinner("Generating social copy suggestions..."):
                captions = run_captioner(captioner, frames, limit=caption_count)

            default_title = captions[0] if captions else "Magnetic headline"
            default_subtitle = captions[1] if len(captions) > 1 else "Quick context to drive clicks"

            st.markdown("### Canva-grade overlay")
            title_text = st.text_input("Hero headline", value=default_title)
            subtitle_text = st.text_input("Support line", value=default_subtitle)

            if st.button("Create thumbnail", type="primary"):
                hero_frame = frames[selected_idx]
                styled = stylize_thumbnail(hero_frame, title_text, subtitle_text, PALETTES[palette_name], overlay_opacity)
                st.image(styled, caption="Thumbnail preview", use_column_width=True)
                st.download_button(
                    "Download PNG",
                    data=to_bytes(styled),
                    file_name="thumbnail.png",
                    mime="image/png",
                )

            st.markdown("### Social copy ideas")
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

with tabs[1]:
    st.subheader("Upload a single image")
    image_file = st.file_uploader("Image file", type=["png", "jpg", "jpeg"], key="image-upload")

    if image_file:
        image = Image.open(image_file).convert("RGB")
        st.image(image, caption="Base image", use_column_width=True)

        with st.spinner("Loading BLIP captioner (first run may download weights)..."):
            captioner = load_captioner()

        caption = run_captioner(captioner, [image], limit=1)[0]
        title_text = st.text_input("Hero headline", value=caption, key="img-title")
        subtitle_text = st.text_input("Support line", value="", key="img-sub")

        if st.button("Create thumbnail from image", type="primary"):
            styled = stylize_thumbnail(image, title_text, subtitle_text, PALETTES[palette_name], overlay_opacity)
            st.image(styled, caption="Thumbnail preview", use_column_width=True)
            st.download_button(
                "Download PNG",
                data=to_bytes(styled),
                file_name="thumbnail.png",
                mime="image/png",
                key="img-download",
            )
    else:
        st.info("Upload a single image to style it with branded overlays.")
