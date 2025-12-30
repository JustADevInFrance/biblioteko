# Diagramme d'états transitions pour la Rubrique

```mermaid
stateDiagram-v2
    [*] --> Vide
    Vide --> Enrichie : Ajout d'une oeuvre
    Enrichie --> Actualisée : Mise à jour des oeuvres
    Enrichie --> Vide : Toutes les oeuvres sont supprimées
    Actualisée --> Enrichie
    Enrichie --> [*]
```
