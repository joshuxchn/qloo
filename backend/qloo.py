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
    
    print(f"Making request to: {QLOO_BASE_URL}/v2/insights")
    print(f"Params: {params}")
    
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
    
    print(f"Getting food recommendations based on: {user_profile.favorite_tags}")
    
    # Build all Qloo signals with correct formats
    signals = build_qloo_signals(user_profile, bias_trends="medium")
    
    # Fold dietary restriction URNs (if any) into the same interests signal
    if user_profile.dietary_restrictions:
        existing_tags = signals.get("signal.interests.tags", "")
        all_tags = ([existing_tags] if existing_tags else []) + user_profile.dietary_restrictions
        signals["signal.interests.tags"] = ",".join(all_tags)
    
    print("Sending signals:", signals)
    
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
    
    print(f"Found {len(tags)} specialty dish recommendations from Qloo's taste graph")
    
    # Debug: inspect the returned affinities to see what signals are being used
    print("Debug affinities for first 5 tags:")
    for t in tags[:5]:
        print(f" • {t.get('name', 'Unknown')}: {t.get('query', {})}")
    
    return tags


def get_similar_entities(
    user_profile: UserProfile,
    seed_entity_urn: str,
    take: int = 10
) -> List[Dict]:
    """
    Return entities similar to a given seed entity, incorporating all user signals.
    
    - seed_entity_urn: A Qloo URN like "urn:entity:place:1234" or "urn:entity:movie:ABCD".
    - Uses filter.entities to seed similarity, plus signal.* params from build_qloo_signals.
    """
    print(f"Getting entities similar to {seed_entity_urn} based on user preferences")
    
    # 1) Derive filter.type from the URN (e.g. "urn:entity:place")
    parts = seed_entity_urn.split(":")
    if len(parts) < 4 or parts[0] != "urn" or parts[1] != "entity":
        raise ValueError(f"Invalid entity URN: {seed_entity_urn}")
    filter_type = f"urn:entity:{parts[2]}"
    
    # 2) Build all of the user's signals (interests, demographics, location, trends)
    signals = build_qloo_signals(user_profile)
    
    print("Sending signals for similar entities:", signals)
    print(f"Using filter.entities: {seed_entity_urn}")
    print(f"Using filter.type: {filter_type}")
    
    # 3) Fire the Insights call, seeding with filter.entities
    try:
        response = qloo_insights(
            filter_type=filter_type,
            take=take,
            **{"filter.entities": seed_entity_urn},   # seed similarity
            **signals
        )
    except Exception as e:
        print(f"Error calling insights for similar entities: {e}")
        return []
    
    if not response or "entities" not in response.get("results", {}):
        print("No similar entities found")
        return []
    
    entities = response["results"]["entities"]
    print(f"Found {len(entities)} similar entities")
    
    # Debug: show similarity scores
    print("Debug entity similarities:")
    for i, entity in enumerate(entities[:5]):
        name = entity.get("name", "Unknown")
        affinity = entity.get("query", {}).get("affinity", 0)
        print(f" • {name}: {affinity:.3f}")
    
    # 4) Return the raw entities (with name, entity_id, popularity, query.affinity, etc.)
    return entities


def food_recommender_workflow(user_profile: UserProfile) -> Dict:
    """Complete food recommendation workflow using API-driven recommendations"""
    print("=== Starting Food Recommendation Workflow ===")
    print("Getting food recommendations directly from Qloo API")
    
    # Step 1: Signal Collection (already done in user_profile)
    print(f"User Profile: Age {user_profile.age}, City: {user_profile.city}")
    print(f"Food Interests: {user_profile.favorite_tags}")
    
    # Step 2: Get food recommendations from API
    print("\n--- Getting Food Recommendations from API ---")
    food_recommendations = get_food_recommendations(user_profile, take=50)
    
    if not food_recommendations:
        return {"error": "No food recommendations found"}
    
    print(f"Food recommendations: {[t.get('name', '') for t in food_recommendations[:8]]}")
    
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

def print_food_workflow_results(results: Dict):
    """Pretty print food workflow results"""
    if "error" in results:
        print(f"Error: {results['error']}")
        return
        
    print("=== FOOD RECOMMENDATION RESULTS ===")
    
    profile = results["user_profile"]
    print(f"User: Age {profile['age']}, City: {profile['city']}")
    print(f"Food Interests: {', '.join(profile['food_interests']) if profile['food_interests'] else 'None specified'}")
    
    print("\n--- FOOD RECOMMENDATIONS ---")
    for i, food in enumerate(results["food_recommendations"], 1):
        print(f"{i}. {food['name']} (Affinity: {food['affinity']:.3f}, Weight: {food['weight']:.3f})")

if __name__ == "__main__":
    print(f"Using API Key: {QLOO_API_KEY[:10]}..." if QLOO_API_KEY else "No API Key found")
    
    # Create test user profile with food preferences
    test_user = UserProfile(
        age=15,
        gender="female", 
        city="Los Angeles",
        favorite_tags=["urn:tag:genre:place:restaurant:chinese", "urn:tag:genre:place:restaurant:italian"],
        audiences=["foodies"],
        dietary_restrictions=[]  # Remove dietary restrictions for testing
    )
    
    print("\n=== TESTING FOOD RECOMMENDER WORKFLOW ===")
    results = food_recommender_workflow(test_user)
    print_food_workflow_results(results)
    
    print("\n" + "="*50)
    print("=== TESTING SIMILAR ENTITY RECOMMENDATIONS ===")
    
    # Test 1: Similar cuisine tags based on user preferences
    reference_cuisine = "urn:tag:genre:place:restaurant:chinese"
    
    print(f"Finding cuisine tags similar to Chinese restaurants for this user...")
    similar_cuisines = get_similar_entities(
        user_profile=test_user,
        entity_id=reference_cuisine,
        entity_type="urn:tag",
        take=5
    )
    
    if similar_cuisines:
        print("\n--- CUISINE TAGS SIMILAR TO CHINESE RESTAURANTS ---")
        for i, tag in enumerate(similar_cuisines, 1):
            name = tag.get("name", "Unknown")
            affinity = tag.get("query", {}).get("affinity", 0)
            tag_id = tag.get("tag_id", tag.get("id", "No ID"))
            print(f"{i}. {name} (Affinity: {affinity:.3f})")
            print(f"   Tag ID: {tag_id}")
    else:
        print("No similar cuisine tags found")
    
    print("\n" + "-"*30)
    
