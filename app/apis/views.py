from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
import json
from core.models import Post, Message, LeadComplete 
import re

# Create your views here.

def salesloftperson(request):
    count = 1
    max_pages = 10 
    while count < max_pages:
        headers = {
            'Authorization': 'Bearer v2_ak_102623_e88ce0ba2b3a3c24bb51555169260804c125cfe04d6f697b0ba36d0fa16ce4b2'

        }
        #url = 'https://api.salesloft.com/v2/people.json?ids=323842909'
        
        url = f'https://api.salesloft.com/v2/crm_activities.json?include_paging_counts=True&per_page=100&page={count}'

        r = requests.get(url, headers=headers)
        status = r.status_code
        data = r.json()
        current_page = data['metadata']['paging']['current_page']
        count= data['metadata']['paging']['current_page'] + 1 
        max_pages = data['metadata']['paging']['total_pages']
        print(current_page)
        print(max_pages)
        """print(current_page)
        print(count)
        print(max_pages)"""
        if data: 

            for i in range(len(data['data'])):
                if data['data'][i]['person']['id'] == 42228998:
                    lead_id = 3
                    leadComplete = LeadComplete.objects.get(pk=lead_id)
                    updatedAt = data['data'][i]['updated_at']
                    createdAt = data['data'][i]['created_at']
                    subject = data['data'][i]['subject']
                    description = data['data'][i]['description']
                    personId = data['data'][i]['person']['id']
                    message = Message.objects.create(leadComplete=leadComplete, createdAt=createdAt,
                    updatedAt=updatedAt, subject=subject, description=description,
                    personId=personId)
                    print(message.subject)
                else:
                    print(data['data'][i]['person']['id'])
            continue

            

def create_post(request):
    posts = Post.objects.all()
    response_data = {}

    if request.POST.get('action') == 'post':
        title = request.POST.get('title')
        description = request.POST.get('description')

        response_data['title'] = title
        response_data['description'] = description

        Post.objects.create(
            title = title,
            description = description,
            )
        return JsonResponse(response_data)

    return render(request, 'connections/modelupdate.html', {'posts':posts}) 

def everstring_update(request):
    headers = {
            'Authorization': 'Token MjhjYjY5ZmUuOTE5NzliMWRjNjI4MDhiNDBhMzQ3NTE4NGIyZmVkOWE='
        }
    url = 'https://api.everstring.com/v1/companies/data_enrich'
    params = {
        'website' : 'www.everstring.com','select': ['alexaRank','businessToBusiness', 'businessToConsumer', 'facilitiesInMultipleLocations', 'financeDeptStrength', 'financeSophistication', 'financeSpend', 'hrDeptStrenght', 'hrSpend',
        'marketingDeptStrenth', 'marketingSpend', 'onlineShoping', 'salesDeptStrength', 'salesSophistication', 'salesSpend', 'shippingMethods', 'shippingProviders', 'socialSophistication', 'techDeptStrength', 'technologySophistication', 'technologySpend', 'numLemmas',
         'inc5000Bucket', 'fortune500Bucket', 'fundingLatestRound_age', 'numInvestors', 'investorNames', 'fundingStrengthBucket',
         'fundTypes', 'fundingTotalAmount', 'fundingLatestRoundAmount', 'numFundTypes', 'top3Industries', 'top3Websites', 'hasMobileApp', 'latestFundingDate', 'facebookUrl', 'linkedinUrl', 'twitterUrl', 'companyListNames',
         'similarCompanies', 'intentTopic', 'intentTime', 'top5Naics', 
        ]}

    params = {
        'website' : 'www.everstring.com','select': ['alexaRank', 
        ]}

    r = requests.get(url, headers=headers, params=params)