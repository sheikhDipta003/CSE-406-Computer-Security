import secrets

iv = list(secrets.token_bytes(16))

print(iv)