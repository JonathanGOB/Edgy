from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask import Flask
from Endpoints import User
from TableStorage.TableStorageConnection import AzureTableStorage

app = Flask(__name__)
api = Api(app)

app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.username

@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    return {
        'name': identity.username,
        'email': identity.email
    }

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    storage = AzureTableStorage()
    table_service = AzureTableStorage.get_table()
    jti = decrypted_token['jti']
    filter = "Token eq '{}'".format(jti)
    existence = table_service.query_entities('revokedtokens', filter=filter)
    existence = list(existence)
    return len(existence) == 1

api.add_resource(User.UserLogin, '/Api/V1/Login', endpoint='Login')
api.add_resource(User.UserRegistration, '/Api/V1/Register', endpoint='Register')
api.add_resource(User.TokenRefresh, 'Api/V1/RefreshToken', endpoint='RefreshToken')
api.add_resource(User.UserLogoutAccess, 'Api/V1/Logout/Access', endpoint='Access')
api.add_resource(User.UserLogoutRefresh, 'Api/V1/Logout/Refresh', endpoint='Refresh')


if __name__ == '__main__':
    app.run()