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

### 29/09/25 ###
---

1. Rédaction de l'analyse du cahier des charges et du glossaire techiques du projet.

2. Réflexion sur les erreurs d'importation de tesseract et de l'utilisation de pytesseract dans l'analyse de charactères.

3. Début d'écriture du README pour les scénarios.

---

### 06/10/25 ###
---

1. Rédaction de plusieurs scénarios pour la liste de scénarios.

2. Le rendu de test du script d'export au format markdown n'est pas optimal. Réflexion sur le choix de l'IA à utiliser (Gémini, Pixtral). On se tournera sur Pixtral car plus ciblé sur OCR et structuration de documents.

3. Réflexion sur le **scénario d'emprunts** quant au fait de passer l'oeuvre en lecture en ligne ou hors ligne. Le hors ligne pourrait poser des problèmes de sécurité sur certains systèmes d'exploitation (Linux) à cause du cache. Il est donc préférable de proposer uniquement l'oeuvre en lecture en ligne pour une meilleure sécurité. 

4. Réflexion sur le **scénario d'emprunts** quant au stockage de données spécifiques dans un fichier (yml, json) dans le répertoire **emprunts** pour chaque emprunts, ce qui permettrait un script de vérification des oeuvres empruntées (gestion de délai).

5. Réflexion sur le fait de tout ce qui est dans le **séquestre** est empruntable ou pas. Dans notre cas, tout ne peut pas être empruntable, on peut donc placer une métadonnée filtre pour les oeuvres empruntables et les non-empruntables.