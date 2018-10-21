from rest_framework import views, serializers, status, viewsets
from rest_framework.response import Response
from .serializer import ProfileSerializer, UserSerializer, WorkersSerializer
from .models import AccountInfoModel, User, WorkerAccountModel

class ProfileView(views.APIView):
    def get(self, request):
        print(request.user)
        serializer = UserSerializer(request.user)
        print(serializer.data)
        if not serializer.data['profile']:
            print('ok')
            get_user = User.objects.get(email=serializer.data['email'])
            new_profile = AccountInfoModel()
            new_profile.user = get_user
            new_profile.save()
            print(new_profile)
            serializer = UserSerializer(instance = get_user)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        print(request.data)
        try:
            profile = AccountInfoModel.objects.get(user=request.data['user'])
        except profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)


class WorkersView(views.APIView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer_worker = WorkersSerializer(data=request.data)
        print(serializer_worker)
        if serializer_worker.is_valid():
            serializer_worker.save()
            return Response(serializer_worker.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer_worker._errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        print(request.data)
        WorkerAccountModel.objects.get(id=request.data['id']).delete()
        return Response(request.data, status=status.HTTP_200_OK)
            