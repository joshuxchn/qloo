import os
import sys
import uuid
import jwt
import json
from datetime import datetime, timezone, timedelta
from flask import Flask, redirect, url_for, request, jsonify
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from flask_cors import CORS
from functools import wraps

# --- Load Environment Variables & Path Setup ---
load_dotenv()
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from Database import db_utils
from Database.user import User
from Database.list import GroceryList
from Database.product import Product
from kroger import KrogerAPI

# --- User Management Logic ---
class AuthUserService:
    def find_user_by_email(self, email):
        conn = db_utils.get_db_connection()
        if conn is None: return None
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT user_id FROM users WHERE email = %s;", (email,))
                result = cur.fetchone()
                return db_utils.get_user_by_id(result[0]) if result else None
        finally:
            conn.close()

    def create_new_user(self, email):
        user_id = str(uuid.uuid4())
        username = email.split('@')[0]
        user = User(user_id=user_id, username=username, email=email, password="google_auth")
        return user if db_utils.add_user_to_db(user) else None

# --- Flask App, CORS, OAuth Initialization ---
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
CORS(app, supports_credentials=True)
oauth = OAuth(app)
user_service = AuthUserService()
kroger_api = KrogerAPI()

oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

# --- JWT Verification Decorator ---
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers and request.headers['Authorization'].startswith('Bearer '):
            token = request.headers['Authorization'].split(" ")[1]
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
            current_user = db_utils.get_user_by_id(data['id'])
            if not current_user:
                 return jsonify({'message': 'User not found!'}), 404
        except Exception:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

# --- API Routes ---
@app.route('/api/products/search', methods=['POST'])
@token_required
def search_kroger_products(current_user):
    data = request.get_json()
    search_term = data.get('searchTerm')
    if not search_term:
        return jsonify({"error": "searchTerm is required"}), 400

    zip_code = current_user.preferred_location or "98075" 
    
    products = kroger_api.productSearch(search_term, limit=3, zip_code=zip_code)
    
    product_dicts = [p.to_dict() for p in products]
    
    return jsonify(product_dicts)

@app.route('/api/user/profile')
@token_required
def get_user_profile(current_user):
    user_data = {
        "id": current_user.user_id, "username": current_user.username,
        "email": current_user.email, "firstName": current_user.first_name,
        "lastName": current_user.last_name, "preferredLocation": current_user.preferred_location,
        "budget": current_user.budget, "shoppingFrequency": current_user.shopping_frequency,
        "shoppingPriority": current_user.shopping_priority,
        "dietaryRestrictions": current_user.dietary_restrictions,
        "allergies": current_user.allergies, "healthGoals": current_user.health_goals,
        "favoriteCuisines": current_user.favorite_cuisines,
        "culturalBackground": current_user.cultural_background,
        "favoriteFoods": current_user.favorite_foods,
        "age": current_user.age, "gender": current_user.gender
    }
    return jsonify(user_data)

@app.route('/api/user/finalize-profile', methods=['POST'])
@token_required
def finalize_profile(current_user):
    profile_data = request.get_json()
    if not profile_data:
        return jsonify({"error": "Missing profile data"}), 400
    current_user.first_name = profile_data.get('first_name')
    current_user.last_name = profile_data.get('last_name')
    current_user.preferred_location = profile_data.get('preferred_location')
    current_user.budget = profile_data.get('budget')
    current_user.shopping_frequency = profile_data.get('shopping_frequency')
    current_user.shopping_priority = profile_data.get('shopping_priority')
    current_user.dietary_restrictions = profile_data.get('dietary_restrictions', [])
    current_user.allergies = profile_data.get('allergies', [])
    current_user.health_goals = profile_data.get('health_goals')
    current_user.favorite_cuisines = profile_data.get('favorite_cuisines', [])
    current_user.cultural_background = profile_data.get('cultural_background')
    current_user.favorite_foods = profile_data.get('favorite_foods')
    current_user.age = profile_data.get('age')
    current_user.gender = profile_data.get('gender')
    if db_utils.update_user_details(current_user):
        return jsonify({"message": "Profile updated successfully"}), 200
    else:
        return jsonify({"error": "Failed to update profile"}), 500

@app.route('/api/user/update-profile', methods=['POST'])
@token_required
def update_profile(current_user):
    profile_data = request.get_json()
    if not profile_data:
        return jsonify({"error": "Missing profile data"}), 400
    current_user.first_name = profile_data.get('firstName', current_user.first_name)
    current_user.last_name = profile_data.get('lastName', current_user.last_name)
    current_user.preferred_location = profile_data.get('preferredLocation', current_user.preferred_location)
    current_user.budget = profile_data.get('budget', current_user.budget)
    current_user.shopping_frequency = profile_data.get('shoppingFrequency', current_user.shopping_frequency)
    current_user.shopping_priority = profile_data.get('shoppingPriority', current_user.shopping_priority)
    current_user.dietary_restrictions = profile_data.get('dietaryRestrictions', current_user.dietary_restrictions)
    current_user.allergies = profile_data.get('allergies', current_user.allergies)
    current_user.health_goals = profile_data.get('healthGoals', current_user.health_goals)
    current_user.favorite_cuisines = profile_data.get('favoriteCuisines', current_user.favorite_cuisines)
    current_user.cultural_background = profile_data.get('culturalBackground', current_user.cultural_background)
    current_user.favorite_foods = profile_data.get('favoriteFoods', current_user.favorite_foods)
    current_user.age = profile_data.get('age', current_user.age)
    current_user.gender = profile_data.get('gender', current_user.gender)
    if db_utils.update_user_details(current_user):
        return jsonify({"message": "Profile updated successfully"}), 200
    else:
        return jsonify({"error": "Failed to update profile in database"}), 500

@app.route('/api/grocery-list/create', methods=['POST'])
@token_required
def create_grocery_list(current_user):
    data = request.get_json()
    list_name = data.get('name')
    items_data = data.get('items', [])
    if not list_name or not items_data:
        return jsonify({"error": "List name and items are required"}), 400
    products_on_list = []
    for item in items_data:
        product = Product(
            name=item.get('name'),
            price=item.get('price', 0.00),
            promo_price=item.get('promo_price'),
            fulfillment_type=item.get('fulfillment_type', 'UNKNOWN'),
            brand=item.get('brand', 'N/A'),
            inventory=item.get('inventory', 'UNKNOWN'),
            size=item.get('size', 'N/A'),
            last_updated=datetime.now(timezone.utc),
            location_ID=item.get('location_ID', 'N/A'),
            upc=item.get('upc', 'N/A'),
            category=item.get('category', 'Uncategorized')
        )
        quantity = item.get('quantity', 1)
        products_on_list.append((product, quantity))
    new_list = GroceryList(
        list_id=str(uuid.uuid4()),
        user_id=current_user.user_id,
        name=list_name,
        timestamp=datetime.now(timezone.utc),
        products_on_list=products_on_list
    )
    if db_utils.add_grocery_list_to_db(new_list):
        return jsonify({"message": "List created successfully", "list_id": new_list.list_id}), 201
    else:
        return jsonify({"error": "Failed to save list"}), 500

@app.route('/api/grocery-list/<string:list_id>', methods=['PUT'])
@token_required
def update_grocery_list_endpoint(current_user, list_id):
    data = request.get_json()
    items_data = data.get('items', [])
    list_name = data.get('name', 'My Grocery List')
    products_on_list = []
    for item in items_data:
        product = Product(
            name=item.get('name'),
            price=item.get('price', 0.00),
            promo_price=item.get('promo_price'),
            fulfillment_type=item.get('fulfillment_type', 'UNKNOWN'),
            brand=item.get('brand', 'N/A'),
            inventory=item.get('inventory', 'UNKNOWN'),
            size=item.get('size', 'N/A'),
            last_updated=datetime.now(timezone.utc),
            location_ID=item.get('location_ID', 'N/A'),
            upc=item.get('upc', 'N/A'),
            category=item.get('category', 'Uncategorized')
        )
        quantity = item.get('quantity', 1)
        products_on_list.append((product, quantity))
    list_to_update = GroceryList(
        list_id=list_id,
        user_id=current_user.user_id,
        name=list_name,
        timestamp=datetime.now(timezone.utc),
        products_on_list=products_on_list
    )
    if db_utils.update_grocery_list(list_to_update, current_user.user_id):
        return jsonify({"message": "List updated successfully"}), 200
    else:
        return jsonify({"error": "Failed to update list or permission denied"}), 404

@app.route('/api/grocery-list/<string:list_id>', methods=['DELETE'])
@token_required
def delete_grocery_list(current_user, list_id):
    if db_utils.remove_grocery_list(list_id, current_user.user_id):
        return jsonify({"message": "List deleted successfully"}), 200
    else:
        return jsonify({"error": "List not found or permission denied"}), 404
        
@app.route('/api/grocery-lists', methods=['GET'])
@token_required
def get_grocery_lists(current_user):
    user_lists = db_utils.get_all_lists_for_user(current_user.user_id)
    return jsonify(user_lists)

# --- SIGN UP FLOW ---
@app.route('/auth/google/signup')
def signup_google():
    redirect_uri = url_for('auth_google_signup_callback', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@app.route('/auth/google/signup/callback')
def auth_google_signup_callback():
    try:
        token = oauth.google.authorize_access_token()
        user_info = token['userinfo']
        email = user_info.get('email')
        if user_service.find_user_by_email(email):
            return redirect(f"{os.getenv('FRONTEND_URL')}/login?error=email_exists")
        user = user_service.create_new_user(email)
        if not user:
            raise Exception("Failed to create new user in database.")
        jwt_payload = {'id': user.user_id, 'email': user.email, 'exp': datetime.now(timezone.utc) + timedelta(hours=24)}
        app_token = jwt.encode(jwt_payload, os.getenv("JWT_SECRET"), algorithm='HS256')
        return redirect(f"{os.getenv('FRONTEND_URL')}/auth/callback?token={app_token}")
    except Exception as e:
        print(f"Signup callback error: {e}")
        return redirect(f"{os.getenv('FRONTEND_URL')}/login?error=true")

# --- SIGN IN FLOW ---
@app.route('/auth/google/login')
def login_google():
    redirect_uri = url_for('auth_google_login_callback', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@app.route('/auth/google/login/callback')
def auth_google_login_callback():
    try:
        token = oauth.google.authorize_access_token()
        user_info = token['userinfo']
        user = user_service.find_user_by_email(user_info.get('email'))
        if not user:
            return redirect(f"{os.getenv('FRONTEND_URL')}/login?error=not_found")
        jwt_payload = {'id': user.user_id, 'email': user.email, 'exp': datetime.now(timezone.utc) + timedelta(hours=24)}
        app_token = jwt.encode(jwt_payload, os.getenv("JWT_SECRET"), algorithm='HS256')
        return redirect(f"{os.getenv('FRONTEND_URL')}/auth/callback?token={app_token}")
    except Exception as e:
        print(f"Login callback error: {e}")
        return redirect(f"{os.getenv('FRONTEND_URL')}/login?error=true")

# --- Main Execution Block ---
if __name__ == '__main__':
    print("🚀 Starting Standalone Authentication Server")
    db_utils.create_tables()
    app.run(host='0.0.0.0', port=8001, debug=True)