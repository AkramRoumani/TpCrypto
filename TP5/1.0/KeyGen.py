import hashlib
import random
import time

# 2-- Standard

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


# Exemple d'usage
a = 119
b = 544
gcd, u, v = euclide_etendu(a, b)

print(f"L'équation: {gcd} = {a}*{u} + {b}*{v}")
print(a*u + v*b)

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

# Encrypt and Decrypt

def encrypt(message, public_key):
    e, n = public_key
    "Chiffrer le message en l'élevant à la puissance de e et en prenant le modulo n."
    cipher_text = pow(message, e, n)
    return cipher_text

def decrypt(cipher_text, private_key):
    d, n = private_key
    "Decrypter le texte chiffré en l'élevant à la puissance de d et en prenant le modulo n."
    decrypted_message = pow(cipher_text, d, n)
    return decrypted_message

# Résultats :

"Clés RSA"
public_key, private_key = generer_cles_RSA(bit_length=2048) 

"Exemple de message"
message = 123

"Crypter le message"
cipher_text = encrypt(message, public_key)
print("Crypté:", cipher_text)

"Décrypter le message"
decrypted_message = decrypt(cipher_text, private_key)
print("Decrypted:", decrypted_message)

"Vérifier le décryptage"
if message == decrypted_message:
    print("Le message décrypté correspond à l'original.")
else:
    print("Le message décrypté ne correspond pas à l'original.")


# 3-- Problèmes d'implémentation :

# Timming attacks :

def exponentiation_cte(m, x, n):
    """
    

    Args:
    m (int): Base 
    x (int): Exposant
    n (int): Modulo

    Returns:
    int: Resultat de (m^x) % n.
    """
    r = 1
    tmp = m

    "Pour avoir le nombre de bits"
    k = x.bit_length()

    for i in range(k - 1, -1, -1):
        bit = (x >> i) & 1
        if bit == 1:
            r = (r * r) % n
            r = (r * m) % n
        else:
            r = (r * r) % n
            tmp = (r * m) % n  
            "La ligne d'avant n'est utilisée que pour garder un temps constant pour chaque itération de chaque boucle."
    return r

print("Exemple de calcul :",exponentiation_cte(234,32,12))

# OAEP :

def hash_function(input_bytes, hash_name='sha256'):
    """
    Calcul de hachage en utilisant hashlib avec le nom du hash spécifié.
    """
    hasher = hashlib.new(hash_name)
    hasher.update(input_bytes)
    return hasher.digest()

def OAEP_padding(message, n, G, H, k0, k1):
    """
    Applique le padding OAEP à un message avant le chiffrement RSA.
    
    Args:
    message (bytes): Le message original à chiffrer.
    n (int): Le module RSA.
    G (function): Une fonction de hachage utilisée pour le masquage.
    H (function): Une fonction de hachage utilisée pour générer le masque.
    k0 (int): Longueur du nombre aléatoire en octets.
    k1 (int): Longueur du padding supplémentaire en octets.
    
    Returns:
    bytes: Le message paddé.
    """
    max_message_length = n - k0 - k1 - 1

    # Étape 1 : Vérification de la longueur du message
    if len(message) > n - k0 - k1 - 1:
        raise ValueError("Le message est trop long")
    
    # Ajout d'un délimiteur
    message += b'\x01'

    # Étape 2 : Génération du nombre aléatoire
    r = random.getrandbits(k0 * 8).to_bytes(k0, byteorder='big')
    
    # Étape 3 : Création de la chaîne de padding de zéros
    padding_length = max_message_length - len(message)
    message += b'\x00' * padding_length
    
    # Étape 5 : Application de la fonction de hachage G au nombre aléatoire
    G_r = G(r)
    
    # Étape 6 : XOR de G(r) avec X
    X_masked = bytes([x ^ y for (x, y) in zip(message, G_r)])
    
    # Étape 7 : Application de la fonction de hachage H à X_maské
    H_X_masked = H(X_masked)
    
    # Étape 8 : XOR de H(X_maské) avec r
    r_masked = bytes([x ^ y for (x, y) in zip(r, H_X_masked)])

    padded_message = X_masked + r_masked  
    print("Longueur du message après padding :", len(padded_message))
    
    # Étape 9 : Concaténation des parties masquées
    return padded_message

# Fonctions de hachage G et H en utilisant SHA-3
def G(input_bytes):
    hasher = hashlib.sha256()
    hasher.update(input_bytes)
    return hasher.digest()[:len(input_bytes)]
def H(input_bytes):
    hasher = hashlib.sha256()
    hasher.update(input_bytes)
    return hasher.digest()[:len(input_bytes)]

message = b"Ceci est un message de test"
n = 256  
k0 = 32  
k1 = 32  

padded_message = OAEP_padding(message, n, G, H, k0, k1)
print("Message paddé :", padded_message)

def OAEP_unpadding(padded_message, n, G, H, k0, k1):
    """
    Retire le padding OAEP d'un message pour récupérer le message original.

    Args:
    padded_message (bytes): Le message chiffré et paddé.
    n (int): Le module RSA.
    G (function): Une fonction de hachage utilisée pour le masquage.
    H (function): Une fonction de hachage utilisée pour générer le masque.
    k0 (int): Longueur de la graine aléatoire en octets.
    k1 (int): Longueur du padding supplémentaire en octets.

    Returns:
    bytes: Le message original, avant l'application du padding.
    """
    

    # Séparation des parties masquées
    X_masked = padded_message[:-(k0)]
    r_masked = padded_message[-(k0):]

    # Récupération de H(X_masked)
    H_X_masked = H(X_masked)

    # Décodage de r
    r = bytes([x ^ y for (x, y) in zip(r_masked, H_X_masked)])

    # Récupération de G(r)
    G_r = G(r)

    # Décodage de X
    X = bytes([x ^ y for (x, y) in zip(X_masked, G_r)])

    # Suppression du padding de zéros et du délimiteur 0x01
   
    message = X[:-1].rstrip(b'\x00')
    return message

# Utilisation d'exemple pour démonstration
print(len(padded_message))
message_original = OAEP_unpadding(padded_message, n, G, H, k0, k1)
print("Message original retrouvé :", message_original)
