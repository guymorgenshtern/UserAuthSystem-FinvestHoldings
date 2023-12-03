class User:
    def __init__(self, username, role, attributes) -> None:
        self.username = username
        self.role = role
        self.attributes = {"role": role}
        self.attributes.update(attributes)

