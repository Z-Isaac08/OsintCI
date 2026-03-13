# 🔍 OSINT CI

> Ivoirian Phone Number Intelligence Tool

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Country](https://img.shields.io/badge/Country-Côte%20d'Ivoire-orange)
![Version](https://img.shields.io/badge/Version-1.0.0-purple)

---

## 📌 Description

**OSINT CI** is an open-source intelligence tool focused on Ivoirian phone numbers (+225).
It allows analysts, researchers, and security professionals to quickly gather publicly
available information about a phone number registered in Côte d'Ivoire.

Built for educational purposes and professional OSINT workflows.

---

## ✨ Features

- ✅ Phone number validation (format + existence)
- ✅ Carrier & line type identification (Orange CI, MTN CI, Moov Africa)
- ✅ Geographic zone detection (Abidjan, Bouaké, San-Pédro, Korhogo...)
- ✅ Spam / fraud risk scoring with pattern analysis
- ✅ Local blacklist lookup & community reporting
- ✅ Social media presence links (WhatsApp, Telegram)
- ✅ Google Dorks generation (TikTok, Facebook, Instagram, LinkedIn, Twitter)
- ✅ Ivoirian-specific dorks (abidjan.net, coinafrique.ci, jumia.ci...)
- ✅ Name search dorks (Truecaller web, Facebook)
- ✅ Email discovery dorks linked to a phone number
- ✅ Standalone email OSINT analysis
- ✅ JSON export
- ✅ Rich CLI interface

---

## ⚙️ Installation

**Requirements:** Python 3.8+

```bash
# Clone the repository
git clone https://github.com/yourusername/osint-ci.git
cd osint-ci

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt
```

---

## 📦 Dependencies

```
phonenumbers
requests
colorama
rich
beautifulsoup4
typer
```

---

## 🚀 Usage

### Full scan

```bash
python main.py scan +2250707777777
python main.py scan +2250707777777 --export    # Export to JSON
python main.py scan +2250707777777 -e          # Short flag
```

### Validate a number

```bash
python main.py validate +2250707777777
```

### Carrier lookup

```bash
python main.py carrier +2250707777777
```

### Spam check

```bash
python main.py spam +2250707777777
```

### Social media & dorks

```bash
python main.py social +2250707777777
```

### Email OSINT

```bash
# Discover emails linked to a phone number
python main.py email +2250707777777

# Analyze a standalone email address
python main.py email contact@exemple.ci
```

### Report a number

```bash
python main.py report +2250707777777
python main.py report +2250707777777 --type arnaque
python main.py report +2250707777777 -t spam
python main.py report +2250707777777 -t harcelement
```

### Help

```bash
python main.py --help
python main.py scan --help
```

---

## 📤 Output Example

```bash
$ python main.py scan +2250708234519
```

```
╭─────────────────╮
│ ✓ Scan Complete │
╰─────────────────╯
  Number       +2250708234519
  Valid        ✅ Yes
  Carrier      MTN CI
  Line Type    Mobile
  Risk Level   Low
  Spam         ✅ No
  Email Dorks  3 generated
```

### JSON Export (`--export`)

```json
{
  "timestamp": "2026-01-15T14:32:10.123456",
  "number": "+2250708234519",
  "validation": {
    "valid": true,
    "e164": "+2250708234519",
    "international": "+225 07 08 23 45 19",
    "carrier": "MTN CI",
    "region": "Côte d'Ivoire",
    "number_type": "Mobile"
  },
  "carrier": {
    "prefix": "07",
    "operator": "MTN CI",
    "line_type": "Mobile",
    "portability_note": "Ce préfixe indique l'opérateur d'origine, pas forcément l'opérateur actuel."
  },
  "spam": {
    "is_spam": false,
    "risk_score": 0,
    "risk_level": "Low",
    "database_match": false,
    "suspicious_pattern": false,
    "pattern_reason": null,
    "note": "Aucune correspondance dans la liste noire locale."
  },
  "social": {
    "whatsapp": {
      "checked": true,
      "found": "unknown",
      "link": "https://wa.me/2250708234519"
    },
    "telegram": {
      "checked": true,
      "found": "unknown",
      "link": "https://t.me/+2250708234519"
    }
  },
  "email_discovery": {
    "email_discovery": {
      "dork": "\"0708234519\" \"@gmail.com\" OR \"@yahoo.fr\" OR \"@outlook.com\"",
      "url": "https://www.google.com/search?q=..."
    }
  }
}
```

---

## 📁 Project Structure

```
osint-ci/
├── main.py                  # CLI entry point
├── requirements.txt         # Dependencies
├── README.md
├── modules/
│   ├── __init__.py
│   ├── banner.py            # ASCII art banner
│   ├── validator.py         # Number validation & parsing
│   ├── carrier.py           # Operator & region lookup
│   ├── spam_checker.py      # Spam detection & blacklist
│   ├── social_checker.py    # Social media links & dorks
│   └── email_checker.py     # Email OSINT & dorks
├── data/
│   └── spam_numbers.json    # Local spam blacklist
└── output/
    └── .gitkeep             # Exported scan results
```

---

## 🗺️ Supported Operators

| Prefix | Operator    | Type   |
| ------ | ----------- | ------ |
| 01     | Moov Africa | Mobile |
| 05     | MTN CI      | Mobile |
| 07     | Orange CI   | Mobile |
| 21     | Moov Africa | Fixe   |
| 25     | MTN CI      | Fixe   |
| 27     | Orange CI   | Fixe   |

---

## 🌍 Supported Regions (Landlines)

| Code | Region          |
| ---- | --------------- |
| 20   | Abidjan Plateau |
| 21   | Abidjan Sud     |
| 22   | Cocody          |
| 23   | Yopougon        |
| 24   | Abobo           |
| 30   | Yamoussoukro    |
| 31   | Bouaké          |
| 32   | Daloa           |
| 33   | Man             |
| 34   | San-Pédro       |
| 35   | Abengourou      |
| 36   | Korhogo         |

---

## 🔭 Roadmap (v2)

- [ ] Truecaller automatic lookup via Camoufox
- [ ] SerpAPI integration for real Google search results
- [ ] HaveIBeenPwned API for leak detection
- [ ] Batch scan (multiple numbers at once)
- [ ] Web interface (Flask/FastAPI)
- [ ] Telegram bot integration

---

## ⚠️ Legal Disclaimer

This tool is intended for **educational and research purposes only**.
All data used is sourced from **publicly available information**.

- Do **not** use this tool to harass, stalk, or harm individuals
- Do **not** use this tool for illegal surveillance
- The author is **not responsible** for any misuse of this tool
- Usage must comply with **Ivoirian law** (Loi n°2013-450 sur la protection des données personnelles)
- Results may be **inaccurate** — always verify through official channels
- The spam blacklist is community-based and may contain errors

By using this tool, you agree to use it **responsibly and legally**.

---

## 👤 Author

**ZC0ok**
Cybersecurity Student | OSINT Researcher
🇨🇮 Côte d'Ivoire

---

## 📄 License

This project is licensed under the **MIT License**.
See [LICENSE](LICENSE) for details.

---

> _"With great power comes great responsibility."_
