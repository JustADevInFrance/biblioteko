## DEVENIR MEMBRE

### Description
Un utilisateur anonyme souhaite devenir membre de l'application.

### Acteurs
- Utilisateur anonyme

### Prérequis
Le scénario « Installer l’application » a été exécuté sans erreur.

### Étapes

1. L'utilisateur a accès à l'application.
2. L'application détecte que l'utilisateur n'est pas membre.
3. L'application propose à l'utilisateur de créer un compte via un lien ou de rester en mode déconnecté, en précisant que les services seront restreints.
4. L'utilisateur clique sur le lien pour créer un compte.
5. L’utilisateur choisit de créer un nouvel identifiant.
6. L’application demande le nom, le prénom et la date de naissance de l’utilisateur.
7. L’utilisateur saisit ces informations.
8. À partir de ces informations, l’application crée :
    - un identifiant unique garantissant l’anonymat,
    - une paire de clés (publique et privée) pour enregistrer les opérations effectuées.
9. L’application transmet l’identifiant et la clé publique au serveur de l’association.
10. L’application affiche les actions permises.
11. L’application affiche la liste des œuvres dans le domaine public.

