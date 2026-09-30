class SecurityAlert:
    def __init__(self, title, message, severity="medium"):
        self.title = title
        self.message = message
        self.severity = severity