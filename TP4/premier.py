import random
import time

def fermat_test(n, a):
    """
    Effectue le test de primalité de Fermat sur un nombre n en utilisant la base a.
    Le test exploite le petit théorème de Fermat qui indique que si n est un nombre premier,
    alors pour tout a (1 < a < n-1), a^(n-1) % n devrait être 1.
    
    Args:
    n (int): Le nombre à tester pour la primalité.
    a (int): La base avec laquelle tester le nombre.

    Returns:
    bool: True si le test passe (n peut être premier), False si le test échoue (n est composé).
    """
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    return pow(a, n - 1, n) == 1

def is_prime(n, k=5):
    """
    Vérifie si un nombre n est premier en utilisant le test de primalité de Fermat avec k bases aléatoires.
    Augmenter k augmente la précision du test.

    Args:
    n (int): Le nombre à tester pour la primalité.
    k (int): Le nombre de bases différentes à utiliser pour le test.

    Returns:
    bool: True si n est probablement premier, False autrement.
    """
    if n <= 1:
        return False
    for _ in range(k):
        a = random.randint(2, n - 2)
        if not fermat_test(n, a):
            return False
    return True

def generate_prime(bit_length):
    """
    Génère un nombre premier d'une taille spécifiée en bits en utilisant la méthode de rejet.
    Ce processus génère des nombres aléatoires jusqu'à ce qu'un soit trouvé qui passe le test de primalité.

    Args:
    bit_length (int): La taille en bits du nombre premier à générer.

    Returns:
    int: Un nombre premier de la taille spécifiée.
    """
    start_time = time.time()
    while True:
        candidate = random.getrandbits(bit_length)
        if is_prime(candidate):
            end_time = time.time()
            print(f"Time to generate a {bit_length}-bit prime: {end_time - start_time:.2f} seconds")
            return candidate

# Tester la génération de nombre premier
bit_sizes = [3072, 4096, 6144, 8192]
for bits in bit_sizes:
    print(f"Generating a {bits}-bit prime...")
    prime = generate_prime(bits)
    print(f"Generated prime (first 50 digits): {str(prime)[:50]}")
