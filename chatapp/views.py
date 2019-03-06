# chat/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
import json
from django.db.utils import IntegrityError
from django.contrib import messages
from django.urls import reverse
from django import forms
from .logupform import LogupForm
from .models import Room, Message
from datetime import datetime
from django.core import serializers
from urllib import parse
from .forms import UploadFileForm
def mylogin(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect(reverse('view-index'))
	if request.method == 'POST':
		username = request.POST.get('username', None)
		password = request.POST.get('password', None)
		print("{} {}".format(username, password))
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			print("login as {}".format(user))
			# Redirect to a success page.
			
			return HttpResponseRedirect(reverse('view-index'))
		else:
			# Return an 'invalid login' error message.
			print("Invalid login")
			messages.add_message(request, messages.WARNING, 'Invalid login!')
			return HttpResponseRedirect(reverse('view-login'))
	return render(request, 'chatapp/login.html', {})

def mylogout(request):
	print("try logout")
	logout(request)
	messages.add_message(request, messages.SUCCESS, 'Logout successfully!')
	return redirect('/chatapp/')

def index(request):
	if request.user.is_authenticated:
		rooms = Room.objects.all()
		return render(request, 'chatapp/index.html', {"Rooms": rooms})
	else:
		return render(request, 'chatapp/login.html', {})

def mylogup(request):
	context = {}
	if request.method == 'POST':
		form = LogupForm(request.POST)
		context['form'] = form
		if form.is_valid():

			data = form.cleaned_data
			try:
			 	user = User.objects.create_user(data['username'], data['email'], data['password'])
			except IntegrityError:
				context['logmes'] = "Username already exists..."
				print("exists")
				
			except Exception:
				context['logmes'] = "General Exception...."
				
			else:
				message = "New User Created..."
				messages.add_message(request, messages.SUCCESS, message)
				print('user created')
				return HttpResponseRedirect(reverse('view-login'))
		else:
			context['logmes'] = "Invalid fields..."
			return render(request, 'chatapp/logup.html', context)
	context['form'] = LogupForm()
	return render(request, 'chatapp/logup.html', context)

def room(request, room_name):
	print("to room view")
	roomname = parse.unquote(room_name)
	room = Room.objects.get(room_name=roomname)
	extension_list = ['png','jpg','gif','svg'];
	#get latest 25 messages
	messages = (reversed(Message.objects.filter(room=room).order_by('-id')[:25])) if Message.objects.filter(room=room) else {}
	print(messages)
	if request.method == 'GET':
		print("Prerender")
		print("Req user: ", request.user)
		print("get_users: ", room.get_users())
		users = room.get_users()
		if request.user.username not in users:
			users = room.get_users() + [request.user.username]
		print("users after append: ", users)
		room.set_users(users)
		room.save()
		return render(request, "chatapp/room.html", {'messages':messages,'room_name_json': roomname, 'users':users,'extension_list':extension_list})

	if request.method == 'POST':
		serialized_messages = serializers.serialize('json', Message.objects.filter(room=room)[0:25])
		print("In POST!")
		sender = request.user
		text = request.POST.get('text', None)
		timestamp = datetime.now()
		mess = Message(room=room, sender=sender, text=text)
		mess.save()
		print("After POST!")
		return JsonResponse({
			'room_name_json': roomname,
		    'messages':serialized_messages,
		    'timestamp':mess.timestamp,
		})

def chatupdate(request, room_name):
	roomname = parse.unquote(room_name)
	room = Room.objects.get(room_name=roomname)
	extension_list = ['png','jpg','gif','svg'];
	#get latest message
	messages = Message.objects.filter(room=room).order_by('-id')[:1]
	print(messages)
	if request.method == 'GET':
		return render(request, "chatapp/chatupdate.html", {'messages':messages,'room_name_json': roomname,'extension_list':extension_list})


def fileupload(request, room_name):
	'''
	Handle file/photo upload.
	'''
	room = Room.objects.get(room_name=room_name)
	sender = request.user
	if request.method == 'POST':
		print("POST file")
		print(request.FILES)
		print("form is valid.")
		filemess = Message(file=request.FILES['file'],room=room, sender=sender)
		filemess.file.name 
		filemess.save()
		return JsonResponse({
			'file_url': filemess.file.url,
			'timestamp': filemess.timestamp,
			})
	
	return render(request, "chatapp/room.html", {})