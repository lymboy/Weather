import gunicorn
from flask import render_template

from app import create_app

app = create_app()

print(gunicorn.__version__)

# @app.route('')
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug = True) 