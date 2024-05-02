import tkinter as tk
from tkinter import messagebox
import logging
from datetime import datetime

class ErrorHandler:
    def __init__(self, log_file='default_log_file.log'):
        self.log_file = log_file
        # Configure logging
        logging.basicConfig(filename=self.log_file, level=logging.ERROR, 
                            format='%(asctime)s:%(levelname)s:%(message)s')
        # Initialize a hidden root Tkinter window
        self.root = tk.Tk()
        self.root.withdraw()

    def log_error(self, error, context_info=None):
        # Log the error with context info if provided
        if context_info:
            logging.error(f'{error} - Context: {context_info}')
        else:
            logging.error(f'{error}')

    def handle_error(self, error, user_message='An error occurred, please try again.'):
        # Handle the error and provide feedback to the user
        self.log_error(error)
        # Display the user_message to the user using a dialog in a GUI
        self.show_error_dialog(user_message)

    # Optional: Method to display errors to the user in a GUI
    def show_error_dialog(self, user_message):

        # Display an error dialog to the user
        messagebox.showerror("Error", user_message)