import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd

# Initialize Firebase
cred = credentials.Certificate('akinprojectsecurity-firebase-adminsdk-j5k32-87c11496a2.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

def fetch_all_data():
    users_ref = db.collection('users').stream()
    
    all_data = []

    for user in users_ref:
        user_id = user.id
        
        # Assuming you have a way to determine task_types, either statically defined or fetched per user
        task_types = ["Custom Text", "Fixed Text", "Free Typing"]  # Example task types
        
        for task_type in task_types:
            sessions_ref = db.collection('users').document(user_id).collection(task_type).stream()
            
            for session in sessions_ref:
                session_data = session.to_dict()
                # Make sure to add the 'user_id', 'task_type', and 'session_id' explicitly
                session_data['user_id'] = user_id
                session_data['task_type'] = task_type
                session_data['session_id'] = session.id
                
                all_data.append(session_data)
    
    return all_data


def save_to_csv(data, filename='theOutput.csv'):
    df = pd.DataFrame(data)
    # Dynamically adjust column order based on what's present
    desired_order = ['user_id', 'task_type', 'session_id']
    actual_order = [col for col in desired_order if col in df.columns] + [col for col in df.columns if col not in desired_order]
    df = df[actual_order]
    df.to_csv(filename, index=False)


# Fetch and save the data
data = fetch_all_data()
save_to_csv(data)

print("Data has been successfully fetched and saved to output.csv.")
