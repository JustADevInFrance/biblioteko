## Déposer une oeuvre numérisée ##

**Description :** Un membre a numérisé une oeuvre et souhaite le partager avec la bibliothèque pour enrichir son fond. Selon le format du fichier (Markdown ou PDF), l'applicarion adapte le traitement avant de soummetre l'oeuvre à la modération.

**Pré-requis :**
- Être membre connecté.
- Disposer d'une oeuvre numérisée localement au format `.md` ou `.pdf`.
- L'application dispose d'un moteur de reconnaissance de texte (Gemini, Pixtral) pour les fichiers PDF.

**Contenu du scénario :**

1. Le membre clique sur **Proposer une oeuvre** dans le menu principal.

2. L'application demande de sélectionner un **fichier à importer**.

3. Le membre choisit une oeuvre depuis son terminal.

### Branchement A - Oeuvre déjà au format Markdown ###

4. L'application détecte le format `.md`.

5. Elle analyse le contenu pour **extraire automatiquement less métadonnées** (titre, auteur, date, etc.).

6. Si certaines données sont manquantes, l'oeuvre est marquée comme **"incomplète"** pour vérification par un bibliothécaire.

7. Le fichier et ses données sont stockées dans le répertoire **a_moderer**.

8. Les bibliothécaires sont notifiés et valident ou complètent les informations.

9. Après validation, l'oeuvre est publiée dans :

    - **fond_commun** (si libre de droits).
    
    - **séquestre** (si protégée).

### Branchement B - Oeuvre au format PDF ###

4. Le système détecte le format `.pdf`.

5. Il exécute une **reconnaissance de texte (OCR)** via une IA (Gemini ou Pixtral).

6. Le texte extrait est automatiquement converti au **format Markdown**.

7. Les métadonnées sont détectées et extraites automatiquement.

8. Si certaines données sont manquantes, l'oeuvre est marquée comme **"incomplète"** pour vérification par un bibliothécaire.

9. Le fichier et ses données sont stockées dans le répertoire **a_moderer**.

10. Les bibliothécaires sont notifiés et valident ou complètent les informations.

11. Après validation, l'oeuvre est publiée dans :

    - **fond_commun** (si libre de droits).
    
    - **séquestre** (si protégée).

### [Back](../README.md) ###