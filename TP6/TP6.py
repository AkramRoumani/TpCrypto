import hashlib
import random
import time
import os
# PARTIE 1

def fermat_test(n, a):
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    return pow(a, n - 1, n) == 1

def is_prime(n, k=5):
    if n <= 1:
        return False
    for _ in range(k):
        a = random.randint(2, n - 2)
        if not fermat_test(n, a):
            return False
    return True

def generate_prime(bit_length):
    start_time = time.time()
    while True:
        candidate = random.getrandbits(bit_length)
        if is_prime(candidate):
            end_time = time.time()
            print(f"Temps pour générer un nombre premier de {bit_length} bit : {end_time - start_time:.2f} secondes")
            return candidate

def euclide_etendu(a, b):
    r, r_prime = a, b
    u, v, u_prime, v_prime = 1, 0, 0, 1
    
    while r_prime != 0:
        q = r // r_prime
        r, r_prime, u, u_prime, v, v_prime = (
            r_prime, r - q * r_prime,
            u_prime, u - q * u_prime,
            v_prime, v - q * v_prime
        )
    "r est le pgcd, u et v sont les coefficients"
    return r, u, v  


# Key Gen

def mod_inverse(e, phi):
    """
    Calcule l'inverse modulaire de e en utilisant la fonction euclide_etendu
    """
    gcd, u, v = euclide_etendu(e, phi)
    if gcd != 1:
        raise Exception("L'inverse modulaire n'existe pas")
    else:
        return u % phi

def generer_cles_RSA(bit_length=2048):
    "Générer deux nombres premier de même taille en bits"
    p = generate_prime(bit_length // 2)
    q = generate_prime(bit_length // 2)
    while p == q:
        q = generate_prime(bit_length // 2)

    "Calculer n et phi(n)"
    n = p * q
    phi_n = (p - 1) * (q - 1)

    "On choisit e=65537 car 65537>2^16 (équilibre entre performance et sécurité) et c'est un nombre premier"
    e = 65537
    while euclide_etendu(e, phi_n)[0] != 1:
        "On incrémente e par 2 jusqu'à avoir deux nombres premiers entre eux"
        e += 2  

    "On calcule d; l'inverse modulaire de e [phi(n)]"
    d = mod_inverse(e, phi_n)

    return (e, n), (d, n)

def exponentielle_modulaire(base, exp, mod):
    """
    exponentielle modulaire
    Args:
    base (int): base.
    exp (int): exposant.
    mod (int): modulo.

    Returns:
    int: (base^exp) % mod.
    """
    result = 1
    base = base % mod  
    while exp > 0:
        # si exp est impaire, multiplier le résultat par la base
        if (exp % 2) == 1:
            result = (result * base) % mod
        # décaler l'esposant par 1 et metter la base au carré
        exp = exp >> 1
        base = (base * base) % mod
    return result

def creer_signature(m, private_key):
    """
    Crée une signature RSA d'un meassage
    Args:
    m (int): le message à signer.
    private_key (tuple): Tuple (d, n) représente la clé privée

    Returns:
    int: La signature.
    """
    d, n = private_key
    # Use the custom modular exponentiation function to create the signature
    return exponentielle_modulaire(m, d, n)

def verifier_signature(m, sigma, public_key):
    """
    Vérifie la signature RSA
    Args:
    m (int): message.
    sigma (int): Signature à verifier.
    public_key (tuple): Tuple (e, n) representant la clé publique.

    Returns:
    bool: True si la signature est correctre, False sinon.
    """
    e, n = public_key

    message_calculated = exponentielle_modulaire(sigma, e, n)

    return message_calculated == m


#PARTIE 2
# print("Signature is valid:", is_valid) 

def crt(signature_p, signature_q, p, q):
    # coeffs de Bézout pour p et q
    _, u, v = euclide_etendu(p, q)
    # Calculer x en utilisant la formule : x = ((signature_q * p * u) + (signature_p * q * v)) % n
    n = p * q
    return (signature_q * p * u + signature_p * q * v) % n

def creer_signature_crt(m, private_key, p, q):
    d, n = private_key
    # Signatures modulo p et q
    sigma_p = exponentielle_modulaire(m, d % (p-1), p)
    sigma_q = exponentielle_modulaire(m, d % (q-1), q)
    # Combiner en utilisant crt
    return crt(sigma_p, sigma_q, p, q)

# Exemple d'usage
p, q = generate_prime(1024), generate_prime(1024)
n = p * q
e = 65537
_, u, v = euclide_etendu(e, (p-1)*(q-1))
d = u % ((p-1)*(q-1))
private_key = (d, n)
public_key = (e, n)



# PARTIE 3

def hash_message(message):
    """Hashes a message using SHA-256."""
    hasher = hashlib.sha256()
    hasher.update(message.encode('utf-8'))
    return hasher.digest()

def create_randomized_signature(m, private_key):
    """Creates a randomized RSA signature."""
    hash1 = hash_message(m)
    salt = os.urandom(16)  # Secure random salt of 16 bytes
    hasher = hashlib.sha256()
    hasher.update(hash1 + salt)
    hashed_value = hasher.digest()
    h = int.from_bytes(hashed_value, 'big')  # Convert bytes to integer
    return exponentielle_modulaire(h, private_key[0], private_key[1]), salt

def verify_randomized_signature(m, sigma, salt, public_key):
    """Verifies a randomized RSA signature."""
    hash1 = hash_message(m)
    hasher = hashlib.sha256()
    hasher.update(hash1 + salt)
    hashed_value = hasher.digest()
    h = int.from_bytes(hashed_value, 'big')
    calculated_h = exponentielle_modulaire(sigma, public_key[0], public_key[1])
    return h == calculated_h


public_key, private_key = generer_cles_RSA(bit_length=2048)

m = 123456789  # Message à signer
sigma = creer_signature(m, private_key)

is_valid = verifier_signature(m, sigma, public_key)
print("La signature est valide :", is_valid)

sigma_crt = creer_signature_crt(m, private_key, p, q)
is_valid_crt = verifier_signature(m, sigma_crt, public_key)
print("La signature CRT est valide :", is_valid_crt)

message = "Ceci est un message de test"
sigma_rand, salt = create_randomized_signature(message, private_key)
is_valid_rand = verify_randomized_signature(message, sigma_rand, salt, public_key)
print("La signature randomisée est valide :", is_valid_rand)


