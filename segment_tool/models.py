from django.db import models
import os
# Create your models here.

class Image (models.Model): 
	image = models.ImageField(upload_to='images/')
	#kernel (x,y) 
	kernel_x = models.IntegerField(default=48) 
	kernel_y = models.IntegerField(default=48)	
	processed_image = models.ImageField(upload_to='processed_images/', blank=True) 






