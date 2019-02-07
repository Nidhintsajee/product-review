# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import sentimental_analysis.senti as s
from collections import defaultdict
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound,JsonResponse
from django.shortcuts import render,render_to_response

from django.core.urlresolvers import reverse
from .models import *

def signout(request):
	logout(request)
	return HttpResponseRedirect('/')

def product(request):
	products= Product.objects.all()
	return render(request,'mens.html',{'products':products})

def single(request,id):
	product = Product.objects.get(id=id)
	reviews = Review.objects.filter(product=product)
	if request.method=='POST':
		name =request.POST.get('Name')
		email=request.POST.get('Email')
		review=request.POST.get('Review')
		rv=Review.objects.filter(user=request.user).exists()
		if request.user.username == name and not rv:
			review1 = Review.objects.update_or_create(user=request.user,product=product,review=review)
			review1.save()
			return render(request,'single.html',{'product':product,'reviews':reviews,'msg1':'Your review added sucessfully','review':review1 })
		else:
			try:
				review1 = Review.objects.get(user=request.user,product=product)
				review1.review = review
				review1.save()
			except Exception as e:
				review1 = Review.objects.update_or_create(user=request.user,product=product,review=review)
				review1.save()
			return render(request,'single.html',{'product':product,'reviews':reviews,'msg':'You edited the review sucessfully','review':review1 })
	return render(request,'single.html',{'product':product,'reviews':reviews})

def log_in(request):
	try:
		if request.method == "POST":
			phone = request.POST.get('phone')
			password = request.POST.get('password')
			user = authenticate(username=phone, password=password)
			if user:
				user_pro = UserProfile.objects.get(user=user)
				if user_pro:
					login(request, user)
					return HttpResponseRedirect(reverse('home_url'))
				else:
					error = "You are not OTP Verified User! please Signup and verify"
					return render(request, 'login.html', {'error': error})
			else:
				error = " Sorry! Phone Number and Password didn't match, Please try again ! "
				return render(request, 'login.html', {'error': error})
		else:
			return render(request, 'login.html', {})
	except Exception as e:
		print ("error", e)
		return HttpResponseRedirect(reverse('home_url'))



def sign_up(request):
	try:
		if request.method == 'POST':
			
			name = request.POST.get('name')
			email = request.POST.get('email')
			phone = request.POST.get('phone')
			pass_1 = request.POST.get('pass1')

			request.session.modified = True
			user_em = User.objects.filter(email=email).exists()
			user_ph = User.objects.filter(username=str(phone)).exists()
			if not user_em and not user_ph:
				user = User.objects.create_user(
					username=phone,
					email=email,
					first_name=name,
					password=pass_1,
				)
				try:
					user_pro = UserProfile(
						user=user,
						email=email,
						phone_no=phone,
					)
					user_pro.save()
				except Exception as e:
					print ("error", e)
					pass
				return render(request, 'login.html', {'phone': phone})
			else:				
				error = " Email or Phone-Number already exists "
				return render(request, 'signup.html', {'error': error})
		else:
			return render(request, 'signup.html',{})
	except Exception as e:
		print("errror",e)
		return HttpResponseRedirect(reverse('home_url'))


def search(request):
	en=0
	if request.method == 'POST':
		name=request.POST.get('hashtag')
		c=request.POST.get('hash_count')
		print("count",c)
		c=int(c)

		# for tweet in tweepy.Cursor(api.search,q=name,count=int(c),lang="en",
		# 						   since="2018-01-01").items():
		tweets =get_tweets(query = name, count = c)
		if tweets and '#' in name and name:

			dd = defaultdict(list)
			for d in list(tweets): # you can list as many input dicts as you want here
				for key, value in d.items():
					dd[key].append(value)
			print("dd",dict(dd))
			dd=dict(dd)
			# del dd['sentiment']
			dd=','.join(dd['text'])

			# print ("dd",str(dd))
			dd=str(dd)
			a=dd.split(',')
				# print (tweet.created_at, tweet.text)
			print("a",len(a))
			en=1

			# pos =[]
			# neg = []
			# neutral = []
			
			# for dd in a:
			# 	# try:
			# 	print(list(s.sentiment(dd))[1])	
			# 	if 'pos' in s.sentiment(dd) and list(s.sentiment(dd))[1] == 1.0:
			# 		pos.append(dd)
			# 	if 'neg' in s.sentiment(dd) and list(s.sentiment(dd))[1] == 1.0:
			# 		neg.append(dd)
			# 	if list(s.sentiment(dd))[1]< 1:
			# 		neutral.append(dd)	
			# 	# except Exception as e:
			# 	# 	pass
			# print('tweets',len(pos)+len(neg)+len(neutral))
			# positive_perc = (100*len(pos)/len(a))
			# negative_perc = (100*len(neg)/len(a))
			# neutral_perc = (100*len(neutral)/len(a))
			return render(request,'senti.html',{'tweets':a,'name1':name,'c':c,'en':en})
		else:
			return render(request,'index.html',{'error1':'oops!! Please Enter valid twitter account'})
	else:
		return render(request,'index.html')

# Create your views here.
def home(request):
	products= Product.objects.all()

	en=0
	if request.method == 'POST':
		p_id=request.POST.get('product')

		product = Product.objects.get(id=p_id)
		reviews = Review.objects.filter(product=product)
		print (reviews)
		
		en=1
		return render(request,'senti.html',{'products':products,'reviews':reviews,'en':en,'product':product})

	else:
		return render(request,'index.html',{'products':products})




def senti(request):
	en=0
	if request.method == 'POST':
		p_id=request.POST.get('product')

		product = Product.objects.get(id=p_id)
		name=product
		reviews = Review.objects.filter(product=product)
		print (reviews)
		if reviews:
			dd=[]
			for r in reviews:
				dd.append(r.review)

			# print ("dd",str(dd))
			# dd=str(dd)
			# 
			dd=','.join(dd)
			a=dd.split(',')
			# print (a,dd)
		pos =[]
		neg = []
		neutral = []
		print("numberof review", len(a))
		for dd in a:
			try:
				if 'pos' in s.sentiment(dd):
					if list(s.sentiment(dd))[1]< 1:
						neutral.append(dd)
					else:
						pos.append(dd)

				if 'neg' in s.sentiment(dd):
					if list(s.sentiment(dd))[1]< 1:
						neutral.append(dd)
					else:
						neg.append(dd)
			except Exception as e:
				print (e)
				pass
		en=0
		positive_perc = (100*len(pos)/len(a))
		negative_perc = (100*len(neg)/len(a))
		neutral_perc = (100*len(neutral)/len(a))
		return render(request,'senti.html',{'ptweets':pos,'nstv_perc':negative_perc,'pstv_perc':positive_perc,'ntweets':neg,'neutral_perc':neutral_perc,'neutral':neutral,'name1':name,'en':en})
	else:
		return render(request,'senti.html')
