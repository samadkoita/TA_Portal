from django.urls import path
from . import views_faculty as vf
from . import views_student as vs
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
    #Enlist faculty web pages


    path("faculty/home/",vf.home,name = "faculty_home"),
    path("faculty/addcourse/",vf.addcourse,name = "faculty_addcourse"),
    path("faculty/<cn>/<sem>/<ye>/",vf.ListApplicants,name ="faculty_applications"),
    path("student/profile",vs.homepage,name="student_profile"),
    #Enlist student web pages
    path("student/courses",vs.CourseList.as_view(),name='course_list'),
    path("student/applications",vs.ApplicationList.as_view(),name='application_list'),
    path("student/edit/",vs.editdetails,name="edit_details"),
    path("student/<cn>/<sem>/<ye>/",vs.applications,name="student_application")
]

