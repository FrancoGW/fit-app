import hashlib

def hash_password(password):
    """Crea un hash seguro de la contraseña con salt."""
    salt = "fitapp2025"  # Este salt debería ser único por usuario en un sistema real
    salted = password + salt
    return hashlib.sha256(salted.encode()).hexdigest()


def verify_password(input_password, stored_password):
    """Verifica si la contraseña ingresada coincide con la almacenada."""
    salt = "fitapp2025"  # Debe ser el mismo salt usado para crear el hash
    input_hash = hashlib.sha256((input_password + salt).encode()).hexdigest()
    return input_hash == stored_password