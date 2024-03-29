from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import UserProfile, State, City


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone_number',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i, v in enumerate(self.fields['phone_number'].validators):
            if isinstance(v, UniqueValidator):
                del self.fields['phone_number'].validators[i]

    def create(self, validated_data):
        try:
            instance = User.objects.get(phone_number=validated_data['phone_number'])
        except User.DoesNotExist:
            instance = User.objects.create_user(phone_number=validated_data['phone_number'], verify_codes=validated_data['verify_code'])
        else:
            instance.set_verify_code(validated_data['verify_code'])
            instance.save(update_fields=['verify_codes'])

        return instance


class ProfileSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(source='user.username', read_only=True)
    # first_name = serializers.CharField(source='user.first_name', required=False, allow_blank=True)
    # last_name = serializers.CharField(source='user.last_name', required=False, allow_blank=True)
    # gender = serializers.BooleanField(required=True)
    state_id = serializers.SerializerMethodField()
    # city_name = serializers.SerializerMethodField()
    is_paid = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        exclude = ('id', 'user')

    def get_is_paid(self, instance):
        if instance.user.payment_set.filter(paid_status=True):
            return True
        return False

    def get_state_id(self, instance):
        return instance.city.state.id

    # def get_city_name(self, instance):
    #     return instance.city.city_name

    def validate_email(self, value):
        request = self.context['request']
        user = request.user
        if user.email is not None:
            raise serializers.ValidationError(_('Email has already been set.'))
        if User.objects.filter(email=value).exclude(id=user.id).exists():
            raise serializers.ValidationError(_('User with this Email already exists.'))
        return value

    def validate_phone_number(self, value):
        request = self.context['request']
        user = request.user
        if user.phone_number is not None:
            raise serializers.ValidationError(_('Phone Number has already been set.'))
        if User.objects.filter(phone_number=value).exclude(id=user.id).exists():
            raise serializers.ValidationError(_('User with this Phone Number already exists.'))
        return value

    def create(self, validated_data):
        request = self.context['request']
        # user = request.user
        validated_data['user'] = request.user
        # user_data = validated_data.get('user')

        try:
            instance = super().create(validated_data)
        except:
            raise serializers.ValidationError(_('User with this Phone Number already exists.'))
        # instance.user.first_name = user_data.get('first_name', instance.user.first_name)
        # instance.user.last_name = user_data.get('last_name', instance.user.last_name)
        # instance.user.save(update_fields=['first_name', 'last_name'])
        return instance

    def update(self, instance, validated_data):
        request = self.context['request']
        # user_data = validated_data.get('user', None)
        # user = request.user
        validated_data['user'] = request.user

        instance = super().update(instance, validated_data)
        # if user_data:
        #     instance.user.first_name = user_data.get('first_name', instance.user.first_name)
        #     instance.user.last_name = user_data.get('last_name', instance.user.last_name)
        #     instance.user.save(update_fields=['first_name', 'last_name'])
        return instance


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'city_name')


class StateSerializer(serializers.ModelSerializer):
    city = serializers.SerializerMethodField()

    class Meta:
        model = State
        fields = ('id', 'state_name', 'city')

    def get_city(self, instance):
        return CitySerializer(instance.city_set.filter(state=instance), many=True).data
