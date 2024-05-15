def quarter_round(a, b, c, d):
    """
    Effectue un 'Quarter Round' sur quatre mots de 32 bits. Ce type de transformation
    est une opération élémentaire dans l'algorithme de chiffrement ChaCha20, qui mélange
    les bits de quatre variables pour augmenter la sécurité cryptographique.

    :param a, b, c, d: Entrées de quatre mots de 32 bits.
    :return: Quatre mots de 32 bits transformés après une série d'opérations arithmétiques et logiques.
    """
    a = (a + b) & 0xffffffff  # Addition modulaire 2^32 entre a et b
    d ^= a  # Opération XOR entre d et le nouveau a
    d = ((d << 16) | (d >> (32 - 16))) & 0xffffffff  # Rotation à gauche de 16 bits sur d

    c = (c + d) & 0xffffffff  # Addition modulaire 2^32 entre c et d
    b ^= c  # Opération XOR entre b et le nouveau c
    b = ((b << 12) | (b >> (32 - 12))) & 0xffffffff  # Rotation à gauche de 12 bits sur b

    a = (a + b) & 0xffffffff  # Nouvelle addition modulaire 2^32 entre a et b
    d ^= a  # Nouvelle opération XOR entre d et le nouveau a
    d = ((d << 8) | (d >> (32 - 8))) & 0xffffffff  # Rotation à gauche de 8 bits sur d

    c = (c + d) & 0xffffffff  # Nouvelle addition modulaire 2^32 entre c et d
    b ^= c  # Nouvelle opération XOR entre b et le nouveau c
    b = ((b << 7) | (b >> (32 - 7))) & 0xffffffff  # Rotation à gauche de 7 bits sur b

    return a, b, c, d

def columnround(state):
    """
    Applique un 'Column Round', qui est un ensemble de 'Quarter Rounds' sur les colonnes
    de l'état (matrice 4x4 de mots de 32 bits). Chaque colonne est traitée individuellement pour mélanger les données verticalement.

    :param state: Liste représentant l'état de 16 mots de 32 bits.
    :return: État modifié après le traitement des colonnes.
    """
    # Applique un 'Quarter Round' sur chaque colonne
    state[0], state[4], state[8], state[12] = quarter_round(state[0], state[4], state[8], state[12])
    state[1], state[5], state[9], state[13] = quarter_round(state[1], state[5], state[9], state[13])
    state[2], state[6], state[10], state[14] = quarter_round(state[2], state[6], state[10], state[14])
    state[3], state[7], state[11], state[15] = quarter_round(state[3], state[7], state[11], state[15])
    return state

def rowround(state):
    """
    Applique un 'Row Round', qui est un ensemble de 'Quarter Rounds' sur les rangées
    de l'état. Chaque rangée est traitée individuellement pour mélanger les données horizontalement.

    :param state: Liste représentant l'état de 16 mots de 32 bits.
    :return: État modifié après le traitement des rangées.
    """
    # Applique un 'Quarter Round' sur chaque rangée
    state[0], state[1], state[2], state[3] = quarter_round(state[0], state[1], state[2], state[3])
    state[4], state[5], state[6], state[7] = quarter_round(state[4], state[5], state[6], state[7])
    state[8], state[9], state[10], state[11] = quarter_round(state[8], state[9], state[10], state[11])
    state[12], state[13], state[14], state[15] = quarter_round(state[12], state[13], state[14], state[15])
    return state

def doubleround(state):
    """
    Effectue un 'Double Round', qui consiste en un 'Column Round' suivi d'un 'Row Round'.
    Cette séquence de deux rounds est essentielle pour assurer un mélange suffisant des bits de l'état.

    :param state: Liste représentant l'état de 16 mots de 32 bits.
    :return: État transformé après un 'Double Round'.
    """
    state = columnround(state)  # Premier passage : Column Round
    state = rowround(state)     # Deuxième passage : Row Round
    return state

def chacha_core(x):
    """
    Applique la transformation de base de ChaCha20, qui consiste en 10 itérations de 'Double Rounds'.
    Cela assure un niveau élevé de diffusion et de confusion des bits de l'état initial.

    :param x: État initial de 16 mots de 32 bits.
    :return: État transformé après 10 'Double Rounds'.
    """
    original_x = x[:]  # Copie de l'état initial pour le calcul final
    for _ in range(10):
        x = doubleround(x)  # Application répétée des Double Rounds
    return [(xi + original_xi) & 0xffffffff for xi, original_xi in zip(x, original_x)]  # Addition finale modulo 2^32

def key_expansion(key, nonce):
    """
    Prépare l'état initial pour le chiffrement ChaCha20 à partir de la clé et du nonce fournis.
    Inclut une constante pour distinguer des schémas d'initialisation différents.

    :param key: Clé de chiffrement de 32 octets.
    :param nonce: Nonce de 12 octets.
    :return: État initial constitué de constantes, clé, compteur de bloc, et nonce.
    """
    assert len(key) == 32  # Vérification de la taille de la clé
    assert len(nonce) == 12  # Vérification de la taille du nonce
    sigma = [0x61707865, 0x3320646e, 0x79622d32, 0x6b206574]  # Constantes 'expand 32-byte k'
    key_words = [int.from_bytes(key[i:i+4], 'little') for i in range(0, 32, 4)]
    nonce_words = [int.from_bytes(nonce[i:i+4], 'little') for i in range(4, 12, 4)]
    counter = [int.from_bytes(nonce[:4], 'little'), 0]  # Compteur initialisé avec partie du nonce
    return sigma + key_words + counter + nonce_words

def encrypt(plaintext, key, nonce):
    """
    Chiffre un message en utilisant ChaCha20. Le message est traité par blocs de 64 octets,
    avec chaque bloc chiffré indépendamment en utilisant un flot de clés généré par `chacha_core`.

    :param plaintext: Message en clair sous forme de liste d'octets.
    :param key: Clé de 32 octets.
    :param nonce: Nonce initial de 8 octets, étendu à 12 octets pour le traitement.
    :return: Message chiffré sous forme de liste d'octets.
    """
    assert len(nonce) == 8  # Vérification de la taille du nonce
    block_count = len(plaintext) // 64 + (1 if len(plaintext) % 64 != 0 else 0)  # Calcul du nombre de blocs
    encrypted_message = []

    for block in range(block_count):
        block_nonce = nonce + block.to_bytes(4, 'little')  # Création du nonce pour ce bloc
        assert len(block_nonce) == 12  # Vérification de la taille du nonce total
        state = key_expansion(key, block_nonce)  # Expansion de la clé avec le nonce du bloc
        key_stream = chacha_core(state)  # Génération du flot de clés
        key_stream_bytes = b''.join(word.to_bytes(4, 'little') for word in key_stream)  # Conversion en octets

        start = block * 64
        end = min((block + 1) * 64, len(plaintext))
        block_bytes = plaintext[start:end]

        block_encrypted = bytes(a ^ b for a, b in zip(block_bytes, key_stream_bytes[:end-start]))  # Chiffrement XOR
        encrypted_message.extend(block_encrypted)

    return bytes(encrypted_message)


# Exemple d'utilisation
key = bytes([0] * 32)  
nonce = bytes([0] * 8)  
encrypted = encrypt(b'Votre message secret ici', key, nonce)
print("Message chiffre:", encrypted)