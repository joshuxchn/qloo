class User:
    """Represents a user in the application, including all profile details."""

    def __init__(self, user_id, username, email, password,
                 list_of_list_ids=None, access_token=None,
                 refresh_token=None, token_type=None,
                 token_expiry=None,
                 first_name=None,
                 last_name=None,
                 preferred_location=None,
                 budget=200,
                 shopping_frequency='Weekly',
                 shopping_priority='Balanced Approach',
                 dietary_restrictions=None,
                 allergies=None,
                 health_goals=None,
                 favorite_cuisines=None,
                 cultural_background=None,
                 favorite_foods=None,
                 age=None,
                 gender=None):
        
        # --- Core User/Auth Fields ---
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.token_type = token_type
        self.token_expiry = token_expiry

        # --- Grocery List Management ---
        self.list_of_list_ids = list_of_list_ids if list_of_list_ids is not None else []

        # --- Basic Information ---
        self.first_name = first_name
        self.last_name = last_name
        self.preferred_location = preferred_location
        self.age = age
        self.gender = gender

        # --- Budget & Shopping Preferences ---
        self.budget = budget
        self.shopping_frequency = shopping_frequency
        self.shopping_priority = shopping_priority
        
        # --- Dietary & Health Preferences ---
        self.dietary_restrictions = dietary_restrictions if dietary_restrictions is not None else []
        self.allergies = allergies if allergies is not None else []
        self.health_goals = health_goals

        # --- Cultural & Taste Preferences ---
        self.favorite_cuisines = favorite_cuisines if favorite_cuisines is not None else []
        self.cultural_background = cultural_background
        self.favorite_foods = favorite_foods

    def __repr__(self):
        return f"<User id='{self.user_id}' username='{self.username}'>"