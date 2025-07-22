import datetime
from datetime import datetime, timedelta, timezone
class User:
    def __init__(self, user_ID, username, email, password, list_of_list_ids, access_token, refresh_token, token_type, token_expiry, preferred_location):
        self.user_id = user_ID
        self.username = username
        self.email = email
        self.password = password
        self.preferred_location = preferred_location
        self.list_of_list_ids = list_of_list_ids if list_of_list_ids else []
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.token_type = token_type
        self.token_expiry = token_expiry if token_expiry else datetime.now(timezone.utc) + timedelta(days=1)