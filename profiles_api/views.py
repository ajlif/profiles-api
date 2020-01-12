from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.
class HelloApiView(APIView):
    """Test API View"""

    def get(self, request, format=None):
        """Returns a list of APIView features"""
        an_apiview =[
        '1',
        '2',
        '3',
        '4',
        ]
        return Response({'message': 'hello', 'numbers are':an_apiview})
