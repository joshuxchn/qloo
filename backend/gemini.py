from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
from kroger import KrogerAPI
from qloo import get_parsed_recommendations, UserProfile
import chromadb
import uuid


load_dotenv("../.env")
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="my_collection")

test_user = UserProfile(
    age=15,
    gender="female", 
    city="Los Angeles",
    favorite_tags=["urn:tag:genre:place:restaurant:chinese", "urn:tag:genre:place:restaurant:italian"],
    audiences=["foodies"],
    dietary_restrictions=[]  # Remove dietary restrictions for testing
)

def similar_products(product: str) -> list[str]:
    prompt = (
        f"You are a grocery‑expert recommender, with knowledge in the composition and popularity of foods.\n"
        f"Generate 5 groceries similar to “{product}”.\n"
        "Output only the items and a 100 character max detailed description of only the ITEM itself, one per line, with no bullets or numbering.\n"
        "Example: Cranberry: Tart, red berry, popular for sauces, juices, and vitamin D benefits\n"
    )
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    raw = response.text.strip()  
    items = [line.strip() for line in raw.splitlines() if line.strip()]

    return items

def qloo_suggestions() -> list[str]:
    recommendations = get_parsed_recommendations(test_user)
    formatted = "\n".join([rec['name'] for rec in recommendations])
    prompt = (
        f"You are a grocery‑expert recommender, with knowledge in the composition and popularity of foods.\n"
        "Output only the items given and a 100 character max detailed description of only the ITEM itself, one per line, with no bullets or numbering.\n"
        "Example: Cranberry: Tart, red berry, popular for sauces, juices, and health benefits\n"
        f"List of items: \n{formatted}"
    
    )
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    raw = response.text.strip()  
    items = [line.strip() for line in raw.splitlines() if line.strip()]
    return items

def embedding():
    data = qloo_suggestions() + similar_products("blueberries")
    
    product_names = [item.split(':')[0].strip() for item in data]
    
    collection.add(
        documents=data,
        metadatas=[{"name": name} for name in product_names],
        ids=[str(uuid.uuid4()) for _ in range(len(data))]
    )

def retreive(query):
    response=collection.query(
        query_texts=f"Please find relevant items related to {query}",
        n_results=5
    )
    return response

def smart_swap(product): 
    config = types.GenerateContentConfig(
        temperature=0,
        tools=[],
        thinking_config=types.ThinkingConfig(include_thoughts=True)
    )
    
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents="""
        


            """,
        config=config
    )

    #thought proccess for complex tasks
    print("Response:")
    for part in response.candidates[0].content.parts:
        if hasattr(part, 'thought') and part.thought:
            print("Thought:", part.text)
        else:
            print("Answer:", part.text)
    return response

embedding()
print(retreive("indian food"))


