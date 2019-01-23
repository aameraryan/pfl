from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from .models import Prospect, Campaign, Lead, View, DNC
from django.contrib.auth import get_user_model
from random import randint
import datetime
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from .forms import ProspectContactForm



Django_User = get_user_model()


def home(request):
    if request.user.is_authenticated:
        return render(request, 'portal/home.html')
    else:
        return HttpResponseRedirect(reverse('portal:login'))


@login_required
def campaigns(request):
    # req_user = Django_User.objects.get(id=request.user.id)
    # context = {'campaigns': Campaign.objects.filter(Users__in=(req_user,))}
    context = {'campaigns': request.user.campaign_set.all()}
    return render(request, 'portal/campaigns.html', context)


def portal_login(request):
    pass
    # if request.method == 'post':

    # return render(request, 'portal/portal_login.html')


@login_required
def get_prospect(request, campaign_id):
    temp_campaign = get_object_or_404(Campaign, id=campaign_id)
    # prospect_queryset = Prospect.objects.filter(~Q(Released_Campaigns__icontains=temp_campaign.Name), Campaigns__in=(temp_campaign, ))
    prospect_queryset = Prospect.objects.all()
    if prospect_queryset.count() == 0:
        context = {'empty_msg': 'No more prospects in this campaign.'}
        return render(request, 'portal/single_prospect.html', context)
    random_number = randint(0, prospect_queryset.count()-1)
    single_prospect = prospect_queryset[random_number]
    single_prospect.Released_Campaigns += (','+temp_campaign.Name)
    single_prospect.save()
    if single_prospect.Phone != '':
        context = {'prospect': single_prospect, 'campaign': temp_campaign, 'form': 'form'}
    else:
        context = {'prospect': single_prospect, 'campaign': temp_campaign, 'form': 'form'}
    return render(request, 'portal/single_prospect.html', context)


@login_required
def campaign_details(request, campaign_id):
    con_campaign = get_object_or_404(Campaign, id=campaign_id)
    user = request.user
    context = {'campaign': con_campaign, 'user': user}
    return render(request, 'portal/campaign_details.html', context)


@login_required
def make_lead(request, prospect_id, campaign_id):
    lead_prospect = get_object_or_404(Prospect, id=prospect_id)
    lead_campaign = get_object_or_404(Campaign, id=campaign_id)
    lead_user = get_object_or_404(Django_User, id=request.user.id)
    Lead.objects.create(Prospect=lead_prospect, Campaign=lead_campaign, Lead_User=lead_user, Lead_On=datetime.date.today())
    lead_prospect.Released_Campaigns += lead_campaign.Name
    lead_prospect.Lead_Count += 1
    lead_prospect.save()

    return HttpResponseRedirect('/get_prospect/'+campaign_id+'/')


@login_required
def make_dnc(request, prospect_id, campaign_id):
    dnc_prospect = get_object_or_404(Prospect, id=prospect_id)
    dnc_campaign = get_object_or_404(Campaign, id=campaign_id)
    dnc_user = get_object_or_404(Django_User, id=request.user.id)
    DNC.objects.create(Prospect=dnc_prospect, Campaign=dnc_campaign, DNC_User=dnc_user, DNC_On=datetime.date.today())
    # dnc_prospect.delete()
    return HttpResponseRedirect('/get_prospect/'+campaign_id+'/')


@login_required
def make_view(request, prospect_id, campaign_id):
    view_prospect = get_object_or_404(Prospect, id=prospect_id)
    view_campaign = get_object_or_404(Campaign, id=campaign_id)
    view_user = get_object_or_404(Django_User, id=request.user.id)
    view_prospect.View_Count += 1
    view_prospect.save()
    View.objects.create(Prospect=view_prospect, Campaign=view_campaign, View_User=view_user, Viewed_On=datetime.date.today())
    # view_prospect.delete()
    return HttpResponseRedirect('/get_prospect/'+campaign_id+'/')

    # phone = request.POST['phone']
    # email = request.POST['email']
    # website = request.POST['website']
    # notes = request.POST['notes']
    # view_prospect.update(Phone=phone, Email=email, Website=website, Notes=notes,
    #     Info_Updated_User=request.user.username, Info_Updated_Campaign=view_campaign.Name)
    # view_prospect.Phone = phone
    # view_prospect.save()


@login_required
def my_leads(request, campaign_id):
    campaign = Campaign.objects.get(id=campaign_id)
    all_leads = Lead.objects.filter(Lead_User=request.user, Campaign=campaign)
    context = {'leads': all_leads, 'campaign_id': campaign_id}
    return render(request, 'portal/my_leads.html', context)


@login_required
def my_dncs(request, campaign_id):
    campaign = Campaign.objects.get(id=campaign_id)
    all_dncs = DNC.objects.filter(DNC_User=request.user, Campaign=campaign)
    context = {'dncs': all_dncs, 'campaign_id': campaign_id}
    return render(request, 'portal/my_dncs.html', context)




@login_required
def my_views(request, campaign_id):
    campaign = Campaign.objects.get(id=campaign_id)
    all_views = View.objects.filter(View_User=request.user, Campaign=campaign)
    context = {'views': all_views, 'campaign_id': campaign_id}
    return render(request, 'portal/my_views.html', context)

#
# @login_required
# def make_changes(request, prospect_id, campaign_id):
#     prospect = get_object_or_404(Prospect, id=prospect_id)
#     campaign = get_object_or_404(Campaign, id=campaign_id)
#     phone = request.POST['phone']
#     email = request.POST['email']
#     company = request.POST['company']
#     notes = request.POST['notes']
#     if phone != '' and prospect.Phone != '-':
#         prospect.Phone = phone
#     else:
#         prospect.Update_Phone = phone
#     if email != '' and prospect.Email != '-':
#         prospect.Email = email
#     else:
#         prospect.Update_Email = email
#     if company != '' and prospect.Company != '-':
#         prospect.Company = company
#     else:
#         prospect.Update_Company = company
#     Old_Info = 'Phone : {0}, Email: {1}, Company: {2}'.format(prospect.Phone, prospect.Email, prospect.Company)
#     prospect.Notes = notes
#     prospect.Info_Updated_User = request.user.username
#     prospect.Info_Updated_Campaign = campaign.Name
#     prospect.To_Be_Updated = True
#     prospect.save()
#     context = {'prospect': prospect, 'campaign': campaign, 'form': 'form'}
#     return render(request, 'portal/single_prospect.html', context)
#
#
#






@login_required
def make_changes(request, prospect_id, campaign_id):
    prospect = get_object_or_404(Prospect, id=prospect_id)
    campaign = get_object_or_404(Campaign, id=campaign_id)
    phone = request.POST['phone']
    email = request.POST['email']
    company = request.POST['company']
    notes = request.POST['notes']
    temp_count = 0
    if phone != '':
        if prospect.Phone == '-':
            prospect.Phone = phone
            prospect.save()
        else:
            prospect.Update_Phone = phone
            prospect.save()
            temp_count += 1
    if email != '':
        if prospect.Email == '-':
            prospect.Email = email
            prospect.save()
        else:
            prospect.Update_Email = email
            prospect.save()
            temp_count += 1
    if company != '':
        if prospect.Company == '-':
            prospect.Company = company
            prospect.save()
        else:
            prospect.Update_Company = company
            prospect.save()
            temp_count += 1
    Old_Info = 'Phone : {0}, Email: {1}, Company: {2}'.format(prospect.Phone, prospect.Email, prospect.Company)
    prospect.Notes = notes
    prospect.Info_Updated_User = request.user.username
    prospect.Info_Updated_Campaign = campaign.Name
    prospect.Old_Info = Old_Info
    if temp_count != 0:
        prospect.To_Be_Updated = True
    else:
        pass
    prospect.save()
    context = {'prospect': prospect, 'campaign': campaign, 'form': 'form'}
    return render(request, 'portal/single_prospect.html', context)










