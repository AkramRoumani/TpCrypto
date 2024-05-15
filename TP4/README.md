# Projet de Cryptographie - Échange de Clés et Tests de Primalité

## Introduction
Ce document décrit l'implémentation et la vérification d'un système d'échange de clés utilisant la cryptographie à clé publique basée sur l'exponentiation modulaire et les tests de primalité. L'objectif principal est de générer des clés sécurisées pour la communication entre deux parties et de valider l'égalité des clés générées des deux côtés.

## Description de la Méthodologie
### Génération de Nombres Premiers
La génération de nombres premiers est cruciale pour la sécurité des algorithmes de cryptographie à clé publique. Nous utilisons le test de primalité de Fermat pour vérifier la primalité des nombres générés aléatoirement.

### Échange de Clés
Nous implémentons un protocole simplifié basé sur le concept de Diffie-Hellman pour l'échange de clés, en utilisant l'exponentiation modulaire pour calculer les clés partagées.

## Détail du Code Implémenté
Le code comprend plusieurs fonctions principales :
- `fermat_test(n, a)`: Réalise le test de primalité de Fermat.
- `is_prime(n, k)`: Vérifie la primalité d'un nombre en utilisant plusieurs bases.
- `generate_prime(bit_length)`: Génère un nombre premier en utilisant la méthode de rejet.
- `measure_exponentiation(base, exponent, modulus, repetitions)`: Mesure le temps nécessaire pour l'exponentiation modulaire.
- `verify_keys(g, p, a, b)`: Vérifie que les clés générées par les deux parties sont identiques.

## Résultats et Discussion

### Temps d'Exécution pour la Génération de Nombres Premiers
![premier Output](../../captures/premier.png)

#### Observations
Les résultats montrent une augmentation significative du temps nécessaire pour générer des nombres premiers à mesure que la taille en bits augmente :
- **3072 bits**: 172.29 secondes
- **4096 bits**: 344.53 secondes
- La génération pour 6144 bits a été interrompue après 2255.591 secondes sans succès.

Cela illustre les défis de la scalabilité avec les tailles de nombres premiers croissantes, mettant en évidence une augmentation exponentielle du temps requis qui rend la méthode impraticable pour des tailles très grandes.

### Exponentiation Modulaire et Vérification des Clés

![echange Output](../../captures/echange.png)

#### Observations
- **Temps d'exécution pour \( g^a \mod p \) (a petit)**: 0.000000 secondes.
- **Temps d'exécution pour \( g^b \mod p \) (b grand)**: 0.001000 secondes.
- **Vérification que \( K = L \)**: Succès.

#### Analyse
1. **Temps d'Exécution**:
   - Le temps d'exécution extrêmement faible pour \( g^a \mod p \) montre l'efficacité de l'implémentation de l'algorithme `pow` de Python, qui optimise les calculs d'exponentiation modulaire.
   - L'augmentation du temps pour l'exposant plus grand (\(b\)) est très minime, passant de 0.000000 à 0.001000 secondes, ce qui reste extrêmement rapide pour des calculs cryptographiques.

2. **Vérification de \( K = L \)**:
   - Le succès de cette vérification est crucial et démontre que le protocole d'échange de clés fonctionne correctement. Les clés calculées des deux côtés sont identiques, ce qui confirme la validité de l'échange.

#### Dédutions
- L'efficacité observée est hautement souhaitable dans les applications de cryptographie où les performances et la rapidité sont essentielles pour la sécurité et la praticité.
- Ces résultats valident non seulement l'efficacité de l'algorithme mais aussi sa fiabilité pour des applications sécurisées en temps réel.

#### Points Positifs
- **Rapidité d'exécution**: Cruciale pour les opérations en temps réel et pour des applications nécessitant de fréquentes renégociations de clé.
- **Fiabilité**: La méthode prouve que les clés générées sont cohérentes et sécurisées, garantissant une communication sécurisée entre les parties.

#### Points Négatifs

- **Sensibilité aux Attaques Temporelles**: Les variations minimes dans le temps d'exécution de l'exponentiation modulaire peuvent exposer à des attaques temporelles, révélant potentiellement des informations sensibles.
- **Considérations de Sécurité à Long Terme**: Avec l'évolution des capacités de calcul et des normes de sécurité, les méthodes actuelles pourraient devenir vulnérables, nécessitant des évaluations et renforcements continus.


### Conclusion
Les résultats confirment l'efficacité des méthodes utilisées pour sécuriser l'échange de clés à travers la cryptographie basée sur l'exponentiation modulaire et les tests de primalité. Cependant, l'augmentation du temps de génération pour les grands nombres premiers nécessite une attention particulière pour les applications pratiques nécessitant une génération rapide de clés.


