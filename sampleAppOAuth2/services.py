from django.conf import settings
from sampleAppOAuth2.models import Bearer
from datetime import datetime
import urllib
import requests
import base64
import json
import random
from jose import jws, jwk
from base64 import urlsafe_b64decode, b64decode
from sampleAppOAuth2 import getDiscoveryDocument

# token can either be an accessToken or a refreshToken
def revokeToken(token):
    revoke_endpoint  = getDiscoveryDocument.revoke_endpoint
    auth_header = 'Basic ' + stringToBase64(settings.CLIENT_ID + ':' + settings.CLIENT_SECRET)
    headers = {'Accept': 'application/json', 'content-type': 'application/json', 'Authorization' : auth_header}
    payload = { 'token': token }
    r = requests.post(revoke_endpoint, json=payload, headers=headers)
    
    if r.status_code >= 500:
        return 'internal_server_error'
    elif r.status_code >= 400:
        return 'Token is incorrect.'
    else:
        return 'Revoke successful'

def getBearerToken(auth_code):
    token_endpoint = getDiscoveryDocument.token_endpoint
    auth_header = 'Basic ' + stringToBase64(settings.CLIENT_ID + ':' + settings.CLIENT_SECRET)
    headers = {'Accept': 'application/json', 'content-type': 'application/x-www-form-urlencoded', 'Authorization' : auth_header}
    payload = {
    'code': auth_code,
    'redirect_uri': settings.REDIRECT_URI,
    'grant_type': 'authorization_code'
    }
    r = requests.post(token_endpoint, data=payload, headers=headers)
    if r.status_code != 200:
        return r.text
    bearer_raw = json.loads(r.text)

    if 'id_token' in bearer_raw:
        idToken = idToken=bearer_raw['id_token']
    else:
        idToken = None
    
    return Bearer(bearer_raw['x_refresh_token_expires_in'],bearer_raw['access_token'],bearer_raw['token_type'], bearer_raw['refresh_token'], bearer_raw['expires_in'], idToken=idToken)

def getBearerTokenFromRefreshToken(refresh_Token):
    token_endpoint = getDiscoveryDocument.token_endpoint
    auth_header = 'Basic ' + stringToBase64(settings.CLIENT_ID + ':' + settings.CLIENT_SECRET)
    headers = {'Accept': 'application/json', 'content-type': 'application/x-www-form-urlencoded', 'Authorization' : auth_header}
    payload = {
    'refresh_token': refresh_Token,
    'grant_type': 'refresh_token'
    }
    r = requests.post(token_endpoint, data=payload, headers=headers)
    bearer_raw = json.loads(r.text)

    if 'id_token' in bearer_raw:
        idToken = idToken=bearer_raw['id_token']
    else:
        idToken = None
    
    return Bearer(bearer_raw['x_refresh_token_expires_in'],bearer_raw['access_token'],bearer_raw['token_type'], bearer_raw['refresh_token'], bearer_raw['expires_in'], idToken=idToken)

def getUserProfile(access_token):
    auth_header = 'Bearer ' + access_token
    headers = {'Accept': 'application/json', 'Authorization' : auth_header,
                'accept' : 'application/json'}
    r = requests.get(settings.SANDBOX_PROFILE_URL, headers=headers)
    status_code = r.status_code
    response = json.loads(r.text)
    return response, status_code

def getCompanyInfo(access_token, realmId):
    route = '/v3/company/{0}/companyinfo/{0}'.format(realmId)
    auth_header = 'Bearer ' + access_token
    headers = {'Authorization' : auth_header,
                'accept' : 'application/json'}
    r = requests.get(settings.SANDBOX_QBO_BASEURL + route, headers=headers)
    status_code = r.status_code
    response = json.loads(r.text)
    return response, status_code

"""
    The validation steps can be found at ours docs at developer.intuit.com
"""
def validateJWTToken(token):
    is_valid = True
    current_time = (datetime.utcnow() - datetime(1970, 1, 1)).total_seconds()
    token_parts = token.split('.')
    idTokenHeader = json.loads(base64.b64decode(token_parts[0]).decode('ascii'))
    idTokenPayload = json.loads(base64.b64decode(incorrect_padding(token_parts[1])).decode('ascii'))
    
    if idTokenPayload['iss'] != settings.ID_TOKEN_ISSUER:
        return False
    elif idTokenPayload['aud'][0] != settings.CLIENT_ID:
        return False
    elif idTokenPayload['exp'] < current_time:
        return False
    
    token=token.encode()
    token_to_verify = token.decode("ascii").split('.')
    message=token_to_verify[0]+'.'+token_to_verify[1]
    idTokenSignature = base64.urlsafe_b64decode(incorrect_padding(token_to_verify[2]))

    keys = getKeyFromJWKUrl(idTokenHeader['kid'])

    publicKey = jwk.construct(keys)
    return publicKey.verify(message.encode('utf-8'), idTokenSignature)

def getKeyFromJWKUrl(kid):
    jwk_uri = getDiscoveryDocument.jwks_uri
    r = requests.get(jwk_uri)
    if r.status_code >= 400:
        return ''
    data = json.loads(r.text)
    
    key = next(ele for ele in data["keys"] if ele['kid']==kid)
    return key

# for decoding ID Token
def incorrect_padding(s):
    return (s + '=' * (4 - len(s) % 4))

def stringToBase64(s):
    return base64.b64encode(bytes(s,'utf-8')).decode()

"""
    Returns a securely generated random string.
    Source from the django.utils.crypto module.
"""
def getRandomString(length,
                      allowed_chars='abcdefghijklmnopqrstuvwxyz'
                                    'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
    return ''.join(random.choice(allowed_chars) for i in range(length))

"""
    Create a random secret key.
    Source from the django.utils.crypto module.
"""
def getSecretKey():
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    return getRandomString(40, chars)