def lfsr(seed, taps, length):
    """
    Implémentation d'un registre à décalage à rétroaction linéaire (LFSR) pour la génération de séquences binaires.
    
    :param seed: État initial du LFSR (liste de bits).
    :param taps: Positions pour l'opération XOR, indexées à partir de 1.
    :param length: Nombre de bits à générer.
    :return: Une liste contenant la séquence de bits générés.
    """
    # Ajustement des positions des robinets pour l'indexation à partir de 0.
    taps = [tap - 1 for tap in taps]
    # Copie de l'état initial dans le registre de décalage.
    sr = seed[:]
    # Liste pour stocker la séquence de bits générés.
    output = []
    
    # Génération des bits un par un.
    for _ in range(length):
        # Calcul du bit de rétroaction par XOR des bits aux positions des robinets.
        feedback_bit = sum([sr[tap] for tap in taps]) % 2
        # Insertion du bit de rétroaction au début du registre.
        sr.insert(0, feedback_bit)
        # Récupération du bit de sortie en supprimant le dernier élément du registre.
        output.append(sr.pop())
    
    return output

def lfsr_debug(seed, taps, length):
    """
    Version détaillée de la fonction LFSR qui affiche les étapes de calcul.
    
    :param seed: État initial du LFSR.
    :param taps: Positions pour l'opération XOR, indexées à partir de 1.
    :param length: Nombre de bits à générer.
    :return: La séquence générée tout en affichant les détails du processus.
    """
    taps = [tap - 1 for tap in taps]
    sr = seed[:]
    output = []

    print("count\tstate\t\toutbit\tseq")
    print("-" * 148)
    
    for count in range(1, length + 1):
        feedback_bit = sum([sr[tap] for tap in taps]) % 2
        sr.insert(0, feedback_bit)
        out_bit = sr.pop()
        output.append(out_bit)

        # Affichage des informations de chaque étape.
        print(f"{count}\t{sr}\t\t{out_bit}\t{output}")
    
    print("-" * 148)
    return output

def Berlekamp_Massey(sequence):
    """
    Algorithme de Berlekamp-Massey pour déterminer le polynôme minimal d'une séquence binaire.
    
    :param sequence: La séquence binaire pour laquelle le polynôme minimal est calculé.
    :return: Liste des coefficients du polynôme minimal.
    """
    f = [1]  # Polynôme minimal initial.
    g = [1]  # Polynôme temporaire pour les calculs.
    L = 0    # Longueur du LFSR estimée.
    m = -1   # Dernière position où le polynôme a été ajusté.
    n = len(sequence)  # Longueur de la séquence.

    for N in range(n):
        d = sequence[N]
        # Mise à jour du terme d en utilisant les coefficients actuels de f.
        for i in range(1, min(L, N) + 1):
            d ^= (f[i] & sequence[N-i])  

        # Si d est non nul, ajustement de f est nécessaire.
        if d == 1:
            t = f[:] 
            new_f_length = max(len(f), N - m + len(g))
            new_f = [0] * new_f_length
            for i in range(len(f)):
                new_f[i] = f[i]
            for i in range(len(g)):
                new_f[N - m + i] ^= g[i]
            f = new_f

            # Mise à jour des variables si la condition est remplie.
            if 2 * L <= N:
                L = N + 1 - L
                m = N
                g = t  

    return f  

# Utilisation des fonctions définies.
seed = [1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0]
taps = [16, 14, 13, 11]
sequence = lfsr(seed, taps, 32)
print("The LFSR sequence is:")
print(sequence)

# Affichage détaillé des calculs pour débogage.
lfsr_debug(seed, taps, 32)  

# Test de différents longueurs de séquences avec l'algorithme de Berlekamp-Massey.
lengths_to_test = [10, 17, 31]
for test_length in lengths_to_test:
    test_sequence = sequence[:test_length]
    print(f"Polynomial coefficients for the first {test_length} bits:")
    print(Berlekamp_Massey(test_sequence))

