# FRIDAY AI — User Manual

## Overview

FRIDAY is a modular, voice‑controlled AI assistant with **12 domains**
of functionality. This manual lists every voice command organized by domain.

---

## 1. Core Voice (always on)

| Command                    | Response                              |
| -------------------------- | ------------------------------------- |
| `time`                     | "The time is 2:30 PM"                |
| `what time is it`          | "The time is 2:30 PM"                |
| `date`                     | "Today is June 10, 2026"             |
| `what is the date`         | "Today is June 10, 2026"             |
| `help`                     | Lists available features              |
| `exit` / `quit` / `bye`    | Shuts down                            |

---

## 2. Learning Memory (learning_memory)

| Command                                    | Response                                |
| ------------------------------------------ | --------------------------------------- |
| `my name is Ayush`                         | "Got it! I will remember you as Ayush." |
| `mera naam Ayush hai`                      | "Got it! I will remember you as Ayush." |
| `call me FRIDAY`                           | "Got it! I will remember you as FRIDAY."|
| `I like pizza`                             | "I will remember that you like pizza."  |
| `mujhe coffee`                             | "I will remember that you like coffee." |
| `mera favorite color blue`                 | "I will remember that you like blue."   |
| `i love machine learning`                  | "I will remember that you like machine learning." |
| `what is my name`                          | "Your name is Ayush."                   |
| `mera naam kya hai`                        | "Your name is Ayush."                   |
| `who am i`                                 | "Your name is Ayush."                   |
| `what do you remember about me`            | Lists all saved preferences             |

---

## 3. Multi‑Agent (multi_agent)

| Command                               | Response                                    |
| ------------------------------------- | ------------------------------------------- |
| `agent status`                        | "Available agents: 4 agents"                |
| `list agents`                         | "Available agents: 4 agents"                |
| `search the web for Python`           | Decomposes into web search subtask          |
| `find and save that to a file`        | Multi-agent coordination                    |
| `check CPU and create a report`       | System + file agents work together          |
| `look up weather and save it`         | Search + save agents                        |
| `run a system diagnostic`             | System agent execution                      |

---

## 4. Browser Engine (browser_engine)

| Command                                         | Response                                      |
| ----------------------------------------------- | --------------------------------------------- |
| `open example.com`                              | "Opened Example Domain"                       |
| `open https://github.com`                       | "Opened GitHub"                               |
| `open google.com`                               | "Opened Google"                               |
| `scrape https://example.com`                    | "Page has 1024 characters of text." / summary |
| `scrape wikipedia.org`                          | Summarizes or reports text length             |
| `download files from https://example.com/files` | "Provide URLs to download."                   |

---

## 5. Vision (nim_vision)

| Command                                             | Response                                        |
| --------------------------------------------------- | ----------------------------------------------- |
| `what is on my screen`                              | Captures and describes screen (BLIP/NVIDIA)     |
| `what is on the screen`                             | Captures and describes screen                   |
| `what screen`                                       | Captures and describes screen                   |
| `find the search button on screen`                  | Locates element and moves mouse                 |
| `find the submit icon on screen`                    | Locates element on screen                       |
| `find the close button`                             | Locates close button                            |
| `read text from image screenshot.png`               | "OCR requires pytesseract…"                     |
| `ocr document.jpg`                                  | "OCR requires pytesseract…"                     |

---

## 6. Media Studio (media_studio)

| Command                                                   | Response                                  |
| --------------------------------------------------------- | ----------------------------------------- |
| `trim silence recording.wav`                              | Trims silent segments from audio          |
| `trim silence audio.mp3`                                  | Trims from audio file                     |
| `convert video.mp4 to .mp3`                               | Converts format via ffmpeg                |
| `convert audio.wav to .flac`                              | Converts to FLAC                          |
| `extract vocals music.mp3`                                | Separates vocal track                     |
| `extract vocals song.wav`                                 | Separates from WAV                        |
| `generate subtitle video.mp4`                             | Creates SRT via Whisper                   |
| `generate subtitle lecture.mp4`                           | Creates subtitles                         |
| `crop video.mp4 for tiktok`                               | Crops to 9:16 for TikTok                  |
| `crop video for instagram`                                | Crops to 1:1 for Instagram                |
| `crop video for youtube`                                  | Crops to 16:9 for YouTube                 |
| `watermark images folder`                                 | Adds watermark to all images              |
| `compress images folder`                                  | Compresses all images in folder           |
| `compress image.jpg`                                      | Compresses single image                   |
| `convert video.mp4 to gif`                                | Creates animated GIF                      |
| `convert animation.mov to gif`                            | Creates GIF from MOV                      |
| `scrub metadata photo.jpg`                                | Removes EXIF/metadata from image          |
| `scrub metadata video.mp4`                                | Removes metadata from video               |

---

## 7. HUD (hud_gui)

| Command                  | Response                       |
| ------------------------ | ------------------------------ |
| `launch hud`             | Opens transparent overlay      |
| `show hud`               | Opens transparent overlay      |
| `hide hud`               | Closes HUD window              |
| `close hud`              | Closes HUD window              |
| `theme matrix`           | Applies Matrix green theme     |
| `theme cyber`            | Applies Cyberpunk theme        |
| `theme minimal`          | Applies Minimal theme          |
| `theme neon`             | Applies Neon theme             |
| `theme aurora`           | Applies Aurora theme           |

---

## 8. Self‑Evolution (self_evolution)

| Command                    | Response                                      |
| -------------------------- | --------------------------------------------- |
| `self-heal`                | Runs diagnostics, checks health + memory      |
| `self heal`                | Runs diagnostics                              |
| `update yourself`          | Pulls latest code from git                    |
| `update myself`            | Pulls latest code from git                    |
| `system status`            | Reports health of voice, LLM, memory          |
| `status report`            | Reports health of voice, LLM, memory          |

---

## 9. Security Vault (security_vault)

| Command                                 | Response                                       |
| --------------------------------------- | ---------------------------------------------- |
| `security status`                       | "All security modules active."                 |
| `encrypt .env`                          | Encrypts environment file with Fernet          |
| `verify system integrity`               | Checks file hashes against manifest            |
| `check integrity`                       | Checks file hashes                             |
| `privacy mode`                          | Enables PII masking                            |
| `enable privacy`                        | Enables PII masking                            |
| `security log`                          | "Security log requires master password."       |

---

## 10. DevOps Compiler (devops_compiler)

| Command                                                          | Response                                        |
| ---------------------------------------------------------------- | ----------------------------------------------- |
| `generate code for a Flask REST API`                             | Asks language, generates code                   |
| `generate code for a React component`                            | Asks language, generates React JSX              |
| `generate code for a SQLAlchemy User model`                      | Generates model code                            |
| `git status`                                                     | Shows working tree status                       |
| `git commit with message added login feature`                    | Stages all and commits                          |
| `create database schema for a blog platform`                     | Generates SQL schema                            |
| `create database schema for an ecommerce store`                  | Generates SQL schema                            |
| `build docker image for this project`                            | Creates Dockerfile and builds image             |
| `generate tests for main.py`                                     | Creates pytest file with test cases             |
| `generate tests for core/voice.py`                               | Creates pytest file for voice module            |
| `benchmark function sort_large_list`                             | Notes: needs function reference                 |
| `extract emails from contact.txt`                                | Extracts and saves to JSON                      |
| `extract emails from data.txt`                                   | Extracts all email addresses                    |
| `create report from README.md`                                   | Converts to PDF (weasyprint/pandoc)             |
| `create report from docs/guide.md`                               | Generates PDF from markdown                     |

---

## 11. Data Analytics (data_analytics)

| Command                                                         | Response                                        |
| --------------------------------------------------------------- | ----------------------------------------------- |
| `analyze sales.csv`                                             | Summary stats: rows, columns, mean, min, max    |
| `analyze data.xlsx`                                             | Summary stats from Excel                        |
| `analyze report.xls`                                            | Summary stats from old Excel                    |
| `plot revenue vs month from sales.csv`                          | Creates scatter chart (PNG)                     |
| `plot temperature vs pressure from weather.csv`                 | Creates scatter chart                           |
| `extract tables from invoice.pdf`                               | Extracts tables to CSV                          |
| `extract tables from report.pdf`                                | Extracts all tables from PDF                    |
| `validate data.json against schema.json`                        | Validates and reports errors                    |
| `merge sales1.xlsx sales2.xlsx into combined.xlsx`              | Merges Excel files                              |
| `merge report1.xlsx report2.xlsx`                               | Combines workbooks                              |
| `forecast sales from monthly.csv for 6`                         | Linear regression forecast + saves CSV          |
| `forecast temperature from climate.csv for 12`                  | Predicts next 12 values                         |
| `anonymize contacts.txt`                                        | Redacts emails and phone numbers                |
| `anonymize customer_data.txt`                                   | Redacts PII                                    |
| `create report from data summary.csv`                           | Generates PowerPoint (python-pptx)              |
| `create report from data financials.csv`                        | Generates PPT with summary table                |

---

## 12. General / Catch‑all (real_ai_brain)

These are handled by the LLM when no specific command pattern matches:

| Command (examples)                            |
| --------------------------------------------- |
| `What is machine learning?`                   |
| `Explain quantum computing in simple terms`   |
| `Tell me a joke`                              |
| `What is the capital of France?`              |
| `How do I make pancakes?`                     |
| `Write a poem about AI`                       |
| `What is 2 + 2?`                              |
| `Translate hello to Spanish`                  |
| `Give me a recipe for pasta`                  |
| `What is the meaning of life?`                |
| `Explain binary search`                       |
| `What is the difference between HTTP and HTTPS?` |
| `Tell me about the solar system`              |
| `How does GPS work?`                          |
| `What is blockchain?`                         |
| `Explain REST APIs`                           |
| `What is the weather like?` (if weather disabled, LLM replies) |
| `Who wrote Romeo and Juliet?`                 |
| `What is the speed of light?`                 |
| `How do I learn Python?`                      |
| `Tell me a fun fact`                          |
| `What is your favorite color?`                |
| `How are you?`                                |
| `What can you do?`                            |

---

## Feature Interaction Notes

| Feature A (enabled) | Feature B (enabled) | Behaviour                                           |
| ------------------- | ------------------- | --------------------------------------------------- |
| `multi_agent`       | —                   | Complex tasks are decomposed into subtasks          |
| `real_ai_brain`     | `learning_memory`   | LLM responses are stored and retrieved as context   |
| `real_ai_brain`     | `data_analytics`    | After CSV analysis, ask natural questions about data |
| `hud_gui`           | `data_analytics`    | Charts appear in HUD popup                          |
| `self_evolution`    | `devops_compiler`   | Generated code can be auto-loaded as plugins        |
| `learning_memory`   | `devops_compiler`   | Preferred code styles stored and reused             |
| `security_vault`    | `data_analytics`    | Anonymized data can be safely analyzed              |

---

## Configuration Tips

```python
# config.py — enable feature domains
FEATURES = {
    "core_voice": True,        # Required for voice I/O
    "real_ai_brain": True,     # OpenRouter LLM
    "learning_memory": True,   # ChromaDB
    "multi_agent": True,       # Task decomposition
    # Set others to True as needed
}
```

For headless/server mode, create `config_production.json`:
```json
{
    "features": { "core_voice": false, "hud_gui": false },
    "log_level": "WARNING"
}
```

---

## Troubleshooting Voice Commands

| Problem                           | Solution                                          |
| --------------------------------- | ------------------------------------------------- |
| FRIDAY doesn't hear me            | Check microphone permissions, run `test_mic.py`   |
| FRIDAY hears but doesn't respond  | Ensure `real_ai_brain` is True or command matches |
| Command not recognized            | Say the exact phrase from this manual             |
| "That command is not recognized"  | Enable `real_ai_brain` in config.py               |
| Feature says "disabled in config" | Enable the feature flag in config.py and restart  |
