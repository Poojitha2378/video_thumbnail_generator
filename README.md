# Video Thumbnail Generator

Automated Social Video Thumbnail & Copy Generator built with Streamlit, OpenCV, and Hugging Face Transformers (BLIP). The UI now mirrors Canva-style thumbnail polish with branded overlays and social-ready copy.

## Features
- Canva-inspired layout with palettes, overlays, and headline/subtitle fields for creator-ready thumbnails.
- Upload an MP4/MOV/AVI/MKV video and extract frames at a chosen interval.
- Preview and select the best of the first five frames to style.
- Generate BLIP-powered social captions for a configurable number of frames, plus a headline suggestion.
- Style a single uploaded image with the same branded overlays (no video required).
- Download the final thumbnail as PNG and captions as a text file.

## Getting Started
Follow these steps to run the app on your local computer.

1) **Install Python 3.9+**
   - Confirm with `python --version`. Use `python3` instead of `python` on macOS/Linux if needed.

2) **Create and activate a virtual environment (recommended):**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

3) **Install dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
   > The first run will download the BLIP captioning model from Hugging Face; keep an internet connection open.

4) **(Optional) Generate a small demo video for local testing:**
   ```bash
   python scripts/generate_sample_video.py samples/demo.mp4
   ```

5) **Run the Streamlit app:**
   ```bash
   streamlit run app.py
   ```
   Streamlit will print a local URL (e.g., http://localhost:8501). Open it in your browser.

6) **Test the flow:**
   - Upload a short video or the generated `samples/demo.mp4`.
   - Pick a palette and overlay strength in the sidebar.
   - Use the frame interval and caption sliders to refine the extraction/copy.
   - Select a hero frame, edit the headline/subtitle, and click **Create thumbnail** for the polished preview.
   - Download the PNG thumbnail and captions text.

7) **Image-only mode (no video):**
   - Switch to the “Single image to thumbnail” tab.
   - Upload a JPG/PNG, tweak the headline/subtitle, and export the styled PNG.

## Demo Suggestions
- Record a short screen capture of the Streamlit UI: upload, frame extraction, and caption output.
- If you deploy to Streamlit Community Cloud, share the public app link along with your demo.
- For a quick test, use the generated `samples/demo.mp4` and set the slider interval to 2 seconds.
