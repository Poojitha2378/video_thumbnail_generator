# Video Thumbnail Generator

Automated Social Video Thumbnail & Copy Generator built with Streamlit, OpenCV, and Hugging Face Transformers (BLIP).

## Features
- Upload an MP4/MOV/AVI/MKV video and extract frames at a chosen interval.
- Preview up to five thumbnail candidates directly in the UI.
- Generate BLIP-powered social captions for a configurable number of frames.
- Download the generated captions as a text file.

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
   - Use the sidebar sliders to adjust frame interval and caption count.
   - View the first five extracted frames and their generated captions.
   - Click “Download captions” to save the suggestions as a text file.

## Demo Suggestions
- Record a short screen capture of the Streamlit UI: upload, frame extraction, and caption output.
- If you deploy to Streamlit Community Cloud, share the public app link along with your demo.
- For a quick test, use the generated `samples/demo.mp4` and set the slider interval to 2 seconds.
