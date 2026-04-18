#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║   🧬  C O D E D N A                                         ║
║   Your Codebase's Genetic Fingerprint                        ║
╚══════════════════════════════════════════════════════════════╝

Scans any code folder and renders a unique DNA strand showing:
  • Language composition
  • Complexity rhythm
  • Comment density
  • Function depth patterns
  • Code entropy score
  • Mutation hotspots (most changed file types)

No two codebases produce the same DNA.
"""

import os
import sys
import re
import json
import math
import time
import shutil
import hashlib
import argparse
import datetime
import random
from pathlib import Path
from collections import defaultdict, Counter

# ─── ANSI ──────────────────────────────────────────────────────
class C:
    RESET    = "\033[0m"
    BOLD     = "\033[1m"
    DIM      = "\033[2m"
    ITALIC   = "\033[3m"
    RED      = "\033[31m"
    GREEN    = "\033[32m"
    YELLOW   = "\033[33m"
    BLUE     = "\033[34m"
    MAGENTA  = "\033[35m"
    CYAN     = "\033[36m"
    WHITE    = "\033[37m"
    GRAY     = "\033[90m"
    BRED     = "\033[91m"
    BGREEN   = "\033[92m"
    BYELLOW  = "\033[93m"
    BBLUE    = "\033[94m"
    BMAGENTA = "\033[95m"
    BCYAN    = "\033[96m"
    BWHITE   = "\033[97m"
    BG_BLACK = "\033[40m"

def col(text, *codes):
    return "".join(codes) + str(text) + C.RESET

def term_width():
    return shutil.get_terminal_size((80, 24)).columns

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def center(text, width=None, color=""):
    w = width or term_width()
    plain = re.sub(r"\033\[[0-9;]*m", "", text)
    pad = max(0, (w - len(plain)) // 2)
    print(" " * pad + (color + text + C.RESET if color else text))

def hr(char="─", color=C.GRAY):
    print(col(char * term_width(), color))

# ─── Language Definitions ──────────────────────────────────────
LANGUAGES = {
    ".py":    {"name": "Python",      "color": C.BBLUE,    "symbol": "🐍", "comment": "#",   "block": ('"""', '"""')},
    ".js":    {"name": "JavaScript",  "color": C.BYELLOW,  "symbol": "☕", "comment": "//",  "block": ("/*", "*/")},
    ".ts":    {"name": "TypeScript",  "color": C.BCYAN,    "symbol": "🔷", "comment": "//",  "block": ("/*", "*/")},
    ".java":  {"name": "Java",        "color": C.BRED,     "symbol": "☕", "comment": "//",  "block": ("/*", "*/")},
    ".cpp":   {"name": "C++",         "color": C.BMAGENTA, "symbol": "⚙️", "comment": "//",  "block": ("/*", "*/")},
    ".c":     {"name": "C",           "color": C.MAGENTA,  "symbol": "🔩", "comment": "//",  "block": ("/*", "*/")},
    ".go":    {"name": "Go",          "color": C.CYAN,     "symbol": "🐹", "comment": "//",  "block": ("/*", "*/")},
    ".rs":    {"name": "Rust",        "color": C.YELLOW,   "symbol": "🦀", "comment": "//",  "block": ("/*", "*/")},
    ".rb":    {"name": "Ruby",        "color": C.BRED,     "symbol": "💎", "comment": "#",   "block": ("=begin", "=end")},
    ".php":   {"name": "PHP",         "color": C.BBLUE,    "symbol": "🐘", "comment": "//",  "block": ("/*", "*/")},
    ".swift": {"name": "Swift",       "color": C.BRED,     "symbol": "🦅", "comment": "//",  "block": ("/*", "*/")},
    ".kt":    {"name": "Kotlin",      "color": C.BMAGENTA, "symbol": "🎯", "comment": "//",  "block": ("/*", "*/")},
    ".cs":    {"name": "C#",          "color": C.BGREEN,   "symbol": "🎮", "comment": "//",  "block": ("/*", "*/")},
    ".html":  {"name": "HTML",        "color": C.BYELLOW,  "symbol": "🌐", "comment": "<!--","block": ("<!--", "-->")},
    ".css":   {"name": "CSS",         "color": C.BBLUE,    "symbol": "🎨", "comment": "/*",  "block": ("/*", "*/")},
    ".sh":    {"name": "Shell",       "color": C.BGREEN,   "symbol": "🖥️", "comment": "#",   "block": (": '", "'")},
    ".r":     {"name": "R",           "color": C.BLUE,     "symbol": "📊", "comment": "#",   "block": ("#", "#")},
    ".lua":   {"name": "Lua",         "color": C.BBLUE,    "symbol": "🌙", "comment": "--",  "block": ("--[[", "]]")},
    ".dart":  {"name": "Dart",        "color": C.BCYAN,    "symbol": "🎯", "comment": "//",  "block": ("/*", "*/")},
    ".scala": {"name": "Scala",       "color": C.BRED,     "symbol": "🔴", "comment": "//",  "block": ("/*", "*/")},
}

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv",
             "env", "dist", "build", ".next", "target", ".idea", ".vscode"}

# ─── DNA Nucleotide Mapping ────────────────────────────────────
# Each code metric maps to a DNA base pair visual
BASES = {
    "high_complexity": ("█", C.BRED),
    "med_complexity":  ("▓", C.BYELLOW),
    "low_complexity":  ("░", C.BGREEN),
    "comment_rich":    ("C", C.BCYAN),
    "comment_sparse":  ("·", C.GRAY),
    "deep_nesting":    ("D", C.BMAGENTA),
    "flat":            ("─", C.BBLUE),
    "blank_heavy":     ("▒", C.GRAY),
}

STRAND_CHARS_TOP = "ATCGATCGATCG"
STRAND_CHARS_BOT = "TAGCTAGCTAGC"

# ─── File Scanner ──────────────────────────────────────────────
def scan_file(path: Path) -> dict:
    """Analyze a single source file and return metrics."""
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return None

    lines = text.splitlines()
    if not lines:
        return None

    total     = len(lines)
    blank     = sum(1 for l in lines if not l.strip())
    ext       = path.suffix.lower()
    lang_info = LANGUAGES.get(ext, {})
    comment_marker = lang_info.get("comment", "#")

    comment_lines = sum(1 for l in lines if l.strip().startswith(comment_marker))

    # Indentation depth as proxy for nesting complexity
    depths = []
    for line in lines:
        if line.strip():
            indent = len(line) - len(line.lstrip())
            depths.append(indent // 4 if indent else 0)

    avg_depth   = sum(depths) / len(depths) if depths else 0
    max_depth   = max(depths) if depths else 0

    # Function/method count (simple heuristic)
    func_patterns = [
        r"^\s*def\s+\w+",           # Python
        r"^\s*function\s+\w+",      # JS
        r"^\s*(public|private|protected|static).*\w+\s*\(",  # Java/C#
        r"^\s*fn\s+\w+",            # Rust
        r"^\s*func\s+\w+",          # Go/Swift
    ]
    func_count = 0
    for line in lines:
        for pat in func_patterns:
            if re.match(pat, line):
                func_count += 1
                break

    # Complexity score (0-10)
    complexity = min(10, round(
        (avg_depth * 1.5) +
        (func_count / max(total, 1) * 20) +
        (max_depth * 0.5)
    ))

    # Comment density (0-1)
    comment_density = comment_lines / max(total - blank, 1)

    # Entropy (how varied are the line lengths)
    lengths = [len(l) for l in lines if l.strip()]
    if lengths:
        mean_len = sum(lengths) / len(lengths)
        variance = sum((l - mean_len) ** 2 for l in lengths) / len(lengths)
        entropy = min(10, math.sqrt(variance) / 10)
    else:
        entropy = 0

    return {
        "path":            str(path),
        "ext":             ext,
        "lines":           total,
        "blank":           blank,
        "comment_lines":   comment_lines,
        "comment_density": comment_density,
        "func_count":      func_count,
        "avg_depth":       avg_depth,
        "max_depth":       max_depth,
        "complexity":      complexity,
        "entropy":         entropy,
        "size":            path.stat().st_size,
    }

# ─── Project Scanner ───────────────────────────────────────────
def scan_project(root: Path) -> dict:
    """Walk a directory and collect all file metrics."""
    files = []
    skipped = 0

    for dirpath, dirnames, filenames in os.walk(root):
        # Prune skip dirs in-place
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fname in filenames:
            fpath = Path(dirpath) / fname
            if fpath.suffix.lower() not in LANGUAGES:
                skipped += 1
                continue
            result = scan_file(fpath)
            if result:
                files.append(result)

    return {"files": files, "skipped": skipped, "root": str(root)}

# ─── DNA Metrics Calculator ────────────────────────────────────
def compute_dna(scan: dict) -> dict:
    files = scan["files"]
    if not files:
        return {}

    total_lines    = sum(f["lines"] for f in files)
    total_files    = len(files)
    total_funcs    = sum(f["func_count"] for f in files)
    total_comments = sum(f["comment_lines"] for f in files)
    total_blank    = sum(f["blank"] for f in files)
    total_size     = sum(f["size"] for f in files)

    avg_complexity     = sum(f["complexity"] for f in files) / total_files
    avg_depth          = sum(f["avg_depth"] for f in files) / total_files
    avg_comment_density= sum(f["comment_density"] for f in files) / total_files
    avg_entropy        = sum(f["entropy"] for f in files) / total_files

    # Language breakdown
    lang_lines = defaultdict(int)
    lang_files = defaultdict(int)
    for f in files:
        lang_lines[f["ext"]] += f["lines"]
        lang_files[f["ext"]] += 1

    # Sort by lines
    lang_breakdown = sorted(lang_lines.items(), key=lambda x: -x[1])

    # Complexity distribution
    complexity_dist = Counter(
        "high" if f["complexity"] >= 7 else
        "med"  if f["complexity"] >= 4 else "low"
        for f in files
    )

    # Generate unique fingerprint hash
    sig_str = f"{total_lines}{total_files}{avg_complexity:.2f}{avg_entropy:.2f}"
    for ext, cnt in lang_breakdown[:3]:
        sig_str += f"{ext}{cnt}"
    fingerprint = hashlib.md5(sig_str.encode()).hexdigest()[:12].upper()

    # Personality archetype
    archetype, archetype_desc = get_archetype(
        avg_complexity, avg_comment_density, avg_depth,
        len(lang_breakdown), avg_entropy
    )

    return {
        "total_lines":         total_lines,
        "total_files":         total_files,
        "total_funcs":         total_funcs,
        "total_comments":      total_comments,
        "total_blank":         total_blank,
        "total_size":          total_size,
        "avg_complexity":      avg_complexity,
        "avg_depth":           avg_depth,
        "avg_comment_density": avg_comment_density,
        "avg_entropy":         avg_entropy,
        "lang_breakdown":      lang_breakdown,
        "lang_files":          dict(lang_files),
        "complexity_dist":     dict(complexity_dist),
        "fingerprint":         fingerprint,
        "archetype":           archetype,
        "archetype_desc":      archetype_desc,
        "files":               files,
    }

# ─── Archetype Engine ──────────────────────────────────────────
def get_archetype(complexity, comment_density, depth, lang_count, entropy):
    archetypes = []

    if complexity >= 7 and comment_density < 0.1:
        archetypes.append(("⚡ The Dark Wizard",
            "High complexity, minimal comments. Powerful but cryptic. Others fear this code."))
    if complexity >= 7 and comment_density >= 0.15:
        archetypes.append(("🏛️ The Scholar",
            "Complex yet well-documented. A rare breed — power with clarity."))
    if complexity < 4 and comment_density >= 0.2:
        archetypes.append(("📖 The Teacher",
            "Clean, simple, heavily commented. Built to be understood, not just executed."))
    if complexity < 4 and comment_density < 0.1:
        archetypes.append(("🥷 The Minimalist",
            "Clean and silent. Every line earns its place. No noise."))
    if lang_count >= 5:
        archetypes.append(("🌍 The Polyglot",
            "Many languages coexist. A diverse ecosystem — or a beautiful mess."))
    if depth >= 4:
        archetypes.append(("🕳️ The Architect",
            "Deep nesting, layered logic. Complexity lives inside complexity."))
    if entropy >= 6:
        archetypes.append(("🎲 The Chaotician",
            "Wildly varied line lengths and patterns. Organic, unpredictable, alive."))
    if not archetypes:
        archetypes.append(("🔬 The Engineer",
            "Balanced, pragmatic, consistent. Gets the job done without drama."))

    chosen = archetypes[0]
    return chosen

# ─── DNA Strand Renderer ───────────────────────────────────────
def render_dna_strand(dna: dict, width: int = 60):
    """Render the core visual DNA double helix."""
    files   = dna["files"]
    n       = min(len(files), width)
    samples = files[:n] if len(files) <= n else random.sample(files, n)

    # Sort by path for determinism
    samples.sort(key=lambda f: f["path"])

    print()
    print(col("  🧬  DNA STRAND  ", C.BOLD + C.BWHITE) +
          col(f"[ {dna['fingerprint']} ]", C.BOLD + C.BCYAN))
    print()

    # Build top strand, bridge, bottom strand
    top_strand    = []
    bridge        = []
    bottom_strand = []

    for i, f in enumerate(samples):
        ext   = f["ext"]
        linfo = LANGUAGES.get(ext, {})
        lc    = linfo.get("color", C.WHITE)

        # Top strand — complexity encoded
        c = f["complexity"]
        if c >= 7:
            top_char, top_col = "█", C.BRED
        elif c >= 4:
            top_char, top_col = "▓", C.BYELLOW
        else:
            top_char, top_col = "░", C.BGREEN

        # Bridge — language-colored connector
        angle = math.sin(i * 0.4)
        if angle > 0.5:
            bridge_char = "╫"
            bridge_col  = lc
        elif angle > 0:
            bridge_char = "┼"
            bridge_col  = C.GRAY
        elif angle > -0.5:
            bridge_char = "╪"
            bridge_col  = lc
        else:
            bridge_char = "│"
            bridge_col  = C.DIM + C.GRAY

        # Bottom strand — comment density encoded
        cd = f["comment_density"]
        if cd >= 0.2:
            bot_char, bot_col = "C", C.BCYAN
        elif cd >= 0.05:
            bot_char, bot_col = "·", C.CYAN
        else:
            bot_char, bot_col = "▪", C.GRAY

        top_strand.append(col(top_char, top_col))
        bridge.append(col(bridge_char, bridge_col))
        bottom_strand.append(col(bot_char, bot_col))

    indent = "  "
    chunk  = 50  # chars per row

    for start in range(0, len(samples), chunk):
        end    = start + chunk
        t_row  = top_strand[start:end]
        br_row = bridge[start:end]
        bt_row = bottom_strand[start:end]

        # Helix effect — offset bottom strand
        offset = "  " if (start // chunk) % 2 == 0 else ""

        print(indent + "".join(t_row))
        print(indent + "".join(br_row))
        print(indent + offset + "".join(bt_row))
        print()

    # Legend
    print(col("  LEGEND", C.BOLD + C.BWHITE))
    print(col("  Top strand  :", C.GRAY) +
          col(" █ High", C.BRED) + col(" ▓ Med", C.BYELLOW) + col(" ░ Low", C.BGREEN) +
          col("  complexity", C.GRAY))
    print(col("  Bridge      :", C.GRAY) + col(" language color", C.CYAN))
    print(col("  Bot strand  :", C.GRAY) +
          col(" C rich", C.BCYAN) + col(" · some", C.CYAN) + col(" ▪ sparse", C.GRAY) +
          col("  comments", C.GRAY))
    print()

# ─── Language Bar Chart ────────────────────────────────────────
def render_language_bars(dna: dict):
    total = dna["total_lines"] or 1
    breakdown = dna["lang_breakdown"][:8]

    print(col("  🔬  GENOME COMPOSITION", C.BOLD + C.BWHITE))
    print()

    max_bar = term_width() - 36

    for ext, lines in breakdown:
        linfo = LANGUAGES.get(ext, {"name": ext, "color": C.WHITE, "symbol": "?"})
        pct   = lines / total
        bar_w = max(1, int(pct * max_bar))
        bar   = "█" * bar_w

        name_padded = (linfo["name"])[:12].ljust(12)
        pct_str     = f"{pct*100:5.1f}%"

        print(f"  {linfo['symbol']}  {col(name_padded, linfo['color'] + C.BOLD)}  "
              f"{col(bar, linfo['color'])}"
              f"  {col(pct_str, C.BWHITE)}  {col(str(lines) + ' lines', C.GRAY)}")

    print()

# ─── Stats Panel ───────────────────────────────────────────────
def render_stats(dna: dict):
    print(col("  📊  VITAL STATISTICS", C.BOLD + C.BWHITE))
    print()

    def stat(label, value, unit="", color=C.BWHITE):
        print(f"  {col(label.ljust(22), C.GRAY)}  {col(str(value), color + C.BOLD)}  {col(unit, C.DIM)}")

    stat("Total Lines",        f"{dna['total_lines']:,}",   "lines of code",  C.BGREEN)
    stat("Source Files",       f"{dna['total_files']:,}",   "files",          C.BCYAN)
    stat("Functions/Methods",  f"{dna['total_funcs']:,}",   "callables",      C.BYELLOW)
    stat("Comment Lines",      f"{dna['total_comments']:,}","lines",          C.CYAN)
    stat("Blank Lines",        f"{dna['total_blank']:,}",   "lines",          C.GRAY)
    stat("Codebase Size",      _human_size(dna['total_size']), "",             C.BWHITE)

    print()

    # Mini complexity gauge
    ac = dna["avg_complexity"]
    gauge_w  = 20
    filled   = int((ac / 10) * gauge_w)
    gauge_c  = C.BGREEN if ac < 4 else C.BYELLOW if ac < 7 else C.BRED
    gauge    = col("█" * filled, gauge_c) + col("░" * (gauge_w - filled), C.GRAY)
    print(f"  {col('Avg Complexity'.ljust(22), C.GRAY)}  {gauge}  {col(f'{ac:.1f}/10', gauge_c + C.BOLD)}")

    cd   = dna["avg_comment_density"] * 100
    cd_c = C.BGREEN if cd >= 15 else C.BYELLOW if cd >= 5 else C.BRED
    filled2 = int((min(cd, 30) / 30) * gauge_w)
    gauge2   = col("█" * filled2, cd_c) + col("░" * (gauge_w - filled2), C.GRAY)
    print(f"  {col('Comment Density'.ljust(22), C.GRAY)}  {gauge2}  {col(f'{cd:.1f}%', cd_c + C.BOLD)}")

    ent   = dna["avg_entropy"]
    ent_c = C.BMAGENTA if ent >= 6 else C.BYELLOW if ent >= 3 else C.CYAN
    filled3 = int((ent / 10) * gauge_w)
    gauge3   = col("█" * filled3, ent_c) + col("░" * (gauge_w - filled3), C.GRAY)
    print(f"  {col('Code Entropy'.ljust(22), C.GRAY)}  {gauge3}  {col(f'{ent:.1f}/10', ent_c + C.BOLD)}")

    print()

# ─── Archetype Card ────────────────────────────────────────────
def render_archetype(dna: dict):
    name, desc = dna["archetype"][0], dna["archetype"][1]
    w = min(term_width() - 4, 66)
    border_col = C.BMAGENTA

    top    = col("╔" + "═" * (w - 2) + "╗", border_col)
    bottom = col("╚" + "═" * (w - 2) + "╝", border_col)

    def row(text, text_color=""):
        plain = re.sub(r"\033\[[0-9;]*m", "", text)
        pad   = w - 2 - len(plain) - 1
        return col("║", border_col) + " " + (text_color + text + C.RESET if text_color else text) + " " * max(0, pad) + col("║", border_col)

    print(top)
    print(row(""))
    print(row(f"  🧬  CODEBASE ARCHETYPE", C.BOLD + C.BWHITE))
    print(row(""))
    print(row(f"  {name}", C.BOLD + C.BMAGENTA))
    print(row(""))

    # Wrap description
    wrapped = []
    for line in re.sub(r"\s+", " ", desc).split(". "):
        if line:
            wrapped.extend(re.findall(r".{1,58}", line + "."))
    for wline in wrapped[:3]:
        print(row(f"  {wline}", C.ITALIC + C.BWHITE))

    print(row(""))
    print(row(f"  Fingerprint: {dna['fingerprint']}", C.GRAY))
    print(row(""))
    print(bottom)
    print()

# ─── Hot Files ─────────────────────────────────────────────────
def render_hotfiles(dna: dict):
    files = sorted(dna["files"], key=lambda f: -f["complexity"])[:5]
    if not files:
        return

    print(col("  🔥  COMPLEXITY HOTSPOTS", C.BOLD + C.BWHITE))
    print()

    for i, f in enumerate(files, 1):
        linfo = LANGUAGES.get(f["ext"], {"color": C.WHITE, "name": "?"})
        name  = Path(f["path"]).name[:40]
        bar_w = int(f["complexity"] * 2)
        bar   = col("█" * bar_w, C.BRED if f["complexity"] >= 7 else C.BYELLOW)
        print(f"  {col(str(i), C.GRAY)}.  {col(name.ljust(42), linfo['color'])}  "
              f"{bar}  {col(str(f['complexity']) + '/10', C.BWHITE)}")
        print(f"       {col(str(f['lines']) + ' lines', C.GRAY)}  "
              f"{col(str(f['func_count']) + ' funcs', C.GRAY)}  "
              f"{col('depth ' + str(f['max_depth']), C.GRAY)}")
    print()

# ─── Helpers ───────────────────────────────────────────────────
def _human_size(b: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if b < 1024:
            return f"{b:.1f} {unit}"
        b /= 1024
    return f"{b:.1f} TB"

# ─── Animated Scan Progress ────────────────────────────────────
SPINNER = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]

def animate_scan(root: Path) -> dict:
    sys.stdout.write(col("\n  Sequencing DNA", C.CYAN))
    sys.stdout.flush()

    scan = {"files": [], "skipped": 0, "root": str(root)}
    i = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fname in filenames:
            fpath = Path(dirpath) / fname
            if fpath.suffix.lower() not in LANGUAGES:
                scan["skipped"] += 1
                continue
            result = scan_file(fpath)
            if result:
                scan["files"].append(result)
            sys.stdout.write(f"\r  {SPINNER[i % len(SPINNER)]}  Sequencing DNA...  "
                             f"{col(str(len(scan['files'])) + ' files', C.BWHITE)}")
            sys.stdout.flush()
            i += 1
            time.sleep(0.002)

    sys.stdout.write(f"\r  ✅  Sequencing complete — "
                     f"{col(str(len(scan['files'])) + ' source files', C.BGREEN)} analyzed\n")
    sys.stdout.flush()
    return scan

# ─── Export JSON ───────────────────────────────────────────────
def export_json(dna: dict, root: Path):
    out = {
        "generated":        datetime.datetime.now().isoformat(),
        "project":          str(root),
        "fingerprint":      dna["fingerprint"],
        "archetype":        dna["archetype"][0],
        "total_lines":      dna["total_lines"],
        "total_files":      dna["total_files"],
        "avg_complexity":   round(dna["avg_complexity"], 2),
        "avg_entropy":      round(dna["avg_entropy"], 2),
        "comment_density":  round(dna["avg_comment_density"], 3),
        "languages":        {ext: lines for ext, lines in dna["lang_breakdown"]},
        "hotspots": [
            {"file": Path(f["path"]).name, "complexity": f["complexity"]}
            for f in sorted(dna["files"], key=lambda x: -x["complexity"])[:10]
        ],
    }
    path = Path(f"codedna_{dna['fingerprint']}.json")
    path.write_text(json.dumps(out, indent=2))
    print(col(f"  💾  Report saved → {path}", C.BGREEN))

# ─── Splash ────────────────────────────────────────────────────
SPLASH = r"""
   ██████╗ ██████╗ ██████╗ ███████╗██████╗ ███╗   ██╗ █████╗
  ██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔══██╗████╗  ██║██╔══██╗
  ██║     ██║   ██║██║  ██║█████╗  ██║  ██║██╔██╗ ██║███████║
  ██║     ██║   ██║██║  ██║██╔══╝  ██║  ██║██║╚██╗██║██╔══██║
  ╚██████╗╚██████╔╝██████╔╝███████╗██████╔╝██║ ╚████║██║  ██║
   ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝
"""

def splash():
    clear()
    for line in SPLASH.split("\n"):
        center(line, color=C.BCYAN)
    center(col("Your Codebase's Genetic Fingerprint", C.DIM + C.CYAN))
    print()

# ─── Main ──────────────────────────────────────────────────────
HELP = f"""
{col('CodeDNA', C.BOLD + C.BCYAN)} — Your Codebase's Genetic Fingerprint

{col('USAGE', C.BOLD)}
  python codedna.py <path>            Scan a project folder
  python codedna.py <path> --export   Also save JSON report
  python codedna.py <path> --no-dna   Skip DNA strand visual
  python codedna.py <path> --hot      Only show hotspots

{col('EXAMPLES', C.BOLD)}
  python codedna.py .
  python codedna.py ~/projects/myapp --export
  python codedna.py /usr/lib/python3 --no-dna
"""

def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("path",     nargs="?", default=".")
    parser.add_argument("--export", action="store_true")
    parser.add_argument("--no-dna", action="store_true")
    parser.add_argument("--hot",    action="store_true")
    parser.add_argument("--help",   action="store_true")
    args = parser.parse_args()

    if args.help:
        splash()
        print(HELP)
        return

    root = Path(args.path).resolve()
    if not root.exists():
        print(col(f"\n  ✗  Path not found: {root}", C.BRED))
        sys.exit(1)

    splash()
    print(col(f"  📁  Project: ", C.GRAY) + col(str(root), C.BWHITE))
    print(col(f"  📅  Scanned: ", C.GRAY) + col(datetime.datetime.now().strftime("%B %d, %Y %H:%M"), C.GRAY))
    hr()

    scan = animate_scan(root)

    if not scan["files"]:
        print(col("\n  No supported source files found.\n", C.YELLOW))
        print(col(f"  Supported: {', '.join(LANGUAGES.keys())}", C.GRAY))
        return

    dna = compute_dna(scan)

    hr()
    render_archetype(dna)

    if not args.hot:
        if not args.no_dna:
            render_dna_strand(dna)
            hr()
        render_language_bars(dna)
        hr()
        render_stats(dna)
        hr()

    render_hotfiles(dna)

    if args.export:
        hr()
        export_json(dna, root)

    print()

if __name__ == "__main__":
    main()
