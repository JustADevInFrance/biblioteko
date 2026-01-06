# Journal de paillasse

## Etudiant : Tom Mequinion

### 22/09/25 
---
1. Découverte de l'API d'une IA pour automatiser certaines tâches locales.

2. Discussion autour de la transformation d'un livre scanné en format PDF en fichier en format __Markdown__.

    Deux idées différentes me sont venues à l'esprit :

    - Une première implémentation dans laquelle je construis le fichier markdown page par page directement via l'analyse __OCR__. Dans celle-ci, les métadonnées sont récupérées avec des regex. Pour la vérification des métadonnées ainsi que des règles de copyright, on peut interroger l'API WikiData de Wikipedia.

    - Une deuxième implémentation, dans laquelle je construis le fichier markdown en page par page avec l'API OpenAI. Je lui envoie un prompt contenant l'analyse OCR de la page qu'il pourra possiblement corriger et transformer en fichier markdown. Les métadonnées sont aussi récupérées via les regex. On aura la possibilité de vérifier les métadonnées avec l'IA ainsi que les règles de copyright.

**Décision :** Privilégier l'IA pour améliorer la qualité et réduire les erreurs de structures.

3. Début d'écriture du glossaire métier via le cahier des charges du projet. Non terminé pour l'instant.

**Ce que j'ai fait :** Recherche d'une API d'IA pouvant être intégrée et utilisée pour notre projet et écriture d'un script avec Tesseract + API.

---

### 29/09/25 
---

1. Discussion sur l’extraction des textes : Gemini ne détecte pas correctement les colonnes sur certaines pages.
    - **Débat :** faut-il tenter de corriger les colonnes manuellement ou changer d’outil ?
    - **Décision :** rester sur Gemini pour les tests, mais envisager un outil plus précis pour les versions finales (Pixtral).

2. Scénario “devenir membre” écrit et discuté pour valider le flux utilisateur.

3. Réflexion sur l’optimisation du découpage des PDF avant analyse OCR pour éviter les erreurs de mise en forme.

**Ce que j'ai fait :** 
- Je me suis ravisé sur l'utilisation de Tesseract car très lourd et je me suis intéressé plus profondément aux IA et à leurs possibles intégration dans mon script. 
- Ecriture et débat sur le scénario *"Devenir membre"*. 
- Finalisation du glossaire métier avec l'aide de l'IA pour trouver les différents points importants dans le cahier des charges.

---

### 06/10/25 
---

1. Le rendu de test du script d'export au format markdown n'est pas optimal. 
    - **Débat :** Réflexion sur le choix de l'IA à utiliser (Gémini, Pixtral). 
    - **Décision :** On se tournera sur Pixtral car plus ciblé sur OCR et structuration de documents.

2. Réflexion sur le **scénario d'emprunts** quant au fait de passer l'oeuvre en lecture en ligne ou hors ligne. Le hors ligne pourrait poser des problèmes de sécurité sur certains systèmes d'exploitation (Linux) à cause du cache. Il est donc préférable de proposer uniquement l'oeuvre en lecture en ligne pour une meilleure sécurité. 

3. Réflexion sur le **scénario d'emprunts** quant au stockage de données spécifiques dans un fichier (yml, json) dans le répertoire **emprunts** pour chaque emprunts, ce qui permettrait un script de vérification des oeuvres empruntées (gestion de délai).

4. Réflexion sur le fait de tout ce qui est dans le **séquestre** est empruntable ou pas. Dans notre cas, tout ne peut pas être empruntable, on peut donc placer une métadonnée filtre pour les oeuvres empruntables et les non-empruntables.

**Ce que j'ai fait :** 

- Rédaction de plusieurs scénarios pour la liste de scénarios.
- Multiples réflexions avec mon collègue ainsi que d'autres groupe concernant certains scénarios.

---

### 13/10/25 

1. Discussions sur l’automatisation de l’extraction de texte avec ChatGPT et Mistral pour structurer les fichiers Markdown.

2. Débat sur la qualité de l’OCR et la correction automatique : faut-il intervenir manuellement sur certains passages ou tout automatiser ?

3. Discussion avec le client lors de la présentation du glossaire métier et de la liste de scénarios concernant les informations sur les droits d'auteurs des oeuvres et la création d'une base de données listant les oeuvres libres ou soumises aux droits d'auteurs.

**Ce que j'ai fait :**

- Rédaction de quelques scénarios et modification du scénario d'emprunt avec les réflxions vues précédemment.
- Modification du script d'export en markdown (non fonctionnel pour l'instant).
- Passage et présentation du glossaire métier et de la liste de scénarios.

### 20/10/25

1. Gestion des œuvres sous droits :

    - **Débat :** héberger dans un pays "libre de droit" ou sur l’espace utilisateur → trop de risques légaux.
    - **Décision :** ne proposer que des oeuvres du domaine public ou avec droits clairs.

2. Débat sur la sécurité et la mise à jour des sessions pour les œuvres empruntées :

    - **Décision :** rafraîchissement périodique pour éviter la copie ou l’accès non autorisé.

3. Discussions sur les diagrammes UML et le modèle de données : structuration cohérente des classes et interactions.

**Ce que j'ai fait :**

- Travail sur plusieurs diagrammes UML de classes avec l'aide de l'IA et via les scénarios écrits plus tôt.

### 09/11/25

1. Utilisation des DCP (Diagramme de Classes du Problème) pour analyser les scénarios.

2. Débat sur les relations entre entités, contrôles et dialogues : quelle granularité pour les classes ?

    - **Décision :** garder les classes essentielles pour rester fonctionnel et éviter les détails superflus.

**Ce que j'ai fait :**

- Discussions et débats autour des différents diagrammes de classes déjà écrits.
- Réécriture de certains diagrammes de classes et écritures de nouveaux.

### 17/11/25

1. Discussions sur la priorisation des scénarios à modéliser : certains secondaires ou répétitifs peuvent être laissés de côté.

2. Débat sur la structure des diagrammes de séquence : comment représenter les interactions sans complexifier le diagramme.

**Ce que j'ai fait :**

- Discussions autour des diagrammes de séquence et de probables diagrammes d'états transitions.
- Correction de diagrammes de classes et écriture de diagrammes d'états transitions.

### 01/12/25

1. Débat sur le choix du système pour gérer les comptes et l’accès aux données : MySQL ou système sans base.

    - **Décision temporaire :** expérimenter un module “upload” avec Git pour tester la logique.

### 12/12/25

1. Réflexion sur le choix des templates : TAL/METAL vs autre moteur.

    - **Décision :** TAL/METAL intégré à Pyramid pour séparation logique / présentation et facilité de maintenance.

3. Réflexion sur la validation des formulaires et la gestion des erreurs côté serveur.

**Ce que j'ai fait :**
- Création du serveur Pyramid et implémentation de certaines vues : Accueil, Connexion, Inscription, Déconnexion.
- Utilisation de Bootstrap pour plus de simplicité et un développement plus rapide.

### 14/12/25

1. Réflexion sur la gestion de l’upload : stockage temporaire des fichiers vs base de données → stockage temporaire choisi pour réduire les risques et faciliter le traitement.

**Ce que j'ai fait :**
- Appel à l’API Pixtral pour structurer et extraire le contenu du PDF et développement du script adapté.
- Développement des vues accessibles via le rôle de *"membre"* : Proposer un oeuvre.

### 15/12/25

1. Réflexion sur la présentation des aperçus : Markdown → HTML vs PDF intégré.

    - Décision : Markdown transformé en HTML pour compatibilité et flexibilité avec Pyramid/TAL.

2. Débat sur les vues d’administration pour accepter/refuser les demandes : permissions et redirections définies clairement.

**Ce que j'ai fait :**
- Redirections et permission définies pour les vues.
- Ajout du rôle de *"bibliothécaire"* ainsi que des vues pour ce rôle : Aperçu proposition, Accepter une proposition, Refuser une proposition.
- Ajout de la vue pour pouvoir lire une oeuvre (libre de droits) : Aperçu oeuvre.

### 06/01/26

1. Réflexions sur les différences entre test unitaires et tests d'intégration et sur les cas à couvrir en priorité (login, inscription, upload, aperçus, rôles).

**Ce que j'ai fait :**
- Modification du script de lancement du venv `lancement.sh` pour la multiportabilité (Linux/MacOS + Windows avec GitBash).
- Modification et complétion des tests unitaires et d'intégrations.
