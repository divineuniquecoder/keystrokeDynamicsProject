import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd

# Initialize Firebase
cred = credentials.Certificate('akinprojectsecurity-firebase-adminsdk-j5k32-87c11496a2.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

def fetch_all_data_except_task_types_and_users(exclude_task_types, exclude_users):
    users_ref = db.collection('users').stream()
    
    all_data = []

    for user in users_ref:
        user_id = user.id
        
        if user_id not in exclude_users:
            task_types = ["Custom Text", "Fixed Text", "Free Typing"]  # Example task types
            
            for task_type in task_types:
                if task_type not in exclude_task_types:
                    sessions_ref = db.collection('users').document(user_id).collection(task_type).stream()
                    
                    for session in sessions_ref:
                        session_data = session.to_dict()
                        # Make sure to add the 'user_id', 'task_type', and 'session_id' explicitly
                        session_data['user_id'] = user_id
                        session_data['task_type'] = task_type
                        session_data['session_id'] = session.id
                        
                        all_data.append(session_data)
    
    return all_data

# Specify the task types and users you want to exclude
exclude_task_types = ["Custom Text", "Fixed Text"]
#exclude_users = ["test", "user11test", "user1", "user2", "user3", "user4", "user5", "user6", "user7", "user8", "user9", "user10"]
exclude_users = ["user_test11", "user7"]

# Fetch all data except for the specified task types and users
data = fetch_all_data_except_task_types_and_users(exclude_task_types, exclude_users)

def save_to_csv(data, filename='newFreetyping.csv'):
    df = pd.DataFrame(data)
    # Dynamically adjust column order based on what's present
    desired_order = ['user_id', 'task_type', 'session_id']
    actual_order = [col for col in desired_order if col in df.columns] + [col for col in df.columns if col not in desired_order]
    df = df[actual_order]
    df.to_csv(filename, index=False)


# Save the fetched data to a CSV file
save_to_csv(data)

print("Data has been successfully fetched and saved to fixed.csv")
