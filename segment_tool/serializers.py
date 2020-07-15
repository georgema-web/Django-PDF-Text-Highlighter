
from rest_framework import serializers 
from .models import Image 

class ImageSerializer (serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image', 'kernel_x', 'kernel_y', 'processed_image') 
        
