from rest_framework.response import Response,Serializer
from django.contrib.auth import login,logout
from django.shortcuts import redirect,render
from django.http import JsonResponse
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.models import Token
from .serializers import SignupSerializer,LoginSerializer,ChangePasswordSerializer
from rest_framework import status
from .models import CustomUser
from rest_framework.decorators import api_view,APIView,permission_classes,authentication_classes
from django.contrib.auth import authenticate,update_session_auth_hash
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
from django.http import Http404
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode

  
#register users
@api_view(["POST"])
def register_users(request):
        data=request.data
        Serializer=SignupSerializer(data=data)
        if Serializer.is_valid():
            Serializer.save()
            return Response({
                "message":"user added",
            })
        return Response({
            "error":Serializer._errors
        },status=status.HTTP_201_CREATED)

class Login(APIView):
    def post(self,request):
        data=request.data
        Serializer=LoginSerializer(data=data)
        if Serializer.is_valid():
            #check for user validity
            if  CustomUser.objects.filter(email=Serializer.data["email"]).exists():
                user=authenticate(email=Serializer.data["email"],password=Serializer.data["password"])
                if user:
                    token, _ = Token.objects.get_or_create(user=user)
                    login(request,user)
                    return Response({
                        "message":"user logged in" ,
                        "token":token.key                                               
                    },status=status.HTTP_200_OK)
                return Response({"message":"details don't match"})
            return Response({"message":"no such user"})
        return Response({
            "error":Serializer._errors
        })
  
@api_view(['GET'])
@authentication_classes([BasicAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == 'GET':
        try:
            # Delete the user's token to logout
            request.user.auth_token.delete()
            logout(request)
            return Response({'message': 'Successfully logged  out.'},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)})              

@api_view(["POST"])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def change_password(request):
    if request.method=="POST":
        Serializer=ChangePasswordSerializer(data=request.data)
        if Serializer.is_valid():
            user=request.user
            if user.check_password(Serializer.data["old_password"]):
                user.set_password(Serializer.data["new_password"])
                user.save()
                update_session_auth_hash(request,user)#update details
                return Response({
                    "message":"password changed successfully",   
                },status=status.HTTP_200_OK)
            return Response({
                 "message":"enter correct old password",
            },status=status.HTTP_400_BAD_REQUEST)
            print(Response.status_code)
        return Response({"message":"invalid data","error":Serializer._errors},status=status.HTTP_400_BAD_REQUEST)        

###############################################################
# for the resetting forgotten passwd                          #
###############################################################


@api_view(["GET"])
def my_users(request):
        data=CustomUser.objects.all()
        Serializer=SignupSerializer(data,many=True)
        return Response({
            "all the users":Serializer.data,
        })    
  

def password_fill(request): 
     pass
    # if request.method=="POST":
    #       new=request.POST["new"]
    #       new2=request.POST["new2"]
    #       token=request.POST["token"]
    # #authenticate token
    #       try:
    #         user_id = urlsafe_base64_decode(token).decode()
    #         user = CustomUser.objects.get(pk=user_id)
    #       except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
    #         return JsonResponse("not found")
    #       if not default_token_generator.check_token(user, token):
    #         raise Http404("Token is invalid.")
    #       else:
              
    # return render(request,"newpasswd.html")

