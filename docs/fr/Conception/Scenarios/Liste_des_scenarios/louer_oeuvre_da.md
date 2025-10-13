## Louer une oeuvre sous droits d'auteur ##

**Description :**  
Un membre souhaite emprunter une oeuvre protégée par des droits d'auteurs depuis la bibliothèque numérique. L'emprunt s'effectue **en ligne** après vérification de la disponibilité légale et technique de l'oeuvre, et crée un **fichier de métadonnées** dans le répertoire `emprunts/` pour permettre la vérification et la suppression automatique à la fin de la période de prêt.

**Pré-requis :**  
- Être membre connecté.  
- Disposer d'une **connexion Internet active**.
- L'oeuvre doit être marquée comme **empruntable** dans le système.
- Le membre n'a pas dépassé sa **limite d'emprunts simultanés**.
- Le répertoire `emprunts/` doit exister dans l'espace local du membre.  

**Contenu du scénario :**  
1. Le membre ouvre la **rubrique "Catalogue"** ou effectue une recherche d'oeuvre.
2. Il sélectionne une **oeuvre sous droits** et clique sur **Emprunter**.
3. L'application envoie une **requête au serveur** pour vérifier :
    - le **statut juridique** de l'oeuvre (sous droits ou domaine public).
    - le **statut administratif** (validé et approuvée par un bibliothécaire).
    - la **disponibilité** du nombre de copies autorisées.
    - la **licence d'exploitation** (encore active).
4. Si l'oeuvre est **empruntable**, le système poursuit le processus :
    - Génère une **clé de chiffrement unique** pour le membre.
    - Télécharge une **copie chiffrée** de l'oeuvre.
    - Stocke le fichier dans le répertoire `emprunts/`.
    - Crée un **fichier de métadonnées** (JSON ou YAML) associé à l'oeuvre.

**Exemple de fichier `emprunts.oeuvre_12345.json`**

```json
{
    "id_oeuvre": "12345",
    "titre": "Les Misérables",
    "auteur": "Victor Hugo",
    "membre_id": "membre_789",
    "empruntable": true,
    "date_emprunt": "2025-10-06T14:32:00Z",
    "date_retour_prevue": "2025-10-20T14:32:00Z",
    "chemin_fichier": "emprunts/les_miserables.md",
    "cle_chiffrement": "cle_unique_membre_789",
    "statut": "actif"
}
```

### [Back](../README.md) ###