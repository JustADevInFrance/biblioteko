def test_validation_proposition(test_app, db_session, create_admin):
    from app.models import Proposition
    # Créer une proposition
    prop = Proposition(
        titre="Test Livre",
        auteur="Auteur X",
        format_oeuvre="md",
        contenu_markdown="Contenu",
        utilisateur_id=create_admin.id
    )
    db_session.add(prop)
    db_session.commit()

    # Simuler session admin
    test_app.set_cookie("username", "admin")
    test_app.set_cookie("user_id", str(create_admin.id))
    test_app.set_cookie("role", "admin")

    # Valider proposition
    res = test_app.post("/gestion_biblio", {"prop_id": prop.id, "action": "valider"})
    
    # Vérifier que proposition a disparu et oeuvre créée
    from app.models import Oeuvre
    oeuvres = db_session.query(Oeuvre).all()
    assert len(oeuvres) == 1
    assert oeuvres[0].titre == "Test Livre"

