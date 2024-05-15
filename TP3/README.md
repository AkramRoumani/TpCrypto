# Implémentation de la fonction de hachage SHA-3 Keccak

Ce dépôt contient une implémentation en Python de la fonction de hachage SHA-3 Keccak, démontrant les composants clés des fonctions de hachage cryptographiques et fournissant un outil pour générer des hachages avec des propriétés spécifiques.

## Vue d'ensemble

L'implémentation de SHA-3 Keccak est structurée autour de plusieurs fonctions clés qui, ensemble, mettent en œuvre l'algorithme de hachage cryptographique Keccak, qui est la base de la norme SHA-3. Les fonctions sont conçues pour gérer le padding des messages, les permutations d'état, ainsi que les phases d'absorption et de pressage qui définissent la construction éponge utilisée par Keccak.

## Fonctions

### `keccak_padding(message, rate_bits)`
Applique un padding au message pour s'assurer qu'il correspond à un multiple de la taille de bloc (`rate`). Cette fonction ajuste la longueur du message selon les règles de padding de Keccak, en fonction de la quantité de padding nécessaire.

### `absorbing_phase(padded_message, rate_bits)`
Traite le message paddé à travers la phase d'absorption de la construction éponge de Keccak. Elle XOR les blocs du message avec l'état interne puis applique la permutation `keccak_f1600`.

### `squeezing_phase(state, output_bits)`
Extrait le hash de l'état interne après la phase d'absorption. Cette phase extrait le résultat du hash de l'état, en fonction de la longueur de sortie désirée.

### `theta(state)`
Première étape de la permutation `keccak_f1600`. Modifie l'état en calculant la parité des colonnes pour contribuer à la diffusion.

### `rho(state)`
Effectue une rotation des bits dans l'état pour améliorer la diffusion à travers l'état.

### `pi(state)`
Réarrange les lignes et les colonnes de l'état pour améliorer la diffusion des données.

### `chi(state)`
Étape non linéaire de la permutation qui applique une fonction logique conditionnelle aux bits de l'état.

### `iota(state, round_index)`
Ajoute une constante au début de l'état, spécifique à chaque tour, pour éviter des symétries lors des calculs.

### `keccak_f1600(state)`
Applique 24 tours de la permutation `keccak_f1600` à l'état interne, en combinant les fonctions de transformation précitées pour sécuriser le processus de hachage.

### `sha3_keccak(message, rate_bits, output_bits)`
Fonction principale pour calculer le hash SHA-3 d'un message en utilisant l'algorithme Keccak. Cette fonction intègre toutes les étapes, du padding à la production du hash final.

### `find_hash_with_leading_zeros(base_message, rate_bits, output_bits, leading_zeros)`
Cherche une variante d'un message de base qui, une fois haché, produit un hash commençant par un nombre spécifié de zéros hexadécimaux. Utilisé pour des applications nécessitant une preuve de travail.

## Résultats et Discussion

### Résultats de l'Algorithme de Hachage SHA-3 Keccak
Les résultats suivants illustrent les sorties de la fonction `sha3_keccak` pour deux messages légèrement différents, démontrant l'efficacité et la sécurité de l'algorithme en termes de production de hachages uniques pour des entrées distinctes.

![SHA-3 Keccak Output](../../captures/sha.png)

Chaque hachage est distinctement différent, soulignant ainsi l'une des propriétés cruciales d'une fonction de hachage cryptographique — l'unicité. Cela garantit que même de minimes modifications du message d'entrée produisent des résultats largement différents, ce qui est essentiel pour la sécurité des applications de hachage.

### Discussion de la Fonction `find_hash_with_leading_zeros`
La fonction `find_hash_with_leading_zeros` est conçue pour trouver un hachage qui commence par un nombre spécifié de zéros. Cependant, en pratique, cette fonction peut s'exécuter pendant une durée indéterminée sans produire de résultat, en particulier lorsque le nombre de zéros demandés est élevé. Ceci est dû à la nature probabiliste du hachage et à la rareté des hachages commençant par plusieurs zéros, ce qui nécessite un nombre exponentiellement plus grand de tentatives pour trouver un hachage valide.

**Pourquoi c'est normal :**
- **Probabilité Faible :** La probabilité de générer un hachage qui répond à des critères spécifiques de préfixe est très faible. Par exemple, la probabilité qu'un hachage commence par un seul zéro hexadécimal est de 1/16. Pour chaque zéro supplémentaire, cette probabilité est divisée par 16, ce qui rend la tâche exponentiellement plus difficile.
- **Calcul Intensif :** Chaque tentative de générer un nouveau hachage nécessite un calcul complet, ce qui peut devenir très coûteux en termes de temps et de ressources, surtout à mesure que le nombre de tentatives augmente.

### Conclusion
La fonction de hachage SHA-3 Keccak a démontré son efficacité en fournissant des hachages uniques pour des messages différents, ce qui est vital pour des applications de sécurité telles que la vérification d'intégrité et l'authentification. D'autre part, l'utilisation de la fonction `find_hash_with_leading_zeros` illustre les défis associés à la recherche de hachages avec des caractéristiques spécifiques, mettant en lumière les limites pratiques et théorques de l'algorithme en cas de contraintes extrêmes.
