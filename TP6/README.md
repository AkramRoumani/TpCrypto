# Documentation RSA

Ce projet implémente les fonctionnalités de base du chiffrement RSA, ainsi que des techniques avancées pour la signature et la vérification des messages. Le code utilise également le Théorème des Restes Chinois (CRT) et des méthodes de randomisation pour renforcer la sécurité.

## Structure du Code

- **Partie 1** : Fonctions de base et génération de clés RSA.
- **Partie 2** : Signature RSA utilisant CRT pour optimiser les performances.
- **Partie 3** : Signature RSA randomisée pour renforcer la sécurité contre les attaques.

## Fonctionnalités

- **Génération de nombres premiers** : Utilise le test de Fermat pour vérifier la primalité.
- **Génération de clés** : Crée des clés publiques et privées pour le chiffrement RSA.
- **Signature RSA** : Permet de signer des messages en utilisant une clé privée.
- **Vérification RSA** : Permet de vérifier les signatures en utilisant une clé publique.
- **Signature RSA avec CRT** : Utilise le CRT pour effectuer la signature de manière plus efficace.
- **Signature RSA randomisée** : Améliore la sécurité en ajoutant de l'aléatoire au processus de signature.

## Vérification des Signatures

Chaque signature créée par les méthodes `creer_signature` ou `creer_signature_crt` peut être vérifiée en utilisant `verifier_signature`. La méthode prend le message original, la signature, et la clé publique pour confirmer l'authenticité de la signature.

## Exemples d'Utilisation

### Génération de Clés

```python
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




