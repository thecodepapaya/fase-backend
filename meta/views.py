from rest_framework.permissions import DjangoModelPermissions
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.http import HttpResponseRedirect


from .models import MetaData, DownloadLink
from .serializers import MetadataSerializer


class MetadataViewset(viewsets.ModelViewSet):
    queryset = MetaData.objects.all()
    serializer_class = MetadataSerializer
    permission_classes = [DjangoModelPermissions]

    def list(self, request, *args, **kwargs):
        meta_data = MetaData.objects.all()[0]
        serializer = MetadataSerializer(meta_data)
        return Response(serializer.data)


@api_view(http_method_names=['GET', ])
@permission_classes((permissions.AllowAny,))
def ping(request):
    return Response(status=200)


@api_view(http_method_names=['GET', ])
@permission_classes((permissions.AllowAny,))
def download_apk(request):

    apk_url = DownloadLink.objects.first().apk_download

    return HttpResponseRedirect(apk_url)


@api_view(http_method_names=['GET', ])
@permission_classes((permissions.AllowAny,))
def download_ios(request):

    ios_url = DownloadLink.objects.first().ios_download

    return HttpResponseRedirect(ios_url)
