from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from .models import User

from .service.serializers import UserSerializer
from .service.businness_views import _get_data_anonymous_user


class CreateAnonymousUser(APIView):
    def post(self, request):
        user = User.objects.last()
        data = _get_data_anonymous_user(user)

        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "id": data["id"],
                "username": data["username"],
                "password": data["password"],
            },
            status=status.HTTP_201_CREATED,
        )
