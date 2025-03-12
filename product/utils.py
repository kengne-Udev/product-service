import requests
import jwt
from jwcrypto import jwk
from django.conf import settings
from django.core.cache import cache


def get_jwks():
    jwks = cache.get('jwks')
    if not jwks:

        response = requests.get(settings.AUTH_SERVICE_JWKS_URL)
        response.raise_for_status()
        jwks = response.json()['keys']
        cache.set('jwks', jwks, 3600) # Cache for 1 hour
    return jwks

def validate_jwt(token):
    try:
        header = jwt.get_unverified_header(token)
        kid = header['kid']
        jwks = get_jwks()

        matching_key = next((key for key in jwks if key['kid'] == kid), None)

        if not matching_key:
            return None

        public_key = jwk.JWK(**matching_key)
        payload = jwt.decode(token, public_key.export_to_pem().decode('utf-8'), algorithms=['RS256'])
        return payload
    except Exception as e:
        print(f"JWT validation error: {e}")
        return None