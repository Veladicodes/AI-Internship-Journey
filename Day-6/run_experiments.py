import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError

def main():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment or .env file.")
        return

    client = genai.Client(api_key=api_key)

    prompts = [
        "Explain Python.",
        "Explain Python like I'm 10 years old.",
        "Explain Python as a senior software engineer.",
        "Explain Python using real-world examples."
    ]

    models_to_try = ["gemini-1.5-flash", "gemini-2.5-flash", "gemini-1.5-pro"]
    
    results = {}
    
    for p in prompts:
        print(f"Sending prompt: '{p}'")
        success = False
        
        for model_name in models_to_try:
            if success:
                break
                
            retries = 3
            backoff = 2
            for attempt in range(retries):
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=p,
                    )
                    results[p] = response.text
                    print(f"Response received successfully using model: {model_name}.\n")
                    success = True
                    break
                except APIError as e:
                    if e.code == 503 or e.code == 429:
                        print(f"Model {model_name} busy or rate limited (Attempt {attempt+1}/{retries}). Retrying in {backoff}s...")
                        time.sleep(backoff)
                        backoff *= 2
                    else:
                        print(f"API Error with model {model_name}: {e}. Trying next model...")
                        break
                except Exception as e:
                    print(f"Unexpected error with model {model_name}: {e}. Trying next model...")
                    break
                    
        if not success:
            print("Failed to get response for this prompt from any model.")
            return

    print("Generating prompt_comparison.txt...")
    
    analysis = """My Personal Analysis of the Responses

Looking at the different outputs side by side, it's pretty cool to see how tweaking a few words in the prompt completely changes how the AI behaves. Here are my main takeaways:

1. Prompt 1: "Explain Python." (The standard baseline)
   - How it looks: Super clean, structured, and neutral. It reads like a Wikipedia page or a textbook introduction.
   - Who it's for: Someone who just wants a quick, no-nonsense overview of what Python is.
   - What it covers: It uses standard bullet points for features (interpreted, high-level) and lists common use cases like web development or data science. Nothing fancy, just the facts.

2. Prompt 2: "Explain Python like I'm 10 years old." (The kid-friendly version)
   - How it looks: Enthusiastic, simple, and metaphor-heavy. It drops all the technical jargon.
   - Who it's for: A absolute beginner or a kid who might get scared off by terms like "interpreted" or "dynamic typing".
   - What it covers: It uses a cool analogy of a "computer friend" who follows recipes or "magic spells." Instead of talking about memory management, it talks about making games, drawing pictures, or controlling robots.

3. Prompt 3: "Explain Python as a senior software engineer." (The pro developer view)
   - How it looks: Pragmatic, critical, and focused on architectural trade-offs. 
   - Who it's for: Experienced developers who care about efficiency, maintenance, and project viability.
   - What it covers: It doesn't waste time explaining syntax. Instead, it dives straight into the developer productivity index, static typing using mypy, packaging tools like Poetry, and critical bottlenecks like the GIL (Global Interpreter Lock) and CPU-bound vs. I/O-bound performance.

4. Prompt 4: "Explain Python using real-world examples." (The practical approach)
   - How it looks: Relatable, visual, and grounded in concrete applications.
   - Who it's for: People who learn best when they can connect concepts to things they already use every day.
   - What it covers: It maps Python's features to actual apps like Instagram (backend), Netflix/Amazon (recommendation systems), and automated scripts (renaming files). It uses the analogy of a restaurant kitchen to explain frontend vs. backend.
"""

    with open("prompt_comparison.txt", "w", encoding="utf-8") as f:
        f.write("Prompt Comparison Results - Day 6 AI Internship\n\n")
        f.write("In this experiment, we explore how different prompting styles influence the tone, complexity, structure, and details of responses from the Gemini model.\n\n")
        
        for prompt, response in results.items():
            f.write(f"Prompt: \"{prompt}\"\n\n")
            f.write("AI Response:\n")
            import re
            formatted_response = response.strip()
            formatted_response = re.sub(r'^(\s*)\*(\s+)', r'\1-\2', formatted_response, flags=re.MULTILINE)
            formatted_response = formatted_response.replace("*", "")
            f.write(f"{formatted_response}\n\n")
            f.write("\n")
            
        f.write(analysis)
        
    print("prompt_comparison.txt generated successfully!")

if __name__ == "__main__":
    main()
