"""Login Viewset."""
import requests
from django.conf import settings
from django.contrib.auth import logout
from django.utils import timezone
from student_faculty.models import StudentUser,FacultyUser
from rest_framework import viewsets
from rest_framework.response import Response
from login.helpers import perform_login
#from users.models import UserProfile
#from users.serializer_full import UserProfileFullSerializer
from django.http import HttpResponse
import datetime
from django.shortcuts import redirect,render

class LoginViewSet(viewsets.ViewSet):
    """Login"""
    @staticmethod
    def prelogin(request):
        return render(request,"login.html")

    @staticmethod
    def login(request):
        """Log in.
        Uses the `code` and `redir` query parameters."""

        # Check if we have the auth code
        auth_code = request.GET.get('code')
        print('\n\nauth_code', auth_code)
        if auth_code is None:
            return Response({"message": "{?code} is required"}, status=400)

        # Check we have redir param
        redir = 'http://127.0.0.1:8000/login'
        print('redir', redir)
        if redir is None:
            return Response({"message": "{?redir} is required"}, status=400)

        perform_login(auth_code, redir, request)
        try:
            faculty_object = FacultyUser.objects.get(user = request.user)
            return redirect('faculty_home')
        except FacultyUser.DoesNotExist:
            try:
                student_object=StudentUser.objects.get(user=request.user)
                return redirect('student_profile')
            except StudentUser.DoesNotExist:
                return redirect('home')
        now = datetime.datetime.now()
        html = "<html><body>It is now %s.</body></html>" % now
        return HttpResponse(html)

    @staticmethod
    def logout(request):
        """Log out."""

        logout(request)
        #return Response({'message': 'logged out'})
        return redirect('home')


    # @staticmethod
    # def Response(request):
    #     now = datetime.datetime.now()
    #     html = "<html><body>It is now %s.</body></html>" % now
    #     return HttpResponse(html)


'''
    @staticmethod
    def get_user(request):
        """Get session and profile."""

        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return Response({"message": "not logged in"}, status=401)

        # Check if the user has a profile
        try:
            queryset = UserProfileFullSerializer.setup_eager_loading(UserProfile.objects)
            user_profile = queryset.get(user=request.user)
            profile_serialized = UserProfileFullSerializer(
                user_profile, context={'request': request})
        except UserProfile.DoesNotExist:
            return Response({'message': "UserProfile doesn't exist"}, status=500)

        # Count this as a ping
        user_profile.last_ping = timezone.now()
        user_profile.save(update_fields=['last_ping'])

        # Return the details and nested profile
        return Response({
            'sessionid': request.session.session_key,
            'user': request.user.username,
            'profile_id': user_profile.id,
            'profile': profile_serialized.data
        })

'''
from django.http import HttpResponse,HttpRequest
def login_view(request):
    if request.user.is_authenticated:
        try:
            faculty_object = FacultyUser.objects.get(user = request.user)
            return redirect('faculty_home')
        except FacultyUser.DoesNotExist:
            try:
                student_object=StudentUser.objects.get(user=request.user)
                return redirect('student_profile')
            except StudentUser.DoesNotExist:
                return HttpResponse("Some serious error")
    return render(request,'login.html',{})

