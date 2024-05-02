from sklearn.impute import SimpleImputer
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd
import joblib  # For saving and loading models

# Load the preprocessed dataset
data_path = 'postProcessed.csv'  # Update this path accordingly
df = pd.read_csv(data_path)

print("Prediction data shape:", df.shape)
print("Prediction data columns:", df.columns)

# Example for user1 authentication
df['is_user1'] = (df['user_id'] == 'user11').astype(int)

# Preparing data for training and testing
X = df.drop(['user_id', 'is_user1'], axis=1)
y = df['is_user1']

# Splitting the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Creating a pipeline with imputation and SVM classifier
imputer = SimpleImputer(strategy='mean')
svc = SVC(C=1, kernel='rbf', gamma='scale')
pipeline = make_pipeline(imputer, svc)

# Training the model
pipeline.fit(X_train, y_train)

# Saving the trained pipeline to a file with a .pkl extension
model_filename = 'svm11.pkl11'
joblib.dump(pipeline, model_filename)
print(f"Model saved to {model_filename}")

# Loading the model from the file
loaded_pipeline = joblib.load(model_filename)

# Making predictions on the test set using the loaded pipeline
test_predictions = loaded_pipeline.predict(X_test)

# Evaluating the model
test_accuracy = accuracy_score(y_test, test_predictions)
print(f"Test Accuracy: {test_accuracy}")

# `loaded_pipeline` is now ready to make predictions on new data.
