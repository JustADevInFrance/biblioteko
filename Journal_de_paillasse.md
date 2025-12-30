# Journal de paillasse 

## Etudiant : Tom Mequinion 

### 22/09/25 
---

1. Discussion autour de la transformation d'un livre scanné en format PDF en fichier en format __Markdown__.

    Deux idées différentes me sont venues à l'esprit :

    - Une première implémentation dans laquelle je construis le fichier markdown page par page directement via l'analyse __OCR__. Dans celle-ci, les métadonnées sont récupérées avec des regex. Pour la vérification des métadonnées ainsi que des règles de copyright, on peut interroger l'API WikiData de Wikipedia.

    - Une deuxième implémentation (celle que j'ai implémentée), dans laquelle je construis le fichier markdown en page par page avec l'API OpenAI. Je lui envoie un prompt contenant l'analyse OCR de la page qu'il pourra possiblement corriger et transformer en fichier markdown. Les métadonnées sont aussi récupérées via les regex. On aura la possibilité de vérifier les métadonnées avec l'IA ainsi que les règles de copyright.

2. Début d'écriture du glossaire métier via le cahier des charges du projet. Non terminé pour l'instant.

---

### 29/09/25
---

1. Rédaction de l'analyse du cahier des charges et du glossaire techiques du projet.

2. Réflexion sur les erreurs d'importation de tesseract et de l'utilisation de pytesseract dans l'analyse de charactères.

3. Début d'écriture du README pour les scénarios.

---

### 06/10/25
---

1. Rédaction de plusieurs scénarios pour la liste de scénarios.

2. Le rendu de test du script d'export au format markdown n'est pas optimal. Réflexion sur le choix de l'IA à utiliser (Gémini, Pixtral). On se tournera sur Pixtral car plus ciblé sur OCR et structuration de documents.

3. Réflexion sur le **scénario d'emprunts** quant au fait de passer l'oeuvre en lecture en ligne ou hors ligne. Le hors ligne pourrait poser des problèmes de sécurité sur certains systèmes d'exploitation (Linux) à cause du cache. Il est donc préférable de proposer uniquement l'oeuvre en lecture en ligne pour une meilleure sécurité. 

4. Réflexion sur le **scénario d'emprunts** quant au stockage de données spécifiques dans un fichier (yml, json) dans le répertoire **emprunts** pour chaque emprunts, ce qui permettrait un script de vérification des oeuvres empruntées (gestion de délai).

5. Réflexion sur le fait de tout ce qui est dans le **séquestre** est empruntable ou pas. Dans notre cas, tout ne peut pas être empruntable, on peut donc placer une métadonnée filtre pour les oeuvres empruntables et les non-empruntables.

---

### 13/10/25

---

1. Rédaction de quelques scénarios et modification du scénario d'emprunt avec les réflxions vues précédemment.

2. Modification du script d'export en markdown (non fonctionnel pour l'instant).

3. Passage et présentation du glossaire métier et de la liste de scénarios.

---

### 20/10/25 

---

1. Réflexion sur les problèmes de sécurité liés aux oeuvres sous droits d'auteur. Dès qu'une oeuvre sous droits est passée sur le site (ou sur l'application), des données sont stockées et trouvables, même avec la mise en place d'une gestion d'oeuvres empruntables ou non. Ces données posent alors un problème de sécurité au niveau de l'application.

2. Réalisation de quelques diagrammes de classes pour certains scénarios.

---

### 03/11/25

---

1. Mise en commun des idées concernant la gestion des oeuvres sous droits d'auteurs et accessoirement sur les emprunts. L'idée donnée la plus praticable serait une modération humaine (vérification humaine) quant au stockage des oeuvres sous droits. L'idée de notre groupe $-$ refuser les oeuvres sous droits et stocker leurs métadonnées dans une blacklist $-$ n'est probablement pas applicable car certaines oeuvres n'ont pas d'informations trouvables permettant de poruver les droits d'auteur.

2. Rédaction de nouveaux diagrammes de classes pour d'autre scénarios.

---

### 10/11/25

1. Ecriture de plusieurs diagrammes d'états transitions à partir des diagrammes de classes

---

### 01/12/25

1. Choix d'utilisation de Pyramid avec TAL/METAL pour le backend de l'application car demandé par le client dans le cahier des charges.

2. Pour l'instant le choix du framework frontend se tourne vers Bootstrap car plus rapide au vu du temps limité.