```mermaid
stateDiagram-v2
    [*] --> EnAttente
    EnAttente --> Vérifié : Vérification de la disponibilité
    Vérifié --> NonDisponible : Oeuvre non empruntable
    Vérifié --> Actif : Oeuvre empruntée
    Actif --> EnCours : Téléchargement réussi
    EnCours --> Expire : Délai de 2 semaines atteint
    Expire --> NonAccessible : Suppression automatique
    NonAccessible --> [*]
    NonDisponible --> [*]
```