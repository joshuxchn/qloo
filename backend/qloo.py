import httpx
import os
from dotenv import load_dotenv
import json

# Load environment variables from parent directory
load_dotenv("../.env")

QLOO_API_KEY = os.getenv("QLOO_API_KEY")
QLOO_BASE_URL = os.getenv("QLOO_BASE_URL", "https://hackathon.api.qloo.com").rstrip("/")

print(QLOO_API_KEY)

def search_music(query):
    """Search for music entities using Qloo API"""
    headers = {
        "X-Api-Key": QLOO_API_KEY
    }
    
    print(f"Making request to: {QLOO_BASE_URL}/search")
    print(f"Headers: {headers}")
    
    response = httpx.get(
        f"{QLOO_BASE_URL}/search",
        params={"query": query},
        headers=headers
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def get_recommendations(sample_ids, target="music"):
    """Get music recommendations based on sample IDs"""
    headers = {
        "X-Api-Key": QLOO_API_KEY
    }
    
    data = {
        "sample": sample_ids,
        "target": target
    }
    
    print(f"Trying recommendations endpoint with GET method")
    response = httpx.get(
        f"{QLOO_BASE_URL}/recommendations",
        params={
            "sample": ",".join(sample_ids), 
            "filter.type": f"urn:entity:{target}"
        },
        headers=headers
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

if __name__ == "__main__":
    print(f"Using API Key: {QLOO_API_KEY[:10]}..." if QLOO_API_KEY else "No API Key found")
    
    # Test search functionality
    search_results = search_music("d4vd")
    if search_results:
        print(json.dumps(search_results, indent=2))
        
        # Extract some IDs for recommendations
        if "results" in search_results and search_results["results"]:
            sample_ids = [result["entity_id"] for result in search_results["results"][:3]]
            
            print(f"\n=== Getting recommendations based on IDs: {sample_ids} ===")
            recs = get_recommendations(sample_ids)
            if recs:
                print(json.dumps(recs, indent=2))