class SecurityEvent:
    def __init__(self, event_type, description, severity="low"):
        self.event_type = event_type
        self.description = description
        self.severity = severity