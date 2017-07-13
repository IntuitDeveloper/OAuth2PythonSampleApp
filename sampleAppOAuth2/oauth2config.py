
class OAuth2Config:
	
	def __init__(self, issuer='', auth_endpoint='', token_endpoint='', userinfo_endpoint='', revoke_endpoint='', jwks_uri=''):
		self.issuer = issuer
		self.auth_endpoint = auth_endpoint
		self.token_endpoint = token_endpoint
		self.userinfo_endpoint = userinfo_endpoint
		self.revoke_endpoint = revoke_endpoint
		self.jwks_uri = jwks_uri
		
