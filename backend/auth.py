import os
import sys
import uuid
import jwt
from datetime import datetime, timezone, timedelta
from flask import Flask, redirect, url_for, request, jsonify # Added request, jsonify
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from flask_cors import CORS
from functools import wraps # Added wraps for decorator

# --- Load Environment Variables & Path Setup ---
load_dotenv()
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from database import db_utils
from database.user import User

# --- User Management Logic (No changes needed here) ---
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
        user = User(
            user_id=user_id, username=username, email=email, password="google_auth",
            list_of_list_ids=[], access_token=None, refresh_token=None,
            token_type=None, token_expiry=None, preferred_location="98075"
        )
        # Assuming your User class uses user_id, not user_ID
        return user if db_utils.add_user_to_db(user) else None

    def get_or_create_google_user(self, google_profile):
        email = google_profile.get('email')
        if not email:
            raise ValueError("Email not found in Google profile")
        
        existing_user = self.find_user_by_email(email)
        if existing_user:
            return existing_user
        
        return self.create_new_user(email)

# --- Flask App Initialization ---
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
CORS(app)
oauth = OAuth(app)
user_service = AuthUserService()

oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

# === NEW: JWT Verification Decorator ===
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
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except Exception:
            return jsonify({'message': 'Token is invalid!'}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

# === NEW: API Route for User Profile ===
@app.route('/api/user/profile')
@token_required
def get_user_profile(current_user):
    """Returns the profile of the currently logged-in user."""
    user_data = {
        "id": current_user.user_id,
        "username": current_user.username,
        "email": current_user.email,
        "preferred_location": current_user.preferred_location,
        "list_ids": current_user.list_of_list_ids
    }
    return jsonify(user_data)

# === Authentication Routes ===
@app.route('/auth/google')
def login_google():
    redirect_uri = url_for('auth_google_callback', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@app.route('/auth/google/callback')
def auth_google_callback():
    try:
        token = oauth.google.authorize_access_token()
        user_info = token['userinfo']
        
        # This function now correctly finds or creates a user in the DB
        user = user_service.get_or_create_google_user(user_info)
        if not user:
            raise Exception("Failed to create or retrieve user from database.")

        # The payload now correctly uses 'user.user_id'
        jwt_payload = {
            'id': user.user_id,
            'email': user.email,
            'exp': datetime.now(timezone.utc) + timedelta(hours=24)
        }
        app_token = jwt.encode(jwt_payload, os.getenv("JWT_SECRET"), algorithm='HS256')

        return redirect(f"{os.getenv('FRONTEND_URL')}/auth/callback?token={app_token}")

    except Exception as e:
        print(f"Google auth callback error: {e}")
        return redirect(f"{os.getenv('FRONTEND_URL')}/login?error=true")

# --- Main Execution Block ---
if __name__ == '__main__':
    print("🚀 Starting Standalone Authentication Server")
    print("=" * 50)
    print("\n--- Initializing Database Tables ---")
    db_utils.create_tables()
    print("--- Database Table Initialization Complete ---\n")
    app.run(host='0.0.0.0', port=8001, debug=True)