from django.urls import path
from . import views_faculty as vf
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    #Enlist faculty web pages


    path("faculty/home",vf.home,name = "faculty_home"),
    path("faculty/addcourse",vf.addcourse,name = "faculty_addcourse"),
    
    
    #Enlist student web pages

    


]
