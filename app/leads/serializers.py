from rest_framework import serializers

from core.models import Client, Lead, LeadComplete, ClientLeadScore, Engagement, CompanyLead



class ClientSerializer(serializers.ModelSerializer):
    """Serializer for client objects"""

    class Meta:
        model = Client
        fields = ('id', 'name')
        read_only_fields = ('id',)

class LeadSerializer(serializers.ModelSerializer):
    """Serializer for Lead Objects"""

    class Meta:
        model = Lead
        fields = ('id', 'name')
        read_only_fields = ('id',)

class LeadCompleteSerializer(serializers.ModelSerializer):
    """Serialize a leadComplete"""
    client = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Client.objects.all()
    )
    
    class Meta:
        model = LeadComplete
        fields = (
            'id', 'title', 'time_minutes', 'score', 'link', 'client',
            'email', 'lastname', 'phone', 'city', 'state', 'zipCode', 'url',
            'linkedinLead', 'notes', 'salesloftId', 'company', 
        )
        read_only_fields = ('id',)

class LeadCompleteDetailSerializer(LeadCompleteSerializer):
    """Serialize a LeadComplete Detail"""
    client = ClientSerializer(many=True, read_only=True)


class ClientLeadScoreSerializer(serializers.ModelSerializer):
    """Serialize a leadComplete"""
    leadComplete = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=LeadComplete.objects.all()
    )
    
    class Meta:
        model = ClientLeadScore
        fields = (
            'id', 'name', 'client', 'clientAccepted', 'leadComplete',
        )
        read_only_fields = ('id',)

class ClientLeadScoreDetailSerializer(LeadCompleteSerializer):
    """Serialize a LeadScore Detail"""
    leadComplete = LeadCompleteSerializer(many=True, read_only=True)


class EngagementSerializer(serializers.ModelSerializer):
    """Serialize an Enagement Object"""
    leadComplete = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=LeadComplete.objects.all()
    )
    
    class Meta:
        model = Engagement
        fields = (
            'id', 'engagementName', 'leadComplete', 'touches', 'opens', 'click', 'visits', 'pageviews',
        )
        read_only_fields = ('id',)

class EngagementDetailSerializer(LeadCompleteSerializer):
    """Serialize an Engagement Detail"""
    leadComplete = LeadCompleteSerializer(many=True, read_only=True)


class CompanyLeadSerializer(serializers.ModelSerializer):
    """Serialize an CompanyLead Object"""

    class Meta:
        model = CompanyLead
        fields = (
            'id', 'name', 'owlerLink', 'craftUrl', 
            'companyLinkedin', 'url', 'phone',
        )
        read_only_fields = ('id',)
