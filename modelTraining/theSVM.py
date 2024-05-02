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
nu_values = [0.01, 0.1, 0.2]
for nu in nu_values:
    print(f"\nTesting with nu={nu}:")
    oc_svm = OneClassSVM(kernel='rbf', gamma='auto', nu=nu)
    
    # Training on custom text task type only for simplicity
    X_train = preprocess_data(all_users[all_users['task_type_Custom Text'] == 1])
    oc_svm.fit(X_train)

    # Test with true_user and false_user for Custom Text
    X_true_user = preprocess_data(true_user[true_user['task_type_Custom Text'] == 1])
    X_false_user = preprocess_data(false_user[false_user['task_type_Custom Text'] == 1])

    # Generating labels for classification report
    true_labels_true_user = [1] * len(X_true_user)  # True users should not be anomalies
    true_labels_false_user = [-1] * len(X_false_user)  # False users should be anomalies

    # Testing One-Class SVM
    print("One-Class SVM - True user data:")
    test_data(oc_svm, X_true_user, true_labels_true_user)
    print("One-Class SVM - False user data:")
    test_data(oc_svm, X_false_user, true_labels_false_user)
