# MiniMax H3 Hybrid Cond

ComfyUI custom node that combines MiniMax H3 reference conditioning (R2V) with first/last keyframe conditioning (I2V) in one positive conditioning payload.

## Features

- Reference images: `<Picture 1>`, `<Picture 2>`, ...
- Reference videos: `<Video 1>`, ...
- Reference audio support
- Optional first and last I2V keyframes
- Native H3 audio/video latent output
- Per-reference sizing: `match` or `max`
- Runtime payload patch kept inside this custom node; no permanent core patch required

## Install

Copy `minimax_h3_hybrid` into:

```text
ComfyUI/custom_nodes/
```

Restart ComfyUI, then search for:

```text
MiniMax H3 Hybrid Cond (R2V + I2V)
```

## Prompt references

Connect `ref_image_1` and use:

```text
The character in <Picture 1> walks forward.
```

`first_frame` is an I2V keyframe. It is not a Picture reference unless `also_ref_first_frame` is enabled.

## Important

Use one Hybrid node rather than combining separate H3 I2V and R2V conditioning nodes. The H3 packed layout expects keyframe and reference latents in a matching order.

Tested against the `minimax_h3` ComfyUI branch.
