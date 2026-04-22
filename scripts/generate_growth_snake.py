import math
import os
import subprocess
from pathlib import Path


def get_commit_count() -> int:
    """Return commit count from the current repository."""
    try:
        out = subprocess.check_output(
            ["git", "rev-list", "--count", "HEAD"],
            text=True,
        ).strip()
        return max(1, int(out))
    except Exception:
        return 1


def build_points(segments: int, width: int, height: int) -> list[tuple[float, float]]:
    """Build a wave-like snake body with N segments."""
    left_pad = 40
    right_pad = 40
    usable_w = max(100, width - left_pad - right_pad)
    base_y = height * 0.55
    amp = min(28, max(12, height * 0.14))

    points: list[tuple[float, float]] = []
    for i in range(segments):
        t = i / max(1, segments - 1)
        x = left_pad + usable_w * t
        y = base_y + amp * math.sin(t * math.pi * 3.2)
        points.append((x, y))
    return points


def main() -> None:
    commits = get_commit_count()

    # Grows by commit while keeping SVG lightweight.
    segments = min(260, 8 + commits)
    width, height = 900, 180
    body = build_points(segments, width, height)

    out_dir = Path("dist")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "growth-snake.svg"

    parts: list[str] = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Growth snake">'
    )
    parts.append("<defs>")
    parts.append(
        '<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#0b1220"/><stop offset="100%" stop-color="#111827"/></linearGradient>'
    )
    parts.append(
        '<linearGradient id="snake" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#22c55e"/><stop offset="100%" stop-color="#84cc16"/></linearGradient>'
    )
    parts.append("</defs>")
    parts.append(f'<rect x="0" y="0" width="{width}" height="{height}" fill="url(#bg)" rx="18" ry="18"/>')

    parts.append('<text x="24" y="34" font-family="Verdana, sans-serif" font-size="20" fill="#e5e7eb">Snake XP</text>')
    parts.append(
        f'<text x="24" y="58" font-family="Verdana, sans-serif" font-size="14" fill="#93c5fd">Commits eaten: {commits}</text>'
    )

    for i, (x, y) in enumerate(body):
        r = 5.5 if i < len(body) - 1 else 7.2
        opacity = 0.35 + 0.65 * (i / max(1, len(body) - 1))
        parts.append(
            f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" fill="url(#snake)" opacity="{opacity:.3f}"/>'
        )

    head_x, head_y = body[-1]
    parts.append(f'<circle cx="{head_x + 2:.2f}" cy="{head_y - 2:.2f}" r="1.6" fill="#111827"/>')
    parts.append(f'<rect x="{head_x + 7:.2f}" y="{head_y - 1:.2f}" width="8" height="2" fill="#fb7185" rx="1"/>')

    for f in range(4):
        fx = 120 + f * 22
        fy = 118 - (f % 2) * 8
        parts.append(f'<rect x="{fx}" y="{fy}" width="10" height="10" rx="3" fill="#334155"/>')

    parts.append("</svg>")

    out_file.write_text("".join(parts), encoding="utf-8")


if __name__ == "__main__":
    main()
