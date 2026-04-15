"""CLI for AI motion control provider tools."""

from __future__ import annotations

import argparse
import json

from .clients import KlingMotionClient, MotionToolError, WanAnimateClient


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="motion-tools", description="AI motion control provider CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list-tools", help="List available integrated tools")

    wan = sub.add_parser("submit-wan", help="Submit a Wan 2.7 Animate job")
    wan.add_argument("--prompt", required=True)
    wan.add_argument("--image-url")
    wan.add_argument("--motion-strength", type=float, default=0.6)
    wan.add_argument("--duration-seconds", type=int, default=5)

    kling = sub.add_parser("submit-kling", help="Submit a Kling 3.0 Motion Control job")
    kling.add_argument("--prompt", required=True)
    kling.add_argument("--video-url")
    kling.add_argument("--camera-control", default="smooth-pan")
    kling.add_argument("--motion-intensity", type=float, default=0.5)

    status = sub.add_parser("status", help="Check job status")
    status.add_argument("--provider", choices=["wan", "kling"], required=True)
    status.add_argument("--job-id", required=True)

    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    if args.command == "list-tools":
        print("Wan 2.7 Animate")
        print("Kling 3.0 Motion Control")
        return 0

    try:
        if args.command == "submit-wan":
            client = WanAnimateClient()
            result = client.create_job(
                prompt=args.prompt,
                image_url=args.image_url,
                motion_strength=args.motion_strength,
                duration_seconds=args.duration_seconds,
            )
            print(json.dumps(result, indent=2))
            return 0

        if args.command == "submit-kling":
            client = KlingMotionClient()
            result = client.create_job(
                prompt=args.prompt,
                video_url=args.video_url,
                camera_control=args.camera_control,
                motion_intensity=args.motion_intensity,
            )
            print(json.dumps(result, indent=2))
            return 0

        if args.command == "status":
            if args.provider == "wan":
                result = WanAnimateClient().get_job(args.job_id)
            else:
                result = KlingMotionClient().get_job(args.job_id)
            print(json.dumps(result, indent=2))
            return 0
    except MotionToolError as exc:
        parser.error(str(exc))

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
