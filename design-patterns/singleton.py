## singleton Design Pattern ##

class ControlTower:
    def __init__(self):
        print("Initializing Control Tower!")
        
tower1 = ControlTower()
tower2 = ControlTower()

print(tower1 is tower2)

class SingletonControlTower:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None: ## Check if an instance already exists
            cls._instance = super().__new__(cls)
            print("Initializing singleton Control Tower!")
        return cls._instance
        
tower1 = SingletonControlTower()
tower2 = SingletonControlTower()

print(tower1 is tower2)

## eg db reading everytime we should not be creating a new connection
## same goes to logging, we don't need a new files for everytime