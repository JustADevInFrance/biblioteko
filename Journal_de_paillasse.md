# Journal de paillasse #

## Etudiant : Tom Mequinion ##

### 22/09/25 ###
---

1. Discussion autour de la transformation d'un livre scanné en format PDF en fichier en format __Markdown__.

    Deux idées différentes me sont venues à l'esprit :

    - Une première implémentation dans laquelle je construis le fichier markdown page par page directement via l'analyse __OCR__. Dans celle-ci, les métadonnées sont récupérées avec des regex. Pour la vérification des métadonnées ainsi que des règles de copyright, on peut interroger l'API WikiData de Wikipedia.

    - Une deuxième implémentation (celle que j'ai implémentée), dans laquelle je construis le fichier markdown en page par page avec l'API OpenAI. Je lui envoie un prompt contenant l'analyse OCR de la page qu'il pourra possiblement corriger et transformer en fichier markdown. Les métadonnées sont aussi récupérées via les regex. On aura la possibilité de vérifier les métadonnées avec l'IA ainsi que les règles de copyright.

2. Début d'écriture du glossaire métier via le cahier des charges du projet. Non terminé pour l'instant.

---

### ... ###