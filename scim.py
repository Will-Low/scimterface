class NotImplemented(Exception):
    def __init__(self, method, endpoint):
        self.method = method
        self.endpoint = endpoint
    def __str__(self):
        return f"The {self.method} method is not implemented for {self.endpoint}"