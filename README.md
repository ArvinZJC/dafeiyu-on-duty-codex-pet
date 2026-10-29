# Dafeiyu On Duty

An unofficial, fan-made Codex pet based on **大肥鱼** (Dafeiyu, “Big Fat Fish”), also known as **鲸鱼娘** (Whale Girl), a DeepSeek character created by the Chinese community. With her blue hair, frilled maid outfit and whale tail, Dafeiyu On Duty keeps you company with gentle waves, small hops, thoughtful pauses and sixteen look directions.

The character design is adapted from [dsh-pet](https://github.com/PC2005-cloud/dsh-pet). This is a fan project, not an official DeepSeek or OpenAI character.

## Get the pet

Find Dafeiyu On Duty on either pet-sharing site:

- [codex-pets.net](https://codex-pets.net/#/pets/dafeiyu-on-duty)
- [codex-pet.org](https://codex-pet.org/pets/dafeiyu-on-duty)

## Use a cloud pet

1. Download the raw [`spritesheet.webp`](spritesheet.webp). In ChatGPT’s **Settings → Personalization → Pet**, choose **Upload pet**, or ask the Pets plugin to upload it as **Dafeiyu On Duty**. If it is already in your cloud pet library, skip this step.
2. Select **Dafeiyu On Duty** in the pet picker. In the desktop app, open **Settings → Pets** (or **Mini & Pets**, depending on the version).

No local `pets` folder or `pet.json` is needed for a cloud pet. To update it, replace the sprite sheet on the existing cloud pet through the pet editor or Pets plugin.

The [official guide](https://learn.chatgpt.com/docs/pets) documents uploads and says local pets do not automatically sync to the web. Our desktop checks found separate local and cloud copies; replacing local files left the cloud copy unchanged.

## Local installation (alternative)

1. Clone this repository, or download the raw [`pet.json`](pet.json) and [`spritesheet.webp`](spritesheet.webp) files.
2. Create a `dafeiyu-on-duty` folder inside your Codex home directory’s `pets` folder. By default, this is `~/.codex/pets/dafeiyu-on-duty/` on macOS and `%USERPROFILE%\.codex\pets\dafeiyu-on-duty\` on Windows. If you use a custom `CODEX_HOME`, use its `pets` folder instead.
3. Copy both files into that folder:

   ```text
   pets/
   └── dafeiyu-on-duty/
       ├── pet.json
       └── spritesheet.webp
   ```

4. Open **Settings → Mini & Pets**, click the refresh/reload button, then select **Dafeiyu On Duty**.

Only these two files are needed for local installation. To update a local pet, replace both files and refresh the pet picker again.

## Animation examples

View the gallery online: [Dafeiyu On Duty · Animation examples](https://codex-pets.isarvin.com/dafeiyu-on-duty/).

To view it offline, clone this repository and open [`examples/index.html`](examples/index.html) in your browser. The gallery includes:

- **Nine animations:** resting, moving right, moving left, hello wave, little hop, sheepish reaction, curious head tilt, deep in thought and thoughtful check.
- **Frame-by-frame previews:** a separate GIF and a numbered frame sheet for each animation.
- **Sixteen look directions:** an individual direction selector and a clockwise preview.
- **Playback controls:** pause and play, with reduced-motion preferences respected.
- **Automatic light and dark themes:** follows your system preference. Animation previews retain their original light backgrounds.

Standard animation previews use Codex’s frame timings. The look-around preview is an illustrative sweep; in Codex, gaze is controlled by the app. The gallery plays without audio and requires no external resources.

## Social media examples

Watch the [demonstration video](examples/social-media/demo.mp4) or download the [cover image](examples/social-media/cover.png). The 45-second video shows the pet in use on the desktop, followed by its animations in a duty-desk layout, with Chinese captions and a licensed piano soundtrack.

See [social media examples](examples/social-media/README.md) for details and instructions on rebuilding the video.

## Credits and licence

The original character **溟月** was created by [上善无形](https://space.bilibili.com/4456176); the DeepSeek maid Whale Girl design is by [ZipZipPipe](https://space.bilibili.com/4168597). Reference artwork comes from [PC2005-cloud/dsh-pet](https://github.com/PC2005-cloud/dsh-pet).

The character artwork and its derivatives are licensed under **CC BY-NC-SA 4.0**: attribution is required, commercial use is prohibited and adaptations must use the same licence. The project's code and documentation are MIT-licensed. See [character and artwork credits](ATTRIBUTION.md) for the source references and adaptation details.
