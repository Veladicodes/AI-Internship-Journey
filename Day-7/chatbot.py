import os
import sys
import json
import datetime
from dotenv import load_dotenv

try:
    from google import genai
    from google.genai import types
    from google.genai.errors import APIError
except ImportError:
    print("Error: 'google-genai' package is not installed.")
    print("Please run: pip install -r requirements.txt")
    sys.exit(1)

class Colors:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[95m"
    BLUE = "\033[94m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

def enable_windows_ansi():
    if sys.platform == "win32":
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

enable_windows_ansi()

def setup_api_client():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print(f"{Colors.YELLOW}No GEMINI_API_KEY found in environment or .env file.{Colors.RESET}")
        print(f"You can get an API key from Google AI Studio: https://aistudio.google.com/\n")
        user_key = input("Please paste your Gemini API Key here (or press Enter to exit): ").strip()
        if not user_key:
            print(f"{Colors.RED}No API key provided. Exiting program.{Colors.RESET}")
            sys.exit(1)
        try:
            with open(".env", "w") as env_file:
                env_file.write(f"GEMINI_API_KEY={user_key}\n")
            print(f"\n{Colors.GREEN}API Key successfully saved to .env file!{Colors.RESET}")
            api_key = user_key
        except Exception as e:
            print(f"{Colors.RED}Could not save API Key to .env file: {e}{Colors.RESET}")
            api_key = user_key
    try:
        client = genai.Client(api_key=api_key)
        return client
    except Exception as e:
        print(f"{Colors.RED}Error initializing GenAI Client: {e}{Colors.RESET}")
        sys.exit(1)

def load_chat_log():
    if os.path.exists("chat_log.json"):
        try:
            with open("chat_log.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_chat_log(log_entries):
    try:
        with open("chat_log.json", "w", encoding="utf-8") as f:
            json.dump(log_entries, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"{Colors.RED}Error saving JSON log: {e}{Colors.RESET}")

def append_to_history_txt(user_name, question, response_text):
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("chat_history.txt", "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}]\n")
            f.write(f"{user_name}: {question}\n")
            f.write(f"Gemini: {response_text}\n")
            f.write("-" * 50 + "\n")
    except Exception as e:
        print(f"{Colors.RED}Error saving text history: {e}{Colors.RESET}")

def print_header(user_name):
    border = "=" * 60
    welcome_msg = f"Welcome, {user_name}!"
    subtitle = "Ask me anything about programming, code, or general topics."
    instructions = "Type '/help' to see special commands. Type 'exit', 'quit', or 'bye' to leave."
    print(f"\n{Colors.CYAN}{Colors.BOLD}{border}")
    print(f" {welcome_msg.center(58)}")
    print(f" {subtitle.center(58)}")
    print(f" {instructions.center(58)}")
    print(f"{border}{Colors.RESET}\n")

def print_help_menu():
    border = "-" * 50
    print(f"\n{Colors.MAGENTA}{Colors.BOLD}--- Chatbot Command Help ---{Colors.RESET}")
    print(f"Here are the special commands you can run inside the chat:")
    print(f"  {Colors.YELLOW}/help{Colors.RESET}     - Show this help menu with all available options.")
    print(f"  {Colors.YELLOW}/clear{Colors.RESET}    - Clear the terminal screen and reprint the header.")
    print(f"  {Colors.YELLOW}/history{Colors.RESET}  - Display info and count of turns in this session.")
    print(f"  {Colors.YELLOW}exit{Colors.RESET} or {Colors.YELLOW}quit{Colors.RESET} or {Colors.YELLOW}bye{Colors.RESET} - Exit the chat and save logs.")
    print(f"{Colors.MAGENTA}{border}{Colors.RESET}\n")

def clear_screen(user_name):
    os.system('cls' if os.name == 'nt' else 'clear')
    print_header(user_name)

def main():
    client = setup_api_client()
    print(f"{Colors.CYAN}{Colors.BOLD}--- Gemini AI Terminal Chatbot ---{Colors.RESET}")
    user_name = input("Enter your name to begin: ").strip()
    if not user_name:
        user_name = "User"
    print_header(user_name)
    model_name = "gemini-1.5-flash"
    chat = None
    for model_candidate in ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-1.5-pro"]:
        try:
            chat = client.chats.create(model=model_candidate)
            model_name = model_candidate
            break
        except Exception:
            continue
    if not chat:
        print(f"{Colors.RED}{Colors.BOLD}Failed to initialize chat session with any supported Gemini model. Check your API key or connection.{Colors.RESET}")
        sys.exit(1)
    chat_logs = load_chat_log()
    session_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    while True:
        try:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            prompt_prefix = f"{Colors.BLUE}[{current_time}]{Colors.RESET} {Colors.GREEN}{Colors.BOLD}{user_name}:{Colors.RESET} "
            user_input = input(prompt_prefix).strip()
            if user_input.lower() in ["exit", "quit", "bye"]:
                print(f"\n{Colors.MAGENTA}{Colors.BOLD}Goodbye, {user_name}! Thanks for chatting. Have a great day!{Colors.RESET}")
                break
            if not user_input:
                continue
            if user_input.startswith("/"):
                command = user_input.lower().strip()
                if command == "/help":
                    print_help_menu()
                elif command == "/clear":
                    clear_screen(user_name)
                elif command == "/history":
                    history_len = len(chat.get_history()) if chat else 0
                    turns = history_len // 2
                    print(f"\n{Colors.YELLOW}Current session details:{Colors.RESET}")
                    print(f"- Active Model: {model_name}")
                    print(f"- Conversation Turns: {turns} (Total messages: {history_len})")
                    print(f"- Session ID: {session_id}\n")
                else:
                    print(f"\n{Colors.RED}Unknown command: {user_input}. Type /help to see all commands.{Colors.RESET}\n")
                continue
            print(f"{Colors.YELLOW}Thinking (using {model_name})...{Colors.RESET}", end="\r")
            response = chat.send_message(user_input)
            print(" " * 50, end="\r")
            reply_time = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"{Colors.BLUE}[{reply_time}]{Colors.RESET} {Colors.CYAN}{Colors.BOLD}AI (Gemini):{Colors.RESET}")
            print(f"{response.text}\n")
            print(f"{Colors.BLUE}" + "-" * 60 + f"{Colors.RESET}\n")
            append_to_history_txt(user_name, user_input, response.text)
            chat_logs.append({
                "session_id": session_id,
                "timestamp": datetime.datetime.now().isoformat(),
                "user": user_name,
                "question": user_input,
                "response": response.text
            })
            save_chat_log(chat_logs)
        except KeyboardInterrupt:
            print(f"\n\n{Colors.MAGENTA}{Colors.BOLD}Goodbye, {user_name}! Chat ended.{Colors.RESET}")
            break
        except APIError as e:
            print(" " * 50, end="\r")
            print(f"{Colors.RED}{Colors.BOLD}Gemini API Error: {e.message} (Code: {e.code}){Colors.RESET}\n")
        except Exception as e:
            print(" " * 50, end="\r")
            print(f"{Colors.RED}{Colors.BOLD}Error occurred: {e}{Colors.RESET}\n")

if __name__ == "__main__":
    main()
