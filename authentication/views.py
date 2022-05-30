from rest_framework import viewsets
from .models import Token
from .serializers import TokenSerializer


# class TokenViewset(viewsets.ModelViewSet):
#     serializer_class = TokenSerializer

#     def get_queryset(self):
#         user = self.request.user
#         token = Token.objects.filter(user=user)
#         return token
def login():
    pass
