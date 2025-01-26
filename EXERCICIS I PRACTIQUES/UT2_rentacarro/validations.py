from datetime import datetime
import re

# Lista de palabras ofensivas
OFFENSIVE_WORDS = ['caca', 'pedo', 'culo', 'pis', 'java', 'php']

def validate_form(data):
    """
    Valida los datos del formulario.
    :param data: Diccionario con los datos enviados desde el formulario.
    :return: Lista de errores (vacía si no hay errores).
    """
    errors = []

    # Username
    username = data.get('username', '').strip()
    if len(username) < 6 or len(username) > 15:
        errors.append("El username debe tener entre 6 y 15 caracteres.")
    if any(word in username.lower() for word in OFFENSIVE_WORDS):
        errors.append("El username contiene palabras no permitidas.")

    # Nombre y apellidos
    nom = data.get('nom', '').strip()
    llinatges = data.get('llinatges', '').strip()
    if len(nom) > 50:
        errors.append("El campo 'Nom' no puede exceder 50 caracteres.")
    if len(llinatges) > 50:
        errors.append("El campo 'Llinatges' no puede exceder 50 caracteres.")

    # Contraseña
    password = data.get('password', '')
    password_repeat = data.get('password_repeat', '')
    if not validate_password(password):
        errors.append("La contraseña debe tener al menos 8 caracteres, incluir una mayúscula, una minúscula, un número y un carácter especial.")
    if password != password_repeat:
        errors.append("Las contraseñas no coinciden.")

    # Email
    email = data.get('email', '').strip()
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        errors.append("El correo electrónico no es válido.")

    # Teléfono
    telefon = data.get('telefon', '').replace(' ', '')
    if not re.match(r'^[0-9+]+$', telefon):
        errors.append("El número de teléfono contiene caracteres no válidos.")

    return errors

def validate_password(password):
    """
    Valida que la contraseña cumpla con los requisitos.
    :param password: Contraseña a validar.
    :return: True si es válida, False si no lo es.
    """
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):  # Al menos una mayúscula
        return False
    if not re.search(r'[a-z]', password):  # Al menos una minúscula
        return False
    if not re.search(r'[0-9]', password):  # Al menos un número
        return False
    if not re.search(r'[^A-Za-z0-9]', password):  # Al menos un carácter especial
        return False
    return True
