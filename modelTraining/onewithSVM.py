import pandas as pd
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report

# Load datasets
all_users = pd.read_csv('userALLPRO.csv')
true_user = pd.read_csv('user_test11trueusers_AlltasksPRO.csv') # authenticate user
false_user = pd.read_csv('user_test7Falseusers_AlltasksPRO.csv') # unauthenticate user

# Remove the 'user_id' column from all datasets
all_users.drop('user_id', axis=1, inplace=True)
true_user.drop('user_id', axis=1, inplace=True)
false_user.drop('user_id', axis=1, inplace=True)

# Pre-process data
def preprocess_data(df):
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(df)
    return features_scaled

# Function to test data against the model
def test_data(model, data, true_labels):
    predictions = model.predict(data)
    print(classification_report(true_labels, predictions, zero_division=0))

# Train One-Class SVM on all_users with different 'nu' values
# Train One-Class SVM on all_users with different 'nu' values
nu_values = [0.01, 0.1, 0.2]
tasks = ['Custom Text', 'Fixed Text', 'Free Typing']  # List of tasks

for nu in nu_values:
    print(f"\nTesting with nu={nu}:")
    oc_svm = OneClassSVM(kernel='rbf', gamma='auto', nu=nu)
    
    for task in tasks:
        print(f"Training on {task} task type:")
        X_train = preprocess_data(all_users[all_users[f'task_type_{task}'] == 1])
        oc_svm.fit(X_train)

        # Test with true_user and false_user for the current task
        true_user_task = preprocess_data(true_user[true_user[f'task_type_{task}'] == 1])
        false_user_task = preprocess_data(false_user[false_user[f'task_type_{task}'] == 1])

        # Generating labels for classification report
        true_labels_true_user = [1] * len(true_user_task)  # True users should not be anomalies
        true_labels_false_user = [-1] * len(false_user_task)  # False users should be anomalies

        # Testing One-Class SVM
        print(f"One-Class SVM - True user data for {task}:")
        test_data(oc_svm, true_user_task, true_labels_true_user)
        print(f"One-Class SVM - False user data for {task}:")
        test_data(oc_svm, false_user_task, true_labels_false_user)
