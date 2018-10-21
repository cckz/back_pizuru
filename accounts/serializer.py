from rest_framework import serializers
from .models import AccountInfoModel, User, WorkerAccountModel

class WorkersSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkerAccountModel
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = AccountInfoModel
        fields = '__all__'

#        profile = super(ProfileSerializer, self).create(validated_data)
#        profile.save()
#        return profile


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=True, read_only=True)
    workers = WorkersSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('email', 'profile', 'workers',)
