# FRIDAY AI — Personal Voice Assistant

FRIDAY is a modular, voice‑controlled AI assistant with 12 domains of
functionality, from voice interaction and browser automation to code generation,
data analytics, and self‑evolution.

---

## 1. Installation

### 1.1 System Requirements

| Component  | Minimum                                        |
| ---------- | ---------------------------------------------- |
| Python     | 3.10 or later                                  |
| OS         | Windows 10+, macOS 13+, Ubuntu 22+             |
| RAM        | 4 GB (8 GB recommended)                        |
| Disk       | 2 GB (for models and dependencies)             |
| Microphone | Required for voice input                       |
| Speakers   | Required for voice output                      |

### 1.2 Install Dependencies

```bash
# Recommended — create a virtual environment first
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate

# Install all packages
pip install -r requirements_full.txt

# Install Playwright browser engine
playwright install chromium
```

> **Tip:** If you only want the core voice assistant, install just the `requirements.txt`
> file instead. The full list includes many optional packages.

### 1.3 System Tools (Optional)

| Tool      | Needed For                    | Install (Windows)                          | Install (macOS)        | Install (Ubuntu)         |
| --------- | ----------------------------- | ------------------------------------------ | ---------------------- | ------------------------ |
| **ffmpeg**  | Audio/video processing        | `winget install ffmpeg` or download from gyan.dev | `brew install ffmpeg`  | `sudo apt install ffmpeg` |
| **git**     | Git version control commands  | `winget install Git.Git`                   | `brew install git`     | `sudo apt install git`   |
| **pandoc**  | PDF report generation (fallback) | `winget install pandoc`                  | `brew install pandoc`  | `sudo apt install pandoc` |

---

## 2. API Keys

FRIDAY uses **OpenRouter** as its default LLM provider. Other APIs are optional.

| Service     | Environment Variable         | Required For              | Get It At                                  |
| ----------- | ---------------------------- | ------------------------- | ------------------------------------------ |
| OpenRouter  | `OPENROUTER_API_KEY`         | `real_ai_brain` (LLM)     | https://openrouter.ai/keys                 |
| NVIDIA NIM  | `NVIDIA_API_KEY`             | `nim_vision` (vision)     | https://build.nvidia.com/                  |
| ElevenLabs  | `ELEVENLABS_API_KEY`         | HUD voice synthesis       | https://elevenlabs.io/                     |
| OpenAI      | `OPENAI_API_KEY`             | Whisper subtitles         | https://platform.openai.com/api-keys       |

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxx
# Optional:
NVIDIA_API_KEY=nvapi-xxxxxxxxxxxx
ELEVENLABS_API_KEY=xxxxxxxxxxxx
OPENAI_API_KEY=sk-xxxxxxxxxxxx
```

> ⚠️ **Never commit `.env` to version control.** It is already listed in `.gitignore`.

---

## 3. Configuration

Edit `config.py` in the project root. Feature flags control which domains
are active at startup:

```python
FEATURES = {
    # Core (always needed)
    "core_voice": True,          # Speech input / output
    "female_voice": True,        # Female TTS voice (False = male/default)
    "real_ai_brain": True,       # OpenRouter LLM
    "learning_memory": True,     # ChromaDB vector memory
    "multi_agent": True,         # Task decomposition

    # Advanced (enable as needed)
    "browser_engine": False,     # Playwright web automation
    "nim_vision": False,         # Screen / image analysis
    "media_studio": False,       # Audio/video editing
    "hud_gui": False,            # Transparent overlay HUD
    "self_evolution": False,     # Auto-update / self-heal
    "security_vault": False,     # Encryption, integrity checks
    "devops_compiler": False,    # Code generation, git, Docker
    "data_analytics": False,     # CSV analysis, charts, reports
}
```

Set a flag to `True` to enable its domain and voice commands.

### Voice Configuration

FRIDAY uses **pyttsx3** for text‑to‑speech. By default, `female_voice` is `True`,
which selects the first available female voice on your system:

| Setting | Effect |
| ------- | ------ |
| `"female_voice": True` | Scans for "female", "Zira", "girl", or "woman" in voice names (default) |
| `"female_voice": False` | Uses the first available voice (usually male) |

**How voice selection works:**
1. On **Windows** — prioritises "Microsoft Zira" (female) if available.
2. On **macOS** — selects "Samantha" or another female voice.
3. On **Linux** — depends on installed speech‑dispatcher voices.
4. If no female voice is found, a warning is logged and the system default is used.

**Alternative TTS engines** (add via `.env`):
- `gTTS` — Google Text‑to‑Speech (always female, no configuration needed).
- `ELEVENLABS_API_KEY` — set in `.env` to use ElevenLabs voices; choose a female
  voice ID like `"Bella"`, `"Rachel"`, or `"Nicole"`.

To switch to a male voice, simply set `"female_voice": False` in `config.py`.

---

## 4. Running

```bash
# Activate virtual environment (if using one)
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate

# Launch FRIDAY
python run_friday.py
```

Say **"help"** to hear available commands based on your enabled features.

Press **Ctrl+C** or say **"exit"**, **"quit"**, or **"bye"** to stop.

### Quick Test

```bash
# Run the integration test suite (no API key required)
python test_integration.py

# Run with full tests (includes LLM call and browser)
python test_integration.py --full
```

---

## 5. Voice Commands (by domain)

### Core
- "what time is it" / "time"
- "what is the date" / "date"
- "help"
- "exit" / "quit" / "bye"

### Learning Memory
- "my name is [name]" / "mera naam [name] hai"
- "I like [thing]" / "remember that I like [thing]"
- "what is my name" / "mera naam kya hai"
- "what do you remember about me"

### Multi-Agent
- "agent status" / "list agents"
- Complex tasks like "search and save" or "check CPU and create a file"

### Browser Engine
- "open [url]"
- "scrape [url]"
- "download files"

### Vision
- "what is on my screen"
- "find [button] on screen"
- "read text from image" / "ocr"

### Media Studio
- "trim silence [file]"
- "convert [file] to [format]"
- "extract vocals [file]"
- "generate subtitle [file]"
- "crop [file] for [platform]"
- "watermark [folder]"
- "compress [file/folder]"
- "convert [file] to gif"
- "scrub metadata [file]"

### HUD
- "launch hud" / "show hud"
- "hide hud" / "close hud"
- "theme [name]"

### Self-Evolution
- "self-heal" / "self heal"
- "update yourself"
- "system status" / "status report"

### Security Vault
- "security status"
- "encrypt .env"
- "verify system integrity" / "check integrity"
- "privacy mode" / "enable privacy"
- "security log"

### DevOps Compiler
- "generate code for [description]"
- "git status"
- "git commit with message [msg]"
- "create database schema for [description]"
- "build docker image for this project"
- "generate tests for [module]"
- "extract emails from [file]"
- "create report from [markdown_file]"

### Data Analytics
- "analyze [file.csv]"
- "plot [x] vs [y] from [file]"
- "extract tables from [file.pdf]"
- "validate [json] against [schema]"
- "merge [file1.xlsx] [file2.xlsx]"
- "forecast [column] from [file] for [periods]"
- "anonymize [file.txt]"
- "create report from data [file.csv]"

---

## 6. Project Structure

```
FRIDAY_ULTIMATE/
├── config.py                    # Feature flags & API keys
├── .env                         # Secrets (gitignored)
├── run_friday.py                # Entry point launcher
├── main.py                      # Command handler
├── test_friday.py               # Core test suite
├── test_integration.py          # Full integration tests
├── requirements.txt             # Core dependencies
├── requirements_full.txt        # All dependencies
├── README_FINAL.md              # This file
│
├── core/                        # Domain 0 — Voice engine
│   └── voice.py
├── advanced/
│   ├── llm/                     # Domain 0 — OpenRouter
│   ├── memory/                  # Domain 2 — ChromaDB + user prefs
│   ├── multi_agent/             # Domain 3 — Coordinator + agents
│   ├── browser_engine/          # Domain 4 — Playwright
│   ├── vision/                  # Domain 5 — BLIP / NVIDIA
│   ├── media_studio/            # Domain 6 — Audio/video
│   ├── hud/                     # Domain 7 — Transparent GUI
│   ├── devops_compiler/         # Domain 8 — Code & DevOps
│   ├── data_analytics/          # Domain 9 — Data & reports
│   ├── self_evolution/          # Domain 10 — Self-heal / update
│   └── security_vault/          # Domain 11 — Encryption & audit
├── output/                      # Generated charts, reports, etc.
├── generated/                   # Generated code files
├── memory_db/                   # ChromaDB persistent storage
└── logs/                        # Startup & runtime logs
```

---

## 7. Troubleshooting

### "No module named 'speech_recognition'"
Make sure your virtual environment is activated and dependencies are installed:
```bash
pip install -r requirements_full.txt
```

### "Microphone not found" or voice input not working
- Check that your microphone is connected and not muted.
- On Windows, go to Settings → Privacy & security → Microphone and allow app access.
- On Linux, install `portaudio`:
  ```bash
  sudo apt install portaudio19-dev python3-pyaudio
  ```

### "Playwright executable not found"
```bash
playwright install chromium
```

### "OpenRouter API key is not set"
Add your key to `.env`:
```
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxx
```

### "ffmpeg not found"
Install ffmpeg (see Section 1.3) and ensure it is on your system PATH.

### "tkinter not found" (HUD)
- Windows: tkinter is included with Python.
- macOS: Reinstall Python from python.org (Homebrew Python includes tkinter).
- Ubuntu: `sudo apt install python3-tk`

### HUD window appears but is unresponsive
The HUD uses tkinter and must run on the main thread on macOS. Try disabling
`hud_gui` in `config.py` if you experience issues.

### Feature X is enabled but commands don't work
Make sure the feature flag is set to `True` in `config.py` and the domain's
dependencies are installed (check with `pip list | grep <package>`).

---

## 8. Updating

FRIDAY can self-update when `self_evolution` is enabled:
```bash
# Say
"update yourself"
```

Or manually:
```bash
git pull
pip install -r requirements_full.txt --upgrade
playwright install chromium
```
