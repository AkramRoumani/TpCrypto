# Implémentation de l'Algorithme de Chiffrement ChaCha20 en Python

Ce dépôt contient une implémentation en Python de l'algorithme de chiffrement ChaCha20. ChaCha20 est un chiffre de haute sécurité pour le chiffrement symétrique à clé secrète, conçu par Daniel J. Bernstein. Vous trouverez ci-dessous une explication détaillée de chaque fonction et de leur rôle dans l'algorithme global.

## Vue d'ensemble

Le code fourni met en œuvre le chiffre ChaCha20, reconnu pour sa vitesse et sa sécurité. Il inclut une configuration complète pour chiffrer des messages en utilisant une clé secrète et un nonce pour garantir la sécurité et l'unicité du processus de chiffrement.

## Fonctions

### `quarter_round`
- **Description** : Transforme quatre mots de 32 bits (a, b, c, d) à travers une série d'opérations élémentaires : addition modulaire, XOR et rotations à gauche.
- **Opérations** :
  - **Addition modulaire** : Additionne a et b, résultat pris modulo \(2^{32}\).
  - **XOR** : Combine le résultat avec d en utilisant XOR.
  - **Rotation à gauche** : Tourne d à gauche de 16 bits.
  - Ce processus est répété avec différentes combinaisons et tailles de rotation (16, 12, 8 et 7 bits). Cette fonction fait partie de l'opération de mélange des bits qui complique la relation entre les bits d'entrée et de sortie.

### `columnround`
- Effectue un 'Column Round' sur l'état, qui est une liste de 16 mots de 32 bits. Chaque colonne de l'état passe par la fonction `quarter_round`, mélangeant les bits verticalement au sein de l'état.

### `rowround`
- Semblable à `columnround`, mais applique la transformation `quarter_round` sur chaque rangée de l'état, mélangeant les bits horizontalement.

### `doubleround`
- Combine un `columnround` et un `rowround`. Cette séquence de deux rounds est essentielle pour mélanger les bits de l'état à la fois verticalement et horizontalement.

### `chacha_core`
- Applique 10 `Double Rounds` sur l'état initial de 16 mots de 32 bits. Après ces itérations, chaque mot de l'état final est additionné modulo \(2^{32}\) au mot correspondant de l'état initial, assurant une réversibilité nécessaire pour le déchiffrement.

### `key_expansion`
- Génère l'état initial à partir d'une clé de 32 octets et d'un nonce de 12 octets. Les valeurs initiales incluent une constante fixe sigma pour assurer une diversité entre les clés différentes, même si elles sont identiques.

### `encrypt`
- Chiffre un message donné en utilisant l'algorithme ChaCha20. Pour chaque bloc de 64 octets du message, il génère un flot de clés en utilisant `chacha_core` et chiffre ce bloc par un XOR avec ce flot de clés. Ce processus est répété pour chaque bloc du message, avec un compteur incrémenté pour chaque bloc pour assurer l'unicité du flot de clés même si le message dépasse 64 octets.

## Exemple d'utilisation

Un exemple est fourni pour montrer comment utiliser ces fonctions pour chiffrer un message avec une clé et un nonce spécifiques.

```python
key = bytes([0] * 32)  
nonce = bytes([0] * 8)  à 8 octets
encrypted = encrypt(b'Votre message secret ici', key, nonce)
print("Message chiffré:", encrypted)
