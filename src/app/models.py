from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime
from passlib.hash import bcrypt
import json

Base = declarative_base()

# -------------------------
# Proposition
# -------------------------
class Proposition(Base):
    __tablename__ = 'propositions'

    id = Column(Integer, primary_key=True)
    titre = Column(String, nullable=False)
    auteur = Column(String, nullable=False)
    format_oeuvre = Column(String, nullable=False)
    contenu_markdown = Column(Text, nullable=False)
    meta_info = Column(Text)
    utilisateur_id = Column(Integer, ForeignKey("utilisateurs.id"))
    date_creation = Column(DateTime, default=datetime.utcnow)
    est_valide = Column(Boolean, default=False)
    est_explicite = Column(Boolean, default=False)
    libre_de_droit = Column(Boolean, default=False)

    utilisateur = relationship("Utilisateurs")

    def __init__(self, titre, auteur, format_oeuvre, contenu_markdown, est_valide=False, est_explicite=False, libre_de_droit=False):
        self.titre = titre
        self.auteur = auteur
        self.format_oeuvre = format_oeuvre
        self.contenu_markdown = contenu_markdown
        self.est_valide = est_valide
        self.est_explicite = est_explicite
        self.libre_de_droit = libre_de_droit
        self.date_creation = datetime.utcnow()

    @property
    def meta(self):
        if self.meta_info:
            try:
                return json.loads(self.meta_info)
            except json.JSONDecodeError:
                return {}
        return {}

    @meta.setter
    def meta(self, value):
        self.meta_info = json.dumps(value)


# -------------------------
# Oeuvre
# -------------------------
class Oeuvre(Base):
    __tablename__ = 'oeuvres'

    id = Column(Integer, primary_key=True)
    titre = Column(String, nullable=False)
    auteur = Column(String, nullable=False)
    annee = Column(Integer)
    format_oeuvre = Column(String, nullable=False)
    contenu_markdown = Column(Text, nullable=False)
    est_explicite = Column(Boolean, default=False)
    libre_de_droit = Column(Boolean, default=True)
    utilisateur_id = Column(Integer, ForeignKey("utilisateurs.id"))
    date_creation = Column(DateTime, default=datetime.utcnow)

    utilisateur = relationship("Utilisateurs")

    def __init__(self, titre, auteur, format_oeuvre, contenu_markdown, est_explicite=False, libre_de_droit=True):
        self.titre = titre
        self.auteur = auteur
        self.format_oeuvre = format_oeuvre
        self.contenu_markdown = contenu_markdown
        self.est_explicite = est_explicite
        self.libre_de_droit = libre_de_droit
        self.date_creation = datetime.utcnow()


# -------------------------
# Utilisateurs
# -------------------------
class Utilisateurs(Base):
    __tablename__ = "utilisateurs"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="membre")
    is_active = Column(Boolean, default=True)
    date_creation = Column(DateTime, default=datetime.utcnow)

    def __init__(self, username, email, role="membre"):
        self.username = username
        self.email = email
        self.role = role

    def set_password(self, password):
        self.password_hash = bcrypt.hash(password)

    def check_password(self, password):
        return bcrypt.verify(password, self.password_hash)


# -------------------------
# DemandeRole
# -------------------------
class DemandeRole(Base):
    __tablename__ = "demandes_roles"

    id = Column(Integer, primary_key=True)
    utilisateur_id = Column(Integer, ForeignKey("utilisateurs.id"), nullable=False)
    role_demande = Column(String, default="bibliothecaire")
    statut = Column(String, default="en_attente")  # en_attente | accepte | refuse
    motif_refus = Column(Text)
    date_demande = Column(DateTime, default=datetime.utcnow)
    date_traitement = Column(DateTime)

    utilisateur = relationship("Utilisateurs")


# -------------------------
# Création de l'admin
# -------------------------
def create_admin_if_not_exists():
    session = Session()

    ADMIN_USERNAME = "admin"
    ADMIN_EMAIL = "jonuma2100@gmail.com"
    ADMIN_PASSWORD = "admin"

    existing_admin = session.query(Utilisateurs).filter_by(username=ADMIN_USERNAME).first()

    if not existing_admin:
        admin_user = Utilisateurs(username=ADMIN_USERNAME, email=ADMIN_EMAIL, role="admin")
        admin_user.set_password(ADMIN_PASSWORD)
        session.add(admin_user)
        try:
            session.commit()
            print(f"[INFO] Admin '{ADMIN_USERNAME}' créé avec succès !")
        except Exception as e:
            session.rollback()
            print(f"[ERROR] Impossible de créer l'admin : {e}")
    session.close()


# -------------------------
# Création de la base SQLite et Session
# -------------------------
engine = create_engine('sqlite:///bibliotheque.db', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
