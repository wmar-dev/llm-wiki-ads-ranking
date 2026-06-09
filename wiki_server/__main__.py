from wiki_server.app import create_app
from wiki_server import config

if __name__ == "__main__":
    app = create_app()
    app.run(host=config.HOST, port=config.PORT)
