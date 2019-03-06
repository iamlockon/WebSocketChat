from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from .models import Room

def modal(request):
	obj = request.POST
	room_name = obj.get('room_name', None)
	topic = obj.get('topic', None)
	max_capacity = obj.get('max_capacity', None)
	if Room.objects.filter(room_name=room_name).exists() or max_capacity == '':
		return JsonResponse({'isValid': False})
	else:
		#create room.
		room = Room(room_name=room_name, max_capacity=max_capacity, topic=topic)
		room.save()
		return JsonResponse({'isValid': True})
