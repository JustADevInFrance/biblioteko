```mermaid
stateDiagram-v2
    [*] --> Initial
    Initial --> Ajout : Nouvelle oeuvre détectée
    Initial --> Suppression : Oeuvre supprimée
    Initial --> Modification : Métadonnées modifiées
    Ajout --> MisAJour : Index réécrit
    Suppression --> MisAJour
    Modification --> MisAJour
    MisAJour --> [*]
```