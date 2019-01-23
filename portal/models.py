from django.db import models
from django.conf import settings
from django.db.models.signals import post_save


class Campaign(models.Model):
    Name = models.CharField(max_length=200)
    Start_Date = models.DateField(blank=True, null=True)
    Status = models.BooleanField(default=False)
    End_Date = models.DateField(blank=True, null=True)
    Users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    def __str__(self):
        return self.Name


class Prospect(models.Model):
    Name            = models.CharField(max_length=200)
    Phone           = models.CharField(max_length=200, blank=True, null=True, default='-')
    Email           = models.CharField(max_length=200, blank=True, null=True, default='-')
    Job_Title       = models.CharField(max_length=200, blank=True, null=True, default='-')
    Industry_Type   = models.CharField(max_length=200, blank=True, null=True, default='-')
    Company         = models.CharField(max_length=200, blank=True, null=True, default='-')
    Website         = models.CharField(max_length=200, blank=True, null=True, default='-')
    Emp_Size        = models.CharField(max_length=200, blank=True, null=True, default='-')
    City            = models.CharField(max_length=200, blank=True, null=True, default='-')
    Country         = models.CharField(max_length=200, blank=True, null=True, default='-')
    State           = models.CharField(max_length=200, blank=True, null=True, default='-')
    Zip_Code        = models.CharField(max_length=200, blank=True, null=True, default='-')
    Direct_Or_Extension     = models.CharField(max_length=200, blank=True, null=True, default='-')
    Campaigns       = models.ManyToManyField(Campaign, blank=True)
    Lead_Count      = models.IntegerField(default=0)
    View_Count      = models.IntegerField(default=0)
    Released_Campaigns      = models.CharField(max_length=1000, default='-')
    Info_Updated_User       = models.CharField(max_length=200, blank=True, null=True, default='-')
    Info_Updated_Campaign   = models.CharField(max_length=200, blank=True, null=True, default='-')
    Notes           = models.TextField(blank=True, null=True, default='')
    To_Be_Updated   = models.BooleanField(default=False)
    Update_Phone    = models.CharField(max_length=200, blank=True, null=True, default='-')
    Update_Email    = models.CharField(max_length=200, blank=True, null=True, default='-')
    Update_Company  = models.CharField(max_length=200, blank=True, null=True, default='-')
    Old_Info        = models.TextField(blank=True, null=True, default='-')

    def __str__(self):
        return self.Name

    def info_update(self, **kwargs):
        for field, value in kwargs.items():
            self.field = value
            self.save()
        self.save()


# def emp_size_setter(sender, instance, *args,**kwargs):
#     emp_stanadrd = [(1, 10), (11, 50), (51, 200), (201, 500),
#                     (501, 1000), (1001, 5000), (5001, 10000), (10001, 99999)]
#     emp_class = ['1to1', '11to50', '51to200', '201to500',
#                  '501to2000', '1001to5000', '5001to10000', '10000+']
#     try:
#         instance.emp_size
#     except:
#
#     try:
#         for rng in emp_stanadrd:
#             if
#
# post_save.connect(emp_size_setter, sender=Prospect)


class Lead(models.Model):
    Lead_On = models.DateField(blank=True, null=True)
    Prospect = models.ForeignKey(Prospect, on_delete=models.CASCADE)
    Campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    Lead_User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.Prospect.Name


class View(models.Model):
    Viewed_On = models.DateField(blank=True, null=True)
    Prospect = models.ForeignKey(Prospect, on_delete=models.CASCADE)
    Campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    View_User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.Prospect.Name


class DNC(models.Model):
    DNC_On = models.DateField(blank=True, null=True)
    Prospect = models.ForeignKey(Prospect, on_delete=models.CASCADE)
    Campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    DNC_User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.Prospect.Name



