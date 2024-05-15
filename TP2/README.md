# Projet AES (Advanced Encryption Standard)

Ce projet implémente l'algorithme de chiffrement et de déchiffrement AES (Advanced Encryption Standard) en Python, couvrant toutes les étapes principales du processus AES, y compris la génération de clés, le chiffrement et le déchiffrement.

## Structure du projet et Fonctionnalités

Le script Python `aes.py` contient plusieurs fonctions définies pour effectuer le chiffrement et le déchiffrement AES:

- `subbyte(a)`: Applique la transformation SubBytes à l'État.
- `shiftrows(a)`: Applique la transformation ShiftRows à l'État.
- `mixColumns(a)`: Applique la transformation MixColumns à l'État.
- `add_round_key(state, round_key)`: Ajoute la clé de ronde à l'État.
- `key_expansion(key, Sbox, rc)`: Expands the main key into all round keys.
- `complete_encryption(state)`: Fonction pour chiffrer complètement un bloc de données.
- `inv_subbyte(a)`, `inv_shiftrows(a)`, `invMixColumns(a)`: Fonctions pour les étapes inverses dans le déchiffrement AES.
- `complete_decryption(state)`: Fonction pour déchiffrer complètement un bloc de données chiffré.
- `multiply_poly(a, b)`, `inverse_in_gf2_8(x)`, `apply_affine_transformation(x)`: Fonctions pour les opérations dans GF(2^8).

### Résultats Attendus

Le script est conçu pour fournir un chiffrement et un déchiffrement complets en utilisant l'Advanced Encryption Standard (AES). Après le chiffrement d'un bloc de données, le script devrait renvoyer un état chiffré, et le déchiffrement de cet état devrait restaurer les données originales. Ces résultats démontrent la conformité de l'implémentation avec les spécifications AES.

### Validation des Fonctionnalités

- **Conformité de la S-Box et de la InvS-Box** : La S-Box et la InvS-Box utilisées pour les transformations SubBytes et InvSubBytes sont conformes aux spécifications définies par le NIST. La transformation affine et l'inversion dans GF(2^8) ont été testées pour assurer l'exactitude des résultats.
- **Transformations ShiftRows et InvShiftRows** : Les décalages appliqués correspondent précisément à ceux spécifiés dans le standard AES, assurant ainsi une manipulation correcte de l'état durant le chiffrement et le déchiffrement.
- **Fonctionnement de MixColumns et InvMixColumns** : Ces opérations manipulent les colonnes de l'état par des combinaisons linéaires qui sont cruciales pour assurer la diffusion dans AES. Les résultats sont conformes aux attentes théoriques.
- **Génération de clés** : La fonction de l'expansion de clés a été validée pour générer correctement toutes les clés de ronde requises pour le processus de chiffrement/déchiffrement AES.
- **Intégrité des données** : Après le chiffrement et le déchiffrement successifs d'un bloc de données, l'état original est parfaitement restauré, validant ainsi l'exactitude de l'ensemble du processus.

### Tests et Exemples de Résultats

Les tests effectués montrent que pour un bloc de données initial, le script produit un état chiffré et parvient à restaurer l'état original après déchiffrement. Voici un exemple :

```python
État initial: [[0x32, 0x88, 0x31, 0xe0], [0x43, 0x5a, 0x31, 0x37], [0xf6, 0x30, 0x98, 0x07], [0xa8, 0x8d, 0xa2, 0x34]]
État chiffré: [[0x39, 0x02, 0xdc, 0x19], [0x25, 0xdc, 0x11, 0x6a], [0x84, 0x09, 0x85, 0x0b], [0x1d, 0xfb, 0x97, 0x32]]
État déchiffré: [[0x32, 0x88, 0x31, 0xe0], [0x43, 0x5a, 0x31, 0x37], [0xf6, 0x30, 0x98, 0x07], [0xa8, 0x8d, 0xa2, 0x34]]
