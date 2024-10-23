from application import create_app
from application.config import app_config

app = create_app('application.config.Config')  

if __name__ == "__main__":
    app.run()

        