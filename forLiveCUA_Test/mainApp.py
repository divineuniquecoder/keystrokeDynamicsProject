# Import your custom classes
from userInterface import UserInterface
from sessionManager import SessionManager
from authenticationManager import AuthenticationManager
from dataBase import DataBase
from dataCollector import DataCollector
from metricsCalculation import MetricsCalculator
from errorHandler import ErrorHandler
from configManager import ConfigManager
from taskManager import TaskManager
from joblib import load  # Used to load the pre-trained model


if __name__ == '__main__':

    # Instantiate ConfigManager
    config_manager = ConfigManager()

    class MainApp:
        def __init__(self, config_manager, metrics_calculator=None):
            self.config_manager = config_manager
            credentials_path = self.config_manager.get_setting('firebaseCredentialsPath')
            self.database_handler = DataBase(credentials_path)
            self.auth_manager = AuthenticationManager(self.database_handler)
            self.error_handler = ErrorHandler()
            self.task_manager = TaskManager()
            # Use provided metrics_calculator or create a new one if None is provided
            self.metrics_calculator = metrics_calculator if metrics_calculator else MetricsCalculator()

            # Initially, user_id is None until a user successfully logs in
            self.user_id = None

            # Initialization of DataCollector and SessionManager is deferred to after user login
            self.data_collector = None
            self.session_manager = None
            self.ui = None
            self.initialize_ui()

        def initialize_ui(self):
            # Initialize UserInterface without DataCollector and SessionManager
            # These will be set later, after successful login
            self.ui = UserInterface(self.session_manager, self.auth_manager, self.error_handler, self.data_collector, self.update_user_session)

        def update_user_session(self, user_id):

            pipeline = load("svm11.pkl")
            # This method is called after successful login to update user_id, DataCollector, and SessionManager
            self.user_id = user_id
            self.data_collector = DataCollector(self.metrics_calculator, self.ui, self.task_manager, self.config_manager.get_setting('firebaseCredentialsPath'), pipeline)
            self.session_manager = SessionManager(self.data_collector, self.database_handler, self.task_manager, self.user_id)
            

            # Set the UserInterface in DataCollector
            self.data_collector.set_user_interface(self.ui)

            # Update UserInterface with the newly created SessionManager and DataCollector
            self.ui.update_session_manager_and_data_collector(self.session_manager, self.data_collector)

        def run(self):
            # Start the application by running the user interface
            self.ui.run()

        def handle_user_sign_in(self, username, password):
            # Use auth_manager to handle sign in
            success, message = self.auth_manager.sign_in(username, password)
            if success:
                self.ui.show_task_selection()
            else:
                self.ui.show_error(message)

        def handle_user_register(self, username, password):
            # Use auth_manager to handle registration
            success, message = self.auth_manager.register(username, password)
            if success:
                self.ui.show_task_selection()
            else:
                self.ui.show_error(message)

        def start_session(self, task_type):
            # Use session_manager to start a new session with the specified task type
            self.session_manager.start_session(task_type)

        def pause_session(self):
            # Use session_manager to pause the current session
            self.session_manager.pause_session()

        def resume_session(self):
            # Use session_manager to resume the session
            self.session_manager.resume_session()

       

    # Instantiate and run MainApp
    app = MainApp(config_manager)
    app.run()