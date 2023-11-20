import secrets

# Gerar uma chave secreta para a aplicação
secret_key = secrets.token_hex(16)  # Isso criará uma chave hexadecimal de 16 bytes
print(secret_key)