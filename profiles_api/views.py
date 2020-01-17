from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters

from profiles_api import serializers
from profiles_api import models
from profiles_api import permissions

# for login api viewset
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
# permission : make the vieset readonly if the user is not authenticated
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class HelloApiView(APIView):
    """Test API View"""
    #configure the api view to have the serializer class
    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """Returns a list of APIView features"""
        an_apiview =[
        '1',
        '2',
        '3',
        '4',
        ]
        return Response({'message': 'hello', 'numbers are':an_apiview})

    def post(self, request):
        """Create hello message with our name"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # name field is defined in the serializer
            name = serializer.validated_data.get('name')
            # use f string functionality & {} to insert variable into string
            message = f'Hello {name}'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
                )

    # update the object identified by id not by primary key pk
    # update by replacing the old object with the object that was provided
    def put(self, request, pk=None):
        """Handle updating an object"""
        return Response({'method': 'PUT'})

    # update an object with only the field provided in the request
    def patch(self, request, pk=None):
        """Handle a partial update of an object"""
        return Response({'method': 'PATCH'})

    def delete(self, request, pk=None):
        """Delete an object"""
        return Response({'method': 'DELETE'})


class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet"""
    serializer_class = serializers.HelloSerializer

    def list(self, request):
        """Return a hello message."""
        a_viewset = [
            'Uses actions (list, create, retrieve, update, partial_update)',
            'Automatically maps to URLS using Routers',
            'Provides more functionality with less code',
        ]

        return Response({'message': 'Hello!', 'a_viewset': a_viewset})

    def create(self, request):
        """Create a new hello message"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'hello {name}!'
            return Response({'message':message})
        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
                )

    def retrieve(self, request, pk=None):
        """Handle getting an object by its ID"""

        return Response({'http_method': 'GET'})

    def update(self, request, pk=None):
        """Handle updating an object"""

        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        """Handle updating part of an object"""

        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None):
        """Handle removing an object"""

        return Response({'http_method': 'DELETE'})


# ModelViewSet : managing models throgh our api
# viewset access the serializer through an endpoint
class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()

    # authentication and permission
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)

    #search profile
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)


class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    # ObtainAuthToken is handy and we could add it directly to the urls.py
    # however it doesnt by default enable itself in the browsable django admin site
    # so we need to customise this class to make it browsable api to make easy for us to test
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating , reading and updating profile feed items"""
    # authentication
    authentication_classes = (TokenAuthentication,)
    # set the serializer class of this viewset to ProfileFeedItemSerializer
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()

    # add permissions
    permission_classes = (
        permissions.UpdateOwnStatus,
        IsAuthenticated
    )

    # customise the behaviour for creating object over the viewset.
    # get called every time we make http post to viewset
    def perform_create(self, serializer):
        """sets the user profile to the logged in user"""
        # adding TokenAuthentication to the viewset :if the user is autheticated than the user is associated in the req
        # save fn of the serializer : save content of the object in the db.
        # user_profile will be passed in addition to all the item of the serializer
        serializer.save(user_profile = self.request.user)


