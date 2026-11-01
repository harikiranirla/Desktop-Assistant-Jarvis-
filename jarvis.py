"""
Desktop Assistant (Jarvis)
==========================
A beginner-friendly desktop voice assistant built with Python.

Features:
  - Voice input via microphone (SpeechRecognition)
  - Voice output via text-to-speech (pyttsx3)
  - Tkinter GUI with start/exit buttons and status display
  - Open websites (Google, YouTube, Gmail)
  - Google search from voice
  - Open system apps (calculator, notepad)
  - Tell time, date, and day of week
  - Greeting based on time of day
  - Graceful handling of unknown commands and errors

Author: (Your Name)
"""

import os
import sys
import time
import webbrowser
import subprocess
import datetime
import threading

# --- Third-party libraries ---
import pyttsx3          # Text-to-speech
import speech_recognition as sr  # Speech recognition

# --- Tkinter GUI ---
import tkinter as tk
from tkinter import ttk, scrolledtext


# ============================================================
#  TEXT-TO-SPEECH ENGINE
# ============================================================

# Initialise the pyttsx3 engine once and reuse it everywhere.
engine = pyttsx3.init()

# Try to set a slightly slower rate so beginners can follow along.
try:
    engine.setProperty("rate", 170)
except Exception:
    pass  # If setting the rate fails, the default rate is fine.


def speak(text):
    """Speak the given text aloud AND return the text (for GUI display)."""
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"[speak error] {e}")
    return text


# ============================================================
#  GREETING
# ============================================================

def greet_user():
    """Return a greeting string based on the current hour of the day."""
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        greeting = "Good Morning!"
    elif 12 <= hour < 17:
        greeting = "Good Afternoon!"
    elif 17 <= hour < 21:
        greeting = "Good Evening!"
    else:
        greeting = "Good Night!"
    return greeting


# ============================================================
#  SPEECH RECOGNITION
# ============================================================

def take_command():
    """
    Listen to the microphone and convert speech to text.

    Returns:
        str  -- the recognised command (lowercased) or an empty string
                if nothing was understood or an error occurred.
    """
    recognizer = sr.Recognizer()

    # Adjust these for better accuracy; keep them gentle so ambient
    # noise doesn't cause false triggers.
    recognizer.pause_threshold = 1
    recognizer.energy_threshold = 4000

    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=8)
    except sr.WaitTimeoutError:
        return ""
    except Exception as e:
        print(f"[microphone error] {e}")
        return ""

    try:
        # Google's free web speech API is used here.  An internet
        # connection is required.
        query = recognizer.recognize_google(audio, language="en-in")
        return query.lower()
    except sr.UnknownValueError:
        # Speech was not understandable.
        return ""
    except sr.RequestError as e:
        print(f"[recognition service error] {e}")
        return ""
    except Exception as e:
        print(f"[recognition error] {e}")
        return ""


# ============================================================
#  COMMAND PROCESSING
# ============================================================

def open_website(url):
    """Open a URL in the default web browser."""
    webbrowser.open(url)


def open_app(app_name):
    """
    Try to open a common desktop application.

    Works on Windows, macOS, and Linux.  Returns True on success,
    False otherwise.
    """
    app_name = app_name.lower()

    # Map friendly names to OS-specific commands.
    if app_name in ("calculator", "calc"):
        if sys.platform.startswith("win"):
            subprocess.Popen("calc", shell=True)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", "-a", "Calculator"])
        else:
            subprocess.Popen(["gnome-calculator"])
        return True

    if app_name in ("notepad", "text editor"):
        if sys.platform.startswith("win"):
            subprocess.Popen("notepad", shell=True)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", "-a", "TextEdit"])
        else:
            subprocess.Popen(["gedit"])
        return True

    return False


def process_command(query):
    """
    Take the recognised text and decide what Jarvis should do.

    Returns:
        response (str): What Jarvis says back to the user.
    """
    query = query.lower().strip()

    # --- Stop / Exit ---
    if any(word in query for word in ("exit", "quit", "stop jarvis", "bye")):
        speak("Goodbye! Have a nice day.")
        # Schedule GUI close from the main thread.
        app_root.after(500, app_root.destroy)
        return "Goodbye! Have a nice day."

    # --- Greeting ---
    if "hello" in query or "hi jarvis" in query or "hey jarvis" in query:
        msg = f"{greet_user()} I am Jarvis. How can I help you?"
        return speak(msg)

    # --- Time ---
    if "time" in query and "date" not in query:
        now = datetime.datetime.now().strftime("%I:%M %p")
        msg = f"The time is {now}"
        return speak(msg)

    # --- Date ---
    if "date" in query and "time" not in query:
        today = datetime.datetime.now().strftime("%B %d, %Y")
        msg = f"Today's date is {today}"
        return speak(msg)

    # --- Day of the week ---
    if "day" in query and "today" in query:
        day = datetime.datetime.now().strftime("%A")
        msg = f"Today is {day}"
        return speak(msg)

    # --- Date and time together ---
    if "date and time" in query or "date and time" in query:
        now = datetime.datetime.now().strftime("%B %d, %Y, %I:%M %p")
        msg = f"Today is {now}"
        return speak(msg)

    # --- Open Google ---
    if "open google" in query:
        open_website("https://www.google.com")
        msg = "Opening Google"
        return speak(msg)

    # --- Open YouTube ---
    if "open youtube" in query:
        open_website("https://www.youtube.com")
        msg = "Opening YouTube"
        return speak(msg)

    # --- Open Gmail ---
    if "open gmail" in query:
        open_website("https://mail.google.com")
        msg = "Opening Gmail"
        return speak(msg)

    # --- Search Google ---
    if query.startswith("search "):
        search_term = query.replace("search ", "").strip()
        if search_term:
            open_website(f"https://www.google.com/search?q={search_term.replace(' ', '+')}")
            msg = f"Searching Google for {search_term}"
            return speak(msg)
        else:
            msg = "What would you like me to search for?"
            return speak(msg)

    # --- Open applications ---
    if query.startswith("open "):
        app = query.replace("open ", "").strip()
        if open_app(app):
            msg = f"Opening {app}"
            return speak(msg)
        # If not a known app, try a web search as fallback.
        open_website(f"https://www.google.com/search?q={app.replace(' ', '+')}")
        msg = f"I couldn't find {app} on your computer, so I searched Google for it."
        return speak(msg)

    # --- Who are you ---
    if "who are you" in query or "your name" in query:
        msg = "I am Jarvis, your desktop assistant. I can open websites, tell the time, and more."
        return speak(msg)

    # --- Thank you ---
    if "thank you" in query or "thanks" in query:
        msg = "You're welcome!"
        return speak(msg)

    # --- Unknown command ---
    msg = "I'm sorry, I didn't understand that. Could you please repeat?"
    return speak(msg)


# ============================================================
#  GRAPHICAL USER INTERFACE (Tkinter)
# ============================================================

class JarvisApp:
    """Main Tkinter application window for Jarvis."""

    def __init__(self, root):
        self.root = root
        self.root.title("Desktop Assistant – Jarvis")
        self.root.geometry("560x560")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e272e")

        self._build_ui()

    # ----------------------------------------------------------
    #  UI Construction
    # ----------------------------------------------------------

    def _build_ui(self):
        bg = "#1e272e"
        card_bg = "#2d3a44"
        accent = "#34ace0"
        text_light = "#ecf0f1"

        # --- Title ---
        title = tk.Label(
            self.root,
            text="🤖 Desktop Assistant – Jarvis",
            font=("Segoe UI", 18, "bold"),
            bg=bg,
            fg=accent,
        )
        title.pack(pady=(20, 5))

        # --- Status label ---
        self.status_var = tk.StringVar(value="Status: Idle")
        status_label = tk.Label(
            self.root,
            textvariable=self.status_var,
            font=("Segoe UI", 12),
            bg=bg,
            fg=text_light,
        )
        status_label.pack(pady=(0, 10))

        # --- Visual indicator (LED) ---
        self.led = tk.Label(
            self.root,
            text="●",
            font=("Segoe UI", 40),
            bg=bg,
            fg="#7f8c8d",
        )
        self.led.pack(pady=(0, 5))

        # --- Recognised command display ---
        cmd_frame = tk.LabelFrame(
            self.root,
            text="Recognized Command",
            font=("Segoe UI", 11, "bold"),
            bg=card_bg,
            fg=text_light,
            bd=2,
            relief="groove",
        )
        cmd_frame.pack(fill="x", padx=30, pady=5)

        self.cmd_var = tk.StringVar(value="—")
        self.cmd_label = tk.Label(
            cmd_frame,
            textvariable=self.cmd_var,
            font=("Consolas", 13),
            bg=card_bg,
            fg="#f1c40f",
            wraplength=480,
            justify="center",
        )
        self.cmd_label.pack(padx=10, pady=10)

        # --- Response display (scrollable text area) ---
        resp_frame = tk.LabelFrame(
            self.root,
            text="Assistant Response",
            font=("Segoe UI", 11, "bold"),
            bg=card_bg,
            fg=text_light,
            bd=2,
            relief="groove",
        )
        resp_frame.pack(fill="both", expand=True, padx=30, pady=5)

        self.response_text = scrolledtext.ScrolledText(
            resp_frame,
            font=("Segoe UI", 11),
            bg=card_bg,
            fg="#2ecc71",
            wrap="word",
            height=6,
            state="disabled",
        )
        self.response_text.pack(fill="both", expand=True, padx=10, pady=10)

        # --- Button row ---
        btn_frame = tk.Frame(self.root, bg=bg)
        btn_frame.pack(pady=15)

        self.listen_btn = tk.Button(
            btn_frame,
            text="🎙  Start Listening",
            font=("Segoe UI", 13, "bold"),
            bg=accent,
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.start_listening,
        )
        self.listen_btn.pack(side="left", padx=10)

        self.exit_btn = tk.Button(
            btn_frame,
            text="❌  Exit",
            font=("Segoe UI", 13, "bold"),
            bg="#e74c3c",
            fg="white",
            activebackground="#c0392b",
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.safe_exit,
        )
        self.exit_btn.pack(side="left", padx=10)

    # ----------------------------------------------------------
    #  Helpers
    # ----------------------------------------------------------

    def set_status(self, text):
        """Update the status label safely from any thread."""
        self.root.after(0, self.status_var.set, text)

    def set_command(self, text):
        """Update the recognised-command label."""
        self.root.after(0, self.cmd_var.set, text)

    def set_response(self, text):
        """Append a line to the response text area."""
        def _append():
            self.response_text.config(state="normal")
            self.response_text.insert("end", text + "\n")
            self.response_text.see("end")
            self.response_text.config(state="disabled")
        self.root.after(0, _append)

    def set_led(self, color):
        """Change the LED indicator colour."""
        self.root.after(0, lambda: self.led.config(fg=color))

    # ----------------------------------------------------------
    #  Listening logic (runs in a background thread)
    # ----------------------------------------------------------

    def start_listening(self):
        """Disable the button and start listening in a background thread."""
        self.listen_btn.config(state="disabled")
        self.set_status("Status: Listening...")
        self.set_led("#e74c3c")          # red = recording
        self.set_command("Listening...")
        threading.Thread(target=self._listen_thread, daemon=True).start()

    def _listen_thread(self):
        """Background thread: capture audio, process command, update GUI."""
        query = take_command()

        if query:
            self.set_command(query)
            self.set_led("#f39c12")      # orange = processing
            self.set_status("Status: Processing...")
            response = process_command(query)
            self.set_response(f"You: {query}\nJarvis: {response}")
        else:
            self.set_command("—")
            self.set_response("Jarvis: Sorry, I didn't catch that. Please try again.")
            self.set_status("Status: Idle")

        self.set_led("#7f8c8d")          # grey = idle
        self.set_status("Status: Idle")
        self.root.after(0, lambda: self.listen_btn.config(state="normal"))

    # ----------------------------------------------------------
    #  Exit
    # ----------------------------------------------------------

    def safe_exit(self):
        """Ask for confirmation before quitting."""
        from tkinter import messagebox
        if messagebox.askokcancel("Exit", "Do you want to exit Jarvis?"):
            self.root.destroy()


# ============================================================
#  MAIN ENTRY POINT
# ============================================================

def main():
    global app_root
    app_root = tk.Tk()
    app = JarvisApp(app_root)

    # Greet the user when the app starts (in a background thread so
    # the GUI appears immediately).
    def welcome():
        greeting = greet_user()
        speak(f"{greeting} I am Jarvis, your desktop assistant. Click Start Listening and give me a command.")
        app.set_response(f"Jarvis: {greeting} I am Jarvis, your desktop assistant.")
        app.set_status("Status: Idle")
        app.set_led("#7f8c8d")

    app.set_status("Status: Starting...")
    app.set_led("#f39c12")
    threading.Thread(target=welcome, daemon=True).start()

    app_root.mainloop()


if __name__ == "__main__":
    main()
