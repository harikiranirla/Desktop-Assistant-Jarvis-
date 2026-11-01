# Desktop Assistant (Jarvis)

A beginner-friendly **Python voice assistant** that listens to your voice, understands simple commands, and performs everyday computer tasks — built for a college-level Python mini project.

---

## Table of Contents

1. [Overview](#overview)
2. [Project Folder Structure](#project-folder-structure)
3. [Required Python Packages](#required-python-packages)
4. [Installation Commands](#installation-commands)
5. [How to Run in VS Code](#how-to-run-in-vs-code)
6. [Features](#features)
7. [Sample Voice Commands & Expected Responses](#sample-voice-commands--expected-responses)
8. [Explanation of Major Functions](#explanation-of-major-functions)
9. [Common Errors & Solutions](#common-errors--solutions)
10. [Future Enhancements](#future-enhancements)

---

## Overview

Jarvis is a desktop voice assistant that uses your microphone to listen for commands, converts speech to text, performs the requested action, and responds with both voice and on-screen text. It includes a clean Tkinter GUI with a status indicator, recognized-command display, response log, and Start/Exit buttons.

**Technologies used:**

| Library | Purpose |
|---|---|
| `speech_recognition` | Capture microphone audio and convert speech to text |
| `pyttsx3` | Text-to-speech (Jarvis speaks back to you) |
| `pyaudio` | Microphone access backend for SpeechRecognition |
| `tkinter` | Graphical user interface (built into Python) |
| `webbrowser` | Open websites in the default browser |
| `subprocess` | Open system applications (calculator, notepad) |
| `datetime` | Get current time, date, and day of the week |
| `threading` | Keep the GUI responsive during listening |

---

## Project Folder Structure

```
Desktop-Assistant-Jarvis/
│
├── jarvis.py              # Main Python source code (GUI + logic)
├── requirements.txt       # List of pip packages to install
├── README.md              # This file
└── .gitignore             # Files to ignore in version control
```

---

## Required Python Packages

| Package | Version | Why |
|---|---|---|
| `SpeechRecognition` | 3.10.1 | Speech-to-text engine |
| `pyttsx3` | 2.90 | Text-to-speech engine |
| `pyaudio` | 0.2.14 | Microphone audio input |

> `tkinter`, `webbrowser`, `subprocess`, `datetime`, `os`, `sys`, and `threading` are all part of Python's standard library — no extra install needed.

---

## Installation Commands

### 1. Install Python

Download and install **Python 3.8 or later** from [python.org](https://www.python.org/downloads/). During installation on Windows, check **"Add Python to PATH"**.

### 2. Install pip packages

Open a terminal and run:

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install SpeechRecognition pyttsx3 pyaudio
```

### 3. PyAudio troubleshooting

**Windows** (if `pip install pyaudio` fails):

```bash
pip install pipwin
pipwin install pyaudio
```

**macOS:**

```bash
brew install portaudio
pip install pyaudio
```

**Linux (Debian/Ubuntu):**

```bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
```

---

## How to Run in VS Code

1. **Open VS Code.**
2. **Open the project folder:** `File → Open Folder → Desktop-Assistant-Jarvis`
3. **Select the Python interpreter:** `Ctrl+Shift+P` → "Python: Select Interpreter" → choose your Python 3.x installation.
4. **Open a terminal in VS Code:** `Terminal → New Terminal`
5. **Install dependencies** (first time only):

   ```bash
   pip install -r requirements.txt
   ```

6. **Run the assistant:**

   ```bash
   python jarvis.py
   ```

7. The Jarvis GUI window will appear. Click **"Start Listening"** and speak a command.

---

## Features

1. **Graphical Interface** — Clean Tkinter window with title, status, LED indicator, command display, response log, and buttons.
2. **Voice Input** — Uses your microphone to capture speech.
3. **Speech to Text** — Converts your speech into text using Google's speech API.
4. **Voice Response** — Jarvis speaks back using pyttsx3 text-to-speech.
5. **On-Screen Display** — Recognized commands and responses are shown in the GUI.
6. **Date & Time** — Tells you the current time and today's date.
7. **Open Websites** — Google, YouTube, Gmail.
8. **Google Search** — Search anything by saying "search [topic]".
9. **Open Applications** — Calculator and Notepad (cross-platform).
10. **Day of the Week** — Tells you what day it is.
11. **Time-Based Greeting** — "Good Morning", "Good Afternoon", or "Good Evening".
12. **Exit Command** — Say "exit" or "bye" to close Jarvis (with confirmation).
13. **Unknown Command Handling** — Politely asks you to repeat if it doesn't understand.
14. **Error Handling** — Shows clear messages if the microphone or speech service is unavailable.

---

## Sample Voice Commands & Expected Responses

| You Say | Jarvis Responds | Action Taken |
|---|---|---|
| "Hello" | "Good Morning! I am Jarvis. How can I help you?" | Greeting |
| "What is the time?" | "The time is 10:30 AM" | Speaks current time |
| "What is today's date?" | "Today's date is September 15, 2026" | Speaks current date |
| "What day is today?" | "Today is Monday" | Speaks day of week |
| "Open Google" | "Opening Google" | Opens google.com |
| "Open YouTube" | "Opening YouTube" | Opens youtube.com |
| "Open Gmail" | "Opening Gmail" | Opens mail.google.com |
| "Search Python tutorials" | "Searching Google for Python tutorials" | Opens Google search |
| "Open calculator" | "Opening calculator" | Opens system calculator |
| "Open notepad" | "Opening notepad" | Opens system text editor |
| "Who are you?" | "I am Jarvis, your desktop assistant..." | Info response |
| "Thank you" | "You're welcome!" | Polite response |
| "Exit" | "Goodbye! Have a nice day." | Closes the app |

---

## Explanation of Major Functions

### `speak(text)`
Converts text to speech using pyttsx3. The text is also returned so it can be displayed in the GUI response area.

### `greet_user()`
Checks the current hour and returns an appropriate greeting: "Good Morning" (5–11), "Good Afternoon" (12–16), "Good Evening" (17–20), or "Good Night" (21–4).

### `take_command()`
Listens to the microphone, sends the audio to Google's speech recognition API, and returns the recognized text in lowercase. Returns an empty string if nothing was understood or an error occurred.

### `open_website(url)`
Opens a given URL in the system's default web browser using the `webbrowser` module.

### `open_app(app_name)`
Detects the operating system (Windows, macOS, or Linux) and opens common applications like Calculator or Notepad using `subprocess.Popen`. Returns `True` if the app was found, `False` otherwise.

### `process_command(query)`
The "brain" of Jarvis. Takes the recognized text, checks it against known command patterns (time, date, open websites, search, open apps, exit, etc.), and calls the appropriate function. Returns Jarvis's spoken response.

### `JarvisApp` class
The Tkinter GUI class. Key methods:
- `_build_ui()` — Creates all GUI elements (title, status, LED, command display, response area, buttons).
- `start_listening()` — Disables the listen button, changes the LED to red, and starts a background thread to capture audio.
- `_listen_thread()` — Background thread that calls `take_command()` and `process_command()`, then updates the GUI with results.
- `set_status()`, `set_command()`, `set_response()`, `set_led()` — Thread-safe helpers that update GUI elements from any thread using `root.after()`.
- `safe_exit()` — Shows a confirmation dialog before closing the application.

### `main()`
Creates the Tkinter root window, instantiates `JarvisApp`, starts a welcome greeting in a background thread, and runs the Tkinter event loop.

---

## Common Errors & Solutions

### 1. `ModuleNotFoundError: No module named 'speech_recognition'`
**Cause:** SpeechRecognition is not installed.
**Fix:** Run `pip install SpeechRecognition`

### 2. `ModuleNotFoundError: No module named 'pyttsx3'`
**Cause:** pyttsx3 is not installed.
**Fix:** Run `pip install pyttsx3`

### 3. `OSError: No Default Input Device Available`
**Cause:** No microphone is connected or enabled.
**Fix:** Connect a microphone or enable your laptop's built-in mic in system settings.

### 4. `Could not import the PyAudio C module`
**Cause:** PyAudio is not installed (it's the microphone backend).
**Fix:**
- Windows: `pip install pipwin && pipwin install pyaudio`
- macOS: `brew install portaudio && pip install pyaudio`
- Linux: `sudo apt-get install portaudio19-dev python3-pyaudio && pip install pyaudio`

### 5. `speech_recognition.UnknownValueError`
**Cause:** Jarvis heard you but couldn't understand the speech (background noise or unclear speech).
**Fix:** Speak clearly in a quiet room. The app handles this gracefully and asks you to repeat.

### 6. `speech_recognition.RequestError`
**Cause:** No internet connection (Google's speech API requires internet).
**Fix:** Check your internet connection and try again.

### 7. GUI doesn't appear / `ModuleNotFoundError: No module named 'tkinter'`
**Cause:** tkinter is missing (common on some Linux minimal installs).
**Fix:** `sudo apt-get install python3-tk`

### 8. Buttons freeze while listening
**Cause:** Listening runs on the main thread, blocking the GUI.
**Fix:** This project already uses `threading.Thread` to run listening in the background, so the GUI stays responsive. If you modified the code, make sure `take_command()` is called from a thread, not directly.

---

## Future Enhancements

| Feature | Description |
|---|---|
| **Weather Information** | Integrate OpenWeatherMap API to tell the current weather by voice |
| **Reminders & Alarms** | Set voice-activated reminders and alarms stored in a local file or database |
| **Music Control** | Play, pause, and skip songs in Spotify or a local music player |
| **Email Assistance** | Compose and send emails using voice (via SMTP or Gmail API) |
| **AI Conversation** | Integrate OpenAI GPT or similar for natural conversation beyond fixed commands |
| **Wikipedia Search** | Use the Wikipedia API to answer general knowledge questions |
| **Screen Brightness / Volume Control** | Adjust system volume and brightness by voice |
| **Screenshot** | Take a screenshot on voice command |
| **Multi-language Support** | Recognize and respond in multiple languages |
| **Voice Wake Word** | Always-listening mode triggered by saying "Hey Jarvis" |

---

## Notes for Presentation

- This project is intentionally simple and beginner-friendly — each function does one thing and is easy to explain.
- The code is fully commented so you can walk through each section during your presentation.
- The GUI uses threading so it never freezes, demonstrating good practice.
- Error handling is included throughout — microphone errors, recognition errors, and unknown commands are all handled gracefully.
- No dangerous system operations are performed. The exit button asks for confirmation before closing.

---

## License

This project is free to use for educational purposes.
