#!/usr/bin/env bash
# Idempotent install of video/media tooling used by this environment.
# Sources: yt-dlp (GitHub release), openai-whisper (GitHub), HyperFrames + Remotion (npm).
set -euo pipefail

echo "==> FFmpeg"
if ! command -v ffmpeg >/dev/null 2>&1; then
  sudo apt-get update -qq
  sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq ffmpeg
fi
ffmpeg -version | head -1

echo "==> yt-dlp (GitHub release binary)"
YT_DLP_URL="https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp"
if ! command -v yt-dlp >/dev/null 2>&1; then
  sudo curl -fsSL "$YT_DLP_URL" -o /usr/local/bin/yt-dlp
  sudo chmod a+rx /usr/local/bin/yt-dlp
else
  # Keep binary installs refreshable
  sudo curl -fsSL "$YT_DLP_URL" -o /usr/local/bin/yt-dlp
  sudo chmod a+rx /usr/local/bin/yt-dlp
fi
yt-dlp --version

echo "==> Whisper (openai/whisper from GitHub)"
VENV="${HOME}/.venvs/media-tools"
if [[ ! -x "${VENV}/bin/whisper" ]]; then
  sudo apt-get update -qq
  sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq python3-pip python3-venv
  python3 -m venv "${VENV}"
  # shellcheck disable=SC1091
  source "${VENV}/bin/activate"
  pip install -U pip wheel
  pip install 'git+https://github.com/openai/whisper.git'
  deactivate || true
fi
sudo ln -sf "${VENV}/bin/whisper" /usr/local/bin/whisper
whisper --help >/dev/null
echo "whisper OK"

echo "==> HyperFrames + Remotion CLIs"
NPM_BIN="$(dirname "$(command -v npm)")"
# Prefer nvm node for global installs when present
export PATH="${NPM_BIN}:${PATH}"
if ! command -v hyperframes >/dev/null 2>&1; then
  npm install -g hyperframes
fi
if ! command -v remotion >/dev/null 2>&1; then
  npm install -g @remotion/cli
fi
# Ensure /usr/local/bin shims for login shells / non-nvm PATH
HF_BIN="$(command -v hyperframes)"
REM_BIN="$(command -v remotion)"
sudo ln -sf "${HF_BIN}" /usr/local/bin/hyperframes
sudo ln -sf "${REM_BIN}" /usr/local/bin/remotion

echo "==> Versions"
printf 'ffmpeg:      '; ffmpeg -version | head -1
printf 'yt-dlp:      '; yt-dlp --version
printf 'whisper:     '; command -v whisper
printf 'hyperframes: '; hyperframes --version 2>&1 | head -1
printf 'remotion:    '; remotion --version 2>&1 | head -1
echo "Done."
