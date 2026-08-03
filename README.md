# MiniMax H3 Hybrid Cond

ComfyUI custom node for MiniMax H3 conditioning. It supports both reference-to-video (`ref2va` / R2V) and first/last-frame video conditioning (`fl2va` / I2V), including a hybrid mode that uses both in one conditioning payload.

## Install

Copy `minimax_h3_hybrid` into:

```text
ComfyUI/custom_nodes/
```

Restart ComfyUI and search for:

```text
MiniMax H3 Hybrid Cond (R2V + I2V)
```

Required model inputs are the H3 video VAE, H3 audio VAE, and the matching H3 CLIP/text encoder. The node outputs a positive conditioning and an AV latent with native audio.

## Input mapping

| Node input | H3 function | Prompt tag |
|---|---|---|
| `first_frame` | `fl2va` keyframe at frame 0 | Not a Picture tag by default |
| `last_frame` | `fl2va` final keyframe | Not a Picture tag |
| `ref_image_1` | `ref2va` image reference | `<Picture 1>` |
| `ref_image_2` | `ref2va` image reference | `<Picture 2>` |
| `ref_video_1` | `ref2va` video reference | `<Video 1>` |
| `ref_audio_1` | `ref2va` audio reference | `<Audio 1>` |

Reference numbering follows the order of the connected reference inputs. Set `also_ref_first_frame` to `true` only when the first frame should also become the next Picture reference; it is appended after user reference images.

## 1. R2V-only example

Use this when the video should be controlled by reference media without an I2V start frame.

```text
first_frame: empty
last_frame: empty
ref_image_1: cat reference image
ref_image_2: optional character or style reference
also_ref_first_frame: false
```

Prompt:

```text
<Picture 1> is the main cat character. Preserve its identity, face, colors,
clothing, proportions, and silhouette. The cat walks forward and jumps toward
the camera in a cute exaggerated cartoon animation. Use <Picture 2> only for
secondary appearance guidance. Keep the background clean and the motion readable.
```

This uses `minimax_refs` with image reference blocks and `<Picture N>` tags. No keyframe is supplied.

## 2. fl2va / I2V-only example

Use this when the first image must be locked as the opening frame.

```text
first_frame: woman opening image
last_frame: optional final image
ref_image_1: empty
also_ref_first_frame: false
```

Prompt:

```text
Start exactly from the first frame. Preserve the woman's identity, composition,
lighting, background, rendering, and visual style. She slowly looks forward,
then reacts with a cute exaggerated surprise. Keep frame 0 stable and animate
only the requested motion.
```

This uses `minimax_keyframes` for `fl2va`. The first frame is a keyframe, not `<Picture 1>`.

## 3. Hybrid R2V + fl2va example

Use this when a woman image must control the opening/style and a separate cat image must control the cat identity.

```text
first_frame: woman image
last_frame: optional
ref_image_1: cat image
also_ref_first_frame: false
```

Prompt:

```text
The first frame is the authoritative source for the woman's identity, camera,
white background, lighting, rendering, and overall visual style. <Picture 1>
is the authoritative reference for the cat's identity, face, colors, clothing,
proportions, and silhouette. The cat suddenly jumps forward and clings to the
woman's face in a cute, harmless, exaggerated cartoon action. Preserve both
characters and keep the motion readable.
```

This uses both payload sections in one node:

```text
minimax_keyframes = [first_frame, optional last_frame]
minimax_refs      = [ref_image_1, optional other references]
```

The custom runtime patch keeps the latent order aligned with the H3 packed layout:

```text
[keyframe latents] + [reference latents]
```

This avoids the `shape mismatch` that occurs when keyframe latents are overwritten by reference latents.

## Native audio

Connect `ref_audio_1` for an audio reference, or use the H3 audio VAE output for generated native audio. Keep dialogue, sound effects, and timing instructions in the prompt. The node always creates the H3 audio/video latent pair.

## Important settings

- `length` is measured in frames and uses a 24 fps workflow. For approximately 5 seconds use `124` frames.
- `width` and `height` should be multiples of 32.
- `ref_image_size=match` preserves the relative reference image size; `max` limits the reference short edge.
- Do not combine separate H3 I2V and R2V conditioning nodes for the same sample. Use this Hybrid node so the packed layout and latent order remain consistent.
- `negative_constraints` is not required by this node and should only be added to the prompt when explicitly desired.
