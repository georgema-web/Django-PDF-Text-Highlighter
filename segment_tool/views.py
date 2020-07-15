from django.shortcuts import render, redirect
from django.http import HttpResponse 
from .forms import ImageForm
from .models import Image
from .logic.segment_logic import extract_jpg_regions
from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile
from .serializers import ImageSerializer
from rest_framework import generics

#temporary 
import pdb 

# Create your views here.
class ImageListCreate (generics.ListCreateAPIView): 
    
    serializer_class = ImageSerializer 
    
    def get_queryset(self): 
        queryset = Image.objects.all()
        query_pk = self.request.query_params.get('query_pk', None)
        if query_pk:
            queryset = queryset.filter(pk=query_pk)
        return queryset 
   
   
    
'''
#legacy views
def upload(request):
    if request.method == 'POST': 
        form = ImageForm (request.POST, request.FILES) 

        if form.is_valid():
            image_model = form.save()
#            request.session['img_url'] = image_model.image.url
            request.session['img_id'] = image_model.pk  
            return redirect('/segment_tool/segment') #doesn't work, try something else 
    else: 
        form = ImageForm () 
    return render (request, 'segment_tool/upload.html', {'form':form})
        
#main view 
def segment(request): 
    if request.method=='GET': 
        img_id = request.session.get('img_id') 
        image_model = Image.objects.get(pk=img_id)
        img_url = image_model.image.url
        kernel_x = image_model.kernel_x 
        kernel_y = image_model.kernel_y
        
        width = 300
        height = 300
        
        proc_img_name, proc_img = extract_jpg_regions(image_model.image, width, height, (kernel_x, kernel_y))
        
        image_model.processed_image.save(proc_img_name, InMemoryUploadedFile(
            proc_img, 
            None, 
            proc_img_name, 
            'image/jpeg', 
            proc_img.tell,
            None
            )
        )
        img_url = image_model.processed_image.url  
        
    return render(request, 'segment_tool/segment.html', {'img_url' : img_url, 'img_id': img_id, 'kernel_x': kernel_x, 'kernel_y':kernel_y})

def increase_kernel(request): 
    if request.method=='POST': 
        img_id = request.POST.get('img_id') 
        image_model = Image.objects.get(pk=img_id)
        image_model.kernel_x += 1 
        image_model.kernel_y += 1
        image_model.save()
        return HttpResponse("success") 
        
def decrease_kernel(request): 
    if request.method=='POST': 
        img_id = request.POST.get('img_id') 
        image_model = Image.objects.get(pk=img_id)
        image_model.kernel_x -= 1 
        image_model.kernel_y -= 1
        image_model.save()
        return HttpResponse("success") 
'''
