import numpy as np
import joblib
import pandas as pd

class ContinuousAuthentication:
    def __init__(self, model_path):
        """Initializes the ContinuousAuthentication class with a pre-trained model."""
        self.model = self.load_model(model_path)
        

    def load_model(self, model_path):
        """Loads the pre-trained model (pipeline) from the specified path."""
        try:
            model = joblib.load(model_path)
            print("Model loaded successfully.")
            return model
        except FileNotFoundError:
            print(f"Model file not found at {model_path}.")
            return None

    def preprocess_and_predict(self, new_metrics):
        print("Entering the authenticate method.")  # Confirm the method is called
        if self.model is None:
            print("Model is not loaded.")
            return None

        if new_metrics is None:
            print("Error: new_metrics is None.")
            return None

        try:
            # Ensure new_metrics is in the correct shape
            new_metrics = np.array(new_metrics).reshape(1, -1)
            prediction = self.model.predict(new_metrics)
            print("Prediction result:", prediction)
            return prediction
        except Exception as e:
            print(f"Error during prediction: {e}")
            return None
        
    def prepare_features_and_predict(self, new_metrics):
        """
        Prepare the real-time data collected during continuous authentication and predict using the model pipeline.

        :param new_metrics: The real-time data metrics collected.
        :return: The prediction result.
        """
        if new_metrics is None:
            print("Error: new_metrics is None.")
            return None

        try:
            # Assuming new_metrics is already an array of features in the correct order
            features = np.array(new_metrics).reshape(1, -1)
            prediction = self.model.predict(features)
            print("Prediction result:", prediction)
            return prediction
        except Exception as e:
            print(f"Error during prediction: {e}")
            return None


    def predict(self, new_metrics):
        if new_metrics is None:
            print("Error: new_metrics is None.")
            return None
        try:
            # Ensure new_metrics is a DataFrame and has the expected format
            if not isinstance(new_metrics, pd.DataFrame):
                print("Error: new_metrics must be a pandas DataFrame.")
                return None

            # Log descriptive statistics of the input DataFrame
            #print(f"Input features for prediction:\n{new_metrics.describe()}\n")

            # Predict using the model with DataFrame
            prediction = self.model.predict(new_metrics)
            print("Prediction result:", prediction)

            # Log prediction probabilities if the model supports it
            if hasattr(self.model, 'predict_proba'):
                probabilities = self.model.predict_proba(new_metrics)
                print(f"Prediction probabilities:\n{probabilities}")

            return prediction
        except Exception as e:
            print(f"Error during prediction: {e}")
            return None
    
