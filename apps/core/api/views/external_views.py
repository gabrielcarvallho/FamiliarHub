from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from apps.core.services import ExternalService


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cep(request):
    service = ExternalService()

    cep = request.query_params.get('cep', None)
    if cep:
        response = service.request_cep_api(cep)
        return Response(response)
    
    return Response({'detail': 'CEP is required'}, status=status.HTTP_400_BAD_REQUEST)