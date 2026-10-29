#!/usr/bin/env python3
"""Render Dafeiyu's duty-desk video from the packaged artwork."""

import argparse
from contextlib import ExitStack
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from PIL import Image, ImageDraw, ImageFont

ASSETS = Path(__file__).resolve().parents[1]
ROOT = ASSETS.parents[1]
W, H, FPS, DURATION = 1080, 1920, 30, 45
CREAM, BLUE, INK, GREY = "#f6f2e8", "#254cb3", "#19365b", "#69778b"
CHAPTERS = [
    (0, "桌面实录"),
    (7, "今日到岗"),
    (11, "桌边巡游"),
    (15, "认真值班"),
    (21, "小小回应"),
    (25, "视线展示"),
    (33, "互动指南"),
    (40, "陪伴继续"),
]


def run(args):
    subprocess.run(args, check=True)


class Desk:
    def __init__(self, font, index, work):
        self.font = font
        self.index = index
        self.fonts = {}
        self.work = work
        self.atlas = Image.open(ROOT / "spritesheet.webp").convert("RGBA")
        self.animations = json.loads((ROOT / "examples/animations.json").read_text())
        self.cache = {}
        self.bases = {}

    def text(self, im, xy, text, size=36, colour=INK, anchor="la"):
        if size not in self.fonts:
            self.fonts[size] = ImageFont.truetype(self.font, size, index=self.index)
        ImageDraw.Draw(im).text(
            xy, text, font=self.fonts[size], fill=colour, anchor=anchor
        )

    def base(self, number, title, sub):
        key = number, title, sub
        if key in self.bases:
            return self.bases[key].copy()
        im = Image.new("RGB", (W, H), CREAM)
        d = ImageDraw.Draw(im)
        d.rectangle((0, 0, 22, H), fill=BLUE)
        for y in range(490, 1620, 70):
            d.line((90, y, 990, y), fill="#e3e0d8", width=2)
        d.line((120, 475, 120, 1620), fill="#ccc5b7", width=2)
        self.text(im, (80, 83), "DAFEIYU ON DUTY", 30, BLUE)
        self.text(im, (998, 87), number, 26, BLUE, "ra")
        d.line((80, 150, 1000, 150), fill=BLUE, width=3)
        self.text(im, (80, 208), title, 72)
        self.text(im, (84, 320), sub, 30, GREY)
        d.rectangle((80, 1670, 1000, 1673), fill=BLUE)
        self.text(im, (80, 1730), "大肥鱼值班中", 34, BLUE)
        self.text(im, (80, 1790), "非官方 Codex 桌宠", 26, GREY)
        self.text(im, (1000, 1740), "值班日志", 25, GREY, "ra")
        self.bases[key] = im.copy()
        return im

    def pose(self, row, t):
        durations = self.animations[row]["durations_ms"]
        ms = t * 1000 % sum(durations)
        for i, duration in enumerate(durations):
            ms -= duration
            if ms < 0:
                return i
        return len(durations) - 1

    def pet(self, im, row, col, x, y, height=650):
        width = round(height * 192 / 208)
        key = row, col, height
        if key not in self.cache:
            self.cache[key] = self.atlas.crop(
                (col * 192, row * 208, (col + 1) * 192, (row + 1) * 208)
            ).resize((width, height), Image.Resampling.LANCZOS)
        p = self.cache[key]
        im.paste(p, (round(x - width / 2), round(y)), p)

    def badge(self, im, title, subtitle):
        d = ImageDraw.Draw(im)
        d.rectangle((175, 1400, 965, 1565), fill=CREAM, outline=BLUE, width=3)
        self.text(im, (215, 1425), title, 42, BLUE)
        self.text(im, (215, 1495), subtitle, 28, GREY)

    def frame(self, t):
        if t < 7:
            return Image.open(self.work / "intro.png").convert("RGB")
        elif t < 11:
            u = t - 7
            row = 0 if u < 2 else 4
            local = u if u < 2 else u - 2
            im = self.base("01 / 到岗", "今天也来陪你", "安静待着，偶尔开心一跳")
            self.pet(im, row, self.pose(row, local), 570, 600)
            self.badge(
                im, "安静待机" if row == 0 else "轻轻一跳", "不用赶路，先陪你待一会儿。"
            )
        elif t < 15:
            u = t - 11
            row = 1 if u < 2 else 2
            phase = (u % 2) / 2
            x = 320 + 440 * phase if row == 1 else 760 - 440 * phase
            im = self.base(
                "02 / 巡游", "换个位置，继续陪你", "桌边散散步，陪你换换心情"
            )
            ImageDraw.Draw(im).line((170, 1250, 970, 1250), fill=BLUE, width=3)
            self.pet(im, row, self.pose(row, u % 2), x, 680, 560)
            self.badge(
                im,
                "向右出发 →" if row == 1 else "← 转身回来",
                "从桌面这一边，走到另一边。",
            )
        elif t < 21:
            u = t - 15
            i = min(2, int(u // 2))
            row = [7, 6, 8][i]
            title = ["认真想一想", "歪头等你", "再检查一遍"][i]
            im = self.base(
                "03 / 值班", "忙的时候，她也在", "思考、等待、检查，都有小动作"
            )
            self.pet(im, row, self.pose(row, u % 2), 570, 580)
            self.badge(
                im,
                title,
                ["慢慢想，总会有头绪。", "下一步，等你来决定。", "收尾也要认真一点。"][
                    i
                ],
            )
        elif t < 25:
            u = t - 21
            row = 3 if u < 2 else 5
            im = self.base("04 / 回应", "不止会安静站着", "挥挥手，也会有点不好意思")
            self.pet(im, row, self.pose(row, u % 2), 570, 580)
            self.badge(
                im,
                "你好呀" if row == 3 else "有点不好意思",
                "每个状态，都有自己的回应。",
            )
        elif t < 33:
            u = t - 25
            direction = min(15, int(u * 2))
            row = 9 + direction // 8
            col = direction % 8
            im = self.base(
                "05 / 视线",
                "十六个方向，慢慢看一圈",
                "顺时针逐一展示 · 实际视线由应用控制",
            )
            d = ImageDraw.Draw(im)
            for i in range(16):
                a = i * math.tau / 16
                x = 570 + 360 * math.sin(a)
                y = 940 - 360 * math.cos(a)
                r = 12 if i == direction else 5
                d.ellipse(
                    (x - r, y - r, x + r, y + r),
                    fill=BLUE if i == direction else "#b7c3db",
                )
            self.pet(im, row, col, 570, 650, 580)
            self.badge(
                im, f"视线记录 / {direction+1:02d} · 16", "换个方向，看看她的样子。"
            )
        elif t < 40:
            im = self.base(
                "06 / 互动指南",
                "这些时候，她会回应",
                "可暂停阅读 · 2026 年 9 月版本行为参考",
            )
            rows = [
                ("悬停", "开心跳跃"),
                ("向左 / 右拖动", "左右走动"),
                ("初次唤醒提醒", "向你挥手"),
                ("任务进行中", "认真思考"),
                ("需要输入", "歪头等你"),
                ("失败或受阻", "有点不好意思"),
                ("任务完成", "检查结果"),
                ("没有活动提醒", "安静陪伴"),
            ]
            d = ImageDraw.Draw(im)
            d.rectangle((150, 465, 995, 1640), fill=CREAM)
            for i, (trigger, reaction) in enumerate(rows):
                y = 490 + i * 112
                self.text(im, (175, y), trigger, 32, GREY)
                self.text(im, (955, y), reaction, 36, BLUE, "ra")
                d.line((175, y + 78, 955, y + 78), fill="#d5d9e3", width=2)
            self.text(im, (175, 1440), "视线跟随快捷聊天的输入光标，或", 28)
            self.text(im, (175, 1490), "Computer Use 的操作光标，不跟随普通鼠标。", 28)
            self.text(im, (175, 1570), "实际表现以你安装的应用版本为准", 26, GREY)
        else:
            im = self.base("07 / 陪伴", "大肥鱼，陪你慢慢来", "今日值班，陪伴继续")
            self.pet(im, 3, self.pose(3, t - 40), 570, 500, 620)
            self.badge(im, "九种动画 · 十六个视线方向", "忙也好，闲也好，她都在。")
        d = ImageDraw.Draw(im)
        d.rectangle((80, 1855, 1000, 1861), fill="#d9dce0")
        d.rectangle((80, 1855, 80 + 920 * min(t / DURATION, 1), 1861), fill=BLUE)
        return im


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ASSETS / "demo.mp4")
    parser.add_argument("--preview", action="store_true")
    parser.add_argument("--work-dir", type=Path)
    parser.add_argument("--font", default=os.environ.get("DEMO_FONT"))
    parser.add_argument("--font-index", type=int, default=3)
    args = parser.parse_args()
    if not args.font:
        found = sorted(
            Path("/System/Library/AssetsV2/com_apple_MobileAsset_Font8").glob(
                "*/AssetData/PingFang.ttc"
            )
        )
        if not found:
            parser.error("Supply a Chinese font with --font and --font-index.")
        args.font = str(found[0])
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        parser.error("FFmpeg is required.")
    output = args.output.resolve()
    if output in {
        (ASSETS / "screen-recording-edited.mp4").resolve(),
        (ASSETS / "cover.png").resolve(),
        (ASSETS / "merry-go.mp3").resolve(),
    }:
        parser.error("Output must not overwrite a source asset.")
    output.parent.mkdir(parents=True, exist_ok=True)
    with ExitStack() as stack:
        work = args.work_dir or Path(
            stack.enter_context(tempfile.TemporaryDirectory(prefix="dafeiyu-demo-"))
        )
        work.mkdir(parents=True, exist_ok=True)
        intro = work / "opening.mp4"
        shutil.copyfile(ASSETS / "screen-recording-edited.mp4", intro)
        run(
            [
                ffmpeg,
                "-hide_banner",
                "-loglevel",
                "error",
                "-y",
                "-ss",
                "1",
                "-i",
                str(intro),
                "-frames:v",
                "1",
                str(work / "intro.png"),
            ]
        )
        desk = Desk(args.font, args.font_index, work)
        moments = [0, 8, 10, 12, 14, 16, 18, 20, 22, 24, 27, 31, 36, 42]
        contact = Image.new("RGB", (270 * 7, 480 * 2), "white")
        for i, t in enumerate(moments):
            contact.paste(
                desk.frame(t).resize((270, 480)), ((i % 7) * 270, (i // 7) * 480)
            )
        contact.save(work / "review.jpg", quality=95)
        chapters = [
            {
                "title": title,
                "start": start,
                "duration": (CHAPTERS[i + 1][0] if i + 1 < len(CHAPTERS) else DURATION)
                - start,
            }
            for i, (start, title) in enumerate(CHAPTERS)
        ]
        (work / "manifest.json").write_text(
            json.dumps(
                {
                    "width": W,
                    "height": H,
                    "fps": FPS,
                    "duration": DURATION,
                    "chapters": chapters,
                    "music": {
                        "title": "Merry Go",
                        "artist": "Kevin MacLeod",
                        "licence": "CC BY 4.0",
                        "start": 0,
                        "duration": DURATION,
                    },
                    "recording": {
                        "source": "screen-recording-edited.mp4",
                        "duration": CHAPTERS[1][0],
                    },
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        if args.preview:
            target = output.with_suffix(".jpg")
            if target != (work / "review.jpg").resolve():
                shutil.copyfile(work / "review.jpg", target)
            return
        silent = work / "body.mp4"
        command = [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-f",
            "rawvideo",
            "-pix_fmt",
            "rgb24",
            "-s",
            "1080x1920",
            "-r",
            "30",
            "-i",
            "-",
            "-an",
            "-c:v",
            "libx264",
            "-preset",
            "fast",
            "-crf",
            "18",
            "-pix_fmt",
            "yuv420p",
            "-video_track_timescale",
            "15360",
            str(silent),
        ]
        proc = subprocess.Popen(command, stdin=subprocess.PIPE)
        try:
            for i in range(7 * FPS, DURATION * FPS):
                proc.stdin.write(desk.frame(i / FPS).tobytes())
                if i % 300 == 0:
                    print(f"Rendered {i//FPS}/{DURATION}s", flush=True)
        finally:
            proc.stdin.close()
        if proc.wait():
            raise RuntimeError("Video encoding failed.")
        (work / "segments.txt").write_text("file 'opening.mp4'\nfile 'body.mp4'\n")
        run(
            [
                ffmpeg,
                "-hide_banner",
                "-loglevel",
                "error",
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(work / "segments.txt"),
                "-i",
                str(ASSETS / "merry-go.mp3"),
                "-filter_complex",
                "[1:a]atrim=start=0:end=45,asetpts=PTS-STARTPTS,loudnorm=I=-20:TP=-2:LRA=7,afade=t=in:d=0.6,afade=t=out:st=42:d=3[a]",
                "-map",
                "0:v",
                "-map",
                "[a]",
                "-c:v",
                "copy",
                "-c:a",
                "aac",
                "-b:a",
                "192k",
                "-ar",
                "48000",
                "-ac",
                "2",
                "-t",
                "45",
                "-movflags",
                "+faststart",
                str(output),
            ]
        )
        print(f"Rendered {output}", flush=True)


if __name__ == "__main__":
    main()
