from django.db import models

# Create your models here.
class Bearer:
	def __init__(self, refreshExpiry, accessToken, tokenType, refreshToken, accessTokenExpiry, idToken=None):
		self.refreshExpiry = refreshExpiry
		self.accessToken = accessToken
		self.tokenType = tokenType
		self.refreshToken = refreshToken
		self.accessTokenExpiry = accessTokenExpiry
		self.idToken = idToken