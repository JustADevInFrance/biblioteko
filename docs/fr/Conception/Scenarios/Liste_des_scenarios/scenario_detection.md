# Scénario : Détection automatique du genre et du public cible

**Description :**  
Un membre dépose un document PDF sur la plateforme. L’application, aidée d’une IA, analyse automatiquement le contenu du texte pour déterminer le genre littéraire (aventure, technique, poésie, etc.) et le public cible (enfant, adulte, grand public). Le système crée un fichier de métadonnées complet décrivant l’œuvre. Le bibliothécaire valide ou corrige les catégories avant publication.

**Acteurs :**  
- Un membre inscrit  
- Le module d’intelligence artificielle (IA de classification)  
- Un bibliothécaire modérateur

**Prérequis :**  
- Le scénario « Déposer une œuvre » a été exécuté sans erreur et le fichier a été ajouté au répertoire `a_moderer/`.  
- Le texte du document a été extrait par l’IA OCR (Gemini ou Pixtral).

**Étapes :**  
1. Le membre dépose une œuvre numérisée au format PDF.  
2. Le module OCR extrait le texte brut du document.  
3. Le module d’analyse sémantique nettoie et prépare le texte.  
4. L’application via un script détecte automatiquement le **genre littéraire** (ex. Aventure, Technique, Poésie…).  
5. L’IA Scénario : Détection automatique du genre et du public cible

Description :
Uidentifie également le **public cible** (ex. Enfant, Adulte, Grand public…).  
6. L’application crée un **fichier de métadonnées** associé à l’œuvre, contenant toutes les informations descriptives : titre, auteur, année, langue, genre, public, résumé, licence, chemin du fichier, score de confiance, etc.  
7. Le fichier de métadonnées est enregistré dans le dépôt Git à côté du document, sous le format `metadata.yaml` :

```yaml
title: Les aventures de Tintin
author: Hergé
year: 1941
language: fr
genre: Aventure
audience: Enfant
rights: Domaine public
description: Une série d’aventures d’un jeune reporter belge et de son chien Milou.
themes: [Exploration, Mystère, Amitié]
file_format: pdf
checksum: 3e24b7f93d...
confidence_score: 0.92
```

8. Le bibliothécaire accède à l’interface de modération et consulte les catégories et métadonnées proposées.
9. Il peut valider, modifier ou rejeter les suggestions de l’IA.
10. L’application met à jour le fichier de métadonnées validé dans le dépôt Git de la bibliothèque.
11. L’œuvre est publiée dans la section correspondante du fond commun avec ses métadonnées officielles.
12. Le membre reçoit une notification indiquant que son œuvre a été classée, validée et publiée.
