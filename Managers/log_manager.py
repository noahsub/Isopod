from datetime import datetime
from subprocess import CompletedProcess
from typing import List

class LogManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.logs = []  # This will store all log entries
        return cls._instance

    def add_log(self, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.logs.append(f'{timestamp}: {message}')

    def get_logs(self) -> List[str]:
        return self.logs

    def clear_logs(self):
        self.logs.clear()

    def write_system_log(self, completed_process: CompletedProcess):
        if completed_process.returncode == 0:
            self.add_log(f"Command executed successfully: {completed_process.args}")
            self.add_log(f"Output: {completed_process.stdout}")
        else:
            self.add_log(f"Command failed with return code {completed_process.returncode}: {completed_process.args}")
            self.add_log(f"Error output: {completed_process.stderr}")
