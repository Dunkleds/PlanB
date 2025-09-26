from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    email = (request.data.get('email') or '').strip().lower()
    password = request.data.get('password') or ''
    if not email or not password:
        return Response({'error': 'email y password son requeridos'}, status=400)

    # si tu User estándar requiere username:
    username = email.split('@')[0] or email

    try:
        # si usas CustomUser con email como unique, ajusta los campos
        user = User.objects.create_user(username=username, email=email, password=password)
        return Response({'message': 'Usuario creado'}, status=201)
    except IntegrityError:
        return Response({'error': 'El email/usuario ya existe'}, status=409)
