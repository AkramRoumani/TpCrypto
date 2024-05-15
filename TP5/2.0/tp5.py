import random
import time
import os
import hashlib

def extended_euclid(a, b):
    """ Implémente l'algorithme d'Euclide étendu pour trouver le PGCD de a et b, ainsi que les coefficients u et v. """
    r, u, v, r_prime, u_prime, v_prime = a, 1, 0, b, 0, 1
    while r_prime != 0:
        q = r // r_prime
        r, u, v, r_prime, u_prime, v_prime = (
            r_prime, u_prime, v_prime, r - q * r_prime, u - q * u_prime, v - q * v_prime
        )
    return r, u, v

# Appelons la fonction avec les valeurs spécifiées
gcd, u, v = extended_euclid(360, 7)
print(f"PGCD: {gcd}, Coefficient u: {u}, Coefficient v: {v}")

def fermat_test(n, a):
    """ Test de primalité de Fermat pour vérifier si n est un nombre premier. """
    if n % 2 == 0:
        return False
    return pow(a, n - 1, n) == 1

def is_prime(n, k=5):
    """ Vérifie la primalité d'un nombre n en utilisant le test de Fermat k fois pour augmenter la précision. """
    if n <= 1:
        return False
    for _ in range(k):
        a = random.randint(2, n - 2)
        if not fermat_test(n, a):
            return False
    return True

def generate_prime(bit_length):
    """ Génère un nombre premier avec une taille spécifiée en bits. """
    while True:
        candidate = random.getrandbits(bit_length)
        if is_prime(candidate):
            return candidate

def generate_rsa_keys(bit_length=2048):
    """ Génère une paire de clés RSA en utilisant la méthode de génération de nombres premiers. """
    p = generate_prime(bit_length // 2)
    q = generate_prime(bit_length // 2)
    n = p * q
    phi_n = (p - 1) * (q - 1)
    e = 65537  # Valeur courante de e, généralement utilisée car c'est un premier avec beaucoup de petits facteurs de 2.
    gcd, _, _ = extended_euclid(e, phi_n)
    while gcd != 1:
        e = random.randint(2, phi_n - 1)
        gcd, _, _ = extended_euclid(e, phi_n)
    _, d, _ = extended_euclid(e, phi_n)
    d = d % phi_n
    return (e, n), (d,n)  # Clé publique (e, n), Clé privée (d, n)

# Génération des clés RSA
public_key, private_key = generate_rsa_keys()
print("Cle publique:", public_key)
print("Cle privee:", private_key)


def encrypt(message, public_key):
    """ Chiffre un message avec la clé publique.
    
    Args:
        message (int): Le message à chiffrer, représenté comme un entier.
        public_key (tuple): Un tuple (e, n) où e est l'exposant public et n le module RSA.

    Returns:
        int: Le message chiffré.
    """
    e, n = public_key
    return pow(message, e, n)

def decrypt(ciphertext, private_key):
    """ Déchiffre un message avec la clé privée.
    
    Args:
        ciphertext (int): Le message chiffré.
        private_key (tuple): Un tuple (d, n) où d est l'exposant privé et n le module RSA.

    Returns:
        int: Le message déchiffré.
    """
    d, n = private_key
    return pow(ciphertext, d, n)


original_message = 123456789  # Un message de test

# Chiffrement
encrypted_message = encrypt(original_message, public_key)
print(f"Encrypted: {encrypted_message}")

# Déchiffrement
decrypted_message = decrypt(encrypted_message, private_key)
print(f"Decrypted: {decrypted_message}")

# Vérification
assert original_message == decrypted_message, "Le message déchiffré ne correspond pas au message original."



def constant_time_mod_exp(x, m, n, k):
    """ Exponentiation modulaire en temps constant. """
    r = 1
    for i in range(k - 1, -1, -1):
        r = (r * r) % n
        if (x >> i) & 1:  # Si le bit i de x est 1
            r = (r * m) % n
    return r

# Valeurs pour le test
m = 3
x = 15
n = 23
k = x.bit_length()  # Calcul de la longueur en bits de x

# Appel de la fonction
result = constant_time_mod_exp(x, m, n, k)
print(f"Le resultat de {m}^{x} mod {n} est : {result}")


def keccak_padding(message, rate_bits):
    """ 
    Applique un padding au message pour s'assurer qu'il est un multiple de la taille du bloc (rate).
    Utilise différents schémas de padding en fonction du nombre d'octets nécessaires.
    """
    rate_bytes = rate_bits // 8
    message_len = len(message)
    q = rate_bytes - (message_len % rate_bytes)
    
    if q == 1:
        padding = b'\x86'  
    elif q == 2:
        padding = b'\x06\x80'  
    else:
        padding = b'\x06' + (b'\x00' * (q - 2)) + b'\x80'
    
    padded_message = message + padding
    return padded_message

def absorbing_phase(padded_message, rate_bits):
    """
    Absorbe le message paddé dans l'état interne en utilisant des XOR et la permutation keccak_f1600.
    """
    rate_bytes = rate_bits // 8
    state = [0] * 25  
    
    for i in range(0, len(padded_message), rate_bytes):
        block = padded_message[i:i+rate_bytes]
        
        for j in range(len(block)):
            state[j % 25] ^= block[j]
        
        state = keccak_f1600(state)
    
    return state

def squeezing_phase(state, output_bits):
    """
    Extrait le hash du message à partir de l'état interne après absorption et permutation.
    """
    output_bytes = output_bits // 8
    hash_output = bytearray(output_bytes)
    for i in range(output_bytes):
        hash_output[i] = (state[i // 8] >> (8 * (i % 8))) & 0xff
    return hash_output

def theta(state):
    """
    Première étape de la permutation keccak_f1600. Modifie l'état en calculant la parité des colonnes.
    """
    C = [0] * 5
    D = [0] * 5
    new_state = state[:]
    
    for x in range(5):
        C[x] = state[x] ^ state[x+5] ^ state[x+10] ^ state[x+15] ^ state[x+20]

    for x in range(5):
        D[x] = C[(x-1) % 5] ^ C[(x+1) % 5]

    for x in range(5):
        for y in range(5):
            new_state[x+5*y] ^= D[x]
    
    return new_state

def rho(state):
    """
    Effectue une rotation des bits dans l'état pour la diffusion.
    """
    rotations = [
        [0, 1, 62, 28, 27],
        [36, 44, 6, 55, 20],
        [3, 10, 43, 25, 39],
        [41, 45, 15, 21, 8],
        [18, 2, 61, 56, 14]
    ]
    new_state = state[:]
    
    for x in range(5):
        for y in range(5):
            index = x + 5 * y
            new_state[index] = ((state[index] << rotations[x][y]) | (state[index] >> (64 - rotations[x][y]))) & ((1 << 64) - 1)
    
    return new_state

def pi(state):
    """
    Réarrange les lignes et les colonnes de l'état pour la diffusion.
    """
    new_state = [0] * 25
    for x in range(5):
        for y in range(5):
            new_state[y + 5 * ((2 * x + 3 * y) % 5)] = state[x + 5 * y]
    return new_state

def chi(state):
    """
    Étape non linéaire de la permutation keccak_f1600 qui utilise une logique conditionnelle de bits.
    """
    new_state = [0] * 25
    for y in range(5):
        for x in range(5):
            new_state[x + 5 * y] = state[x + 5 * y] ^ ((~state[(x + 1) % 5 + 5 * y]) & state[(x + 2) % 5 + 5 * y])
    return new_state

def iota(state, round_index):
    """
    Ajoute une constante au début de l'état, spécifique à chaque ronde, pour éviter des symétries.
    """
    RC = [
        0x0000000000000001, 0x0000000000008082, 0x800000000000808A,
        0x8000000080008000, 0x000000000000808B, 0x0000000080000001,
        0x8000000080008081, 0x8000000000008009, 0x000000000000008A,
        0x0000000000000088, 0x0000000080008009, 0x000000008000000A,
        0x000000008000808B, 0x800000000000008B, 0x8000000000008089,
         0x8000000000008003, 0x8000000000008002, 0x8000000000000080,
        0x000000000000800A, 0x800000008000000A, 0x8000000080008081,
        0x8000000000008080, 0x0000000080000001, 0x8000000080008008
    ]
    state[0] ^= RC[round_index]
    return state

def keccak_f1600(state):
    """
    Applique 24 rondes de la permutation keccak_f1600 à l'état interne.
    """
    for round_index in range(24):
        state = theta(state)
        state = rho(state)
        state = pi(state)
        state = chi(state)
        state = iota(state, round_index)
    return state

def sha3_keccak(message, rate_bits, output_bits):
    """
    Fonction principale pour calculer le hash SHA-3 d'un message en utilisant l'algorithme Keccak.
    """
    padded_message = keccak_padding(message, rate_bits)
    state = absorbing_phase(padded_message, rate_bits)
    state = keccak_f1600(state)
    hash_output = squeezing_phase(state, output_bits)
    return hash_output


def mgf1(input_bytes, length, rate_bits, output_bits):
    """ Masque de génération de fonction basée sur un algorithme de hachage Keccak SHA-3. """
    counter = 0
    output = b''
    while len(output) < length:
        C = counter.to_bytes(4, byteorder='big')
        output += sha3_keccak(input_bytes + C, rate_bits, output_bits)
        counter += 1
    return output[:length]

def oaep_encode(message, label, k, rate_bits, output_bits):
    """ Encodage OAEP d'un message avec une clé publique RSA de taille k. """
    hash_len = output_bits // 8  # Longueur du hash en octets
    lHash = sha3_keccak(label, rate_bits, output_bits)
    ps = b'\x00' * (k - len(message) - 2 * hash_len - 2)
    db = lHash + ps + b'\x01' + message
    seed = os.urandom(hash_len)
    dbMask = mgf1(seed, k - hash_len - 1, rate_bits, output_bits)
    maskedDB = bytes(x ^ y for x, y in zip(db, dbMask))
    seedMask = mgf1(maskedDB, hash_len, rate_bits, output_bits)
    maskedSeed = bytes(x ^ y for x, y in zip(seed, seedMask))
    return b'\x00' + maskedSeed + maskedDB

def oaep_decode(encoded_message, label, k, rate_bits, output_bits):
    """ Décodage OAEP d'un message. """
    hash_len = output_bits // 8
    lHash = sha3_keccak(label, rate_bits, output_bits)
    Y, maskedSeed, maskedDB = encoded_message[0], encoded_message[1:1+hash_len], encoded_message[1+hash_len:]
    seedMask = mgf1(maskedDB, hash_len, rate_bits, output_bits)
    seed = bytes(x ^ y for x, y in zip(maskedSeed, seedMask))
    dbMask = mgf1(seed, k - hash_len - 1, rate_bits, output_bits)
    db = bytes(x ^ y for x, y in zip(maskedDB, dbMask))
    lHashPrime, rest = db[:hash_len], db[hash_len:]
    index = rest.index(b'\x01')
    message = rest[index+1:]
    if lHash != lHashPrime:
        raise ValueError("Label hash does not match")
    return message

# Usage example
k = 256  
label = b''
message = b'Hello, RSA with OAEP!'
encoded_message = oaep_encode(message, label, k, 1152, 256)  
decoded_message = oaep_decode(encoded_message, label, k, 1152, 256)

print("Encoded Message:", encoded_message)
print("Decoded Message:", decoded_message)
assert message == decoded_message, "OAEP encoding/decoding failed"
