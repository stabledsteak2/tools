# AI Motion Control Tools for Hugging Face

This repository now includes **real Python tools** for motion-control workflows, with ready-to-run wrappers for:

- **Wan 2.7 Animate** (job submit + status checks)
- **Kling 3.0 Motion Control** (job submit + status checks)

These tools are designed to connect to real provider endpoints using API keys and base URLs from environment variables.

## Included tools

- `motion-tools list-tools`
- `motion-tools submit-wan --prompt ...`
- `motion-tools submit-kling --prompt ...`
- `motion-tools status --provider wan|kling --job-id ...`

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
motion-tools list-tools
```

## Provider configuration

Set environment variables before running submit/status commands:

```bash
# Wan 2.7 Animate
export WAN27_BASE_URL="https://your-wan-provider.example"
export WAN27_API_KEY="your_wan_api_key"

# Kling 3.0 Motion Control
export KLING30_BASE_URL="https://your-kling-provider.example"
export KLING30_API_KEY="your_kling_api_key"
```

## Example usage

Submit Wan 2.7 Animate job:

```bash
motion-tools submit-wan \
  --prompt "A dancer stepping forward with smooth camera motion" \
  --image-url "https://example.com/source-frame.png" \
  --motion-strength 0.72 \
  --duration-seconds 6
```

Submit Kling 3.0 Motion Control job:

```bash
motion-tools submit-kling \
  --prompt "Keep subject centered while the camera slowly orbits" \
  --video-url "https://example.com/input.mp4" \
  --camera-control smooth-pan \
  --motion-intensity 0.6
```

Check job status:

```bash
motion-tools status --provider wan --job-id JOB_ID_HERE
motion-tools status --provider kling --job-id JOB_ID_HERE
```

## Project structure

- `src/motion_tools/clients.py` – provider API clients.
- `src/motion_tools/cli.py` – command-line interface.
- `tests/test_cli.py` – parser-level sanity tests.
