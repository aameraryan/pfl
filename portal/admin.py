from django.contrib import admin
from portal.models import Campaign, Prospect, Lead, View, DNC
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter
from import_export.admin import ImportExportModelAdmin


class ProspectAdmin(ImportExportModelAdmin):

    search_fields = ['Name', 'Company', 'Email', 'Phone', 'Website']

    list_filter = [('Campaigns', RelatedDropdownFilter), ('Job_Title', DropdownFilter),
                   ('Emp_Size'),
                   ('State', DropdownFilter), ('Industry_Type', DropdownFilter),
                   ('To_Be_Updated', DropdownFilter), ('Lead_Count', DropdownFilter),
                   ('View_Count', DropdownFilter)]
    actions = ('assign_campaign', )
    list_display = ('Name', 'Phone', 'Job_Title', 'Industry_Type', 'Email', 'State')

    def assign_campaign(self, request, queryset):
        if 'assign' in request.POST:
            campaign_id = request.POST['campaign_id']
            campaign = get_object_or_404(Campaign, id=campaign_id)
            for prospect in queryset:
                prospect.Campaigns.add(campaign)
            if queryset.count() < 2:
                prospect_variable = 'prospect'
            else:
                prospect_variable = 'prospects'
            self.message_user(request, "Successfully {prospect_count} {prospect_variable} assigned to campaign {campaign_name}.".format(
                                                                        prospect_count=queryset.count(),
                                                                        prospect_variable=prospect_variable,
                                                                        campaign_name=campaign.Name))
            return HttpResponseRedirect(request.get_full_path())

        return render(request, 'portal/assign_campaign.html', context={'prospects': queryset,
                                                                       'campaigns': Campaign.objects.all()})



class LeadAdmin(admin.ModelAdmin):
    list_filter = ['Lead_User', 'Lead_On', 'Campaign']
    list_display = ['Prospect', 'Lead_User', 'Lead_On', 'Campaign']
    
    

class DNCAdmin(admin.ModelAdmin):
    list_filter = ['DNC_User', 'DNC_On', 'Campaign']
    list_display = ['Prospect', 'DNC_User', 'DNC_On', 'Campaign']


class ViewAdmin(admin.ModelAdmin):
    list_filter = ['View_User', 'Viewed_On', 'Campaign']
    list_display = ['Prospect', 'View_User', 'Viewed_On', 'Campaign']

    

admin.site.register(Campaign)
admin.site.register(Prospect, ProspectAdmin)

admin.site.register(Lead, LeadAdmin)
admin.site.register(View, ViewAdmin)
admin.site.register(DNC, DNCAdmin)
