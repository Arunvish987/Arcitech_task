from rest_framework import serializers
from .models import *
        
        
class RegistrationModelSerializer(serializers.ModelSerializer):
    # role_type = MassRoleDetailModelSerializer()
    class Meta:
        model = RegistrationModel
        fields = '__all__'


# class ContentModelSerializer(serializers.ModelSerializer):
#     # role_type = MassRoleDetailModelSerializer()
#     class Meta:
#         model = ContentModel
#         fields = '__all__'
        
        
class ContentModelSerializer(serializers.ModelSerializer):
    categories = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = ContentModel
        fields = '__all__'
