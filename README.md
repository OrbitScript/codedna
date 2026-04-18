# 🧬 CodeDNA — Your Codebase's Genetic Fingerprint

> *Every codebase has a unique DNA. Now you can see yours.*

CodeDNA is a zero-dependency Python CLI that scans any source folder and renders a **visual DNA double helix** of your codebase — encoding complexity, comment density, language mix, and code entropy into a unique, colorized terminal visualization.

No two codebases produce the same strand.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🧬 **DNA Strand** | A double helix where each base pair encodes a file's complexity and comment density |
| 🔬 **Genome Composition** | Language breakdown bar chart (supports 20 languages) |
| 🏛️ **Archetype Engine** | Classifies your codebase: Dark Wizard, Scholar, Minimalist, Polyglot, and more |
| 📊 **Vital Statistics** | Lines, files, functions, comment density, entropy gauges |
| 🔥 **Complexity Hotspots** | Top 5 most complex files with nesting depth |
| 🔑 **Unique Fingerprint** | MD5-based 12-char fingerprint — like a git commit hash for your style |
| 💾 **JSON Export** | Save full report for CI pipelines or historical tracking |

---

## 🚀 Quick Start

```bash
# Scan current directory
python codedna.py .

# Scan any project
python codedna.py ~/projects/myapp

# Save a JSON report
python codedna.py . --export

# Skip the DNA strand visual
python codedna.py . --no-dna

# Only show complexity hotspots
python codedna.py . --hot
```

**Zero dependencies.** Python 3.7+ only.

---

## 📸 Example Output

```
  🧬  DNA STRAND  [ A3F2C1B9D4E8 ]

  ░░▓░░▓▓░▓░░░▓░░░▓░▓░▓░░░░░▓░░▓░░░░▓░░░░░░░▓░░░
  ╫┼╪│╫┼╪│╫┼╪│╫┼╪│╫┼╪│╫┼╪│╫┼╪│╫┼╪│╫┼╪│╫┼╪│
  ··C·▪C··▪·C·▪··C▪·▪·▪···▪··▪·▪·▪····▪···▪▪▪·▪·

  LEGEND
  Top strand :  █ High  ▓ Med  ░ Low  complexity
  Bridge     :  language color
  Bot strand :  C rich  · some  ▪ sparse  comments
```

```
╔════════════════════════════════════════════════════╗
║  🧬  CODEBASE ARCHETYPE                            ║
║                                                    ║
║  ⚡ The Dark Wizard                               ║
║                                                    ║
║  High complexity, minimal comments. Powerful but  ║
║  cryptic. Others fear this code.                  ║
║                                                    ║
║  Fingerprint: A3F2C1B9D4E8                        ║
╚════════════════════════════════════════════════════╝
```

---

## 🏛️ Archetypes

Your codebase will be classified as one of these:

| Archetype | Trigger |
|---|---|
| ⚡ The Dark Wizard | High complexity + sparse comments |
| 🏛️ The Scholar | Complex but well-documented |
| 📖 The Teacher | Simple + heavily commented |
| 🥷 The Minimalist | Clean and silent |
| 🌍 The Polyglot | 5+ languages |
| 🕳️ The Architect | Deep nesting |
| 🎲 The Chaotician | High entropy |
| 🔬 The Engineer | Balanced and pragmatic |

---

## 🌐 Supported Languages

Python, JavaScript, TypeScript, Java, C++, C, Go, Rust, Ruby, PHP, Swift, Kotlin, C#, HTML, CSS, Shell, R, Lua, Dart, Scala

---

## 💾 JSON Export

```bash
python codedna.py . --export
# Saves: codedna_A3F2C1B9D4E8.json
```

Output includes fingerprint, archetype, language breakdown, avg complexity, entropy, and top hotspots — ready for CI integration or tracking code health over time.

---

## 📄 License

MIT — free to use, share, and remix.

---

*Built with ❤️ and pure Python. No dependencies. No cloud. Just your code.*
