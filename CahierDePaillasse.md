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
