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

def setup_api_client():
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("No GEMINI_API_KEY found in environment or .env file.")
        print("You can get an API key from Google AI Studio: https://aistudio.google.com/\n")
        
        user_key = input("Please paste your Gemini API Key here (or press Enter to exit): ").strip()
        if not user_key:
            print("No API key provided. Exiting program.")
            sys.exit(1)
            
        try:
            with open(".env", "w") as env_file:
                env_file.write(f"GEMINI_API_KEY={user_key}\n")
            print("\nAPI Key successfully saved to .env file!")
            api_key = user_key
        except Exception as e:
            print(f"Could not save API Key to .env file: {e}")
            api_key = user_key

    try:
        client = genai.Client(api_key=api_key)
        return client
    except Exception as e:
        print(f"Error initializing GenAI Client: {e}")
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
        print(f"Error saving JSON log: {e}")

def append_to_history_txt(user_name, question, response_text):
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("chat_history.txt", "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}]\n")
            f.write(f"{user_name}: {question}\n")
            f.write(f"Gemini: {response_text}\n")
            f.write("-" * 50 + "\n")
    except Exception as e:
        print(f"Error saving text history: {e}")

def print_header(user_name):
    border = "=" * 60
    welcome_msg = f"Welcome, {user_name}!"
    subtitle = "Ask me anything about programming, code, or general topics."
    instructions = "Type your prompt and press Enter. To exit, type 'exit', 'quit', or 'bye'."
    
    print(f"\n{border}")
    print(f" {welcome_msg.center(58)}")
    print(f" {subtitle.center(58)}")
    print(f" {instructions.center(58)}")
    print(f"{border}\n")

def main():
    client = setup_api_client()
    
    print("--- Gemini AI Terminal Chatbot ---")
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
        print("Failed to initialize chat session with any supported Gemini model. Check your API key or connection.")
        sys.exit(1)
        
    chat_logs = load_chat_log()
    session_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    while True:
        try:
            user_input = input(f"{user_name}: ").strip()
            
            if user_input.lower() in ["exit", "quit", "bye"]:
                print(f"\nGoodbye, {user_name}! Thanks for chatting. Have a great day!")
                break
                
            if not user_input:
                continue
                
            print(f"\nThinking (using {model_name})...", end="\r")
            
            response = chat.send_message(user_input)
            
            print(" " * 40, end="\r")
            
            print("AI (Gemini):")
            print(f"{response.text}\n")
            print("-" * 50 + "\n")
            
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
            print(f"\n\nGoodbye, {user_name}! Chat ended.")
            break
        except APIError as e:
            print(" " * 40, end="\r")
            print(f"Gemini API Error: {e.message} (Code: {e.code})\n")
        except Exception as e:
            print(" " * 40, end="\r")
            print(f"Error occurred: {e}\n")

if __name__ == "__main__":
    main()
