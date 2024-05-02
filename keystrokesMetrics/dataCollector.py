import time
from dataBase import DataBase  # Import the DataBase class from your module
import tkinter as tk


class DataCollector:
    def __init__(self, metrics_calculator, ui, task_manager, credentials_path):
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

    def on_key_press(self, event):
        if not self.is_collecting:
            return
        current_time = time.time()
        # Check if the event is within the debounce threshold
        if (current_time - self.last_processed_key_time) < self.debounce_threshold:
            return  # Skip this event if it's too close to the last one
        
        self.last_processed_key_time = current_time  # Update the last processed time

        key = self.resolve_key(event)
        press_time = current_time  # Use the current time as press time

        if self.last_release_time is not None:
            flight_time = press_time - self.last_release_time
            print(f"Logged flight time: {flight_time}")  # Debug print
            self.metrics_calculator.log_flight_time(flight_time)

        if key not in self.key_press_times:  # Avoid duplicating entries for long presses
            self.key_press_times[key] = press_time

        # Log the key press in the sequence with its type (press) and timestamp
        self.keystrokes_sequence.append(('press', key, press_time))

    def on_key_release(self, event):
        if not self.is_collecting:
            return
        key = self.resolve_key(event)
        release_time = time.time()
        press_time = self.key_press_times.pop(key, None)
        if press_time:  # Calculate dwell time and log the keystroke
            dwell_time = release_time - press_time
            print(f"Logged dwell time: {dwell_time}")  # Debug print

            self.keystroke_timings.append((key, press_time, release_time, dwell_time))
            # Pass the dwell time and key to the metrics calculator for any immediate calculations
            self.metrics_calculator.log_dwell_time(dwell_time)
            print(f"MetricsCalculator ID in DataCollector: {id(self.metrics_calculator)}")
            #self.metrics_calculator.calculate_dwell_time(key, dwell_time)
        # Log the key release in the sequence with its type (release) and timestamp
        self.keystrokes_sequence.append(('release', key, release_time))
        self.last_release_time = release_time
        # Handle special keys if necessary
        #if key in ('Shift_L', 'Shift_R', 'Ctrl_L', 'Ctrl_R', 'Alt_L', 'Alt_R'):
            #self.handle_special_key(key, release_time)
        self.periodically_update_metrics()
        
    def periodically_update_metrics(self):
        SOME_THRESHOLD = 10  # Example threshold, adjust based on your needs
        if len(self.keystrokes_sequence) >= SOME_THRESHOLD:
            self.metrics_calculator.update_keystrokes(self.keystrokes_sequence)
            # Clear the sequence after updating to avoid re-processing the same keystrokes
            self.keystrokes_sequence.clear()


    def resolve_key(self, event):
        # Handle special keys explicitly; this might need adjustments based on observed event behavior
        if event.keysym in ('BackSpace', 'Shift_L', 'Shift_R'):
            return event.keysym
        return event.char  # Use the character for regular keys

            
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


    def get_collected_text(self):
        # Retrieve the text from the Tkinter Text widget
        return self.ui.text_input.get("1.0", tk.END)
    


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
