import os
import time
import json
import random
from openai import OpenAI

def get_creative_director_prompt():
    """Generates the prompt for the AI to act as an autonomous creative director."""
    themes = ["Cyberpunk Action", "Slice of Life", "Dark Fantasy", "Mecha", "Isekai", "Supernatural Mystery"]
    random_theme = random.choice(themes)
    
    return f"""
    You are an autonomous Anime Director and Storyboard Artist. Your job is to create a highly engaging, 60-second YouTube Shorts script.
    Today's selected random theme is: {random_theme}.

    REQUIREMENTS:
    1. Invent a captivating micro-story, lore, or character moment.
    2. Write an engaging voiceover script.
    3. Generate visual prompts for an AI Video Generator (AnimateDiff). The visual prompts MUST be comma-separated Danbooru-style tags (e.g., "masterpiece, best quality, 1girl, solo, school uniform, wind blowing, cherry blossoms, highly detailed").
    4. Provide metadata for YouTube and an email notification.
    
    You must respond ONLY with a valid JSON object in the following format:
    {{
        "title": "Catchy YouTube Title",
        "description": "Engaging description...",
        "tags": ["anime", "shorts", "tag3"],
        "email_subject": "New Anime Short Ready: [Title]",
        "email_body": "Your latest video has been rendered and uploaded to Drive. Theme: [Theme].",
        "scenes": [
            {{
                "visual_prompt": "masterpiece, best quality, 1boy, cyber samurai, neon city rain, dynamic pose...",
                "narration": "In the year 2142, the blade is the only law left."
            }}
        ]
    }}
    Ensure the JSON is valid and contains no markdown formatting outside the JSON itself. Do not ask questions, just generate.
    """

def generate_script(provider="groq"):
    """Generates a structured video script."""
    if provider.lower() == "groq":
        client = OpenAI(
            api_key=os.environ.get("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1"
        )
        model_name = "llama3-70b-8192" 
    else:
        client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY")
        )
        model_name = "gpt-4o"

    prompt = get_creative_director_prompt()
    
    print(f"Asking AI Creative Director to brainstorm an Anime Short using {provider}...")
    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"} if provider != "groq" else None
    )
    
    content = response.choices[0].message.content.strip()
    if content.startswith("```json"):
        content = content.replace("```json", "", 1)
    if content.endswith("```"):
        content = content[:content.rfind("```")]
        
    return json.loads(content.strip())

if __name__ == "__main__":
    script_data = generate_script("groq")
    
    os.makedirs("outputs", exist_ok=True)
    date_str = time.strftime("%Y-%m-%d")
    
    # Save the structured data
    json_path = f"outputs/script_{date_str}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(script_data, f, indent=4)
        
    # Also save as latest
    with open("outputs/latest_script.json", "w", encoding="utf-8") as f:
        json.dump(script_data, f, indent=4)
        
    print(f"Storyboarding complete. Saved to outputs/latest_script.json")
