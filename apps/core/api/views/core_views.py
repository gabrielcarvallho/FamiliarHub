import requests

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cep(request):
    cep = request.query_params.get('cep', None)

    if cep:
        cep = cep.replace('-', '').replace('.', '').replace(' ', '')

        if len(cep) != 8:
            return Response({'detail': 'Invalid CEP.'}, status=status.HTTP_400_BAD_REQUEST)

        url = f'https://viacep.com.br/ws/{cep}/json/'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            if 'erro' in data:
                return Response({'detail': 'CEP not found.'}, status=404)

            return Response(data)
        else:
            return Response({'detail': f'Request error: {response.text}'}, status=response.status_code)
    else:
        return Response({'detail': 'CEP is required.'}, status=status.HTTP_400_BAD_REQUEST)