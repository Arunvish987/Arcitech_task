from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from .serializers import *

# password hasher
from argon2 import PasswordHasher
ph = PasswordHasher()

# Create your views here.

# api for user registration
@api_view(['POST'])
def user_registration_api(request):
    # hased_password = ph.hash(request.data['password'])
    # request.data['password'] = hased_password
    
    role_type = MassRoleDetailModel.objects.get(role_num = request.data['role_type'])
    # request.data['role_type'] = role_type
    
    serializer = RegistrationModelSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
   
        user = serializer.instance
        # UserActivityLog.objects.create(user=user, email=user.email,  activity_type='Registration')
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# api for user login
@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if email and password:
        try:
            user = RegistrationModel.objects.get(email=email)
        except RegistrationModel.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # if check_password(password, user.password):
        if user.password == password:
        # if ph.verify(user.password, password):
            refresh = RefreshToken.for_user(user)
            return Response({'message': 'Login successful', 'refresh': str(refresh), 'access': str(refresh.access_token)}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'Both email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    
# api for view all content admin
@api_view(['GET'])
@permission_classes([AllowAny])
def view_all_contents(request):
    get_user_type = request.GET.get('user_type')

    try:
        user = RegistrationModel.objects.get(full_name=get_user_type)
    except RegistrationModel.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if user.role_type.id == 1:
        contents = ContentModel.objects.all()
        serializer = ContentModelSerializer(contents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Unauthorized. Only users with role_type 1 can view all contents.'}, status=status.HTTP_401_UNAUTHORIZED)
    
    
# api for edit content by admin 
@api_view(['PUT', 'PATCH'])
@permission_classes([AllowAny])
def edit_content(request):
    try:
        get_content_id = request.data.get('content_id')
        content = ContentModel.objects.get(pk=get_content_id)
        
        get_user_type = request.data.get('get_user_type')
        user = RegistrationModel.objects.get(full_name=get_user_type)
        
    except ContentModel.DoesNotExist:
        return Response({'error': 'Content not found'}, status=status.HTTP_404_NOT_FOUND)

    if user.role_type.id == 1:
        content.title = request.data.get('title', content.title)
        content.body = request.data.get('body', content.body)
        content.summary = request.data.get('summary', content.summary)

        category_names = request.data.get('categories', [])
        content.categories.set(CategoryModel.objects.filter(name__in=category_names))

        content.save()
        return Response({
            'id': content.id,
            'title': content.title,
            'body': content.body,
            'summary': content.summary,
            'document': content.document.url,
            'user_type': content.user_type.id,
            'categories': [category.name for category in content.categories.all()],
        }, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Unauthorized. Only users with role_type 1 can edit content.'}, status=status.HTTP_401_UNAUTHORIZED)
    
    
# api for delete content by admin  
@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_content(request):
    try:
        get_content_id = request.data.get('content_id')
        content = ContentModel.objects.get(pk=get_content_id)
        
        get_user_type = request.data.get('get_user_type')
        user = RegistrationModel.objects.get(full_name=get_user_type)
        
    except ContentModel.DoesNotExist:
        return Response({'error': 'Content not found'}, status=status.HTTP_404_NOT_FOUND)

    if user.role_type.id == 1:
        content.delete()
        return Response({'message': 'Content deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({'error': 'Unauthorized. Only users with role_type 1 can delete content.'}, status=status.HTTP_401_UNAUTHORIZED)
    
    
    
# api for create content by author
@api_view(['POST'])
@permission_classes([AllowAny])
def create_content(request):
    get_user_type = request.data.get('get_user_type')
    user = RegistrationModel.objects.get(full_name=get_user_type)
    
    if user.role_type.id == 2:
        data = {
            'title': request.data.get('title', ''),
            'body': request.data.get('body', ''),
            'summary': request.data.get('summary', ''),
            'document': request.data.get('document', ''),
            'categories': request.data.get('categories', []),
            'user_type': user.id,
        }
        
        serializer = ContentModelSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Unauthorized. Only users with role_type 1 can create content.'}, status=status.HTTP_401_UNAUTHORIZED)
    
    
# api for view content by author
@api_view(['GET'])
@permission_classes([AllowAny])
def view_author_contents(request):
    get_user_type = request.GET.get('get_user_type')
    user = RegistrationModel.objects.get(full_name=get_user_type)
    
    if user.role_type.id == 2:
        contents = ContentModel.objects.filter(user_type=user)
        data = [
            {
                'id': content.id,
                'title': content.title,
                'body': content.body,
                'summary': content.summary,
                'document': content.document.url,
                'user_type': content.user_type.id,
                'categories': [category.name for category in content.categories.all()],
            }
            for content in contents
        ]
        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Unauthorized. Only users with role_type 1 can view their own contents.'}, status=status.HTTP_401_UNAUTHORIZED)
    
    
# api for edit content by author
@api_view(['PUT', 'PATCH'])
@permission_classes([AllowAny])
def edit_author_content(request):
    try:
        get_content_id = request.data.get('content_id')
        content = ContentModel.objects.get(pk=get_content_id)
        
        get_user_type = request.data.get('get_user_type')
        user = RegistrationModel.objects.get(full_name=get_user_type)
        
    except ContentModel.DoesNotExist:
        return Response({'error': 'Content not found'}, status=status.HTTP_404_NOT_FOUND)

    if user.id == content.user_type.id:
        content.title = request.data.get('title', content.title)
        content.body = request.data.get('body', content.body)
        content.summary = request.data.get('summary', content.summary)

        category_names = request.data.get('categories', [])
        content.categories.set(CategoryModel.objects.filter(name__in=category_names))

        content.save()
        return Response({
            'id': content.id,
            'title': content.title,
            'body': content.body,
            'summary': content.summary,
            'document': content.document.url,
            'user_type': content.user_type.id,
            'categories': [category.name for category in content.categories.all()],
        }, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Unauthorized. You can only edit your own content.'}, status=status.HTTP_401_UNAUTHORIZED)
    
    
   
# api for delete content by author 
@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_author_content(request):
    try:
        get_content_id = request.data.get('content_id')
        content = ContentModel.objects.get(pk=get_content_id)
        
        get_user_type = request.data.get('get_user_type')
        user = RegistrationModel.objects.get(full_name=get_user_type)
        
        # content = ContentModel.objects.get(pk=content_id)
    except ContentModel.DoesNotExist:
        return Response({'error': 'Content not found'}, status=status.HTTP_404_NOT_FOUND)

    if user.id == content.user_type.id:
        content.delete()
        return Response({'message': 'Content deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({'error': 'Unauthorized. You can only delete your own content.'}, status=status.HTTP_401_UNAUTHORIZED)
    
    

# api for search content
@api_view(['GET'])
@permission_classes([AllowAny])
def search_contents(request):
    search_term = request.GET.get('search_word', '').strip()

    if not search_term:
        return Response({'error': 'Search term is required'}, status=status.HTTP_400_BAD_REQUEST)

    contents = ContentModel.objects.filter(
        models.Q(title__icontains=search_term) |
        models.Q(body__icontains=search_term) |
        models.Q(summary__icontains=search_term) |
        models.Q(categories__name__icontains=search_term)
    ).distinct()

    data = [
        {
            'id': content.id,
            'title': content.title,
            'body': content.body,
            'summary': content.summary,
            'document': content.document.url,
            'user_type': content.user_type.id,
            'categories': [category.name for category in content.categories.all()],
        }
        for content in contents
    ]

    return Response(data, status=status.HTTP_200_OK)





    





