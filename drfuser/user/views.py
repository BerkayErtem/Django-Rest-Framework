from datetime import datetime
from django.shortcuts import render
from django.contrib import auth
from rest_framework import status, viewsets
from rest_framework.decorators import APIView, api_view, permission_classes
from rest_framework.authentication import TokenAuthentication,SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import json

from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.permissions import IsAuthenticated
from .serializers import (userSerializer, updateUser, CompanySerializer, subsidiarySerializer, MyTokenObtainPairSerializer, RefreshTokenSerializer,
imageSerializer, ChangePasswordSerializer, FormSerializer, updateForm)
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Subsidiary, User, Company, Image, Form
from rest_framework import generics
from django.utils.decorators import method_decorator 
from rest_framework import permissions

from rest_framework.exceptions import NotFound


from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import JsonResponse

class FormViewSet(viewsets.ModelViewSet):
    serializer_class=FormSerializer
    queryset=Form.objects.all()
    def delete(self, request, *args, **kwargs):
        return self.destroy(request,*args, **kwargs) 
class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class userViewSet(viewsets.ModelViewSet):
    serializer_class= userSerializer
    queryset=User.objects.all() 
    authentication_classes=(TokenAuthentication,)
    permission_classes = ()
    def delete(self, request, *args, **kwargs):
        return self.destroy(request,*args, **kwargs)

class companyViewSet(viewsets.ModelViewSet):
    serializer_class=CompanySerializer
    queryset=Company.objects.all()
    def delete(self, request, *args, **kwargs):
        return self.destroy(request,*args, **kwargs) 

class subsidiaryViewSet(viewsets.ModelViewSet):
    serializer_class=subsidiarySerializer
    queryset=Subsidiary.objects.all()
    def delete(self, request, *args, **kwargs):
        return self.destroy(request,*args, **kwargs) 

class imageViewSet(viewsets.ModelViewSet):
    serializer_class=imageSerializer
    queryset=Image.objects.all()
    def delete(self, request, *args, **kwargs):
        return self.destroy(request,*args, **kwargs) 


class updateUserView(generics.UpdateAPIView): 

    queryset = User.objects.all() 
    serializer_class = updateUser
    permission_classes=(IsAuthenticated,)
class updateFormView(generics.UpdateAPIView):
    queryset=Form.objects.all()
    serializer_class=updateForm
class ChangePasswordView(generics.UpdateAPIView):
    
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

class LogoutView(GenericAPIView):
    serializer_class = RefreshTokenSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, *args):
        sz = self.get_serializer(data=request.data)
        sz.is_valid(raise_exception=True)
        sz.save()
        return Response(status=status.HTTP_204_NO_CONTENT)



def login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        try:
            user= auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user) 
        except:
            raise ValueError
        try:
            if user.is_authenticated:
                msg=('authenticated')
                return JsonResponse(json.dumps(msg), safe=False)
        except:
            msg=('login first')
            #return HttpResponse(msg, content_type='text/plain')
            return JsonResponse(json.dumps(msg), safe=False)
    return HttpResponse('login', content_type='text/plain')

@csrf_exempt
def logout(request):
    auth.logout(request)
    msg='logout'
    return HttpResponse(msg,content_type='text/plain')


# @csrf_exempt
# @login_required
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def k(request):
    import datetime
    now=datetime.datetime.now()
    user=request.user
    print(user)
    return HttpResponse(now, content_type='text/plain')

@csrf_exempt
def forms(request):
    if request.method=='POST':
        i=request.POST.get('i')
    try:
        form=Form.objects.get(id=i)
        if form.approval==True:
            return JsonResponse({'id':form.id,'date':form.date, 'destination':form.destination,'message':'approved'}, safe=False)
        else:
            return JsonResponse({'id':form.id,'date':form.date, 'destination':form.destination,'message':'not approved'}, safe=False)
    except:
        return JsonResponse({'message':' item not found'}, safe=False)
def error404(request, exception):
    msg='custom 404 not found'
    return HttpResponse(request,msg, content_type='text/plain')


class formview(APIView):
    permission_classes=[AllowAny,]
    def post(self,request, *args,**kwargs):
        try:
            i=request.data["i"]
            i=str(i)
            response=Form.objects.filter(id=i)
            form=Form.objects.get(id=i)
            print(form.destination)
            serializer=FormSerializer(response,many=True)
            if form.approval==True:
                return Response({"result":serializer.data,"message":"approved"})
            else:
                return Response({"result":serializer.data,"message":"not approved"})
        except:
             return Response({'message':' item not found'})

class finduserview(APIView):
    permission_classes=[AllowAny,]
    def post(self,request, *args,**kwargs):
        if request.method=='POST':
            username=request.data["username"]
            # id=request.data['id']
        if username:
            response=User.objects.filter(username=username)
            serializer=userSerializer(response,many=True,context={'request': request})
        # if id:
        #     response=User.objects.filter(id=id)
        #     serializer=userSerializer(response,many=True,context={'request': request})
        return Response({"result":serializer.data})
    
        # return Response({'message':' item not found'})

import asyncio
import datetime
def kkk(request):
    
    now=(datetime.datetime.now())
    return now
from asgiref.sync import sync_to_async
def kk(request):

    now = sync_to_async(kkk, thread_sensitive=True)
    print(now)
    return HttpResponse(now,content_type='text/plain')