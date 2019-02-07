# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User

class UserProfile(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	email = models.CharField(max_length=30)
	phone_no = models.CharField(max_length=20)

	def __str__(self):
		return str(self.user.username)

class Product(models.Model):
	name = models.CharField(max_length=30)
	price = models.CharField(max_length=30)
	image = models.ImageField(upload_to='product_image')
	description = models.TextField()

	def __str__(self):
		return str(self.name)

class Review(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	review = models.TextField()

	def __str__(self):
		return str(self.user.username+'-'+self.product.name)
