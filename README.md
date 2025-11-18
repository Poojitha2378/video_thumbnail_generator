# Video Thumbnail Generator

Automated Social Video Thumbnail & Copy Generator built with Streamlit, OpenCV, and Hugging Face Transformers (BLIP).

## Features
- Upload an MP4/MOV/AVI/MKV video and extract frames at a chosen interval.
- Preview up to five thumbnail candidates directly in the UI.
- Generate BLIP-powered social captions for a configurable number of frames.
- Download the generated captions as a text file.

## Getting Started
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. (Optional) Generate a small demo video for local testing:
   ```bash
   python scripts/generate_sample_video.py samples/demo.mp4
   ```
3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
4. Upload a short video (or `samples/demo.mp4`) to see extracted thumbnails and suggested captions.

## Demo Suggestions
- Record a short screen capture of the Streamlit UI: upload, frame extraction, and caption output.
- If you deploy to Streamlit Community Cloud, share the public app link along with your demo.
- For a quick test, use the generated `samples/demo.mp4` and set the slider interval to 2 seconds.
