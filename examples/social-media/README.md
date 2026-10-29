# Social media examples

- [Demonstration video](demo.mp4): a 45-second video showing the pet in use on the desktop, all nine animations and sixteen look directions, with Chinese captions and piano music.
- [Edited screen recording](screen-recording-edited.mp4): the 7-second opening clip, trimmed and framed in portrait format, without music.
- [Cover image](cover.png): artwork for sharing the pet.

Both videos use H.264 at 1080 × 1920 and 30 fps. The demo also includes stereo AAC audio and a guide to triggering the animations, which you can pause to read. The guide reflects how the app behaved in September 2026; controls may differ in later versions.

## Generate the video

You will need Python 3 with `Pillow`, FFmpeg with the `libx264` and `aac` encoders on your `PATH`, and a Chinese font. On macOS, the renderer looks for PingFang SC in the system font collection (face index 3).

Run this command from the repository root:

```sh
python3 examples/social-media/scripts/render_demo.py
```

This rebuilds and replaces `demo.mp4` using the repository’s pet sprites and the two recordings in this directory. It leaves the opening clip and cover unchanged and needs no network connection.

Options:

- `--output /tmp/demo.mp4`: save the video elsewhere.
- `--preview`: save a `.jpg` contact sheet instead of the full video. Requires FFmpeg.
- `--work-dir /tmp/dafeiyu-demo-build`: keep intermediate files, the contact sheet and chapter metadata. These are deleted after rendering unless you specify a work directory.
- `--font /path/to/font.ttf --font-index 0`: choose a font and face index for the generated scenes. This does not change the text in the opening clip. You can also set the font path with `DEMO_FONT`.

## Recordings

The [edited screen recording](screen-recording-edited.mp4) was captured with CleanShot on 30 October 2026. It has already been trimmed and framed for this video, so you do not need the original recording to rebuild the demo.

The [piano recording](merry-go.mp3) is Kevin MacLeod’s “Merry Go”, downloaded from the [official source](https://incompetech.com/music/royalty-free/mp3-royaltyfree/Merry%20Go.mp3). The [track listing](https://incompetech.com/music/royalty-free/index.html?isrc=USUAN1100731) identifies it as piano music licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The demo uses 00:00–00:45, with loudness normalisation and fades at both ends.

## Credits when sharing

Include the following music credit in the post caption or accompanying credits:

> Music: “Merry Go” by Kevin MacLeod (incompetech.com), licensed under CC BY 4.0: https://creativecommons.org/licenses/by/4.0/. Excerpt 00:00–00:45; loudness normalised and fades added. Source: https://incompetech.com/music/royalty-free/index.html?isrc=USUAN1100731

Character credits and non-commercial share-alike terms also apply to the cover and video. Include or link to the [character and artwork credits](../../ATTRIBUTION.md), which name the original creators and link to [dsh-pet](https://github.com/PC2005-cloud/dsh-pet). The separate music licence does not remove these artwork conditions.
