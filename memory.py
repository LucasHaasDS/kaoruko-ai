import json

class MemoryManager:
    def __init__(self):
        try:
            with open("memory.json", "r") as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.data = {
                "user_name": "Lucas",
                "projects": [],
                "remembered_facts": []
            }
    
    def save_memory(self):
            with open("memory.json", "w") as file:
                json.dump(self.data, file, indent=4)


    def remember_fact(self, fact):
        self.data["remembered_facts"].append(fact)
        self.save_memory()
