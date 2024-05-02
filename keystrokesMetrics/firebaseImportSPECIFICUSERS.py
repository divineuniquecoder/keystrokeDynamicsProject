import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd

# Initialize Firebase
cred = credentials.Certificate('akinprojectsecurity-firebase-adminsdk-j5k32-87c11496a2.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

def fetch_all_users_data(exclude_users):
    all_data = []

    users_ref = db.collection('users').stream()

    for user in users_ref:
        user_id = user.id
        
        # Check if the user_id is in the list of excluded users
        if user_id not in exclude_users:
            user_data = fetch_user_data(user_id)
            all_data.extend(user_data)

    return all_data

def fetch_user_data(user_id):
    all_data = []
    task_types = ["Custom Text", "Fixed Text", "Free Typing"]  # Example task types

    for task_type in task_types:
        sessions_ref = db.collection('users').document(user_id).collection(task_type).stream()

        for session in sessions_ref:
            session_data = session.to_dict()
            session_data['user_id'] = user_id
            session_data['task_type'] = task_type
            session_data['session_id'] = session.id

            all_data.append(session_data)

    return all_data

def save_to_csv(data, filename='userALL.csv'):
    df = pd.DataFrame(data)
    # Dynamically adjust column order based on what's present
    desired_order = ['user_id', 'task_type', 'session_id']
    actual_order = [col for col in desired_order if col in df.columns] + [col for col in df.columns if col not in desired_order]
    df = df[actual_order]
    df.to_csv(filename, index=False)

# Specify the users to exclude
exclude_users = ["user7", "user_test11"]

# Fetch and save the data for all users except excluded ones
data = fetch_all_users_data(exclude_users)
save_to_csv(data)

print(f"Data for all users has been successfully fetched and saved to userALL.csv.")
