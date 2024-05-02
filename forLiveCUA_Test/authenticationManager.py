import hashlib

# Global variable user session management
current_logged_in_user = None

class AuthenticationManager:
    def __init__(self, database_handler):
        self.db_handler = database_handler

    def hash_password(self, password):
        # Use hashlib or another library to securely hash the password
        return hashlib.sha256(password.encode()).hexdigest()

    def sign_in(self, username, password):
        global current_logged_in_user
        hashed_password = self.hash_password(password)
        # Validate credentials with the database
        user_data = self.db_handler.retrieve_user(username)
        if user_data and user_data.get('password') == hashed_password:
            current_logged_in_user = username  # Set the global variable to the signed-in user
            return True, username #"Sign-in successful."
        else:
            return False, "Invalid username or password."
        
    # Function to retrieve the current logged-in user's username
    def get_current_user_id():
        return current_logged_in_user

    def register(self, username, password):
        # Check if username already exists
        if self.db_handler.retrieve_user(username):
            return False, "Username already exists. Please choose a different username."
        
        hashed_password = self.hash_password(password)
        # Register a new user with the database
        success, message = self.db_handler.save_user(username, {'password': hashed_password})
        
        # Handle the registration status based on the success flag
        if success:
            return True, message  # Use the success message from save_user
        else:
            return False, message  # Use the failure message from save_user
