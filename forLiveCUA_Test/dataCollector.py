import time
from dataBase import DataBase  # Import the DataBase class from your module
import tkinter as tk
import numpy as np
import threading
import pandas as pd




class DataCollector:
    def __init__(self, metrics_calculator, ui, task_manager, credentials_path, model_scaler):
        #self.ui = ui
        self.metrics_calculator = metrics_calculator
        self.ui = ui
        self.task_manager = task_manager
        self.db = DataBase(credentials_path)  # Pass the credentials path to the DataBase class
        # A dictionary to hold key press times
        self.key_press_times = {}
        # A list to hold all keystroke timings
        self.keystroke_timings = []
        self.keystrokes_sequence = []  # Added to track the sequence of all keystrokes, including special keys
        self.last_release_time = None
        self.is_collecting = True  # Assume collection is allowed initially
        self.last_processed_key_time = 0  # Initialize a last processed key time
        self.debounce_threshold = 0.05  # Threshold in seconds
        self.model_scaler = model_scaler
        self.start_periodic_data_preparation()


    def on_key_press(self, event):
        if not self.is_collecting:
            return
        current_time = time.time()
        key = event.keysym
        # Immediate logging and feedback
        self.metrics_calculator.log_keystroke(key, current_time)
        #print(f"[KeyPress] Timestamp: {current_time}")
        # Debounce check
        if (current_time - self.last_processed_key_time) < self.debounce_threshold:
            return
        self.last_processed_key_time = current_time
        # Handle flight time
        if self.last_release_time:
            flight_time = current_time - self.last_release_time
            self.metrics_calculator.log_flight_time(flight_time)
        self.key_press_times[key] = current_time
        self.keystrokes_sequence.append(('press', key, current_time))

    def on_key_release(self, event):
        if not self.is_collecting:
            return
        current_time = time.time()
        key = event.keysym
        press_time = self.key_press_times.pop(key, None)
        if press_time:
            dwell_time = current_time - press_time
            self.metrics_calculator.log_dwell_time(dwell_time)
            self.keystroke_timings.append((key, press_time, current_time, dwell_time))
        self.keystrokes_sequence.append(('release', key, current_time))
        self.last_release_time = current_time


    def periodically_update_metrics(self):
        SOME_THRESHOLD = 10  # Example threshold, consider adjusting based on testing
        if len(self.keystrokes_sequence) >= SOME_THRESHOLD:
            self.metrics_calculator.update_keystrokes(self.keystrokes_sequence)
            self.keystrokes_sequence.clear()  # Prepare for the next batch of keystrokes
            # Optionally, directly invoke a metrics calculation here if needed,
            # or rely on the existing periodic calculation to handle this in its next cycle.


    def resolve_key(self, event):
        # Handle special keys explicitly; this might need adjustments based on observed event behavior
        if event.keysym in ('BackSpace', 'Shift_L', 'Shift_R'):
            return event.keysym
        return event.char  # Use the character for regular keys

    def start_periodic_data_preparation(self, interval=5):
        """Initiates periodic data preparation for authentication."""
        threading.Timer(interval, self.start_periodic_data_preparation, [interval]).start()
        # Call the prepare_metrics_for_authentication method to process collected data
        prepared_data = self.prepare_metrics_for_authentication()
        # Here, you might further process prepared_data or make decisions based on it


            
    def handle_special_key(self, key, timestamp):
        # This example just logs the special key usage.
        # You might want to record this information for analysis, 
        # or use it in real-time to adjust the behavior of your application.
        
        # For instance, you might log the time a special key was pressed:
        special_key_usage = {
            'key': key,
            'timestamp': timestamp,
            'event': 'release'
        }
        
        # You could append this to a list of special key events:
        self.special_key_events.append(special_key_usage)
        
        # If you're interested in the dwell time of special keys, you could calculate it:
        if key in self.key_press_times:
            dwell_time = timestamp - self.key_press_times[key]
            self.special_key_dwell_times.append((key, dwell_time))
        
        # Or you might handle specific behavior, like enabling 'Shift' mode:
        if key in ('Shift_L', 'Shift_R'):
            self.shift_mode = False  # Assuming you set it to True on key press

        # Any other special handling can be added here.
            
    def pause_collection(self):
        self.is_collecting = False
        print("Data collection paused.")

    def resume_collection(self):
        self.is_collecting = True
        print("Data collection resumed.")

    def on_event(self, event):
        if not self.is_collecting:
            return  # Ignore the event because collection is paused
        # Process the event here
        print(f"Event processed: {event}")

    def resume_collection(self):
            # Logic to resume data collection, for example:
            # Re-bind the key event handlers if they were unbound on pause
            self.ui.root.bind("<KeyPress>", self.on_key_press)
            self.ui.root.bind("<KeyRelease>", self.on_key_release)
            print("Data collection resumed.")

    def reset_collector(self):
        # Reset the collector to prepare for a new session
        self.key_press_times.clear()
        self.keystroke_timings.clear()

    '''
    def get_collected_text(self):
        # Retrieve the text from the Tkinter Text widget
        return self.ui.text_input.get("1.0", tk.END)
    '''

    '''
    def get_collected_text(self):
        # Retrieve the text from the Tkinter Text widget named 'text_input_continuous'
        return self.ui.text_input_continuous.get("1.0", tk.END)
    '''

    def store_data_in_database(self, additional_data=None):
        # Prepare the internal metrics for storage
        data_to_store = {
            'flight_times': self.metrics_calculator.flight_times,
            'dwell_times': self.metrics_calculator.dwell_times,
            # Include any other internal data relevant for storage
        }
        
        # If additional data is provided, merge it with the internal metrics
        if additional_data is not None:
            data_to_store.update(additional_data)
        
        # Here, you would add your logic to actually store 'data_to_store' in your database.
        # For demonstration, we're just printing the data.
        print("Data to be stored:", data_to_store)
        
        # Return the specific metrics 'flight_times' and 'dwell_times'
        return {
            'flight_times': data_to_store['flight_times'],
            'dwell_times': data_to_store['dwell_times']
        }


    def start_collection(self):
            # Start data collection process
    # Bind key events to handlers
        self.ui.root.bind("<KeyPress>", self.on_key_press)
        self.ui.root.bind("<KeyRelease>", self.on_key_release)


    def pause_collection(self):
        self.is_collecting = False
        print("Data collection paused.")

    def resume_collection(self):
        self.is_collecting = True
        print("Data collection resumed.")

    def on_event(self, event):
        if not self.is_collecting:
            return  # Ignore the event because collection is paused
        # Process the event here
        print(f"Event processed: {event}")







    def end_collection(self):
        # Logic to finalize data collection, such as unbinding event handlers
        self.ui.root.unbind("<KeyPress>")
        self.ui.root.unbind("<KeyRelease>")

        # Update the MetricsCalculator with the collected keystrokes before ending
        self.metrics_calculator.update_keystrokes(self.keystrokes_sequence)
                # Print the entire keystroke sequence and timings for review
        print("Keystroke Sequence:")
        for event in self.keystrokes_sequence:
            print(event)
        
        print("Keystroke Timings:")
        for timing in self.keystroke_timings:
            print(timing)
            # Call the method to store the data in the database
        self.store_data_in_database()
        # Possibly return the collected data or handle it as needed
        return self.keystroke_timings

    def set_user_interface(self, ui):
        self.ui = ui

    def get_collected_text(self):
        # Ensure the text_input_continuous widget is set up before accessing it
        if hasattr(self.ui, 'text_input_continuous'):
            return self.ui.text_input_continuous.get("1.0", "end-1c")
        else:
            print("text_input_continuous widget is not yet set up.")
            return ""



    def prepare_metrics_for_authentication(self):
        # Existing code to compute metrics...

        # Debug data collection
        print(f"Keystrokes recorded: {len(self.metrics_calculator.keystrokes)}")
        print(f"Timestamps recorded: {len(self.metrics_calculator.timestamps)}")
        collected_text = self.get_collected_text()
        print(f"Collected text length: {len(collected_text)}")

        # Check if there's enough data
        if len(self.metrics_calculator.keystrokes) < 50 or len(self.metrics_calculator.timestamps) < 50:
            print("Insufficient data to calculate metrics.")
            return None

        if len(collected_text) < 50:  # Ensuring enough text for structure analysis
            print("Insufficient text for structure analysis.")
            return None

        # Compute basic and advanced metrics
        error_rate, backspace_usage, capital_letters = self.calculate_basic_metrics()
        flight_times_stats, dwell_times_stats, inter_key_latencies_stats = self.calculate_advanced_metrics()
        paragraph_count, sentence_count = self.metrics_calculator.structure_analysis(collected_text)
        bigram_frequencies = self.metrics_calculator.calculate_bigram_frequencies_excluding_shift()
        bigram_freq_sum = sum(bigram_frequencies.values())

        rhythm_variability = np.std(self.metrics_calculator.inter_key_latencies()) if self.metrics_calculator.inter_key_latencies() else 0
        cpm = self.metrics_calculator.calculate_characters_per_minute()
        wpm = self.metrics_calculator.calculate_typing_speed()  # Assuming this method exists


        # Compile the feature dictionary with explicit naming
        feature_dict = {
            'cpm': [cpm],
            'wpm': [wpm],
            'rhythm_variability': [rhythm_variability],
            'backspace_count': [backspace_usage],
            'capital_letters': [capital_letters],
            'error_rate': [error_rate],
            'sentence_count': [sentence_count],
            'paragraph_count': [paragraph_count],
            'dwell_time_mean': [dwell_times_stats[0]],
            'dwell_time_std': [dwell_times_stats[1]],
            'dwell_time_median': [dwell_times_stats[2]],
            'flight_time_mean': [flight_times_stats[0]],
            'flight_time_std': [flight_times_stats[1]],
            'flight_time_median': [flight_times_stats[2]],
            'inter_key_latency_mean': [inter_key_latencies_stats[0]],
            'inter_key_latency_std': [inter_key_latencies_stats[1]],
            'inter_key_latency_median': [inter_key_latencies_stats[2]],
            'bigram_freq_sum': [bigram_freq_sum],
        }

        # Convert the feature dictionary to a pandas DataFrame
        features_df = pd.DataFrame.from_dict(feature_dict)

        # Optional: Handle possible NaNs in features
        features_df.fillna(0, inplace=True)
        
        # Before returning the preprocessed features
        #print(f"Prepared features for prediction:\n{features_df.describe()}")


        # Return the preprocessed features as a pandas DataFrame
        return features_df

    def calculate_basic_metrics(self):
        #typing_speed = self.metrics_calculator.calculate_typing_speed()
        error_rate = self.metrics_calculator.calculate_error_rate()
        backspace_usage = self.metrics_calculator.calculate_backspace_usage()
        capital_letters = self.metrics_calculator.capitalisation_pattern()
        return error_rate, backspace_usage, capital_letters

    def calculate_advanced_metrics(self):
        flight_times = self.metrics_calculator.flight_times
        dwell_times = self.metrics_calculator.dwell_times
        inter_key_latencies = self.metrics_calculator.inter_key_latencies()
        
        flight_times_stats = [np.mean(flight_times), np.std(flight_times), np.median(flight_times)]
        dwell_times_stats = [np.mean(dwell_times), np.std(dwell_times), np.median(dwell_times)]
        inter_key_latencies_stats = [np.mean(inter_key_latencies), np.std(inter_key_latencies), np.median(inter_key_latencies)]
        
        return flight_times_stats, dwell_times_stats, inter_key_latencies_stats









