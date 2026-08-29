Terminal AI Chatbot - Week 1 Project
==================================

Hey, this is my terminal chatbot project that I built for the first week of my AI internship. It's a basic Python command-line app that connects to Google's Gemini API and lets you have a conversation. 

It handles conversation history under the hood so Gemini remembers what you said previously, logs the chats so you don't lose them, and has some handy command line features.


Features
--------
* Timestamps: Prints the time [HH:MM:SS] for every message so you know when things were sent.
* Command intercepts: Before sending text to Google, the app checks if you typed a command. This saves our API quota.
* Commands built in:
  - /help: Lists all keyboard shortcuts.
  - /clear: Clears the terminal screen and repaints the welcome banner.
  - /history: Shows you the active model, session ID, and how many messages have been sent.
* Automatic logs:
  - chat_history.txt: A simple text file that appends all conversation turns.
  - chat_log.json: A structured JSON file for saving raw data (with session IDs and timestamps).
* Model Fallbacks: Tries gemini-1.5-flash and gemini-2.5-flash first, and falls back to gemini-1.5-pro if there's any network issue.
* Secure Key Loading: Uses python-dotenv. If you don't have a key saved, it asks you to paste it in and creates a .env file for you.


What you need
-------------
Make sure you have python installed.
Dependencies are in requirements.txt (google-genai, python-dotenv).


How to set it up
----------------
1. Open your terminal in this folder:
   cd Day-7

2. Create a virtual environment:
   python -m venv .venv

3. Activate it:
   - On Windows: .venv\Scripts\activate.bat (or .venv\Scripts\Activate.ps1 in PowerShell)
   - On Mac/Linux: source .venv/bin/activate

4. Install the requirements:
   pip install -r requirements.txt

5. Put your API key in a .env file:
   Create a new file named `.env` and add your key:
   GEMINI_API_KEY=your_actual_key_here
   (Or, you can just run the app and it will prompt you to paste it in).


How to run it
-------------
python chatbot.py


What it looks like (Sample Output)
----------------------------------
--- Gemini AI Terminal Chatbot ---
Enter your name to begin: Adithya

============================================================
                     Welcome, Adithya!                     
============================================================

[23:12:47] Adithya: /help

--- Chatbot Command Help ---
  /help     - Show this help menu.
  /clear    - Clear the terminal screen.
  /history  - Show turns in this session.
  exit      - Close the chatbot.
--------------------------------------------------

[23:12:55] Adithya: Hey, what is Python?
Thinking (using gemini-2.5-flash)...
[23:12:57] AI (Gemini):
Python is a popular programming language known for being easy to read and write...
--------------------------------------------------

[23:13:05] Adithya: /history

Current session details:
- Active Model: gemini-2.5-flash
- Conversation Turns: 1 (Total messages: 2)
- Session ID: 20260628_231247

[23:13:12] Adithya: exit
Goodbye, Adithya! Thanks for chatting.


Challenges I ran into
---------------------
1. The New Google GenAI library: The SDK changed recently, so a lot of online tutorials are outdated. For example, getting the chat history count broke because the old `.history` attribute didn't exist anymore. I had to look up the methods in a python shell and found `get_history()` instead.
2. Windows Colors: Windows console doesn't show ANSI colors by default. I had to add some win32 ctypes configuration in Python to make the text colorize nicely.
3. Git Safety: I had to make sure my .env file was added to .gitignore so my private key didn't accidentally get pushed to GitHub.
