import argparse
import json
from pathlib import Path

import cv2
from rapidocr_onnxruntime import RapidOCR


def clean_text(text):
    return " ".join(str(text).replace("\n", " ").split())


def process(video_path, frames_dir, ocr_dir, engine):
    stem = video_path.stem
    out_json = ocr_dir / f"{stem}.json"
    expected_frames = [frames_dir / f"{stem}_{i}.jpg" for i in range(1, 6)]
    if out_json.exists() and all(path.exists() for path in expected_frames):
        return "skip"

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        return "open-failed"
    count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    duration = count / fps if count else 0
    fractions = (0.10, 0.30, 0.50, 0.70, 0.90)
    rows = []
    for order, fraction in enumerate(fractions, 1):
        cap.set(cv2.CAP_PROP_POS_MSEC, duration * fraction * 1000)
        ok, frame = cap.read()
        if not ok:
            continue
        frame_path = frames_dir / f"{stem}_{order}.jpg"
        encoded_ok, encoded = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 88])
        if not encoded_ok:
            continue
        frame_path.write_bytes(encoded.tobytes())
        result, _ = engine(frame)
        texts = []
        if result:
            for item in result:
                if len(item) >= 2:
                    texts.append(clean_text(item[1]))
        rows.append({"fraction": fraction, "time": round(duration * fraction, 2), "frame": frame_path.name, "ocr": texts})
    cap.release()
    out_json.write_text(json.dumps({"video": video_path.name, "duration": duration, "frames": rows}, ensure_ascii=False, indent=2), encoding="utf-8")
    return len(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--video-dir", default="video")
    parser.add_argument("--frames-dir", default="frames")
    parser.add_argument("--ocr-dir", default="frame_ocr")
    args = parser.parse_args()

    video_dir = Path(args.video_dir)
    frames_dir = Path(args.frames_dir)
    ocr_dir = Path(args.ocr_dir)
    frames_dir.mkdir(parents=True, exist_ok=True)
    ocr_dir.mkdir(parents=True, exist_ok=True)
    engine = RapidOCR()
    files = sorted(video_dir.glob("p*.mp4"))
    for index, path in enumerate(files, 1):
        try:
            print(f"[{index}/{len(files)}] {path.name}: {process(path, frames_dir, ocr_dir, engine)}", flush=True)
        except Exception as exc:
            print(f"[{index}/{len(files)}] {path.name}: ERROR {exc}", flush=True)


if __name__ == "__main__":
    main()
