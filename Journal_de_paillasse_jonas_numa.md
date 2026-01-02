# Journal de paillasse

## Date : Lundi 22 Septembre 2025
Pour cette séance j'ai pu aprrendre à utliser l'api d'une IA dans le but d'éssayer d'automatiser des taches en local.

## Date : Lundi 29 Septembre 2025
Dans cette séance, j'ai pu générer un Markdown à partir d'une page de livre à l'aide de Gemini. Le problème qui se pose est que Gemini n'arrive pas à détecter les colonnes sur une page.

J'ai également pu écrire le scénario pour devenir membre. Pour le scénario d'installation, je suis toujours indécis sur ce que nous allons faire.

Je compte maintenant travailler sur la manière de découper intelligemment un PDF avant de procéder à son analyse.

## Date : Lundi 06 Octobre 2025
# Avancement sur les scénarios de la bibliothèque numérique

Nous avons pu avancer sur plusieurs scénarios. Les scénarios les plus basiques ont été pris en compte, il reste maintenant à identifier et formaliser les scénarios complémentaires.  

---

## 1. Scénario de stockage des œuvres non retenues après modération

Nous avons proposé un scénario où les livres **non retenus après modération** pourraient être conservés dans un **dossier spécifique non prévu dans le cahier des charges**.  
L’objectif serait de stocker **les informations sur le livre** ainsi que **sur le membre qui l’a proposé**, sans pour autant les rendre accessibles aux autres utilisateurs.

## 2. Gestion des œuvres sous droits (répertoire `séquestre`)

Nous avons abordé avec le professeur la question de la meilleure manière de gérer les livres sous droits :  
1. **Proposition non retenue :**  
   Mettre les livres sous droits sur un **serveur distant**, là où la législation leverait temporairement les droits.  
   - Rejetée à cause des **risques de fraude et de contournement de la législation**.  

2. **Discussion :**  
   Définir clairement la **politique de l’application** pour décider quels documents peuvent être conservés ou partagés.

## 3. Gestion des livres empruntés
Nous avons également discuté de la façon de gérer l’accès aux ouvrages empruntés :  
1. **Proposition non retenue :**  
   Offrir un accès **hors ligne** aux fichiers.  
   - Rejetée en raison de **failles de sécurité potentielles**.  
2. **Proposition retenue (pour l’instant) :**  
   Accès à la session en ligne, avec **rafraîchissement toutes les 10 minutes** pour permettre des vérifications et garantir la sécurité.

## Date : Lundi 13 Octobre 2025
Aujourd’hui, je me suis concentré sur le fichier export.md. Pour l’instant, j’ai réussi à générer du Markdown en utilisant ChatGPT, ce qui m’a permis de mieux comprendre le fonctionnement et la manière d’appeler les API de Mistral pour l’OCR et la correction de texte. L’objectif est de pouvoir automatiser l’extraction et la mise en forme des textes scannés à partir des fichiers PDF.

## Date : Lundi 20 octobre 2025

### Compte rendu de la séance

Aujourd’hui, nous avons discuté de la manière de **gérer les œuvres sous droits**.  
Plusieurs propositions ont été examinées, mais certaines ont été **écartées** :

1. **Héberger le serveur dans un pays où l’œuvre est libre de droit**  
   → Problème : le pays d’origine de l’utilisateur peut détecter et appliquer sa propre législation, ce qui ne résout pas la question de la responsabilité juridique.

2. **Héberger uniquement les utilisateurs (les œuvres stockées sur leurs espaces personnels)**  
   → Même dans ce cas, la loi pourrait se retourner contre la plateforme hébergeuse qui facilite l’accès à ces œuvres.


### Solution retenue

Ne **pas proposer d’ouvrages sous droits** aux utilisateurs.  
Seules les **œuvres du domaine public** ou celles dont les **droits de diffusion sont clairement établis** seront accessibles sur la plateforme.


### Travaux réalisés

- Début du travail sur les **diagrammes UML** avec **Mermaid**.  
- Discussion sur la structure et la cohérence du **modèle de données**.  
- Première version des diagrammes de **classes** et **cas d’utilisation** en cours.

# Rapport des résultats

## Date : Dimanche 09 Novembre 2025

### Résumé

Pour chaque scénario étudié, j'ai pu rédiger son **Diagramme de Classes Participatif (DCP)**.

### Définition du DCP

Le **DCP (Diagramme de Classes du Problème)** est un diagramme UML utilisé lors de l'analyse des cas d'utilisation pour identifier les **classes d’analyse participantes**. Il permet de représenter clairement :

- Les **entités** du domaine métier (données manipulées).  
- Les **contrôles** (logique et coordination des cas d’utilisation).  
- Les **dialogues** (interfaces ou interactions avec l’utilisateur).  

Ce type de diagramme met en avant les **classes qui entrent en jeu lors des différents scénarios**, sans surcharger les détails techniques, et fournit une **vision globale du système du point de vue fonctionnel**.

### Observations

- J'ai pu utiliser le DCP pour **identifier les relations entre entités, contrôles et dialogues** pour chaque scénario.  
- Les modèles se basent sur les scénarios **réels et pertinents**, ce qui les rend directement exploitables pour la conception et l'implémentation.  
- L’approche permet de **préparer la conception détaillée sans se perdre dans des détails obsolètes ou superflus**.  
- Ces diagrammes facilitent la **communication avec les développeurs et les parties prenantes**, en donnant une vue claire des responsabilités et interactions de chaque classe.

### Conclusion

L'utilisation des **DCP pour chaque scénario** a permis :

- De structurer l’analyse des cas d’utilisation de manière cohérente.  
- D’assurer que toutes les entités et interactions importantes sont prises en compte.  
- De créer une base solide pour la **modélisation détaillée et l’implémentation ultérieure** (par exemple en MVVM ou MVC).  

En résumé, le DCP est un outil efficace pour **passer de l’analyse fonctionnelle à la conception logicielle**, tout en restant fidèle aux besoins exprimés dans les scénarios.

## Date : Dimanche 17 Novembre 2025

Aujourd’hui, j’ai pu mettre en place plusieurs diagrammes de séquence en m’appuyant sur le diagramme de classes UML existant.  
L’intelligence artificielle m’a aidé à structurer les interactions entre les différents composants (dialogues, contrôleurs, entités, services), ce qui m’a permis d’obtenir des représentations cohérentes et correctement alignées avec les cas d’utilisation identifiés.

Pour le moment, j’ai choisi de laisser de côté certains scénarios jugés secondaires ou répétitifs, ainsi que ceux qui ne constituent que des variantes mineures de scénarios déjà modélisés. Cela me permet de me concentrer en priorité sur les cas les plus significatifs pour l’application et de clarifier la logique générale avant d’approfondir les chemins alternatifs.

Les résultats actuels sont organisés sous forme de code Markdown, facilitant leur intégration dans la documentation et leur évolution future.

## Date : Lundi 01 Décembre 2025

Aujourd'hui, je travaille sur la maîtrise de **Pyramid** afin d'accéder au dépôt Git et de mieux gérer les comptes ainsi que les accès aux données de l'application.

Pour l'instant, j'ai réussi à créer un module **upload.pt** permettant de téléverser un document dans un dépôt Git.

Je vais maintenant me concentrer sur la mise en place d'un système **no-MySQL** pour gérer les comptes utilisateurs, les bibliothécaires et autres rôles.

## Date : Samedi 13 Décembre 2025

Après une longue discussion avec mon collègue, nous avons décidé de gérer les utilisateurs à l’aide d’une base de données MySQL, tandis que les œuvres numériques seront gérées via des dépôts Git.

---

## Technologies et justification des choix

### 1. Git  
Git est une technologie de gestion de versions distribuée. Elle est utilisée pour assurer la gestion, la traçabilité et l’historique des œuvres déposées dans la bibliothèque numérique.

Deux branches principales ont été mises en place :

#### 1.1 master  
La branche **master** gère les œuvres validées, notamment celles présentes dans le répertoire `fond_commun`, ainsi que les œuvres sous droits placées dans le `séquestre`.

#### 1.2 moderation  
La branche **moderation** est dédiée aux œuvres en attente de validation. Les fichiers sont stockés dans le répertoire `a_moderer` et exposés via une interface web accessible uniquement aux bibliothécaires.

L’utilisation de Git permet :
- Une traçabilité complète des dépôts, validations et suppressions d’œuvres.
- Un historique fiable des actions effectuées sur chaque fichier, utile en cas de litige lié aux droits d’auteur.
- Une séparation claire des états d’une œuvre (proposée, validée, séquestrée).
- La synchronisation et la diffusion des œuvres via des dépôts distants, favorisant une bibliothèque décentralisée.

---

### 2. Docker  
Docker est une technologie largement utilisée dans les environnements cloud et DevOps pour le déploiement et les tests applicatifs.

Son utilisation dans ce projet permet :
- D’isoler l’application et ses dépendances (Python, Git, bibliothèques).
- D’éviter les problèmes d’installation liés au système hôte.
- De garantir un comportement identique de l’application sur différents systèmes d’exploitation.
- De simplifier le lancement de l’application à l’aide d’une seule commande, même pour un utilisateur non technique.

---

### 3. Pyramid  
Le framework web **Pyramid** a été choisi pour sa flexibilité et son intégration naturelle avec Python.

Il présente plusieurs avantages :
- Une architecture modulaire adaptée aux projets de taille moyenne à grande.
- Une bonne compatibilité avec les scripts Python existants (OCR, traitement PDF, conversion Markdown).
- Une gestion claire des routes, des vues et des permissions, essentielle pour distinguer les rôles utilisateurs et bibliothécaires.
- Une approche explicite favorisant la compréhension et la maintenance du code.

---

### 4. TAL / METAL  
**TAL/METAL** est utilisé en complément de Pyramid pour la gestion des templates HTML.

Ce choix permet :
- Une séparation claire entre la logique métier et la présentation.
- Un rendu dynamique des pages (upload, modération, consultation des œuvres).
- Une intégration native et performante avec Pyramid, sans dépendances lourdes.

---

### 5. Mermaid  
**Mermaid** est utilisé pour intégrer des diagrammes directement dans les documents Markdown.

Il permet :
- La génération de diagrammes lisibles et maintenables (architecture, flux applicatifs, branches Git).
- Une documentation cohérente et versionnée avec le reste du projet.
- Une meilleure compréhension globale du système sans dépendre d’outils externes.



# Rapport d'avancement du projet – Gestion des ouvrages

---

# Rapport d'avancement du projet – Gestion des ouvrages

---

### 1 Janvier 2026
Suite à ma précédente analyse du projet sur la gestion des ouvrages avec Git, j’ai eu une discussion avec mon collègue pour décider entre continuer à utiliser Git pour stocker les données ou passer à une base de données qu’il avait déjà commencée.  

L’utilisation de Git présentait plusieurs inconvénients :  
1. Capacité limitée pour gérer de gros volumes de données.  
2. Accès aux données plus compliqué comparé à une base de données.  

La décision finale a été de privilégier l’usage d’une base de données.  

J’ai repris son code et tout changé dans ma branche. Le code n’était pas terminé et manquait d’ergonomie, j’ai donc dû **refactorer plusieurs parties** pour améliorer la lisibilité et l’organisation du projet.

#### Pages et vues principales
- **Page d’accueil (`home`)** : affichage du contenu principal et de la barre de navigation.  
- **Liste des œuvres (`oeuvres`)** : récupération de toutes les œuvres depuis la base et affichage.  
- **Connexion et inscription (`connect`)** :  
  - Connexion avec vérification du mot de passe et gestion de session.  
  - Inscription avec création d’un nouvel utilisateur et gestion des doublons.  
- **Déconnexion (`logout`)** : suppression complète de la session et redirection vers l’accueil.  
- **Upload d’œuvres (`upload`)** : gestion de l’upload de fichiers, création d’une proposition, et gestion des erreurs.  
- **Aperçu des propositions (`apercu_prop`)** :  
  - Affichage de la proposition, actions pour annuler ou envoyer.  
  - Conversion du Markdown en HTML pour l’affichage.  
- **Aperçu des œuvres (`apercu_oeuvre`)** : affichage du contenu Markdown transformé en HTML.  

---

### 2 Janvier 2026
Aujourd’hui, j’ai travaillé sur plusieurs fonctionnalités et améliorations :  

#### Gestion des rôles et administration
- Ajout d’un **admin par défaut** pour traiter les demandes de rôles.  
- Gestion des demandes de rôle par les utilisateurs avec vérification qu’une demande n’est pas déjà en cours.  
- Gestion côté admin pour **refuser ou consulter les demandes**.  

#### Tests et stabilité
- Ajout de **tests unitaires initiaux** pour certaines fonctionnalités critiques.  
- Gestion des erreurs liées aux uploads et aux formulaires pour éviter les plantages.  

#### Environnement et lancement
- Mise en place d’un **venv** depuis la racine du projet.  
- Installation des dépendances via `requirements.txt`.  
- Lancement du serveur avec `pserve`.  
- Automatisation via le script `lancement.sh` qui :  
  - Crée et active le venv.  
  - Installe les dépendances.  
  - Installe le package en mode édition.  
  - Démarre le serveur pour tests en local.  

Ces améliorations permettent désormais de naviguer sur l’application, proposer et visualiser des œuvres, gérer les utilisateurs et les rôles, tout en gardant le projet stable et fonctionnel.

---

### Lancement du programme
Pour lancer le programme :  
1. Se placer à la **racine du projet**.  
2. Lancer le script `lancement.sh` :  

```bash
./lancement.sh
