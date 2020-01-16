from flask_restful import Api, Resource
from flask import Flask
from User import User

app = Flask(__name__)
api = Api(app)

api.add_resource(User, '/Api/V1/User', endpoint='User')

if __name__ == '__main__':
    app.run()