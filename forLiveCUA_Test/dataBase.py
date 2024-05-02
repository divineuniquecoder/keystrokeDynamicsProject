import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class DataBase:
    def __init__(self, credentials_path):
        if not firebase_admin._apps:
        # Initialize Firebase admin with your project's credentials.
            cred = credentials.Certificate(credentials_path)
            firebase_admin.initialize_app(cred)
        
        # Get a reference to the Firestore service
        self.db = firestore.client()

    def get_user(self, user_id):
        # Get a user document from Firestore
        user_ref = self.db.collection('users').document(user_id)
        return user_ref.get()

    def add_user(self, user_id, user_data):
        # Add a new user document to Firestore
        user_ref = self.db.collection('users').document(user_id)
        user_ref.set(user_data)

    def retrieve_user(self, username):
        try:
            user_ref = self.db.collection('users').document(username)
            user_doc = user_ref.get()
            if user_doc.exists:
                return user_doc.to_dict()  # Or any other format you're using
            else:
                return None  # or any other indication that the user does not exist
        except Exception as e:
            print(f"An error occurred while retrieving the user: {e}")
            # Optionally log the error or handle it further
            return None
    def save_user(self, username, user_data):
            # Add a new user document to Firestore
            try:
                user_ref = self.db.collection('users').document(username)
                user_ref.set(user_data)
                return True, "User registered successfully."
            except Exception as e:
                # Handle any exceptions (e.g., network issues, permission problems)
                return False, f"Failed to register user: {e}"
            
            
    def store_session_data(self, session_id, session_data):
        try:
           session_ref = self.db.collection('session_data').document(session_id)
           session_ref.set(session_data)
           return True
        
        except Exception as e:
           print(f"Failed to store session data: {e}")
           return False

    def store_user_session_data(self, user_id, session_id, task_type, session_data):
        try:
            # Reference to the user's document
            user_ref = self.db.collection('users').document(user_id)
            
            # Reference to the session document within a task-specific subcollection
            session_ref = user_ref.collection(task_type).document(session_id)
            
            # Set the session data
            session_ref.set(session_data)
            print("Session data stored successfully under: " + user_id)
            return True
        except Exception as e:
            print(f"Failed to store session data for user {user_id}: {e}")
            return False
