from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Client, Lead, LeadComplete, ClientLeadScore, Engagement, CompanyLead

from leads import serializers
from urllib.parse import urlparse


class BaseLeadsAttrViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    """Base viewset for user owned lead attributes"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create new object"""
        serializer.save(user=self.request.user)




class ClientViewSet(BaseLeadsAttrViewSet):
    """Manage tags in the database"""
    queryset = Client.objects.all()
    serializer_class = serializers.ClientSerializer


class LeadViewSet(BaseLeadsAttrViewSet):
    """Manage leads in the database"""
    queryset = Lead.objects.all()
    serializer_class = serializers.LeadSerializer

class LeadCompleteViewSet(viewsets.ModelViewSet):
    """Manage LeadComplete in the database"""
    serializer_class = serializers.LeadCompleteSerializer
    queryset = LeadComplete.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def _params_to_insts(self, qs):
        """Convert a list of string ids to a list of integers"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Retrieve the leadcomplete for the authed user"""
        client = self.request.query_params.get('client')
        email = self.request.query_params.get('email')
        queryset = self.queryset
        if client and email:
            client_ids = self._params_to_insts(client)
            queryset = queryset.filter(client__id__in=client_ids).filter(email=email)
        return queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.LeadCompleteDetailSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new leadComplete"""
        serializer.save(user=self.request.user)

class ClientLeadScoreViewSet(viewsets.ModelViewSet):
    """Manage ClientLeadScore in the database"""
    serializer_class = serializers.ClientLeadScoreSerializer
    queryset = ClientLeadScore.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def _params_to_insts(self, qs):
        """Convert a list of string ids to a list of integers"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Retrieve the ClientLeadScore for the authed user"""
        queryset = ClientLeadScore.objects.all()
        leadComplete = self.request.query_params.get('leadComplete', None)
        if leadComplete is not None:
            queryset = queryset.filter(leadComplete=leadComplete)
        return queryset

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.ClientLeadScoreDetailSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new leadComplete"""
        serializer.save(leadComplete=self.leadComplete)


class EngagementViewSet(viewsets.ModelViewSet):
    """Manage Engagement in the database"""
    serializer_class = serializers.EngagementSerializer
    queryset = Engagement.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def _params_to_insts(self, qs):
        """Convert a list of string ids to a list of integers"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Retrieve the Engagement for the leadComplete"""
        queryset = Engagement.objects.all()
        leadComplete = self.request.query_params.get('leadComplete', None)
        if leadComplete is not None:
            queryset = queryset.filter(leadComplete=leadComplete)
        return queryset

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.EngagementDetailSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new enagement"""
        serializer.save()

class CompanyLeadViewSet(viewsets.ModelViewSet):
    """Manage Engagement in the database"""
    serializer_class = serializers.CompanyLeadSerializer
    queryset = CompanyLead.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    

    def _params_to_insts(self, qs):
        """Convert a list of string ids to a list of integers"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Retrieve the Engagement for the leadComplete"""
        queryset = CompanyLead.objects.all()
        url = self.request.query_params.get('url', None)
        if url is not None:
            queryset = queryset.filter(url=url)
        return queryset
        

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.CompanyLeadSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new enagement"""
        url = urlparse(self.request.data['url']).netloc
        urlstr = str(url)
        urllower = urlstr.lower()
        
        serializer.save(url= urllower)