from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv("../.env")
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def schedule_meeting():
    print("1")
    return "meeting scheduled"

def add_to_calendar():
    print("2") 
    return "added to calendar"

def reminder_notif():
    print("3")
    return "reminder of meeting"
def cheer():
    print("4")
    return "cheer"

config = types.GenerateContentConfig(
    temperature=0,
    tools=[schedule_meeting, add_to_calendar, reminder_notif, cheer],
    thinking_config=types.ThinkingConfig(include_thoughts=True)
)

response = client.models.generate_content(
    model="gemini-2.5-flash", 
    contents="schedule a meeting, then add to calendar. if Tim is running late, send him a reminder. otherwise, send a cheer. Let's say tim is not running late",
    config=config
)

#thought proccess for complex tasks
print("Response:")
for part in response.candidates[0].content.parts:
    if hasattr(part, 'thought') and part.thought:
        print("🔍 Thought:", part.text)
    else:
        print("💬 Answer:", part.text)