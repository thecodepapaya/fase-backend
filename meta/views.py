from rest_framework import permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import MetaData
from .serializers import MetadataSerializer


class MetadataViewset(viewsets.ModelViewSet):
    queryset = MetaData.objects.all()
    serializer_class = MetadataSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def list(self, request, *args, **kwargs):
        meta_data = MetaData.objects.all()[0]
        serializer = MetadataSerializer(meta_data)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(http_method_names=['GET', ])
@permission_classes((permissions.AllowAny,))
def ping(request):
    return Response(status=200)
