#!/usr/bin/env python3
"""Render the GitHub contribution grid as a scan-beam animation.

Pulls the viewer's contribution calendar over GraphQL and emits an animated SVG:
a teal beam sweeps left to right and each week-column resolves into colour as it
passes -- the same gesture as the profile header.
"""
import json
import os
import subprocess
import sys

USER = os.environ.get("PROFILE_USER", "NesanSelvan")
OUT = os.environ.get("OUT_PATH", "assets/contrib-scan.svg")

CELL, GAP = 11, 3
PITCH = CELL + GAP
PAD_X, TOP, BOT = 34, 76, 46
LEVELS = ["#161B22", "#0E4F47", "#12766B", "#1CA697", "#2DD4BF"]

QUERY = """
{ user(login: "%s") { contributionsCollection { contributionCalendar {
    totalContributions
    weeks { contributionDays { contributionCount date weekday } }
} } } }
""" % USER


def fetch():
    out = subprocess.run(
        ["gh", "api", "graphql", "-f", "query=" + QUERY],
        capture_output=True, text=True, check=True,
    ).stdout
    return json.loads(out)["data"]["user"]["contributionsCollection"]["contributionCalendar"]


def level(count, peak):
    if count <= 0:
        return 0
    for i, edge in enumerate((0.10, 0.25, 0.50), start=1):
        if count <= max(1, round(peak * edge)):
            return i
    return 4


def main():
    cal = fetch()
    weeks = cal["weeks"]
    total = cal["totalContributions"]
    peak = max((d["contributionCount"] for w in weeks for d in w["contributionDays"]), default=1)

    cols = len(weeks)
    grid_w = cols * PITCH - GAP
    W = grid_w + PAD_X * 2
    H = TOP + 7 * PITCH - GAP + BOT

    # beam sweeps between these keyTimes; a column lights the moment it is crossed
    B0, B1 = 0.12, 0.60
    sweep_x0, sweep_x1 = PAD_X - 30, W - PAD_X + 30

    first = weeks[0]["contributionDays"][0]["date"]
    last = weeks[-1]["contributionDays"][-1]["date"]

    p = []
    p.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
        f'role="img" aria-label="{total} GitHub contributions from {first} to {last}">'
    )
    p.append("""
  <defs>
    <linearGradient id="beam" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#2DD4BF" stop-opacity="0"/>
      <stop offset="20%" stop-color="#2DD4BF" stop-opacity="0.95"/>
      <stop offset="80%" stop-color="#2DD4BF" stop-opacity="0.95"/>
      <stop offset="100%" stop-color="#2DD4BF" stop-opacity="0"/>
    </linearGradient>
    <filter id="glow" x="-400%" y="-40%" width="900%" height="180%">
      <feGaussianBlur stdDeviation="5" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>""")
    p.append(f'  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="16" fill="#0D1117" stroke="#21262D" stroke-width="1.5"/>')

    mono = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace"
    p.append(f'  <g font-family="{mono}">')
    p.append(f'    <text x="{PAD_X}" y="38" font-size="15" font-weight="600" fill="#E6EDF3" letter-spacing="0.3">contribution scan</text>')
    p.append(f'    <text x="{PAD_X}" y="58" font-size="12.5" fill="#7D8590">{first} → {last}</text>')
    p.append(f'    <text x="{W-PAD_X}" y="38" font-size="15" font-weight="600" fill="#2DD4BF" text-anchor="end">{total:,}</text>')
    p.append(f'    <text x="{W-PAD_X}" y="58" font-size="12.5" fill="#7D8590" text-anchor="end">contributions</text>')

    # dim base grid -- always present, so the shape reads before the beam arrives
    p.append('    <g fill="#161B22">')
    for x, week in enumerate(weeks):
        for day in week["contributionDays"]:
            cx = PAD_X + x * PITCH
            cy = TOP + day["weekday"] * PITCH
            p.append(f'<rect x="{cx}" y="{cy}" width="{CELL}" height="{CELL}" rx="2.5"/>')
    p.append("    </g>")

    # one animated group per column -- 53 animate tags instead of ~371
    for x, week in enumerate(weeks):
        live = [d for d in week["contributionDays"] if d["contributionCount"] > 0]
        if not live:
            continue
        cx = PAD_X + x * PITCH
        frac = (cx - sweep_x0) / (sweep_x1 - sweep_x0)
        kt = round(B0 + (B1 - B0) * frac, 4)
        p.append(f'    <g opacity="0"><animate attributeName="opacity" dur="14s" repeatCount="indefinite" '
                 f'values="0;0;1;1;0" keyTimes="0;{kt};{round(min(kt+0.012,0.95),4)};0.93;1"/>')
        for d in live:
            cy = TOP + d["weekday"] * PITCH
            p.append(f'<rect x="{cx}" y="{cy}" width="{CELL}" height="{CELL}" rx="2.5" '
                     f'fill="{LEVELS[level(d["contributionCount"], peak)]}"/>')
        p.append("</g>")

    p.append(f'    <text x="{PAD_X}" y="{H-18}" font-size="12" fill="#484F58" opacity="0">resolved {cols} weeks'
             f'<animate attributeName="opacity" dur="14s" repeatCount="indefinite" values="0;0;0.9;0.9;0" keyTimes="0;0.62;0.67;0.93;1"/></text>')

    legend_x = W - PAD_X - 150
    p.append(f'    <text x="{legend_x-10}" y="{H-18}" font-size="11.5" fill="#484F58" text-anchor="end">less</text>')
    for i, c in enumerate(LEVELS):
        p.append(f'<rect x="{legend_x + i*16}" y="{H-28}" width="11" height="11" rx="2.5" fill="{c}"/>')
    p.append(f'    <text x="{legend_x + 5*16 + 2}" y="{H-18}" font-size="11.5" fill="#484F58">more</text>')

    p.append(f'''    <g filter="url(#glow)">
      <rect y="{TOP-16}" width="2" height="{7*PITCH-GAP+30}" fill="url(#beam)" opacity="0">
        <animate attributeName="x" dur="14s" repeatCount="indefinite" values="{sweep_x0};{sweep_x0};{sweep_x1};{sweep_x1};{sweep_x0}" keyTimes="0;{B0};{B1};0.93;1"/>
        <animate attributeName="opacity" dur="14s" repeatCount="indefinite" values="0;0;1;1;0;0" keyTimes="0;{B0-0.01};{B0+0.02};{B1-0.02};{B1};1"/>
      </rect>
    </g>''')
    p.append("  </g>\n</svg>\n")

    svg = "\n".join(p)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        f.write(svg)
    print(f"wrote {OUT} — {total:,} contributions, {cols} weeks, peak {peak}/day, {len(svg):,} bytes")


if __name__ == "__main__":
    sys.exit(main())
