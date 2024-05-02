import tkinter as tk
from tkinter import messagebox

class UserInterface:
    def __init__(self, session_manager, auth_manager, error_handler, data_collector, update_user_session):
        self.session_manager = session_manager
        self.auth_manager = auth_manager
        self.error_handler = error_handler
        self.data_collector = data_collector
        self.root = tk.Tk()
        self.root.title('Keystroke Dynamics Authentication')
        self.update_user_session = update_user_session

        # Initialize UI components for sign-in/register, task selection, and typing
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)

        self.show_sign_in()

    def update_session_manager_and_data_collector(self, session_manager, data_collector):
        self.session_manager = session_manager
        self.data_collector = data_collector

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        # Use the AuthenticationManager to attempt registration
        success, message = self.auth_manager.register(username, password)
        
        if success:
            # Registration was successful
            messagebox.showinfo("Registration Success", message)
            # Optionally redirect the user to the sign-in page or another appropriate UI state
            self.show_sign_in()
        else:
            # Registration failed
            messagebox.showerror("Registration Failed", message)


    def show_sign_in(self):
        # Clear the frame
        for widget in self.frame.winfo_children():
            widget.destroy()

        # Display sign-in form
        tk.Label(self.frame, text='Username:').grid(row=0, column=0)
        self.username_entry = tk.Entry(self.frame)
        self.username_entry.grid(row=0, column=1)

        tk.Label(self.frame, text='Password:').grid(row=1, column=0)
        self.password_entry = tk.Entry(self.frame, show='*')
        self.password_entry.grid(row=1, column=1)

        tk.Button(self.frame, text='Sign In', command=self.authenticate).grid(row=2, column=0, columnspan=2)
        tk.Button(self.frame, text='Register', command=self.show_register).grid(row=3, column=0, columnspan=2)

    def authenticate(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        success, message_or_user_id = self.auth_manager.sign_in(username, password)
        if success:
            #user_id = message_or_user_id  # Assuming message_or_user_id contains the user ID
            self.update_user_session(message_or_user_id)  # This will initialize SessionManager and DataCollector
            self.show_task_selection()  # Now it's safe to proceed to task selection
        else:
            messagebox.showerror("Authentication failed", message_or_user_id)  # Display error message


    def show_register(self):
        # Clear the frame
        for widget in self.frame.winfo_children():
            widget.destroy()

        # Display registration form
        tk.Label(self.frame, text='Username:').grid(row=0, column=0)
        self.username_entry = tk.Entry(self.frame)
        self.username_entry.grid(row=0, column=1)

        tk.Label(self.frame, text='Password:').grid(row=1, column=0)
        self.password_entry = tk.Entry(self.frame, show='*')
        self.password_entry.grid(row=1, column=1)

        tk.Button(self.frame, text='Register', command=self.register).grid(row=2, column=0, columnspan=2)

    def authenticate(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        success, message_or_user_id = self.auth_manager.sign_in(username, password)
        if success:
            # Call the update_user_session method of MainApp to initialize the session manager
            self.update_user_session(message_or_user_id)  # Assuming the sign-in method returns the user ID on success
            self.show_task_selection()  # Proceed to show the task selection UI
        else:
            messagebox.showerror("Authentication failed", message_or_user_id)



    def show_task_selection(self):
            # Clear the frame
            for widget in self.frame.winfo_children():
                widget.destroy()

            # Display task selection options
            tk.Label(self.frame, text='Select a task:').grid(row=0, column=0)

            tasks = ["Free Typing", "Fixed Text", "Custom Text"]  # tasks
            for i, task in enumerate(tasks):
                tk.Button(self.frame, text=task, command=lambda t=task: self.handle_task_selection(t)).grid(row=i+1, column=0)
   
    def handle_task_selection(self, task):
            self.task_manager.set_task(task)  # Set the current task
            # Start the session for the selected task
            self.session_manager.start_session(task)
            
            # Show the typing interface
            self.show_typing_interface()

    def start_session(self, task):
        # Use session_manager to start a new session with the selected task
        self.session_manager.start_session(task)
        # Potentially update the UI to the typing interface


    def run(self):
        # Start the Tkinter event loop
        self.root.mainloop()

    def show_error(self, message):
        messagebox.showerror("Error", message)

    def handle_task_selection(self, task):
        # Start the session for the selected task
        self.session_manager.start_session(task)
        
        # Show the typing interface
        self.show_typing_interface()
        

    def show_typing_interface(self):
            # Clear the current interface
            for widget in self.frame.winfo_children():
                widget.destroy()

            # Set up the typing interface
            self.text_input = tk.Text(self.frame, height=10, width=50)
            self.text_input.pack()

             # Pause buttons
            self.pause_button = tk.Button(self.frame, text="Pause", command=self.pause_session)
            self.pause_button.pack(side=tk.LEFT, padx=(10, 10))

             # "Resume" button 
            self.resume_button = tk.Button(self.frame, text="Resume Session", command=self.resume_session)
            self.resume_button.pack(side=tk.LEFT)  # Adjust the position as needed

            self.end_button = tk.Button(self.frame, text="End", command=self.end_session)
            self.end_button.pack(side=tk.RIGHT, padx=(10, 10))

            # Bind key events for capturing keystrokes
            self.text_input.bind("<KeyPress>", self.data_collector.on_key_press)
            self.text_input.bind("<KeyRelease>", self.data_collector.on_key_release)

            # Set focus to the text input widget
            self.text_input.focus_set()

    def pause_session(self):
            # Call the pause_session method of your session_manager
            self.session_manager.pause_session()
            # Disable the pause button and enable the resume button
            self.pause_button.config(state=tk.DISABLED)
            self.resume_button.config(state=tk.NORMAL)

    def resume_session(self):
            # Call the method in SessionManager to resume the session
            self.session_manager.resume_session()
           # Enable the pause button and disable the resume button
            self.pause_button.config(state=tk.NORMAL)
            self.resume_button.config(state=tk.DISABLED)

    def end_session(self):
        # Call the end_session method of your session_manager
        self.session_manager.end_session()
        # Optionally, you could also switch back to the task selection screen or close the application
        self.show_task_selection()


# Assuming you have session_manager and auth_manager already created
# ui = UserInterface(session_manager, auth_manager)
# ui.run()
