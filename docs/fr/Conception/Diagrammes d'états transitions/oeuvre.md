# Diagramme d'états transitions pour l'Oeuvre

```mermaid
stateDiagram-v2
    [*] --> Soumise
    Soumise --> EnModération : Vérification par un bibliothécaire
    EnModération --> Rejetée : Non conforme
    EnModération --> Validée : Acceptée
    Validée --> DomainePublic : Libre de droits
    DomainePublic --> Diffusée : Distribution automatique aux membres
    Diffusée --> [*]
    Rejetée --> [*] 
```