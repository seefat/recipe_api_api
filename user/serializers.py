from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from django.utils.translation import gettext as _


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['email','password','name']
        extra_kwargs = {'password':{'write_only':True,'min_length':5}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

class AuthTokenSeializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type':'password'},
        trim_whitespace = False,
    )

    def validate(self, attrs):
        email = attrs.get('request')
        password = attrs.get('password')
