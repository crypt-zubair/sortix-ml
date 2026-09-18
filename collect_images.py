"""
Quick webcam capture tool for SORTIX dataset collection.
Run this once per class, changing CLASS_NAME each time.

Controls:
  SPACE = save current frame
  q     = quit

Usage:
  python collect_images.py --class dry
"""
import cv2
import os
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument("--class", dest="cls", required=True,
                     choices=["dry", "wet", "mixed", "sanitary"])
parser.add_argument("--out", default="data/raw")
args = parser.parse_args()

save_dir = os.path.join(args.out, args.cls)
os.makedirs(save_dir, exist_ok=True)

existing = [f for f in os.listdir(save_dir) if f.endswith(".jpg")]
counter = len(existing)

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Could not open webcam. Check index (try 1 instead of 0) or permissions.")

print(f"Collecting for class: {args.cls}")
print(f"Saving to: {save_dir}")
print("SPACE = save frame | q = quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    display = frame.copy()
    cv2.putText(display, f"Class: {args.cls} | Saved: {counter}",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.imshow("SORTIX Dataset Collector", display)

    key = cv2.waitKey(1) & 0xFF
    if key == ord(" "):
        fname = os.path.join(save_dir, f"{args.cls}_{counter:04d}_{int(time.time())}.jpg")
        cv2.imwrite(fname, frame)
        counter += 1
        print(f"Saved {fname}")
    elif key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
print(f"Done. {counter} images saved for class '{args.cls}'.")