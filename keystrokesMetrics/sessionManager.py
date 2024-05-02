import time
from metricsCalculation import MetricsCalculator
import uuid
import numpy as np
import pandas as pd
import os
from openpyxl import load_workbook


class SessionManager:
    def __init__(self, data_collector, db_handler, task_manager, user_id):
        self.data_collector = data_collector
        self.db_handler = db_handler
        self.current_session = None
        self.current_task_type = None
        self.session_start_time = None
        self.session_end_time = None
        self.current_task = None
        self.current_session_active = False
        self.task_manager = task_manager
        self.user_id = user_id

    def generate_unique_session_id(self):
        return str(uuid.uuid4())

    def set_user_id(self, user_id):
        self.user_id = user_id

    def start_session(self, task_type):
        self.data_collector.reset_collector()  # Reset data collector for a clean start
        self.metrics_calculator = MetricsCalculator()
        # Generate a unique session ID at the start of each session
        self.current_session_id = self.generate_unique_session_id()

        if not self.current_session_active:
            self.current_session_active = True
            self.session_start_time = time.time()
            self.task_manager.set_task(task_type)
            self.data_collector.start_collection()
            print(f"Session for task '{task_type}' started with Session ID: {self.current_session_id}")
        else:
            print("A session is already active.")



    def pause_session(self):
        if self.current_session_active:
            self.current_session_active = False
            self.data_collector.pause_collection()
            print("Session paused.")
        else:
            print("No session is active to pause.")

    def resume_session(self):
        if not self.current_session_active:
            self.current_session_active = True
            self.data_collector.resume_collection()
            print("Session resumed.")
        else:
            print("The session is already active.")




    def process_data(self, raw_data):
        current_task = self.task_manager.get_current_task()

        # Initialize the MetricsCalculator if it's not already initialized
        if not hasattr(self, 'metrics_calculator'):
            self.metrics_calculator = MetricsCalculator()
        
        # Feed the raw data into the MetricsCalculator
        for item in raw_data:
            key, press_time, release_time, dwell_time = item
            # Assuming you want to log the press time for each keystroke
            self.metrics_calculator.log_keystroke(key, press_time)


        # Somewhere in your session manager, you should have access to the actual typed text and the reference text.
        # This is just an example. You'll need to adapt it to how your application actually retrieves or stores these values.
        typed_text = self.data_collector.get_collected_text()  # Method to get the text typed by the user.

        # General Metrics
        wpm = self.metrics_calculator.calculate_typing_speed()
        inter_key_latencies = self.metrics_calculator.calculate_inter_key_latency()
        rhythm_variability = self.metrics_calculator.calculate_typing_rhythm_variability()
        backspace_count = self.metrics_calculator.calculate_backspace_usage()
        bigram_freq = self.metrics_calculator.calculate_bigram_frequencies()
        cpm = self.metrics_calculator.calculate_characters_per_minute()
        capital_letters = self.metrics_calculator.capitalisation_pattern()
        shift_key_usage = self.metrics_calculator.calculate_shift_key_usage()

        processed_data = {
            'wpm': wpm,
            'inter_key_latencies': inter_key_latencies,
            'rhythm_variability': rhythm_variability,
            'backspace_count': backspace_count,
            'bigram_freq': bigram_freq,
            'cpm': cpm,
            'capital_letters': capital_letters,
            'shift_key_usage': shift_key_usage,
        }
          # Add additional data/metrics collection and analysis as needed for continuous authentication
       
        # Example: Collect and analyze patterns specific to the task
        if current_task == "Fixed Text":

            error_rate = self.metrics_calculator.calculate_error_rate()
            punctuation_count = self.metrics_calculator.punctuation_metrics()
            processed_data['error_rate'] = error_rate
            processed_data['punctuation_count'] = punctuation_count

        elif current_task == "Custom Text":
                # Collect and process metrics specific to the transcription task
        # Assuming you have additional custom data or you want to store the processed metrics
            storage_status = self.data_collector.store_data_in_database(processed_data)
            
            # Optionally, handle the storage status
            processed_data.update(storage_status)
            #processed_data['storage_status'] = storage_status
        
        # Only for Free Typing
        elif current_task == "Free Typing":
            # Collect and process metrics specific to the free typing task
            punctuation_count = self.metrics_calculator.punctuation_metrics()
            paragraph_count, sentence_count = self.metrics_calculator.structure_analysis(typed_text)
            processed_data['punctuation_count'] = punctuation_count
            processed_data['paragraph_count'] = paragraph_count
            processed_data['sentence_count'] = sentence_count
        # Combine metrics into a structured format for storage or further analysis

     
        return processed_data

    def set_data_collector(self, data_collector):
        self.data_collector = data_collector


    def validate_and_log_session_data(self, session_data):
        # Convert numpy arrays to lists and handle None values
        for key, value in session_data.items():
            if isinstance(value, np.ndarray):
                session_data[key] = value.tolist()  # Convert numpy arrays to lists
            elif value is None:
                session_data[key] = 'None'  # Convert None values to a string representation
            # Implement additional validations as necessary
                
            if 'bigram_freq' in session_data:
                session_data['bigram_freq'] = {str(key): value for key, value in session_data['bigram_freq'].items()}
        #print("Final session data ready for storage:", session_data)
        return session_data
    


    def save_to_text_file(self, user_id, session_id, task_type, processed_data, file_path='session_datauser11test.csv'):
        # Prepare new data as a string in CSV format
        new_data = f"{user_id},{session_id},{task_type},{','.join(str(value) for value in processed_data.values())}\n"

        # Check if the file exists to determine whether to append or write
        mode = 'a' if os.path.exists(file_path) else 'w'
        with open(file_path, mode) as file:
            if mode == 'w':
                # Write header only if creating a new file
                header = "User ID,Session ID,Task Type," + ",".join(processed_data.keys()) + "\n"
                file.write(header)
            file.write(new_data)






    def end_session(self):
            if self.current_session_active:
                self.current_session_active = False
                self.session_end_time = time.time()
                
                # Finalize data collection
                raw_data = self.data_collector.end_collection()

                # Inside end_session, before processing data for storage
                # Debug print statements to verify metrics before processing for storage
                #print("MetricsCalculator Dwell Times:", self.metrics_calculator.dwell_times)
                #print("MetricsCalculator Flight Times:", self.metrics_calculator.flight_times)
                print(f"MetricsCalculator ID in SessionManager before processing data: {id(self.metrics_calculator)}")

                
                # Process the collected data
                processed_data = self.process_data(raw_data)

                        # Print the processed data to verify its content before storing
                print("Processed data being stored:", processed_data)
                
                # Store the data
                #self.store_data(processed_data)

                # Use the unique session ID when storing the session data
                user_id = self.user_id  # Get the current user's ID
                task_type = self.task_manager.get_current_task()
                self.db_handler.store_user_session_data(user_id, self.current_session_id, task_type, processed_data)

                # Save the processed data to an Excel file
                self.save_to_text_file(user_id, self.current_session_id, task_type, processed_data)

                
                session_duration = self.session_end_time - self.session_start_time
                print(f"Session ended. Duration: {session_duration} seconds.")
                
                # Optional: Provide feedback to the user
                #self.provide_user_feedback(session_duration, processed_data)
            else:
                print("No active session to end.")










