import secrets
class SecureStorage:

    def __init__(self):
        self._temporary_storage = {}

    def store_secret(self, key, info):
        # Use secrets.token_hex to generate a secure token
        secure_token = secrets.token_hex(16)
        self._temporary_storage[key] = (info, secure_token)
        return secure_token

    def retrieve_secret(self, key, token):
        # Check if the key exists in the temporary storage
        if key in self._temporary_storage:
            stored_password, secure_token = self._temporary_storage[key]

            # Check if the entered token matches the stored secure token
            if secure_token == token:
                return stored_password

        return None
    