import time

# Paramètres pour l'échange de clés Diffie-Hellman
p = 415167219750333579635445231409720715892493028342172336866540737203845400079931  # Nombre premier grand
g = 2  # Base pour le logarithme, généralement une petite constante

# Exposants choisis par Alice et Bob
a = 2  # Exposant simple pour Alice
b = 403498691310681121399439373609808651688837448891420032479  # Exposant complexe pour Bob

def measure_exponentiation(base, exponent, modulus, repetitions=10):
    """
    Mesure le temps d'exécution de l'exponentiation modulaire pour une base, un exposant et un modulo donnés.

    Args:
    base (int): La base de l'exponentiation.
    exponent (int): L'exposant utilisé dans l'exponentiation.
    modulus (int): Le modulo pour l'opération modulaire.

    Returns:
    float: Le temps total pris pour les répétitions spécifiées.
    """
    start_time = time.time()
    for _ in range(repetitions):
        pow(base, exponent, modulus)
    end_time = time.time()
    return end_time - start_time

# Mesurer et afficher le temps pour les exposants a et b
time_a = measure_exponentiation(g, a, p)
time_b = measure_exponentiation(g, b, p)
print(f"Temps d'execution pour g^a mod p (a petit): {time_a:.6f} secondes")
print(f"Temps d'execution pour g^b mod p (b grand): {time_b:.6f} secondes")

def verify_keys(g, p, a, b):
    """
    Vérifie que les clés générées par Alice et Bob sont équivalentes après un échange Diffie-Hellman.

    Args:
    g (int): La base utilisée dans l'échange.
    p (int): Le nombre premier utilisé comme module.
    a (int): L'exposant secret d'Alice.
    b (int): L'exposant secret de Bob.

    Returns:
    bool: True si les clés calculées par Alice et Bob sont identiques, False autrement.
    """
    A = pow(g, a, p)
    B = pow(g, b, p)
    K = pow(B, a, p)
    L = pow(A, b, p)
    return K == L

keys_match = verify_keys(g, p, a, b)
print(f"Verification que K = L: {'Succes' if keys_match else 'Echec'}")
