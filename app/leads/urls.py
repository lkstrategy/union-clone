from django.urls import path, include
from rest_framework.routers import DefaultRouter

from leads import views


router = DefaultRouter()
router.register('clients', views.ClientViewSet)
router.register('leads', views.LeadViewSet)
router.register('leadComplete', views.LeadCompleteViewSet)
router.register('clientleadscore', views.ClientLeadScoreViewSet)
router.register('engagement', views.EngagementViewSet)
router.register('company', views.CompanyLeadViewSet)

app_name = 'leads'

urlpatterns = [
    path('', include(router.urls))
]
