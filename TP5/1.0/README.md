# TP de Chiffrement RSA avec OAEP

Ce projet implémente un système de chiffrement RSA en Python, utilisant l'algorithme de padding OAEP pour améliorer la sécurité lors du chiffrement des messages. Il inclut également des fonctions pour tester la primalité des nombres, essentielles pour la génération de clés RSA.

## Fonctionnalités

- **Test de primalité de Fermat**: Vérifie si un nombre est premier en utilisant le petit théorème de Fermat, un prérequis pour la sélection des nombres premiers dans la génération de clés RSA.
- **Génération de nombres premiers**: Fonction pour générer des nombres premiers utilisés dans la création des clés RSA.
- **Padding OAEP**: Implémente le padding OAEP pour sécuriser le chiffrement RSA en rendant les messages chiffrés plus résistants aux attaques.
- **Chiffrement et Déchiffrement RSA**: Fonctions pour chiffrer et déchiffrer des messages en utilisant les clés RSA générées.

## Détails des Fonctions

- **fermat_test(n, a)**: Teste si `n` est un nombre premier en utilisant `a` comme base.
- **is_prime(n, k=5)**: Détermine si `n` est premier en exécutant le test de Fermat plusieurs fois pour réduire la probabilité d'erreurs.
- **generate_prime(bit_length)**: Génère un nombre premier de la taille spécifiée, en utilisant le test de primalité pour vérifier chaque candidat.
- **euclide_etendu(a, b)**: Implémente l'algorithme d'Euclide étendu pour trouver le pgcd de `a` et `b`, ainsi que les coefficients de l'identité de Bézout.
- **generer_cles_RSA(bit_length=2048)**: Génère une paire de clés publique et privée pour le chiffrement RSA.
- **encrypt(message, public_key)**: Chiffre un message avec la clé publique RSA.
- **decrypt(cipher_text, private_key)**: Déchiffre un message avec la clé privée RSA.
- **OAEP_padding(message, n, G, H, k0, k1)**: Applique le padding OAEP au message avant chiffrement.
- **OAEP_unpadding(padded_message, n, G, H, k0, k1)**: Retire le padding OAEP d'un message après déchiffrement.

## Utilisation

Pour utiliser les fonctions de chiffrement et de déchiffrement avec RSA et OAEP, vous devez d'abord générer une paire de clés RSA. Ensuite, vous pouvez chiffrer un message avec la clé publique et le déchiffrer avec la clé privée. Le padding OAEP est automatiquement appliqué pendant ces opérations.

### Exemple de Code

```python
public_key, private_key = generer_cles_RSA(2048)
message = b"Message secret"
cipher_text = encrypt(message, public_key)
print("Message chiffré:", cipher_text)

decrypted_message = decrypt(cipher_text, private_key)
print("Message déchiffré:", decrypted_message)

message = b"Ceci est un message de test"
n = 256  
k0 = 32  
k1 = 32  

padded_message = OAEP_padding(message, n, G, H, k0, k1)
print("Message paddé :", padded_message)

message_original = OAEP_unpadding(padded_message, n, G, H, k0, k1)
print("Message original retrouvé :", message_original)