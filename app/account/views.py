from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from core.models import User, LeadComplete, CompanyLead, Engagement, ClientLeadScore, Message, NewsArticles
from django.http import HttpResponse, JsonResponse
import requests
import re
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

def register(request):
    if request.method == 'POST':
        #Get form values
        firstName = request.POST['firstname']
        lastName = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        #check if passwords match
        if password == password2:
            #check username
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Account already exists with that email')
                return redirect('register')
            else:
                user = User.objects.create_user(email=email, password=password, name=firstName)
                user.save();
                messages.success(request, 'You are now registered and can log in')
                return redirect('login')

        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    else:
       return render(request, 'account/register.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
       return render(request, 'account/login.html')

def logout(request):
    return redirect(request, 'index')

def dashboard(request):
    leadCompletes = LeadComplete.objects.filter(client=request.user.client)
    
    
    context = {
        'leadCompletes' : leadCompletes
    }
    return render(request, 'account/dashboard.html', context)

def leadCompleteView(request, lead_id):
    leadShow = get_object_or_404(LeadComplete, id=lead_id, client=request.user.client)
    companyLead = leadShow.company
    leadScore = ClientLeadScore.objects.get(leadComplete=lead_id)
    leadEngagement = Engagement.objects.get(leadComplete=lead_id)
    message = Message.objects.order_by('-updatedAt').filter(leadComplete=lead_id)
    article = NewsArticles.objects.order_by('-datePublished').filter(company=companyLead)[:9:1]
    openLead = LeadComplete.objects.all()
    paginator = Paginator(message, 5)
    page = request.GET.get('page')
    paged_messages = paginator.get_page(page)


    def excelcleaner(textstring):
    # This will find any 2 or more spaces and replace with a newline char

        return re.sub('\s{2,}', '\n', textstring)

    context = {
        'leadShow' : leadShow,
        'companyLead' : companyLead,
        'leadScore' : leadScore,
        'leadEngagement' : leadEngagement,
        'leadMessages' : paged_messages,
        'articles' : article,
        'openLeads' : openLead
    }
    
    return render(request, 'account/lead.html', context)
    
def ajax_change_status(request):
    engagement_id = request.GET.get('engagement_id')
    print(engagement_id)
    engagement = Engagement.objects.get(pk=engagement_id)
    slid = engagement.leadComplete.salesloftId
    slkey = engagement.leadComplete.client.salesloftkey
    bearer = f"Bearer {slkey}"
    urlstring = f"https://api.salesloft.com/v2/people.json?ids={slid}"
    if engagement: 
        headers = {
        'Authorization': bearer
        }
        url = urlstring

        r = requests.get(url, headers=headers)
        data = r.json()
        print(data['data'][0]['counts'])
        engagement.touches = data['data'][0]['counts']['emails_sent']
        engagement.opens = data['data'][0]['counts']['emails_viewed']
        engagement.click = data['data'][0]['counts']['emails_clicked']
        engagement.replied = data['data'][0]['counts']['emails_replied_to']
        engagement.save()
        
    else: 
        return HttpResponse('not today')
    return JsonResponse(data)


def ajax_get_news(request):
    leadCompany_id = request.GET.get('leadCompany_id')
    print(leadCompany_id)
    company = CompanyLead.objects.get(pk=leadCompany_id)
    companySearchUrl = company.url
   
    if leadCompany_id: 
        headers = {
        'x-rapidapi-key': "e541337254msh68ba99fc7c0be8bp1aa281jsn23250d6e2913",
        'x-rapidapi-host': "contextualwebsearch-websearch-v1.p.rapidapi.com"
        }
        searchList = f'{companySearchUrl},'
        querystring = {"q": searchList,"pageNumber":"1","pageSize":"10","autoCorrect":"true","safeSearch":"true",
        "withThumbnails":"true","fromPublishedDate":"null","toPublishedDate":"null"}
        url = "https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/search/NewsSearchAPI"

        r = requests.get(url, headers=headers, params=querystring)
        data = r.json()
        
        if data: 
            for i in range(len(data['value'])):
                title = data['value'][i]['title']
                company = company
                articleurl = data['value'][i]['url']
                description = data['value'][i]['description']
                datepublished = data['value'][i]['datePublished']
                provider = data['value'][i]['provider']['name']
                news = NewsArticles.objects.create(title=title, provider=provider, datePublished=datepublished,company=company, url=articleurl, description=description)
            else:
                print('nothing to show')
           

        else: 
            return HttpResponse('not today')
        return JsonResponse(data)

        
def ajax_update_lead_status(request):
    leadComplete_id = request.GET.get('leadComplete_id')
    print(leadComplete_id)
    leadComplete = LeadComplete.objects.get(pk=leadComplete_id)
    
   
    if leadComplete_id:
        leadComplete.status = leadComplete.FAVORITE
        leadComplete.save()
        print('got it')
    else: 
        return HttpResponse('not today')
    return HttpResponse('success')


def ajax_update_lead_archived(request):
    leadComplete_id = request.GET.get('leadComplete_id')
    print(leadComplete_id)
    leadComplete = LeadComplete.objects.get(pk=leadComplete_id)
    
   
    if leadComplete_id:
        leadComplete.status = leadComplete.ARCHIVE
        leadComplete.save()
        print('got it')
    else: 
        return HttpResponse('not today')
    return HttpResponse('success')

   