import argparse
import glob
import json
import os
import time
from pathlib import Path


def add_cuda_paths():
    roots = [
        r"C:/Users/*/AppData/Roaming/Python/Python313/site-packages/nvidia/*/bin",
        r"C:/Users/*/AppData/Local/Programs/Python/Python313/Lib/site-packages/nvidia/*/bin",
    ]
    bins = [p for pattern in roots for p in glob.glob(pattern)]
    if bins:
        os.environ["PATH"] = ";".join(bins) + ";" + os.environ.get("PATH", "")
        for path in bins:
            try:
                os.add_dll_directory(path)
            except (FileNotFoundError, OSError):
                pass


def transcribe_one(model, audio_path, out_dir):
    out_json = out_dir / f"{audio_path.stem}.json"
    out_txt = out_dir / f"{audio_path.stem}.txt"
    if out_json.exists() and out_txt.exists():
        return "skip"

    segments, info = model.transcribe(
        str(audio_path),
        language="zh",
        task="transcribe",
        beam_size=5,
        vad_filter=True,
        vad_parameters={"min_silence_duration_ms": 500},
        condition_on_previous_text=True,
    )
    rows = []
    for seg in segments:
        text = seg.text.strip()
        if text:
            rows.append({"start": round(seg.start, 2), "end": round(seg.end, 2), "text": text})

    payload = {
        "file": audio_path.name,
        "duration": getattr(info, "duration", None),
        "language": getattr(info, "language", "zh"),
        "segments": rows,
    }
    out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    out_txt.write_text("\n".join(f"[{r['start']:07.2f}-{r['end']:07.2f}] {r['text']}" for r in rows), encoding="utf-8")
    return len(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--audio-dir", default="audio")
    parser.add_argument("--out-dir", default="transcripts")
    parser.add_argument("--model", default="small")
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--compute-type", default="float16")
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--end", type=int, default=9999)
    args = parser.parse_args()

    add_cuda_paths()
    from faster_whisper import WhisperModel

    audio_dir = Path(args.audio_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    files = [
        path for path in sorted(audio_dir.glob("p*.mp3"))
        if args.start <= int(path.stem[1:]) <= args.end
    ]
    if not files:
        raise SystemExit(f"No mp3 files found in {audio_dir}")

    print(f"Loading Whisper model {args.model} on {args.device}...")
    model = WhisperModel(args.model, device=args.device, compute_type=args.compute_type)
    started = time.time()
    for index, audio_path in enumerate(files, 1):
        t0 = time.time()
        try:
            result = transcribe_one(model, audio_path, out_dir)
            print(f"[{index}/{len(files)}] {audio_path.name}: {result} ({time.time() - t0:.1f}s)", flush=True)
        except Exception as exc:
            print(f"[{index}/{len(files)}] {audio_path.name}: ERROR {exc}", flush=True)
    print(f"Finished in {(time.time() - started) / 60:.1f} min")


if __name__ == "__main__":
    main()
