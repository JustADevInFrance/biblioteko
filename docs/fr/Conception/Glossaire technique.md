# Glossaire technique

## Rôles et utilisateurs

* **Utilisateur** : personne interagissant avec l’application (peut être *anonyme*, *membre* ou *bibliothécaire*).
* **Anonyme** : utilisateur non authentifié ou sans compte.
* **Membre** : utilisateur inscrit à la plateforme, disposant d’un espace disque partagé.
* **Bibliothécaire** : rôle chargé de la modération, de l’enrichissement des métadonnées, de la validation/rejet des œuvres.

---

## Composants du système

* **Bibliothèque numérique décentralisée** : système distribué de gestion et de partage d’œuvres numériques.
* **Dépôt Git** : système de gestion de versions utilisé comme stockage principal des œuvres et de leurs métadonnées.
* **Arborescence de fichiers** : structure hiérarchique permettant de représenter les œuvres dans le dépôt.
* **Module** : composant logiciel indépendant pouvant être utilisé et testé séparément en ligne de commande.
* **Modulaire** : caractéristique d’un système dont les fonctionnalités sont divisées en modules indépendants et réutilisables.
* **Intégration continue** : processus automatisé permettant de tester et valider les modules au fur et à mesure de leur développement.

---

## Répertoires du dépôt

* **fond_commun** : répertoire contenant les œuvres libres de droits.
* **emprunts** : répertoire contenant les œuvres sous droits empruntées, chiffrées avec la clé du membre.
* **séquestre** : répertoire sécurisé où sont stockées les œuvres sous droits en attente, avec accès restreint.
* **a_moderer** : répertoire contenant les œuvres proposées par les membres en attente de validation.

---

## ⚙️ Technologies utilisées

* **Python** : langage de programmation imposé pour le projet.
* **Pyramid** : framework web côté serveur utilisé pour développer l’application.
* **Framework web** : ensemble d’outils et de bibliothèques facilitant le développement d’applications web (ex. Pyramid).
* **TAL/METAL** : langage de templates utilisé côté serveur (hérité de Zope/Plone).
* **SolidJS** : framework JavaScript moderne « React-like » pour le développement côté client.
* **Bootstrap** : framework CSS/JS pour le prototypage rapide et la mise en page côté client.
* **Côté serveur** : ensemble des composants logiciels exécutés sur le serveur, gérant la logique métier, les données et la sécurité.
* **Côté client** : ensemble des composants logiciels exécutés dans le navigateur de l’utilisateur, gérant l’interface et l’interaction avec le serveur.

---

## Fonctions principales

* **Numérisation** : action de transformer une œuvre physique (ex. livre) en fichier numérique (PDF).
* **Livres scannés** : fichiers PDF obtenus à partir de la numérisation d’ouvrages papier.
* **Fichiers numériques** : documents dématérialisés (PDF, Markdown, audio, vidéo, etc.) stockés et manipulés par l’application.
* **Reconnaissance de texte (OCR)** : usage d’IA (Gemini, Pixtral) pour extraire du texte des fichiers scannés.
* **Téléchargement** : action de récupérer une œuvre depuis la plateforme au format PDF ou Markdown.
* **Location numérique** : mise à disposition d’une œuvre protégée pour une durée limitée (2 semaines).
* **Modération** : processus de contrôle exercé par les bibliothécaires (validation, rejet, ajout de métadonnées).
* **Diffusion automatique** : mise à disposition des œuvres devenues libres de droit auprès des membres.

---

## Aspects légaux et sécurité

* **Propriété intellectuelle** : cadre légal protégeant les œuvres sous droit.
* **Œuvre sous droit** : œuvre encore protégée par la législation en vigueur.
* **Œuvre libre de droit** : œuvre appartenant au domaine public.
* **Chiffrement** : mécanisme de protection des œuvres empruntées via une clé associée à chaque membre.
* **Gestion des droits** : ensemble des règles et mécanismes permettant de respecter la législation sur les copies et la diffusion.

---

## Méthodes et bonnes pratiques

* **Modélisation UML** : usage du langage de modélisation UML (diagrammes de classes, d’activités, de séquence, etc.) pour représenter la structure et le comportement du système.
* **Design patterns** : modèles de conception orientée objet réutilisables pour résoudre des problèmes récurrents de conception logicielle.
* **Documentation** : ensemble des textes et schémas décrivant le système (architecture, choix techniques, API, guide utilisateur, etc.).
