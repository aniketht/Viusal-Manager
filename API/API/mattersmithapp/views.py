from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
import jwt
from django.core.files.storage import FileSystemStorage 
from django.core.paginator import Paginator
from mattersmithapp.models import *
from functools import wraps
import os
import base64
from mattersmithapp.serializers import *
# Create your views here.
def jwtValidator(func):
    @wraps(func)
    def decorator(request, *args, **kwargs):
        if request.META.get('HTTP_AUTHORIZATION') is not None:
    	   user=Profile.objects.filter(token=request.META['HTTP_AUTHORIZATION']).count()
    	   if user==0:
    	      return Response({'msg' : 'Please provide valid auth token'},status.HTTP_404_NOT_FOUND)
           return func(request, *args, **kwargs)
        else:
            return Response({'msg' : 'Please provide valid auth token'},status.HTTP_404_NOT_FOUND)
    return decorator
class Users(APIView):
	  #@method_decorator(jwtValidator, name='dispatch')
	  def get(self,request):
	  	  print 'hi--------------',
	  	  userData=User.objects.all()
	  	  serializeData = UserSerializer(userData, many=True)
	  	  return Response({"msg":"user list",'status' :status.HTTP_200_OK,'user':serializeData.data})
	  def post(self, request):
	  	  body_unicode = request.body.decode("utf-8")
	  	  body = json.loads(body_unicode)
	  	  serializer = UserSerializer(data=body)
	  	  if serializer.is_valid():
	  	  	User.objects.create_user(username=body['username'], first_name=body['first_name'], last_name=body['last_name'],password=body['password'],email = body['email'])
	  	  	return Response({'success':'User registered successfully'},status.HTTP_200_OK)
	  	  else:
	  	  	return Response({'msg':'error occured while registration ! please enter valid input'},status.HTTP_404_NOT_FOUND)
class login(APIView):
	  def post(self, request):
	  	  if request.method =="POST":
	  	  	 body_unicode = request.body.decode("utf-8")
	  	  	 body = json.loads(body_unicode)
			 username = body["username"]
			 password = body["password"]
			 user = authenticate(username=username, password=password)
			 token=None;
			 if user is not None:
			 	 payload = {'id': user.id,'email': user.email}
			 	 encoded = jwt.encode({'some': payload}, 'secret', algorithm='HS256')
			 	 if user.is_active:
			 	 	user = User.objects.get(pk=user.id)
					user.profile.token =encoded
					user.save()
			 	 	if user.is_superuser and user.is_staff:
			 	 	   return Response({'id' : user.id,'token':encoded, 'username':user.username,'status':status.HTTP_200_OK, 'user':'superuser'})
			 	 	elif user.is_staff:
					    return Response({'id' : user.id,'token':encoded, 'username':user.username,'status':status.HTTP_200_OK, 'user':"admin"})
					else:
						return Response({'id' : user.id,'token':encoded, 'username':user.username,'status':status.HTTP_200_OK, 'user':"user"})
				 else:
				     return Response({"success":"false"}) 
			 else:
			     return Response({'msg' : 'Invalid Credentials ! please enter valid input'},status.HTTP_404_NOT_FOUND)
class project(APIView):
      def post(self,request):
          body_unicode = request.body.decode("utf-8")
          body = json.loads(body_unicode)
          user_id=request.GET.get('user_id')
          project = Projects()
          if Projects.objects.filter(name=body['projectName']).exists():
             return Response({'msg':'Project alredy exits'},status.HTTP_200_OK)
          project.name = body['projectName']
          project.user_id=user_id
          project.save()
          allProject=Projects.objects.filter(user_id=user_id)
          jsondata = ProjectSerializer(allProject,many=True)
          return Response({'msg' : 'project added successfully','project' : jsondata.data},status.HTTP_200_OK)
      def get(self,request):
          user_id=request.GET.get('user_id')
          allProject=Projects.objects.filter(user_id=user_id)
          jsondata = ProjectSerializer(allProject,many=True)
          return Response({'project' : jsondata.data},status.HTTP_200_OK)
class Images(APIView):
      def post(self,request):
          user_id=request.GET.get('user_id')
          # TODO
          pass
                 
          
              
                 
          
	  
			
