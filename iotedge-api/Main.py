from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask import Flask, jsonify
from Endpoints import User, EdgeDevice, SensorDevice, Sensor, SensorData
from TableStorage.TableStorageConnection import AzureTableStorage
from flask_cors import CORS
import Settings.Salt  as salt
app = Flask(__name__)
api = Api(app)
CORS(app)

app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['JWT_SECRET_KEY'] = salt.secret
app.config['PROPAGATE_EXCEPTIONS'] = True
jwt = JWTManager(app)


# message if jwt is revoked
@jwt.revoked_token_loader
def return_json_revoke_response():
    return jsonify({
        "message": "token revoked"
    }), 401


# return identity of jwt user
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.email


# return claims from jwt token
@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    return {
        'name': identity.username,
        'email': identity.email,
        'id': identity.id
    }


# return true or false if jwt token is in blacklist
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    storage = AzureTableStorage()
    table_service = storage.get_table()
    jti = decrypted_token['jti']
    filter = "Token eq '{}'".format(jti)
    existence = table_service.query_entities('revokedtokens', filter=filter)
    existence = list(existence)
    return len(existence) == 1


# User endpoints
api.add_resource(User.UserLogin, '/Api/V1/Login', endpoint='Login')
api.add_resource(User.UserRegistration, '/Api/V1/Register', endpoint='Register')
api.add_resource(User.TokenRefresh, '/Api/V1/RefreshToken', endpoint='RefreshToken')
api.add_resource(User.UserLogoutAccess, '/Api/V1/Logout/Access', endpoint='Access')
api.add_resource(User.UserLogoutRefresh, '/Api/V1/Logout/Refresh', endpoint='Refresh')
api.add_resource(User.Account, '/Api/V1/Account', endpoint='Account')

# EdgeDevices endpoints
api.add_resource(EdgeDevice.EdgeDevices, '/Api/V1/EdgeDevices', endpoint="EdgeDevices")
api.add_resource(EdgeDevice.SingleEdgeDevice, '/Api/V1/EdgeDevices/<string:id>')

# SensorsDevices endpoints
api.add_resource(SensorDevice.SensorsDevices, '/Api/V1/SensorsDevices', endpoint="SensorDevices")
api.add_resource(SensorDevice.GetEdgeSensorsDevices, '/Api/V1/EdgeDevices/<string:id>/SensorsDevices')
api.add_resource(SensorDevice.SingleSensorsDevice, '/Api/V1/SensorsDevices/<string:id>')

# Sensors endpoints
api.add_resource(Sensor.Sensors, '/Api/V1/Sensors', endpoint="Sensors")
api.add_resource(Sensor.SingleSensor, '/Api/V1/Sensors/<string:id>')
api.add_resource(Sensor.GetEdgeDeviceSensors, '/Api/V1/EdgeDevices/<string:id>/Sensors')
api.add_resource(Sensor.GetSensorDeviceSensors, '/Api/V1/SensorsDevices/<string:id>/Sensors')

# SensorData endpoints
api.add_resource(SensorData.SensorData, '/Api/V1/SensorData', endpoint="SensorData")
api.add_resource(SensorData.SingleSensorData, '/Api/V1/SensorData/<string:id>')
api.add_resource(SensorData.GetSensorSensorData, '/Api/V1/Sensors/<string:id>/SensorData')
api.add_resource(SensorData.GetSensorDeviceSensorData, '/Api/V1/SensorDevices/<string:id>/SensorData')

if __name__ == '__main__':
    app.run()
