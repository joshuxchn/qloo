from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
from kroger import KrogerAPI
from qloo import get_parsed_recommendations, UserProfile
import chromadb
from chromadb.config import Settings
import uuid
from Database.product import Product
from pydantic import BaseModel
from typing import Optional
import datetime

class ProductSchema(BaseModel):
    name: str
    price: float = 0.0
    promo_price: Optional[float] = None
    fulfillment_type: str = "UNKNOWN"
    brand: str = "N/A"
    inventory: str = "UNKNOWN"  
    size: str = "N/A"
    last_updated: Optional[datetime.datetime] = None
    location_ID: str = "N/A"
    upc: str = "N/A"
    category: str = "Uncategorized"

# Create KrogerAPI instance
kroger_api = KrogerAPI()



load_dotenv("../.env")

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(name="my_collection")


test_user = UserProfile(
    age=15,
    gender="female", 
    city="Los Angeles",
    favorite_tags=["urn:tag:genre:place:restaurant:chinese", "urn:tag:genre:place:restaurant:italian"],
    audiences=["foodies"],
    dietary_restrictions=[]  
)

def search_kroger_products(search_term: str, limit: int) -> list[dict]:
    """Search for products using Kroger API.
    
    Args:
        search_term: Product name to search for
        limit: Maximum number of products to return
        
    Returns:
        List of product dictionaries from Kroger stores
    """
    try:
        products = kroger_api.productSearch(search_term, limit=limit)
        return [product.to_dict() for product in products] if products else []
    except Exception as e:
        print(f"Kroger API error: {e}")
        return []
    
def similar_products(product: str) -> list[str]:
    prompt = (
        f"You are a grocery-expert recommender, with knowledge in the composition and popularity of foods.\n"
        f"Generate 5 groceries similar to '{product}'.\n"
        "Output only the items and a 100 character max detailed description of only the ITEM itself, one per line, with no bullets or numbering.\n"
        "Example: Cranberry: Tart, red berry, popular for sauces, juices, and vitamin D benefits\n"
    )
    
    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=prompt
    )
    raw = response.text.strip()  
    items = [line.strip() for line in raw.splitlines() if line.strip()]

    return items

def qloo_suggestions() -> list[str]:
    recommendations = get_parsed_recommendations(test_user)
    formatted = "\n".join([rec['name'] for rec in recommendations])
    prompt = (
        f"You are a grocery-expert recommender, with knowledge in the composition and popularity of foods.\n"
        "Output only the items given and a 100 character max detailed description of only the ITEM itself, one per line, with no bullets or numbering.\n"
        "Example: Cranberry: Tart, red berry, popular for sauces, juices, and health benefits\n"
        f"List of items: \n{formatted}"
    )
    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=prompt
    )
    raw = response.text.strip()  
    items = [line.strip() for line in raw.splitlines() if line.strip()]
    return items

def qloo_suggestions_with_affinity() -> list[dict]:
    """Get Qloo suggestions with affinity scores"""
    return get_parsed_recommendations(test_user)

def deterministic_id(name: str) -> str:

    return str(uuid.uuid5(uuid.NAMESPACE_DNS, name))

def embedding(product):
    data = qloo_suggestions() + similar_products(product)
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
        tools=[search_kroger_products],
        response_mime_type="application/json",
        response_schema=list[ProductSchema]
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=f"""
        You are a groceries expert and recommender. Here are 3 similar products to {product}:
        {', '.join(names)}
        
        For each of these 3 products, search for them using search_kroger_products function.
        From the Kroger API results, select the best matching products and return them as a structured list.
        
        Return exactly 3 products with all their details (name, price, brand, category, etc.).
        """,
        config=config
    )

    # Convert ProductSchema objects to Product objects
    product_objects = []
    if hasattr(response, 'parsed') and response.parsed:
        for product_schema in response.parsed:
            product_dict = product_schema.model_dump()
            product_obj = Product.from_dict(product_dict)
            product_objects.append(product_obj)
            print(f"Created Product: {product_obj.name} - ${product_obj.price}")

    print(f"Returned {len(product_objects)} Product objects")
    return product_objects


def suggestions_retreive():
    """Get the 5 products with highest affinity scores from Qloo and search Kroger for them"""

    qloo_recs = qloo_suggestions_with_affinity()

    top_5_recs = sorted(qloo_recs, key=lambda x: x.get('affinity', 0), reverse=True)[:5]
    
    print(f"Top 5 highest affinity products:")
    for i, rec in enumerate(top_5_recs, 1):
        print(f"{i}. {rec['name']} (Affinity: {rec.get('affinity', 0):.3f})")
    

    product_objects = []
    for rec in top_5_recs:
        product_name = rec['name']
        print(f"Searching Kroger for: {product_name}")
        

        kroger_results = search_kroger_products(product_name, limit=1)
        
        if kroger_results:
            product_dict = kroger_results[0]
            product_obj = Product.from_dict(product_dict)
            product_objects.append(product_obj)
            print(f"  Found: {product_obj.name} - ${product_obj.price}")
        else:
            print(f"  No Kroger results found for: {product_name}")
    
    print(f"Returned {len(product_objects)} Product objects from Kroger")
    return product_objects



# Test the affinity-based suggestions
print("Testing suggestions_retreive with affinity scores:")
top_suggestions = suggestions_retreive()

embedding("tangerine")  
smart_swap("tangerine")