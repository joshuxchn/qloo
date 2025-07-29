# backend/database/user.py

class User:
    """Represents a user in the application."""

    def __init__(self, user_id, username, email, password,
                 list_of_list_ids=None, access_token=None,
                 refresh_token=None, token_type=None,
                 token_expiry=None, preferred_location=None):
        """
        Initializes a User object.
        Note: All parameters use snake_case for consistency.
        """
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.list_of_list_ids = list_of_list_ids if list_of_list_ids is not None else []
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.token_type = token_type
        self.token_expiry = token_expiry
        self.preferred_location = preferred_location

    def __repr__(self):
        """Provides a developer-friendly representation of the User object."""
        return f"<User id='{self.user_id}' username='{self.username}' email='{self.email}'>"