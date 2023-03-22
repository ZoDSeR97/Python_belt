from app import app
from app.controllers import users, bands

if __name__ == "__main__":
    app.run(debug=True)