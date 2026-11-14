#!/usr/bin/env python3
"""Beat-synced Instagram reel polish for Upside Down clip."""
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "source_large.mp4"
OUT = ROOT / "out" / "upside_down_trial.mp4"

STRONG = [0.396, 1.238, 2.07, 2.496, 2.912, 3.192, 3.749, 4.3, 4.731, 5.142, 5.688, 6.535, 7.657, 8.214, 8.76]
FLASH = [2.07, 4.3, 8.76]
FLIP_START, SPIN_IN, HOLD, SPIN_OUT = 4.865, 0.18, 0.42, 0.18
W, H, FPS = 1080, 1920, 30

def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    zoom_add = "+".join(f"max(0\\,1-abs(t-{b})/0.1)" for b in STRONG)
    zoom = f"1+min(0.12\\,0.10*({zoom_add}))"
    a_hold = FLIP_START + SPIN_IN
    a_out = a_hold + HOLD
    a_done = a_out + SPIN_OUT
    rot = (
        f"if(lt(t\\,{FLIP_START})\\,0\\,"
        f"if(lt(t\\,{a_hold})\\,PI*(t-{FLIP_START})/{SPIN_IN}\\,"
        f"if(lt(t\\,{a_out})\\,PI\\,"
        f"if(lt(t\\,{a_done})\\,PI*(1-(t-{a_out})/{SPIN_OUT})\\,0))))"
    )
    flash = "+".join(f"max(0\\,1-abs(t-{b})/0.05)" for b in FLASH)
    vf = (
        f"[0:v]fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
        f"eq=contrast=1.08:brightness=0.03:saturation=1.22:gamma=0.96,"
        f"unsharp=5:5:0.6:5:5:0.0,"
        f"scale=w='iw*({zoom})':h='ih*({zoom})':eval=frame,crop={W}:{H},"
        f"rotate='{rot}':ow={W}:oh={H}:c=black@0,"
        f"eq=brightness='0.18*min(1\\,{flash})',"
        f"drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
        f"text='UPSIDE DOWN':fontsize=72:fontcolor=white:borderw=3:bordercolor=black@0.35:"
        f"x=(w-text_w)/2:y=h*0.18:enable='between(t,0.15,1.55)',"
        f"drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:"
        f"text='boy you turn me':fontsize=36:fontcolor=white@0.92:"
        f"x=(w-text_w)/2:y=h*0.24:enable='between(t,0.55,1.55)',"
        f"format=yuv420p[v]"
    )
    cmd = [
        "ffmpeg","-y","-i",str(SRC),"-filter_complex",vf,
        "-map","[v]","-map","0:a","-af","loudnorm=I=-14:TP=-1.5:LRA=11",
        "-c:v","libx264","-preset","medium","-crf","18","-profile:v","high",
        "-c:a","aac","-b:a","192k","-movflags","+faststart","-t","9.067",str(OUT),
    ]
    subprocess.check_call(cmd)
    print("wrote", OUT)

if __name__ == "__main__":
    main()
