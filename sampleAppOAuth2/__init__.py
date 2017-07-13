from django.conf import settings
import requests
from .oauth2config import OAuth2Config

def getDiscoveryDocument():
    r = requests.get(settings.DISCOVERY_DOCUMENT)
    if r.status_code >= 400:
        return ''
    discovery_doc_json = r.json()
    discovery_doc = OAuth2Config(
        issuer=discovery_doc_json['issuer'], 
        auth_endpoint=discovery_doc_json['authorization_endpoint'], 
        userinfo_endpoint=discovery_doc_json['userinfo_endpoint'], 
        revoke_endpoint=discovery_doc_json['revocation_endpoint'], 
        token_endpoint=discovery_doc_json['token_endpoint'], 
        jwks_uri=discovery_doc_json['jwks_uri'])
    
    return discovery_doc

getDiscoveryDocument=getDiscoveryDocument()