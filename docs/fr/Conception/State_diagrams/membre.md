# Diagramme d'états transitions pour le Membre

```mermaid
stateDiagram-v2
    [*] --> NonInscrit
    NonInscrit --> Inscrit : Formulaire validé
    Inscrit --> Connecté : Authentification réussie
    Connecté --> Déconnecté : Déconnexion
    Déconnecté --> Connecté : Nouvelle session
    Déconnecté --> [*]
```
