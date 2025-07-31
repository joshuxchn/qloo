from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
from kroger import KrogerAPI
from qloo import get_parsed_recommendations, UserProfile
import chromadb
import uuid

# Create KrogerAPI instance
kroger_api = KrogerAPI()

# Wrapper function for Gemini function calling
def search_kroger_products(search_term: str, limit: int) -> list:
    """
    Search for products using Kroger API.
    
    Args:
        search_term: Product name to search for
        limit: Maximum number of products to return
        
    Returns:
        List of product names found in Kroger stores
    """
    try:
        products = kroger_api.productSearch(search_term, limit=limit)
        return [product.name for product in products] if products else []
    except Exception as e:
        print(f"Kroger API error: {e}")
        return []


load_dotenv("../.env")
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
chroma_client = chromadb.HttpClient(host='localhost', port=8000)
collection = chroma_client.get_or_create_collection(name="my_collection")

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

def deterministic_id(name: str) -> str:

    return str(uuid.uuid5(uuid.NAMESPACE_DNS, name))

def embedding():
    data = qloo_suggestions() + similar_products("blueberries")
    ids   = []
    docs  = []
    metas = []
    for item in data:
        name = item.split(":",1)[0].strip()
        id_  = deterministic_id(name)
        ids.append(id_)
        docs.append(item)
        metas.append({"name": name})

    collection.upsert(
        ids=ids,
        documents=docs,
        metadatas=metas,
    )

def retreive(query):
    response=collection.query(
        query_texts=f"Please find relevant items related to {query}",
        n_results=3
    )

    names = [meta['name'] for meta in response['metadatas'][0]]
    return names

def smart_swap(product): 
    names = retreive(product)

    config = types.GenerateContentConfig(
        temperature=0,
        tools=[search_kroger_products],
        thinking_config=types.ThinkingConfig(include_thoughts=True)
    )
    
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=f"""
            You are a groceries expert and recommender. Here are 3 similar products to {product}:
            {', '.join(names)}
            
            For each of these 3 products, search for them using search_kroger_products function.
            Then return the actual Kroger product names you found, one per line.
            
            Return these 3 product names as grocery alternatives, one per line.
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

embedding()  # Run once to populate database
smart_swap("tangerine")


