import httpx
import os
from dotenv import load_dotenv
import json
from typing import Dict, List, Optional

# Load environment variables
load_dotenv()

QLOO_API_KEY = os.getenv("QLOO_API_KEY")
QLOO_BASE_URL = os.getenv("QLOO_BASE_URL", "https://hackathon.api.qloo.com").rstrip("/")

class UserProfile:
    """User profile for food recommendations"""
    def __init__(self, age=None, gender=None, city=None, favorite_tags=None, 
                 audiences=None, dietary_restrictions=None):
        self.age = age
        self.gender = gender  
        self.city = city  # Note: not used in API calls due to limitations
        self.favorite_tags = favorite_tags or []
        self.audiences = audiences or []  # Note: not used in API calls due to limitations
        self.dietary_restrictions = dietary_restrictions or []

def build_qloo_signals(user_profile: UserProfile, bias_trends: str = "medium") -> Dict:
    """Build Qloo signal parameters from user profile"""
    signals = {}
    
    if user_profile.favorite_tags:
        signals["signal.interests.tags"] = ",".join(user_profile.favorite_tags)
    
    if user_profile.age is not None:
        # Convert age to Qloo age groups (hackathon API requirement)
        if user_profile.age <= 24:
            age_group = "24_and_younger"
        elif user_profile.age <= 29:
            age_group = "25_to_29"
        elif user_profile.age <= 34:
            age_group = "30_to_34"
        elif user_profile.age <= 44:
            age_group = "35_to_44"
        elif user_profile.age <= 54:
            age_group = "45_to_54"
        else:
            age_group = "55_and_older"
        signals["signal.demographics.age"] = age_group
        
    if user_profile.gender:
        signals["signal.demographics.gender"] = user_profile.gender
        
    # Note: audiences and location signals don't work with this API
    # Removed to keep only working signals
        
    # Valid trend bias values for hackathon API
    signals["bias.trends"] = bias_trends
    
    return signals


def qloo_insights(filter_type: str, take: int, **signals) -> Optional[Dict]:
    """Generic Qloo insights API call"""
    headers = {
        "X-Api-Key": QLOO_API_KEY
    }
    
    params = {
        "filter.type": filter_type,
        "take": take,
        **signals
    }
    
    response = httpx.get(
        f"{QLOO_BASE_URL}/v2/insights",
        params=params,
        headers=headers,
        timeout=30.0
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def get_food_recommendations(user_profile: UserProfile, take: int = 50) -> Optional[List[Dict]]:
    """Get food recommendations using Qloo's cross-domain embedding magic"""
    
    if not user_profile.favorite_tags:
        return []
    

    
    # Build all Qloo signals with correct formats
    signals = build_qloo_signals(user_profile, bias_trends="medium")
    
    # Fold dietary restriction URNs (if any) into the same interests signal
    if user_profile.dietary_restrictions:
        existing_tags = signals.get("signal.interests.tags", "")
        all_tags = ([existing_tags] if existing_tags else []) + user_profile.dietary_restrictions
        signals["signal.interests.tags"] = ",".join(all_tags)
    

    
    # Call Qloo with working signals only
    response = qloo_insights(
        filter_type="urn:tag",
        take=take,
        **{"filter.tag.types": "urn:tag:specialty_dish:place"},
        **signals
    )
    
    tags = response.get("results", {}).get("tags", []) if response else []
    
    if not tags:
        print("No specialty dish recommendations found from API")
        return []
    


    
    return tags


def food_recommender_workflow(user_profile: UserProfile) -> Dict:
    """Complete food recommendation workflow using API-driven recommendations"""

    
    # Step 1: Signal Collection (already done in user_profile)

    
    # Step 2: Get food recommendations from API

    food_recommendations = get_food_recommendations(user_profile, take=50)
    
    if not food_recommendations:
        return {"error": "No food recommendations found"}
    

    
    # Step 3: Package results
    results = {
        "user_profile": {
            "age": user_profile.age,
            "city": user_profile.city,
            "food_interests": user_profile.favorite_tags
        },
        "food_recommendations": [
            {
                "name": t.get("name", "Unknown"),
                "tag_id": t.get("tag_id", t.get("id", "")),
                "type": t.get("subtype", t.get("type", "")),
                "affinity": t.get("query", {}).get("affinity", 0),
                "weight": t.get("weight", 0)
            } for t in food_recommendations
        ],
        "raw_data": {
            "food_recommendations": food_recommendations
        }
    }
    
    return results

def parse_search_results(search_data):
    """Parse search results into readable format"""
    if not search_data or "results" not in search_data:
        return "No results found"
    
    parsed = []
    for result in search_data["results"]:
        name = result.get("name", "Unknown")
        entity_id = result.get("entity_id", "N/A")
        entity_type = result.get("type", "Unknown type")
        parsed.append(f"• {name} (ID: {entity_id}, Type: {entity_type})")
    
    return "\n".join(parsed)

def parse_recommendations(rec_data):
    """Parse recommendation results into readable format"""
    if not rec_data or "results" not in rec_data:
        return "No recommendations found"
    
    parsed = []
    for result in rec_data["results"]:
        name = result.get("name", "Unknown")
        entity_id = result.get("entity_id", "N/A")
        score = result.get("score", "N/A")
        parsed.append(f"• {name} (Score: {score}, ID: {entity_id})")
    
    return "\n".join(parsed)

def get_parsed_recommendations(user_profile: UserProfile) -> List[Dict]:
    """
    Get parsed recommendations from start to finish and return as a clean list.
    
    Args:
        user_profile: UserProfile object with user preferences
        
    Returns:
        List of dictionaries containing parsed recommendation data, or empty list if error
    """
    # Run the complete workflow
    results = food_recommender_workflow(user_profile)
    
    # Handle error case
    if "error" in results:
        print(f"Error getting recommendations: {results['error']}")
        return []
    
    # Extract and return the food recommendations list
    return results.get("food_recommendations", [])

def print_food_workflow_results(results: Dict):
    """Pretty print food workflow results"""
    if "error" in results:
        print(f"Error: {results['error']}")
        return
        
    
    profile = results["user_profile"]
    print(f"User: Age {profile['age']}, City: {profile['city']}")
    print(f"Food Interests: {', '.join(profile['food_interests']) if profile['food_interests'] else 'None specified'}")
    

    for i, food in enumerate(results["food_recommendations"], 1):
        print(f"{i}. {food['name']} (Affinity: {food['affinity']:.3f}, Weight: {food['weight']:.3f})")

if __name__ == "__main__":

    
    # Create test user profile with food preferences
    test_user = UserProfile(
        age=25,
        gender="female", 
        city="Los Angeles",
        favorite_tags=["urn:tag:genre:place:restaurant:chinese", "urn:tag:genre:place:restaurant:italian"],
        audiences=["foodies"],
        dietary_restrictions=[]
    )
    
  
    
    recommendations = get_parsed_recommendations(test_user)
    
    if recommendations:
        print(f"\nSuccessfully retrieved {len(recommendations)} recommendations!")
        print("\nTop 10 recommendations:")
        for i, rec in enumerate(recommendations[:10], 1):
            print(f"{i:2d}. {rec['name']}")
            print(f"    Tag ID: {rec['tag_id']}")
            print(f"    Affinity: {rec['affinity']:.3f}")
            print(f"    Weight: {rec['weight']}")
            print()
        
        print("\nJust the food names (first 15):")
        food_names = [rec['name'] for rec in recommendations[:15]]
        for name in food_names:
            print(f"• {name}")
            
    else:
        print("No recommendations found or error occurred")
    
