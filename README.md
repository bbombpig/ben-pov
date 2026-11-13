# ben-pov

POV workspace for programmatic video and media tooling.

## Tooling

| Tool | Status | Source |
|------|--------|--------|
| **FFmpeg** | System package | Ubuntu `ffmpeg` |
| **yt-dlp** | `/usr/local/bin/yt-dlp` | [yt-dlp/yt-dlp](https://github.com/yt-dlp/yt-dlp) GitHub release |
| **Whisper** | `/usr/local/bin/whisper` | [openai/whisper](https://github.com/openai/whisper) via venv |
| **HyperFrames** | `hyperframes` CLI | [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) (npm) |
| **Remotion** | `remotion` CLI | [@remotion/cli](https://www.npmjs.com/package/@remotion/cli) |

Install or refresh everything:

```bash
./scripts/install-media-tools.sh
```

HyperFrames agent skills live under `.agents/skills/` (installed from the HyperFrames GitHub repo).
