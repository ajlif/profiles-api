from rest_framework import serializers


class HelloSerializer(serializers.Serializer):
    """Serialilizes a name field for testing our APIView"""
    #whenever it receive a post or patch request,validate the input with max_length =10
    name = serializers.CharField(max_length=10)
