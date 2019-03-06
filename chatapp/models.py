from django.db import models
import json 

# Create your models here.

class Room(models.Model):
    room_name = models.CharField(max_length=30,blank=False)
    topic = models.CharField(max_length=30, blank=False, default='Programming')
    max_capacity = models.IntegerField(blank=False, default=2)
    users = models.CharField(max_length=200, default=list())

    def __str__(self):
    	return self.room_name

    def set_users(self, x):
        self.users = json.dumps(x)

    def get_users(self):
        return json.loads(self.users)
class Message(models.Model):
	room = models.ForeignKey(
		'Room',
		on_delete=models.CASCADE,
	)
	timestamp = models.DateTimeField(auto_now_add=True)
	sender = models.CharField(max_length=50)
	text = models.CharField(max_length=255,blank=True)
	file = models.FileField(upload_to='documents/',blank=True)

	def __str__(self):
		return self.text
	def get_extension(self):
		return self.file.name.split('.')[1].lower()
	def get_filename(self):
		return self.file.name.split('/')[1]