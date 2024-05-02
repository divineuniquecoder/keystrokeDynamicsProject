import numpy as np
import traceback


class MetricsCalculator:
    def __init__(self):
        self.keystrokes = []
        self.timestamps = []
        self.corrections = 0  # Add this to track corrections
        self.total_characters = 0  # Add this to track total characters typed
        self.reset_metrics()
        self.dwell_times = []
        self.flight_times = []

    def log_keystroke(self, key, timestamp):

        # Log keystroke and timestamp
        self.keystrokes.append((key, timestamp))
        self.timestamps.append(timestamp)
       # print(f"Keystroke: {key}, Timestamp: {timestamp}")
            # Check if the keystroke is a correction
        if key in ["BackSpace", "Delete"]:
            self.corrections += 1
        else:
            self.total_characters += 1

    def calculate_typing_speed(self):
        # Check if there's enough data to calculate typing speed
        if len(self.keystrokes) > 0 and len(self.timestamps) >= 2:
            # Assume a word is 5 characters on average
            characters = len(self.keystrokes)
            time_elapsed = self.timestamps[-1] - self.timestamps[0]
            words = characters / 5
            minutes = time_elapsed / 60
            wpm = words / minutes if minutes > 0 else 0
            return wpm
        else:
            # Return a default value or NaN if there isn't enough data
            return float('nan')  # Or 0, or another placeholder that makes
        
        
    def calculate_error_rate(self):
        #print(f"Corrections: {self.corrections}")
        #print(f"Total Characters: {self.total_characters}")
        # Use internal data to calculate the error rate
        effective_characters = self.total_characters - self.corrections
        #print(f"Effective Characters: {effective_characters}")
        error_rate = self.corrections / effective_characters if effective_characters > 0 else 0
        #print(f"Error Rate: {error_rate}")
        return error_rate

    def log_dwell_time(self, dwell_time):
        #print(f"Logging dwell time: {dwell_time}")  # Debug print
        # This method is called from on_key_release to log each dwell time
        self.dwell_times.append(dwell_time)
        #print(f"MetricsCalculator ID at logging dwell time: {id(self)}")
        #print(f"After Logging, Dwell Times: {self.dwell_times}")  # Immediate check

    def log_flight_time(self, flight_time):
        #print(f"Logging flight time: {flight_time}")  # Debug print
        # This method is called from on_key_press to log each flight time
        #print("Logging flight time:", flight_time)
        #traceback.print_stack()
        self.flight_times.append(flight_time)
        #print(f"MetricsCalculator ID at logging flight time: {id(self)}")
        #print(f"After Logging, Flight Times: {self.flight_times}")  # Immediate check

    def calculate_key_patterns(self):
        # Analyze patterns like the use of SHIFT, CAPS LOCK, etc.
        shift_uses = self.keystrokes.count('Shift')
        caps_lock_uses = self.keystrokes.count('CapsLock')
        return shift_uses, caps_lock_uses

    def reset_metrics(self):
        # Reset the metrics for a new session
        self.keystrokes = []
        self.timestamps = []
        self.corrections = 0
        self.total_characters = 0
    
    def inter_key_latencies(self):
        # Calculate inter-key latency, ensuring no negative values
        inter_key_latencies = [max(0, t2 - t1) for t1, t2 in zip(self.timestamps[:-1], self.timestamps[1:])]
        return inter_key_latencies


    def calculate_typing_rhythm_variability(self):
        # Calculate the standard deviation of the inter-key latencies
        inter_key_latencies = self.inter_key_latencies()
        rhythm_variability = np.std(inter_key_latencies) if inter_key_latencies else 0
        return rhythm_variability


    def update_keystrokes(self, keystrokes_sequence):
        # Update the internal list of keystrokes with the enhanced data from DataCollector
        self.keystrokes.extend(keystrokes_sequence)

    def calculate_bigram_frequencies_excluding_shift(self):
        # Initialize an empty dictionary to store bigram frequencies.
        bigram_freq = {}

        # Extract just the keystroke characters, ignoring non-string types, 'BackSpace', and 'Shift' keys.
        keystroke_chars = [keystroke[0] for keystroke in self.keystrokes if isinstance(keystroke[0], str) and keystroke[0] not in ['BackSpace', 'Shift']]

        # Iterate through the keystrokes, forming bigrams and updating their counts.
        for i in range(len(keystroke_chars) - 1):
            # Form a bigram from the current and next keystroke character.
            bigram = keystroke_chars[i] + keystroke_chars[i + 1]
            
            # Update the count of the bigram in the dictionary if the bigram is purely alphabetic.
            if bigram.isalpha():
                bigram_freq[bigram] = bigram_freq.get(bigram, 0) + 1

        # Return the dictionary containing bigram frequencies.
        return bigram_freq


    def calculate_shift_key_usage(self):
        # Count occurrences of 'Shift_L' and 'Shift_R' in the keystrokes to calculate shift key usage
        shift_key_usage = sum(1 for key, _ in self.keystrokes if key in ('Shift_L', 'Shift_R'))
        return shift_key_usage

    def calculate_backspace_usage(self):
        # Initialize backspace count
        backspace_count = 0
        
        # For debugging purposes, keep track of timestamps
        backspace_timestamps = []

        # Iterate over the keystrokes and count 'BackSpace' occurrences
        for key, timestamp in self.keystrokes:
            if key == 'BackSpace':
                backspace_count += 1
                backspace_timestamps.append(timestamp)

        # Debugging output
        print(f"BackSpace timestamps: {backspace_timestamps}")
        print(f"Total BackSpace count: {backspace_count}")
        return backspace_count

    
    def calculate_characters_per_minute(self):
        # Ensure there are at least two timestamps to calculate the time difference
        if len(self.timestamps) < 2:
            print("Insufficient data to calculate characters per minute.")
            return 0  # Or return None, depending on how you want to handle this case

        # If check passes, proceed with the original calculation
        characters = len(self.keystrokes)
        time_elapsed = self.timestamps[-1] - self.timestamps[0]  # Now safe to access
        minutes = time_elapsed / 60
        cpm = characters / minutes if minutes > 0 else 0
        return cpm

    def capitalisation_pattern(self):
        # Extract only the keystrokes from the tuples in self.keystrokes
        keystrokes_only = [key for key, _ in self.keystrokes]
        
        # Calculate capital letters and shift key usage
        capital_letters = sum(1 for key in keystrokes_only if key.isupper())
    
        
        return capital_letters

    def punctuation_metrics(self, text_data):
        # Assuming `text_data` is a string from which you're counting punctuation.
        punctuation_marks = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
        punctuation_count = {mark: 0 for mark in punctuation_marks}
        
        for char in text_data:
            if char in punctuation_marks:
                punctuation_count[char] += 1
        
        # Filter out punctuation marks that do not appear in the text
        punctuation_count = {mark: count for mark, count in punctuation_count.items() if count > 0}

        return punctuation_count


    
    def structure_analysis(self, text):
        # Structure Metrics (Text structure Analysis)
        paragraph_count = text.count('\n') + 1  # Assuming new paragraphs are separated by newline character
        sentence_count = text.count('.') + text.count('!') + text.count('?')  # Add other sentence terminators if needed
        return paragraph_count, sentence_count

