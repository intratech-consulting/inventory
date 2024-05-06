class HealthManager:
    def __init__(self):
        self.health = True  # Initial health state is True
        
    def set_health(self, new_health):
        self.health = new_health  # Update the health state

    def get_health(self):
        return self.health  # Get the current health state