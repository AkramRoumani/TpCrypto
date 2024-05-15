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


def find_hash_with_leading_zeros(base_message, rate_bits, output_bits, leading_zeros):
    """
    Recherche un message modifié par ajout de compteur tel que le hash SHA-3 du message commence par un nombre spécifié de zéros.
    :param base_message: message de base en bytes auquel un compteur est ajouté.
    :param rate_bits: taille du bloc de bits utilisée pour le hachage (rate).
    :param output_bits: taille souhaitée du hash de sortie en bits.
    :param leading_zeros: nombre de zéros hexadécimaux souhaités au début du hash.
    :return: le premier message modifié et son hash correspondant qui satisfait la condition.
    """
    
    counter = 0
    zeros_prefix = '0' * leading_zeros  
    
    while True:
        new_message = base_message + str(counter).encode()
        hash_output = sha3_keccak(new_message, rate_bits, output_bits)
        hash_hex = hash_output.hex()
        if hash_hex.startswith(zeros_prefix):
            return new_message, hash_hex 
        counter += 1  


# Définir les paramètres de la fonction de hachage
rate_bits = 1152  
output_bits = 224

# Définir deux messages différents
message1 = b"Hello, world!"
message2 = b"Hello, world?!"

# Calculer le hachage pour le premier message
hash_output1 = sha3_keccak(message1, rate_bits, output_bits)
hash_hex1 = hash_output1.hex()

# Calculer le hachage pour le second message
hash_output2 = sha3_keccak(message2, rate_bits, output_bits)
hash_hex2 = hash_output2.hex()

# Afficher les résultats
print("Message 1:", message1)
print("SHA-3-224 Hash 1:", hash_hex1)
print("Message 2:", message2)
print("SHA-3-224 Hash 2:", hash_hex2)


base_message = b"Example message!"
leading_zeros = 5
found_message, found_hash = find_hash_with_leading_zeros(base_message, rate_bits, output_bits, leading_zeros)
print(f"Found message: {found_message.decode()}")
print(f"SHA-3 Hash with leading zeros: {found_hash}")
