from django.urls import path, include

from rest_framework.routers import DefaultRouter

from profiles_api import views


# viewset use router in order to generate the different routes available in ViewSet
router = DefaultRouter()
# no need to specify the / in the router endpoint
router.register('hello-viewset', views.HelloViewSet, basename='hello-viewset')
# no need to specify the basename, we have defined queryset nel view
router.register('profile', views.UserProfileViewSet)


urlpatterns = [
    path('hello-view/', views.HelloApiView.as_view()),
    path('login/', views.UserLoginApiView.as_view()),
    path('', include(router.urls))
]
