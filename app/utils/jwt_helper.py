from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

jwt = JWTManager()

def create_token(identity, expires_delta=None):
    return create_access_token(identity=identity, expires_delta=expires_delta)

def get_current_user():
    return get_jwt_identity()