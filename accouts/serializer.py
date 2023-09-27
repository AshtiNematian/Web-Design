from rest_framework import serializers
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from accounts.models import Users

'''
serializer of user for registration
'''


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)

    class Meta:
        model = Users
        fields = ['email', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        return attrs

    def create(self, validated_data):
        return Users.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = Users
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)

    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = Users.objects.get(email=obj['email'])
        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = Users
        fields = ['email', 'password', 'tokens', 'id']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        filtered_user_by_email = Users.objects.filter(email=email)
        user = auth.authenticate(email=email, password=password)

        if filtered_user_by_email.exists() and filtered_user_by_email[0].auth_provider != 'email':
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        return {
            'id': user.id,
            'email': user.email,
            'tokens': user.tokens,

        }

        return super().validate(attrs)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        exclude = (
            'password', 'is_superuser', 'courses', 'is_staff', 'is_active', 'user_permissions', 'groups', 'last_login',)
        read_only_fields = ('email',)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.save()


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Users
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "رمز عبور برابر نیست"})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "رمز عبور قبلی  اشتباه است"})
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})

        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')
