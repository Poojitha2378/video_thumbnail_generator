"""
Generate a small sample video for testing the Streamlit thumbnail demo.

Usage:
    python scripts/generate_sample_video.py samples/demo.mp4

Creates a 3-second, 640x360 MP4 with color gradients and text overlays.
"""
import sys
from pathlib import Path

import cv2
import numpy as np


def create_demo_video(output_path: Path, fps: int = 10, duration_sec: int = 3):
    width, height = 640, 360
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))

    total_frames = fps * duration_sec
    for frame_idx in range(total_frames):
        # Animated gradient background
        gradient = np.linspace(0, 255, width, dtype=np.uint8)
        gradient = np.tile(gradient, (height, 1))

        # Cycle colors across frames for visual variety
        frame = cv2.merge(
            [gradient,
             np.roll(gradient, frame_idx * 5, axis=1),
             np.roll(gradient, frame_idx * 10, axis=1)]
        )

        # Overlay moving rectangle
        rect_width = 140
        x_pos = (frame_idx * 12) % (width + rect_width) - rect_width
        y_pos = height // 3
        cv2.rectangle(frame, (x_pos, y_pos), (x_pos + rect_width, y_pos + 80), (255, 255, 255), -1)

        # Overlay text
        cv2.putText(
            frame,
            "Sample video for thumbnail testing",
            (40, height - 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (50, 50, 50),
            2,
            cv2.LINE_AA,
        )

        writer.write(frame)

    writer.release()


def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/generate_sample_video.py <output_path>")
        sys.exit(1)

    output_path = Path(sys.argv[1])
    output_path.parent.mkdir(parents=True, exist_ok=True)
    create_demo_video(output_path)
    print(f"Sample video written to {output_path}")


if __name__ == "__main__":
    main()
