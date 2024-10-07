from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import User
from .serializers import User_Serializer


@login_required(login_url='login')
@api_view(['GET'])
def get_routes(request):
    routes = [
        'GET /api/users',
    ]
    return Response(routes)

@login_required(login_url='login')
@api_view(['GET'])
def get_users(request):
    users = User.objects.all()
    serialized = User_Serializer(users, many=True)

    return Response(serialized.data)