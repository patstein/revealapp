from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from rest_framework import serializers

User = get_user_model()


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label='Registration Email Address'
    )

    def validate_email(self, email):
        try:
            User.objects.get(email=email)
            raise serializers.ValidationError('User already exists!')
        except User.DoesNotExist:
            return email

    @staticmethod
    def send_registration_email(email, validation_code):
        message = EmailMessage(
            subject='Registration with Jacob',
            body=f'Your registration code is {validation_code}',
            to=[email],
        )
        message.send()

    def save(self, validated_data):
        email = validated_data.get('email')
        new_user = User.objects.create_user(
            username=email,
            email=email,
            # is_active=False,
        )
        self.send_registration_email(
            email=email,
            validation_code=new_user.user_profile.validation_code,
        )
        return new_user


class ValidationSerializer(RegistrationSerializer):
    email = serializers.EmailField(
        label='Validation Email',
        write_only=True,
    )

    code = serializers.CharField(
        label='Validation Code',
        write_only=True,
    )

    password = serializers.CharField(
        label='Password',
        write_only=True,
    )

    password_repeat = serializers.CharField(
        label='Password',
        write_only=True,
    )

    first_name = serializers.CharField(
        label='First Name',
    )

    last_name = serializers.CharField(
        label='Last Name',
    )

    def validate_email(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('User does not exist!')

    def validate(self, data):
        user = data.get('email')
        if data.get('password') != data.get('password_repeat'):
            raise serializers.ValidationError('The two Passwords do not match. Try again!')

        if data.get('code') != user.user_profile.validation_code:
            print('codeee', user.user_profile.validation_code)
            print('code22', data.get('validation_code'))
            raise ValidationError('The code you entered is false. Try again!')

        return data

    def save(self, validated_data):
        user = validated_data.get('email')
        user.first_name = validated_data.get('first_name')
        user.last_name = validated_data.get('last_name')
        user.set_password(validated_data.get('password'))
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name']
