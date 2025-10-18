from .views import *
from django.urls import path, include
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router=routers.DefaultRouter()
router.register('users',UserViewSet,basename='users')
router.register('expenses', ExpensesViewSet, basename='expenses')
router.register('plans',PlanViewSet,basename='plans')
plans_router=routers.NestedDefaultRouter(router,'plans',lookup='plan')
plans_router.register('planitems',PlanItemViewSet,basename='planitems')

# router.register('planitems',PlanItemViewSet,basename='planitems')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(plans_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

]
