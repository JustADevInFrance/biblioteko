from infra.pyramid_app import create_app
from waitress import serve

app = create_app()

if __name__ == "__main__":
    print("Serveur Pyramid démarré sur http://localhost:6543")
    serve(app, host="0.0.0.0", port=6543)
