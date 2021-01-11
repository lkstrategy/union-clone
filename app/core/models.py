from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                            PermissionsMixin
from django.conf import settings
from urllib.parse import urlparse, quote
import requests
import urllib.request
from datetime import datetime




class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.is_staff = False
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves new superuse"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_client = models.BooleanField(default=False)
    client = models.ForeignKey('Client', on_delete=models.CASCADE, blank=True, null=True)
   

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Client(models.Model):
    """Model to be used for client"""
    name = models.CharField(max_length=255)
    salesloftkey = models.CharField(max_length=255, blank=True)
   

    def __str__(self):
        return self.name


class Lead(models.Model):
    """Lead to be added"""
    name = models.CharField(max_length=255)
    client = models.ForeignKey(
        Client,
        on_delete=models.DO_NOTHING, default=1
    )
    lead = models.ForeignKey('LeadComplete', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class LeadComplete(models.Model):
    """Complete lead info"""
    OPEN = 'open'
    FAVORITE = 'favorite'
    ARCHIVE = 'archived'
    ACCEPTED = 'acccepted'
    STATUS = [
        (OPEN, ('Open')),
        (FAVORITE, ('Favorite')),
        (ARCHIVE, ('Archived')),
        (ACCEPTED, ('Accepted')),   
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
    )
    title=models.CharField(max_length=255)
    time_minutes = models.IntegerField()
    score = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    firstname = models.CharField(max_length=255, blank=True)
    client = models.ForeignKey('Client', on_delete=models.CASCADE, blank=True, null=True)
    email = models.CharField(max_length=255, null=True)
    lastname = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    state = models.CharField(max_length=255, null=True)
    zipCode = models.IntegerField(null=True)
    url = models.CharField(max_length=255, null=True)
    linkedinLead = models.CharField(max_length=255, null=True)
    notes = models.TextField(max_length=500, null=True)
    salesloftId = models.IntegerField(null=True)
    company = models.ForeignKey('CompanyLead', on_delete=models.DO_NOTHING, null=True)
    status = models.CharField(max_length=32, 
        choices=STATUS, 
        default=OPEN
        )

    @property
    def leadName(self):
        return ''.join(
            [self.title,'', self.firstname, '', self.lastname]
        )
    
    def __str__(self):
        return self.leadName

class CompanyLead(models.Model):
    """Company Associated with LeadComplete"""
    name = models.CharField(max_length=255)
    owlerLink = models.CharField(max_length=255)
    craftUrl = models.CharField(max_length=255)
    companyLinkedin = models.CharField(max_length=255)
    url = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=255, null=True)
    estimatedAge = models.CharField(max_length=255, null=True, blank=True)
    employeeBand = models.CharField(max_length=255, null=True, blank=True)
    revenueBand = models.CharField(max_length=255, null=True, blank=True)
    keywords = models.TextField(max_length=1000, null=True, blank=True)
    alexaRank = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    similarCompanyOne = models.CharField(max_length=255, null=True, blank=True)
    similarCompanyTwo = models.CharField(max_length=255, null=True, blank=True)
    similarCompanyThree = models.CharField(max_length=255, null=True, blank=True)
    companyIndustry = models.CharField(max_length=255, null=True, blank=True)
    companyFacebook = models.CharField(max_length=255, null=True, blank=True)



    def save(self, *args, **kwargs):
        url = self.url
        if url is not None:
            headers = {
            'Authorization': 'Token MjhjYjY5ZmUuOTE5NzliMWRjNjI4MDhiNDBhMzQ3NTE4NGIyZmVkOWE='
            }
            apiurl = 'https://api.everstring.com/v1/companies/data_enrich'
            params = {
            'website' : url, 'select': ['alexaRank','businessToBusiness', 'businessToConsumer', 'facilitiesInMultipleLocations', 'financeDeptStrength', 'financeSophistication', 'financeSpend', 'hrDeptStrenght', 'hrSpend',
            'marketingDeptStrenth', 'marketingSpend', 'onlineShoping', 'salesDeptStrength', 'salesSophistication', 'salesSpend', 'shippingMethods', 'shippingProviders', 'socialSophistication', 'techDeptStrength', 'technologySophistication', 'technologySpend', 'numLemmas',
            'inc5000Bucket', 'fortune500Bucket', 'fundingLatestRound_age', 'numInvestors', 'investorNames', 'fundingStrengthBucket',
            'fundTypes', 'fundingTotalAmount', 'fundingLatestRoundAmount', 'numFundTypes', 'top3Industries', 'top3Websites', 'hasMobileApp', 'latestFundingDate', 'facebookUrl', 'linkedinUrl', 'twitterUrl', 'companyListNames',
            'similarCompanies', 'intentTopic', 'intentTime', 'top5Naics','FacebookUrl',
            ]}
            r = requests.get(apiurl, headers=headers, params=params)

            print(r.status_code)
            print('before if')
        
            if r.status_code == 200:
                print('after if')
                data = r.json()
                if self.employeeBand != data['data'][0]['ES_EmployeeBand'] or self.alexaRank != data['data'][0]['ES_AlexaRank']:
                    print(r.content)
                    self.employeeBand = data['data'][0]['ES_EmployeeBand']
                    self.alexaRank = data['data'][0]['ES_AlexaRank']
                    self.estimatedAge = data['data'][0]['ES_EstimatedAge']
                    self.revenueBand = data['data'][0]['ES_RevenueBand']
                    self.city = data['data'][0]['ES_City']
                    self.state = data['data'][0]['ES_State']
                    self.similarCompanyThree = data['data'][0]['ES_SimilarCompanies'][2]['domain']
                    self.similarCompanyTwo = data['data'][0]['ES_SimilarCompanies'][1]['domain']
                    self.similarCompanyOne = data['data'][0]['ES_SimilarCompanies'][0]['domain']
                    self.companyIndustry = data['data'][0]['ES_Industry']
                    try:
                        self.companyFacebook = data['data'][0]['ES_Facebook_Url']
                    except KeyError:
                        self.companyFacebook = "Not available"
                    

                    self.save()
                    
        super(CompanyLead, self).save(*args, **kwargs)
            
    
 

    def __str__(self):
        return self.name


class Engagement(models.Model):
    """Engagement associated with the lead"""
    engagementName = 'Lead Engagement'
    leadComplete = models.ForeignKey('LeadComplete', on_delete=models.DO_NOTHING, null=True)
    touches = models.IntegerField()
    opens = models.IntegerField()
    click = models.IntegerField()
    visits = models.IntegerField()
    pageviews = models.IntegerField()
    active = models.BooleanField(default=False, blank=True)
    replied = models.IntegerField(blank=True, null=True)


    def __str__(self):
        return self.engagementName


class ClientLeadScore(models.Model):
    name = 'Client Lead Score'
    client = models.ForeignKey('Client', on_delete=models.CASCADE, default=1)
    score = models.IntegerField()
    clientAccepted = models.BooleanField(default=False)
    leadComplete = models.ForeignKey('LeadComplete' , on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Post (models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.title

class Message(models.Model):
    leadComplete = models.ForeignKey('LeadComplete', on_delete=models.CASCADE)
    createdAt = models.CharField(max_length=255)
    updatedAt = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    description = models.TextField(max_length=5000)
    personId = models.IntegerField()
    subjectEncoded = models.CharField(blank=True, max_length=255)
    descriptionEncoded = models.TextField(blank=True, max_length=5000)
   
    
   

    def save(self, *args, **kwargs):
        print('in the save') 
        if self.save:
            print('in the thing')
            try: 
                print('in the try')
                """Clean up the updatedat date/time"""
                try:
                    cleanedUpdated = self.updatedAt[:self.updatedAt.index('.')]
                    self.updatedAt = datetime.strptime(cleanedUpdated, "%Y-%m-%dT%H:%M:%S")
                except:
                    print('nothing')

                """Clean up the created date/time"""
                try:
                    cleanedCreated = self.createdAt[:self.createdAt.index('.')]
                    self.createdAt = datetime.strptime(cleanedCreated, "%Y-%m-%dT%H:%M:%S")
                except: 
                    print('nothing')
                    
                
                self.subject = self.subject.replace("Body:","")
                self.subjectEncoded = self.subject.replace("Email:","Re:")
                self.subject = self.subject.replace("Email:","")
                self.description = self.description.replace('\xa0', ' ')
                self.subjectEncoded = quote(self.subject)
                #self.subjectEncoded = self.subject.replace(' ', '%20').replace('\n', '%0A').replace('?', '%3F').replace('=', '%3D')
                #self.subjectEncoded = self.subject.replace(' ', '%20').replace('\n', '%0A')
                self.descriptionEncoded = quote(self.description)
                #self.descriptionEncoded = self.description.replace(' ', '%20').replace('\n', '%0A').replace('?', '%3F').replace('=', '%3D')
                #self.descriptionEncoded = self.description.replace(' ', '%20').replace('\n', '%0A')
                 
            except Exception as e:
                print(e)
        
                    
        super(Message, self).save(*args, **kwargs)

    def __str__(self):
        return self.subject

class NewsArticles(models.Model):
    company = models.ForeignKey('CompanyLead', on_delete=models.CASCADE)
    title = models.TextField(max_length=1000)
    url = models.TextField(max_length=1000)
    description = models.TextField(max_length=1500)
    datePublished = models.CharField(max_length=255)
    provider = models.CharField(max_length=255)

    def __str__(self):
        return self.title