from rest_framework import serializers

from profiles_api import models


class HelloSerializer(serializers.Serializer):
    """Serialilizes a name field for testing our APIView"""
    #whenever it receive a post or patch request,validate the input with max_length =10
    name = serializers.CharField(max_length=10)

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""
    #work with ModelSerializer: use meta class to configure the serializer to point to a specific model
    class Meta:
        model = models.UserProfile
        # define the list of fields that we want manage with the serializer
        fields = ('id', 'email', 'name', 'password')
        # make password field write only to not allow to users to access the pwd hash
        # so the pwd is used to create or update object not to retrieve object
        extra_kwargs = {
        'password':{
            'write_only': True,
            'style':{'input_type': 'password'}
            }
        }

    # ovveride the create function : cz by default ModelSerializer allow us to
    #create simple object in db,so uses the default create fn of the obj manager
    #to create the objec.ovveride because the pwd that created as a hash is not
    # the clear text pwd i would do by default if we dont ovveride the function.
    #create_user is a fn in models > userProfileManager
    def create(self, validated_data):
        """Create and return a new user"""
        user = models.UserProfile.objects.create_user(
            email = validated_data['email'],
            name = validated_data['name'],
            password = validated_data['password']
        )
        return user
