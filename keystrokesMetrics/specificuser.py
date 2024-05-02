import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd

# Initialize Firebase
cred = credentials.Certificate('akinprojectsecurity-firebase-adminsdk-j5k32-87c11496a2.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

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

def save_to_csv(data, filename='user_test7Falseusers_Alltasks.csv'):
    df = pd.DataFrame(data)
    # Dynamically adjust column order based on what's present
    desired_order = ['user_id', 'task_type', 'session_id']
    actual_order = [col for col in desired_order if col in df.columns] + [col for col in df.columns if col not in desired_order]
    df = df[actual_order]
    df.to_csv(filename, index=False)

# Specify the user_id here
user_id = 'user7'

# Fetch and save the data for a specific user
data = fetch_user_data(user_id)
save_to_csv(data)

print(f"Data for user {user_id} has been successfully fetched and saved to output.csv.")
