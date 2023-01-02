from django.shortcuts import render

from .models import Campaign
import dashboard.scripts.script as script

# Create your views here.


def dashboard(request):
    return render(request, 'dashboard/dashboard.html')


def base(request):
    return render(request, 'layout/base.html')


def demo(request):
    campaignDF = script.getAllCampaign()
    context = {
        'campaignLength': len(campaignDF),
    }
    return render(request, 'dashboard/demo.html', context)
