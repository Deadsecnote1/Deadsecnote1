#!/usr/bin/env python3
"""Builds all SVG assets for Thanushiyan's GitHub profile:
- assets/hero-dark.svg & hero-light.svg
- assets/btn-tryhackme-dark.svg & btn-tryhackme-light.svg
- assets/btn-linkedin-dark.svg & btn-linkedin-light.svg
- assets/btn-github-dark.svg & btn-github-light.svg
- assets/btn-email-dark.svg & btn-email-light.svg
- assets/stack-dark.svg & stack-light.svg
- assets/footer-dark.svg & footer-light.svg
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
GLYPHS = json.load(open(os.path.join(ROOT, ".github", "scripts", "glyphs.json")))
OUT = os.path.join(ROOT, "assets")
os.makedirs(OUT, exist_ok=True)


def offset_path(d, dx):
    tokens = re.findall(r"([A-Za-z])|(-?\d+(?:\.\d+)?)", d)
    parts = []
    cmd = ""
    i = 0
    while i < len(tokens):
        c, num = tokens[i]
        if c:
            cmd = c
            parts.append(cmd)
            i += 1
        else:
            if cmd == "M":
                x = float(num) + dx
                y = float(tokens[i + 1][1])
                parts.append(f"{x:g} {y:g}")
                i += 2
                cmd = "L"
            elif cmd == "L":
                x = float(num) + dx
                y = float(tokens[i + 1][1])
                parts.append(f"{x:g} {y:g}")
                i += 2
            elif cmd == "H":
                x = float(num) + dx
                parts.append(f"{x:g}")
                i += 1
            elif cmd == "V":
                y = float(num)
                parts.append(f"{y:g}")
                i += 1
            elif cmd == "Q":
                cx = float(num) + dx
                cy = float(tokens[i + 1][1])
                x = float(tokens[i + 2][1]) + dx
                y = float(tokens[i + 3][1])
                parts.append(f"{cx:g} {cy:g} {x:g} {y:g}")
                i += 4
            elif cmd == "Z":
                parts.append("Z")
                i += 1
            else:
                parts.append(num)
                i += 1
    out = []
    for p in parts:
        if p in "MLHVQZ":
            out.append(p)
        else:
            if out and out[-1] not in "MLHVQZ":
                out.append(" ")
            out.append(p)
    return "".join(out)


def text_path(font_key, text, tracking=0):
    f = GLYPHS[font_key]
    adv = 0
    parts = []
    for ch in text:
        if ch not in f["g"]:
            ch = " "
        a, d = f["g"][ch]
        if d:
            parts.append(offset_path(d, adv))
        adv += a + tracking
    return "".join(parts), adv


def text_element(font_key, text, size, x, y, fill, anchor="start", tracking=0, cls=""):
    f = GLYPHS[font_key]
    upm = f["upm"]
    tr = tracking * upm / size
    d, adv = text_path(font_key, text, tr)
    w = adv * size / upm
    if anchor == "end":
        x -= w
    elif anchor == "middle":
        x -= w / 2
    sc = size / upm
    c = f' class="{cls}"' if cls else ""
    return f'<path{c} fill="{fill}" transform="translate({x:.2f} {y:.2f}) scale({sc:.5f} {-sc:.5f})" d="{d}"/>', w


def generate_hero():
    for theme in ["dark", "light"]:
        is_dark = theme == "dark"
        bg = "#0c0c0d" if is_dark else "#f6f5f2"
        card_stroke = "url(#edge)"
        edge_top = "#ffffff" if is_dark else "#000000"
        text_primary = "#f2f1ee" if is_dark else "#121214"
        text_muted = "#8e8e93" if is_dark else "#6b6b71"
        line_color = "#26262a" if is_dark else "#e3e1dc"
        pill_bg = "#141416" if is_dark else "#ffffff"
        pill_stroke = "#26262a" if is_dark else "#e3e1dc"
        accent = "#00f076" if is_dark else "#059669"
        accent_secondary = "#0e4429" if is_dark else "#7bd4a4"
        grain_val = "1" if is_dark else "0"
        grain_alpha = ".06" if is_dark else ".05"
        dots_opacity = ".14" if is_dark else ".08"
        scan_shine = "#00f076" if is_dark else "#059669"
        scan_base = "#8e8e93" if is_dark else "#6b6b71"

        # Generate text paths
        t_meta, _ = text_element("M", "THANUSHIYAN · SRI LANKA", 14, 72, 92, text_muted, tracking=1.6)
        t_status, _ = text_element("B", "OPEN TO INTERNSHIPS", 14.5, 1030, 90, text_primary)
        t_name, _ = text_element("B", "THANUSHIYAN", 98, 66, 240, text_primary)
        t_subname, _ = text_element("B5", "Kanthasami", 44, 70, 318, "url(#shine)")
        t_role, _ = text_element("B5", "Defensive Security · SOC Analyst · Threat Hunter", 22, 72, 404, text_primary)
        t_univ, _ = text_element("B5", "BSc (Hons) in Information Technology @ University of Moratuwa", 19, 72, 444, text_muted)
        t_tags, _ = text_element("M", "WAZUH SIEM  ·  SYSMON TELEMETRY  ·  TRAFFIC ANALYSIS  ·  INCIDENT RESPONSE", 13.5, 72, 546, text_muted, tracking=1.2)

        # ASCII Cyber Security SOC / Radar Display (Right Side)
        ascii_lines = [
            "+-----------------------------------------------------+",
            "| [::] DEADSEC SOC TELEMETRY CONSOLE v4.2             |",
            "| STATUS : ONLINE                     LOCATION : LK   |",
            "+-----------------------------------------------------+",
            "| [01] HOST TELEMETRY                                 |",
            "|      * AGENT    : Sysmon v15.0 / EventID 1,3,7,22   |",
            "|      * ENDPOINT : Win-Server-2025 [MONITORED]       |",
            "|      * INTEGRITY: SHA256 VALIDATED / ZERO ANOMALIES |",
            "|                                                     |",
            "| [02] SIEM / XDR CLUSTER                             |",
            "|      * ENGINE   : Wazuh Manager [ACTIVE / SYNCED]   |",
            "|      * ALERTS   : 0 HIGH / 0 CRITICAL [STABLE]      |",
            "|      * RULES    : MITRE ATT&CK v14.1 FRAMEWORK      |",
            "|                                                     |",
            "| [03] NETWORK THREAT HUNTING                         |",
            "|      * PCAP CAPTURE : 4.8 GB TRAFFIC STREAM         |",
            "|      * PROTOCOLS    : DNS, TLSv1.3, HTTP/2, SSH     |",
            "|      * IOC EXTRACT  : EMOTET / QAKBOT SIGNATURES    |",
            "|      * TIMELINE     : FIRST-TO-LAST RECONSTRUCTED   |",
            "|                                                     |",
            "| [04] LAB ENVIRONMENTS                               |",
            "|      * KALI LINUX   : RECON & PEN-TEST ACTIVE       |",
            "|      * WIRESHARK    : DEEP PACKET INSPECTION        |",
            "|      * BURP SUITE   : WEB VULN ASSESSMENT           |",
            "|      * TRYHACKME    : TOP RANKED LEARNING LABS      |",
            "+-----------------------------------------------------+",
            "| [!] TARGET STATUS: ACTIVE DEFENSE DEPLOYED          |",
            "+-----------------------------------------------------+",
        ]

        text_nodes = []
        y_cursor = 175
        for i, line in enumerate(ascii_lines):
            cls_str = ""
            if i in (1, 26):
                cls_str = ' class="g1"'
            elif i in (5, 11, 17):
                cls_str = ' class="g2"'
            elif i in (9, 21):
                cls_str = ' class="g3"'
            text_nodes.append(f'<text x="760.0" y="{y_cursor:.1f}" textLength="450.0" lengthAdjust="spacingAndGlyphs"{cls_str}>{line}</text>')
            y_cursor += 15.2

        # Dot matrix background
        dot_nodes = []
        for gx in range(20, 1280, 32):
            for gy in range(20, 600, 32):
                dot_nodes.append(f'<circle cx="{gx}" cy="{gy}" r="1.1"/>')

        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="600" viewBox="0 0 1280 600" role="img" aria-label="Thanushiyan Kanthasami, Defensive Security &amp; SOC Analyst">
<defs>
  <style>
    .blur{{animation:settle 1.4s cubic-bezier(.2,.7,.1,1) both}}
    .rise{{animation:settle2 1s cubic-bezier(.2,.7,.1,1) both}}
    .fade{{}}
    @keyframes settle{{from{{transform:translateY(14px)}}to{{transform:none}}}}
    @keyframes settle2{{from{{transform:translateY(8px)}}to{{transform:none}}}}
    @media (prefers-reduced-motion: reduce){{.blur,.rise{{animation:none}}}}
    .glow{{animation:drift 16s ease-in-out infinite alternate}}
    .glow2{{animation:drift2 20s ease-in-out infinite alternate}}
    .ping{{transform-box:fill-box;transform-origin:center;animation:ping 2.2s cubic-bezier(0,0,.2,1) infinite}}
    @keyframes drift{{from{{transform:translate(0,0)}}to{{transform:translate(-180px,-60px)}}}}
    @keyframes drift2{{from{{transform:translate(0,0)}}to{{transform:translate(140px,40px)}}}}
    @keyframes ping{{0%{{transform:scale(1);opacity:.8}}80%,100%{{transform:scale(3.2);opacity:0}}}}
    .asc text{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace;font-size:12.5px;letter-spacing:0.5px}}
    .g1{{animation:gl 6s steps(1) infinite 3s}} .g2{{animation:gl 7.3s steps(1) infinite 4.1s}} .g3{{animation:gl 5.5s steps(1) infinite 2.2s}}
    @keyframes gl{{0%,93%,100%{{transform:none}}94%{{transform:translateX(5px)}}96%{{transform:translateX(-4px)}}}}
  </style>
  <clipPath id="card"><rect width="1280" height="600" rx="28"/></clipPath>
  <linearGradient id="edge" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="{edge_top}" stop-opacity=".14"/><stop offset="1" stop-color="{edge_top}" stop-opacity=".06"/></linearGradient>
  <radialGradient id="dotmask" cx="72%" cy="30%" r="70%"><stop offset="0" stop-color="#fff" stop-opacity=".9"/><stop offset=".7" stop-color="#fff" stop-opacity="0"/></radialGradient>
  <mask id="dm"><rect width="1280" height="600" fill="url(#dotmask)"/></mask>
  <radialGradient id="g1"><stop offset="0" stop-color="{accent}" stop-opacity=".52"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient>
  <radialGradient id="g2"><stop offset="0" stop-color="{accent_secondary}" stop-opacity=".22"/><stop offset="1" stop-color="{accent_secondary}" stop-opacity="0"/></radialGradient>
  <linearGradient id="shine" y1="0" y2="0" gradientUnits="userSpaceOnUse" x1="70" x2="420">
    <stop offset="0" stop-color="{accent}"/><stop offset=".42" stop-color="{accent}"/><stop offset=".5" stop-color="#ffffff"/><stop offset=".58" stop-color="{accent}"/><stop offset="1" stop-color="{accent}"/>
    <animateTransform attributeName="gradientTransform" type="translate" values="-460 0;460 0;460 0" keyTimes="0;.45;1" dur="7s" begin="2s" repeatCount="indefinite"/>
  </linearGradient>
  <filter id="grain" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/>
    <feColorMatrix values="0 0 0 0 {grain_val}  0 0 0 0 {grain_val}  0 0 0 0 {grain_val}  0 0 0 {grain_alpha} 0"/>
  </filter>
  <linearGradient id="scan" gradientUnits="userSpaceOnUse" x1="0" y1="140" x2="0" y2="600">
    <stop offset="0" stop-color="{scan_base}"/><stop offset=".44" stop-color="{scan_base}"/><stop offset=".5" stop-color="{scan_shine}"/><stop offset=".56" stop-color="{scan_base}"/><stop offset="1" stop-color="{scan_base}"/>
    <animateTransform attributeName="gradientTransform" type="translate" values="0 -460;0 460" dur="4.5s" begin="0s" repeatCount="indefinite"/>
  </linearGradient>
  <linearGradient id="pfade" x1="0" y1="0" x2="0" y2="1"><stop offset=".8" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
  <mask id="pmask" maskUnits="userSpaceOnUse" x="730" y="140" width="510" height="460"><rect x="730" y="140" width="510" height="460" fill="url(#pfade)"/></mask>
</defs>
<g clip-path="url(#card)">
  <rect width="1280" height="600" fill="{bg}"/>
  <g class="glow"><circle cx="1100" cy="540" r="420" fill="url(#g1)"/></g>
  <g class="glow2"><circle cx="280" cy="-40" r="360" fill="url(#g2)"/></g>
  <g fill="{edge_top}" fill-opacity="{dots_opacity}" mask="url(#dm)">{"".join(dot_nodes)}</g>
  <rect width="1280" height="600" filter="url(#grain)"/>
</g>
<rect x=".5" y=".5" width="1279" height="599" rx="27.5" fill="none" stroke="{card_stroke}"/>
<g class="fade" style="animation-delay:.1s">{t_meta}</g>
<g class="rise" style="animation-delay:.2s">
  <rect x="986.8" y="62" width="221.2" height="44" rx="22" fill="{pill_bg}" stroke="{pill_stroke}"/>
  <circle cx="1012.8" cy="84" r="5" fill="{accent}"/>
  <circle cx="1012.8" cy="84" r="5" fill="{accent}" class="ping"/>
  {t_status}
</g>
<g class="blur" style="animation-delay:.25s">{t_name}</g>
<g class="blur" style="animation-delay:.40s">{t_subname}</g>
<g class="rise" style="animation-delay:.75s">{t_role}</g>
<g class="rise" style="animation-delay:.85s">{t_univ}</g>
<rect x="72" y="496" width="640" height="1" fill="{line_color}" class="fade" style="animation-delay:1.0s"/>
<g class="rise" style="animation-delay:1.15s">{t_tags}</g>
<g mask="url(#pmask)">
  <g class="asc" fill="url(#scan)" fill-opacity=".92">
    {"".join(text_nodes)}
  </g>
</g>
</svg>
'''
        path = os.path.join(OUT, f"hero-{theme}.svg")
        open(path, "w").write(svg)
        print("Generated", path)


def generate_buttons():
    # Icons: TryHackMe, LinkedIn, GitHub, Email
    icons = {
        "tryhackme": (
            '<g transform="translate(24 20)" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>'
            '</g>'
        ),
        "linkedin": (
            '<g transform="translate(24 20)" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">'
            '<rect x="3" y="3" width="18" height="18" rx="4"/>'
            '<path d="M8 10.5V16M8 7.6v.1M11.5 16v-3.2c0-1.5 1-2.4 2.2-2.4s2 .9 2 2.4V16M11.5 10.5V16"/>'
            '</g>'
        ),
        "github": (
            '<g transform="translate(24 20)" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/>'
            '</g>'
        ),
        "email": (
            '<g transform="translate(24 20)" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">'
            '<rect x="3" y="5" width="18" height="14" rx="2"/>'
            '<path d="m3 7 9 6 9-6"/>'
            '</g>'
        ),
    }

    buttons = [
        ("tryhackme", "TryHackMe", 218, True),   # primary highlight button!
        ("linkedin", "LinkedIn", 200, False),
        ("github", "GitHub", 188, False),
        ("email", "Email", 172, False),
    ]

    for name, label, width, is_primary in buttons:
        for theme in ["dark", "light"]:
            is_dark = theme == "dark"

            if is_primary:
                # Primary pill: bold white/dark contrast
                fill_bg = "#f2f1ee" if is_dark else "#121214"
                stroke_color = "#f2f1ee" if is_dark else "#121214"
                fg = "#0c0c0d" if is_dark else "#f6f5f2"
                sh_fill = "#000000" if is_dark else "#ffffff"
                sh_op = "0.22" if is_dark else "0.18"
            else:
                fill_bg = "#141416" if is_dark else "#ffffff"
                stroke_color = "#26262a" if is_dark else "#e3e1dc"
                fg = "#f2f1ee" if is_dark else "#121214"
                sh_fill = "#ffffff" if is_dark else "#000000"
                sh_op = "0.10" if is_dark else "0.06"

            t_path, adv = text_path("B5", label)
            text_sc = 20 / 2048
            t_elem = f'<path fill="{fg}" transform="translate(60.00 39.00) scale({text_sc:.5f} {-text_sc:.5f})" d="{t_path}"/>'
            arrow_x = width - 42

            icon_svg = icons[name].replace('stroke="currentColor"', f'stroke="{fg}"')

            svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="64" viewBox="0 0 {width} 64" role="img" aria-label="{label}">
<defs>
  <style>
    .ar{{animation:nd 2.6s cubic-bezier(.45,0,.2,1) infinite 0.2s}}
    .sh{{animation:sw 6s ease-in-out infinite 1.4s}}
    @keyframes nd{{0%,60%,100%{{transform:translate(0,0)}}75%{{transform:translate(3px,-3px)}}}}
    @keyframes sw{{0%,70%{{transform:translateX(0)}}100%{{transform:translateX({width + 300}px)}}}}
    @media (prefers-reduced-motion: reduce){{.ar,.sh{{animation:none}}}}
  </style>
  <clipPath id="pc"><rect x="1" y="1" width="{width - 2}" height="62" rx="31.0"/></clipPath>
  <linearGradient id="sg" x1="0" x2="1"><stop offset="0" stop-color="{sh_fill}" stop-opacity="0"/><stop offset=".5" stop-color="{sh_fill}" stop-opacity="{sh_op}"/><stop offset="1" stop-color="{sh_fill}" stop-opacity="0"/></linearGradient>
</defs>
<rect x="1" y="1" width="{width - 2}" height="62" rx="31.0" fill="{fill_bg}" stroke="{stroke_color}"/>
<g clip-path="url(#pc)"><rect class="sh" x="-200" y="0" width="90" height="64" fill="url(#sg)" transform="skewX(-20)"/></g>
{icon_svg}
{t_elem}
<g class="ar"><path d="M{arrow_x} 39l10-10M{arrow_x + 1} 29h9v9" fill="none" stroke="{fg}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" opacity=".75"/></g>
</svg>
'''
            out_file = os.path.join(OUT, f"btn-{name}-{theme}.svg")
            open(out_file, "w").write(svg)
            print("Generated", out_file)


def generate_stack():
    # Toolbox tool definition: (name, icon_svg_path)
    # Icons: 22x22 scaled icons
    icons = {
        "Wazuh": '<path d="M11 2L2 8v6c0 5.5 3.8 10.7 9 12 5.2-1.3 9-6.5 9-12V8l-9-6zm-1 14.5l-3.5-3.5 1.4-1.4 2.1 2.1 5.1-5.1 1.4 1.4L10 16.5z"/>',
        "Sysmon": '<path d="M3 4h16v12H3V4zm0 14h16v2H3v-2zm2-10h12v6H5V8zm2 2v2h2v-2H7zm4 0v2h4v-2h-4z"/>',
        "Wireshark": '<path d="M2 18c4-1 7-4 9-9 1 4 4 8 9 9-4 2-9 2-18 0zm9-16c-1 3-3 6-7 8 3 1 7 1 10-2 2 3 5 4 8 3-4-3-6-6-7-9h-4z"/>',
        "Linux": '<path d="M12 2C9.5 2 8 3.8 8 6.5v4.2c-1.5 1-2.5 2.8-2.5 4.8 0 2.5 1.6 4.5 4 4.5h5c2.4 0 4-2 4-4.5 0-2-1-3.8-2.5-4.8V6.5C16 3.8 14.5 2 12 2zm-1.5 5a1 1 0 1 1 0 2 1 1 0 0 1 0-2zm3 0a1 1 0 1 1 0 2 1 1 0 0 1 0-2zm-1.5 3.5c1.2 0 1.8.8 1.8 1.2 0 .4-.6.8-1.8.8s-1.8-.4-1.8-.8c0-.4.6-1.2 1.8-1.2z"/>',
        "Python": '<path d="M11.9 2c-3.1 0-2.9 1.3-2.9 1.3l.03 1.4h3v.4h-4.2C6.1 5.1 5 6.2 5 7.8c0 1.8.9 2.5 2.1 2.5h1.2v-1.7c0-.9.8-1.7 1.7-1.7h3v-.9c0-1-.8-2-2.1-2h1zm-1.1 1a.6.6 0 1 1 0 1.2.6.6 0 0 1 0-1.2zm1.3 17c3.1 0 2.9-1.3 2.9-1.3l-.03-1.4h-3v-.4h4.2c1.7 0 2.8-1.1 2.8-2.7 0-1.8-.9-2.5-2.1-2.5h-1.2v1.7c0 .9-.8 1.7-1.7 1.7h-3v.9c0 1 .8 2 2.1 2h-1zm1.1-1a.6.6 0 1 1 0-1.2.6.6 0 0 1 0 1.2z"/>',
        "Bash": '<path d="M3 4h16a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2zm2 4l3.5 3L5 14h2l3.5-3L7 8H5zm6 5h5v1.5h-5V13z"/>',
        "Java": '<path d="M8.5 17.5c1.8.2 3.8.2 5.5-.3.5-.2 1-.5 1.5-.8-1.5.5-3.3.7-4.9.5-1.1-.1-2.2-.4-2.1-.4zm.8 1.5c2 .2 4.2.1 6.1-.4 1.1-.3 2.2-.7 3.2-1.3-2.6 1.1-5.7 1.4-8.5.9-.9-.1-1.8-.4-1.8-.4zM12 2s1.5 2-1 4.5 0 3.5 0 3.5c-2.5-2.5-1-4.5 1-8zm3 2s1 1.5-.5 3c-1.8 1.8-.5 2.8-.5 2.8 1.8-1.8.5-3.5.5-5.8h.5zM7.5 14.5c2.5.3 5.3.2 7.7-.4 1.5-.4 3-1 4.3-1.8-3.4 1.4-7.4 1.8-11 1.3-1.2-.2-2.4-.6-2.4-.6z"/>',
        "Git": '<path d="M19.7 10.3l-8-8c-.4-.4-1-.4-1.4 0l-8 8c-.4.4-.4 1 0 1.4l8 8c.4.4 1 .4 1.4 0l8-8c.4-.4.4-1 0-1.4zM11 14.8v-2.2a2 2 0 1 1 1.4-1.9v2.2a2 2 0 1 1-1.4 1.9z"/>',
        "Nmap": '<path d="M11 2a9 9 0 1 0 9 9 9 9 0 0 0-9-9zm0 2a7 7 0 0 1 6.9 6h-2.1a4.9 4.9 0 0 0-4.8-4.8V3.1zm-1 0v2.1A4.9 4.9 0 0 0 5.2 10H3.1A7 7 0 0 1 10 4zm0 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2zm-7 1h2.1a4.9 4.9 0 0 0 4.9 4.9v2.1A7 7 0 0 1 3 11zm9 6.9v-2.1a4.9 4.9 0 0 0 4.9-4.8h2.1a7 7 0 0 1-7 6.9z"/>',
        "Burp Suite": '<path d="M3 4h7v6H3V4zm9 0h7v6h-7V4zm-9 8h7v6H3v-6zm9 0h7v6h-7v-6zM6 7l1 1-1 1M15 7l1 1-1 1"/>',
        "TryHackMe": '<path d="M11 2L3 6.5v9L11 20l8-4.5v-9L11 2zm0 3.3l5 2.8-5 2.8-5-2.8 5-2.8zm-6 4.3l5 2.8v5.6l-5-2.8V9.6zm7 8.4v-5.6l5-2.8v5.6l-5 2.8z"/>',
        "Docker": '<path d="M19.5 8.5c-.3-.2-1.3-.4-2-.2-.3-.5-.7-.9-1.3-1.2l-.7-.4-.3.7c-.2.5-.2 1.3 0 1.8-1 .6-2.5.6-3.7.6H2.5c-.3 0-.5.2-.5.5 0 2.2.8 4.3 2.3 5.8 1.9 2 4.6 3.1 8.2 3.1 5.5 0 9.5-3 9.5-8.2 0-.9-.3-1.8-1-2.5h-1.5zM4 9h2v2H4V9zm3 0h2v2H7V9zm3 0h2v2h-2V9zm3 0h2v2h-2V9zm-6-3h2v2H7V6zm3 0h2v2h-2V6zm3 0h2v2h-2V6z"/>',
        "Splunk": '<path d="M4 14l5-5-5-5h3l5 5-5 5H4zm8 0l5-5-5-5h3l5 5-5 5h-3z"/>',
        "Suricata": '<path d="M11 2a9 9 0 0 0-9 9c0 3.8 2.4 7 5.8 8.3L9 16c-2.4-.8-4-3-4-5.5a6 6 0 0 1 12 0c0 2.5-1.6 4.7-4 5.5l1.2 3.3c3.4-1.3 5.8-4.5 5.8-8.3a9 9 0 0 0-9-9zm0 6a3 3 0 1 0 0 6 3 3 0 0 0 0-6z"/>',
        "Metasploit": '<path d="M11 2L2 6v6c0 5 3.8 9.7 9 11 5.2-1.3 9-6 9-11V6l-9-4zm4 11l-4 4-4-4V8l4 3 4-3v5z"/>',
        "Gobuster": '<path d="M10 2a7 7 0 0 1 5.6 11.2l4.1 4.1-1.4 1.4-4.1-4.1A7 7 0 1 1 10 2zm0 2a5 5 0 1 0 0 10 5 5 0 0 0 0-10zm-2 4h4v2H8V8z"/>',
        "Nikto": '<path d="M11 2a9 9 0 1 0 9 9 9 9 0 0 0-9-9zm-1 4h2v5h-2V6zm0 7h2v2h-2v-2z"/>',
        "MITRE ATT&CK": '<path d="M3 4h16v3H3V4zm0 5h16v3H3V9zm0 5h16v3H3v-3zm0 5h16v1H3v-1zM5 5v1h2V5H5zm0 5v1h4v-1H5zm0 5v1h6v-1H5z"/>',
    }

    rowA_tools = ["Wazuh", "Sysmon", "Wireshark", "Linux", "Python", "Bash", "Java", "Git", "Nmap"]
    rowB_tools = ["Burp Suite", "TryHackMe", "Docker", "Splunk", "Suricata", "Metasploit", "Gobuster", "Nikto", "MITRE ATT&CK"]

    def build_row_svg(tools, y_pos, theme):
        is_dark = theme == "dark"
        surf = "#141416" if is_dark else "#ffffff"
        border = "#26262a" if is_dark else "#e3e1dc"
        fg = "#f2f1ee" if is_dark else "#121214"
        accent = "#00f076" if is_dark else "#059669"

        pills = []
        cur_x = 0.0
        for name in tools:
            t_path, adv = text_path("B5", name)
            tw = adv * 17 / 2048
            pill_w = 28 + 22 + 10 + tw + 28
            # pill rect
            pills.append(f'<rect x="{cur_x:.1f}" y="{y_pos}" width="{pill_w:.1f}" height="60" rx="30" fill="{surf}" stroke="{border}"/>')
            # icon
            icon_d = icons.get(name, '<circle cx="11" cy="11" r="8"/>')
            pills.append(f'<g transform="translate({cur_x + 28:.1f} {y_pos + 19})" fill="{accent}">{icon_d}</g>')
            # label
            sc = 17 / 2048
            tx = cur_x + 28 + 22 + 10
            ty = y_pos + 36
            pills.append(f'<path fill="{fg}" transform="translate({tx:.2f} {ty:.2f}) scale({sc:.5f} {-sc:.5f})" d="{t_path}"/>')
            cur_x += pill_w + 14.0
        return "".join(pills), cur_x

    for theme in ["dark", "light"]:
        is_dark = theme == "dark"
        bg = "#0c0c0d" if is_dark else "#f6f5f2"
        edge_top = "#ffffff" if is_dark else "#000000"
        text_muted = "#8e8e93" if is_dark else "#6b6b71"
        grain_val = "1" if is_dark else "0"
        grain_alpha = ".06" if is_dark else ".05"

        rowA_svg, widthA = build_row_svg(rowA_tools, 108, theme)
        rowB_svg, widthB = build_row_svg(rowB_tools, 192, theme)

        t_head_left, _ = text_element("M", "TOOLBOX & SECURITY STACK", 14, 72, 70, text_muted, tracking=1.6)
        t_head_right, _ = text_element("M", "DEFENSIVE / OFFENSIVE / LABS", 14, 1208, 70, text_muted, anchor="end", tracking=1.6)

        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1280" height="296" viewBox="0 0 1280 296" role="img" aria-label="Toolbox: Wazuh, Sysmon, Wireshark, Linux, Python, Bash, Java, Git, Nmap, Burp Suite, TryHackMe, Docker, Splunk, Suricata, Metasploit, Gobuster, Nikto, MITRE ATT&amp;CK">
<defs>
  <style>
    .ra{{animation:ma 32s linear infinite}}
    .rb{{animation:mb 32s linear infinite}}
    @keyframes ma{{from{{transform:translateX(0)}}to{{transform:translateX(-{widthA:.1f}px)}}}}
    @keyframes mb{{from{{transform:translateX(-{widthB:.1f}px)}}to{{transform:translateX(0)}}}}
    @media (prefers-reduced-motion: reduce){{.ra,.rb{{animation:none}}}}
  </style>
  <clipPath id="card"><rect width="1280" height="296" rx="28"/></clipPath>
  <linearGradient id="edge" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="{edge_top}" stop-opacity=".14"/><stop offset="1" stop-color="{edge_top}" stop-opacity=".06"/></linearGradient>
  <linearGradient id="fadeX" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".08" stop-color="#fff"/><stop offset=".92" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
  <mask id="m"><rect width="1280" height="296" fill="url(#fadeX)"/></mask>
  <g id="rowA">{rowA_svg}</g>
  <g id="rowB">{rowB_svg}</g>
  <filter id="grain" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/>
    <feColorMatrix values="0 0 0 0 {grain_val}  0 0 0 0 {grain_val}  0 0 0 0 {grain_val}  0 0 0 {grain_alpha} 0"/>
  </filter>
</defs>
<g clip-path="url(#card)">
  <rect width="1280" height="296" fill="{bg}"/>
  <rect width="1280" height="296" filter="url(#grain)"/>
  {t_head_left}
  {t_head_right}
  <g mask="url(#m)">
    <g class="ra"><use href="#rowA" xlink:href="#rowA"/><use href="#rowA" xlink:href="#rowA" x="{widthA:.1f}"/></g>
    <g class="rb"><use href="#rowB" xlink:href="#rowB"/><use href="#rowB" xlink:href="#rowB" x="{widthB:.1f}"/></g>
  </g>
</g>
<rect x=".5" y=".5" width="1279" height="295" rx="27.5" fill="none" stroke="url(#edge)"/>
</svg>
'''
        out_file = os.path.join(OUT, f"stack-{theme}.svg")
        open(out_file, "w").write(svg)
        print("Generated", out_file)


def generate_footer():
    for theme in ["dark", "light"]:
        is_dark = theme == "dark"
        bg = "#0c0c0d" if is_dark else "#f6f5f2"
        edge_top = "#ffffff" if is_dark else "#000000"
        text_primary = "#f2f1ee" if is_dark else "#121214"
        text_muted = "#8e8e93" if is_dark else "#6b6b71"
        accent = "#00f076" if is_dark else "#059669"
        grain_val = "1" if is_dark else "0"
        grain_alpha = ".06" if is_dark else ".05"
        btn_bg = "#f2f1ee" if is_dark else "#121214"
        btn_fg = "#0c0c0d" if is_dark else "#f6f5f2"

        t_head, _ = text_element("B", "LET'S INVESTIGATE.", 82, 68, 146, text_primary)
        t_sub, _ = text_element("B5", "Open for internships · davidthanu1006@gmail.com", 20, 72, 216, text_muted)
        t_btn, _ = text_element("B", "GET IN TOUCH", 18, 912, 218, btn_fg)

        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="300" viewBox="0 0 1280 300" role="img" aria-label="Let's investigate. Thanushiyan Kanthasami">
<defs>
  <style>
    .glow{{animation:drift 14s ease-in-out infinite alternate}}
    .arrow{{animation:nudge 2.4s ease-in-out infinite}}
    @keyframes drift{{from{{transform:translate(0,0)}}to{{transform:translate(-160px,30px)}}}}
    @keyframes nudge{{0%,100%{{transform:translate(0,0)}}50%{{transform:translate(4px,-4px)}}}}
    @media (prefers-reduced-motion: reduce){{.glow,.arrow{{animation:none}}}}
  </style>
  <clipPath id="card"><rect width="1280" height="300" rx="28"/></clipPath>
  <linearGradient id="edge" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="{edge_top}" stop-opacity=".14"/><stop offset="1" stop-color="{edge_top}" stop-opacity=".06"/></linearGradient>
  <radialGradient id="g1"><stop offset="0" stop-color="{accent}" stop-opacity="0.34"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient>
  <filter id="grain" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/>
    <feColorMatrix values="0 0 0 0 {grain_val}  0 0 0 0 {grain_val}  0 0 0 0 {grain_val}  0 0 0 {grain_alpha} 0"/>
  </filter>
</defs>
<g clip-path="url(#card)">
  <rect width="1280" height="300" fill="{bg}"/>
  <g class="glow"><circle cx="1120" cy="300" r="360" fill="url(#g1)"/></g>
  <rect width="1280" height="300" filter="url(#grain)"/>
</g>
<rect x=".5" y=".5" width="1279" height="299" rx="27.5" fill="none" stroke="url(#edge)"/>
{t_head}
{t_sub}
<rect x="880" y="186" width="328" height="56" rx="28" fill="{btn_bg}"/>
{t_btn}
<g class="arrow"><path d="M1166.0 222 l14 -14 M1168.0 208 h12 v12" stroke="{btn_fg}" stroke-width="2.2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>
</svg>
'''
        out_file = os.path.join(OUT, f"footer-{theme}.svg")
        open(out_file, "w").write(svg)
        print("Generated", out_file)


if __name__ == "__main__":
    generate_hero()
    generate_buttons()
    generate_stack()
    generate_footer()
    print("Done building all assets!")
