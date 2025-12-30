from models import Session, Utilisateurs

session = Session()

# Supprime l'ancien utilisateur si présent
user_to_delete = session.query(Utilisateurs).filter_by(username="Tom").first()
if user_to_delete:
    session.delete(user_to_delete)
    session.commit()
    print("Utilisateur précédent supprimé")

# Création du nouvel utilisateur
utilisateur = Utilisateurs()
utilisateur.username = "Tom"
utilisateur.email = "tom.mequinion@hotmail.com"
utilisateur.set_password("testB")
utilisateur.role = "bibliothecaire"

session.add(utilisateur) 
session.commit()
session.close()

print("Nouvel utilisateur créé avec succès !")
