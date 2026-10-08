import json
import os

class ProjectMemory:
    def __init__(self, file_path=r"C:\Kaoruko AI\memory.json"):
        self.file_path = file_path
        self.projects = {}

        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                data = json.load(file)
            self.projects = data
