from flask import Flask

from first.views import *


app = Flask(__name__)
app.register_blueprint(first_blueprint)
app.config['JSON_AS_ASCII'] = False

if __name__ == '__main__':
    app.run(debug=True)


