class TaskManager:
    def __init__(self):
        self.current_task = None

    def set_task(self, task_type):
        # Set the current task type (transcription, copy_text, free_typing)
        self.current_task = task_type

    def get_current_task(self):
        # Get the current task type
        return self.current_task
