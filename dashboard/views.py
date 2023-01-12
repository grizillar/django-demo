from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template import RequestContext

from .forms import UploadFileForm
from .models import Campaign, Document
import dashboard.scripts.handler as handler
import dashboard.scripts.dbmap as dbmap

# Create your views here.


def dashboard(request):
    return render(request, 'dashboard/dashboard.html')


def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            type = request.POST.get("type")

            # file function
            colLength = handler.writeCSV(request.FILES['csvfile'])

            if handler.colCheck(colLength, type):
                if type == "FB":
                    handler.insertCampaign(dbmap.FBTransform())
                if type == "LP":
                    handler.insertCampaign(dbmap.LPTransform())
                if type == "LM":
                    handler.insertCampaign(dbmap.LMTransform())
                if type == "GC":
                    handler.insertCampaign(dbmap.GCTransform())
                if type == "GS":
                    handler.insertSiteTraffic(dbmap.GSTransform())

            else:
                print("unmatch")

            return HttpResponseRedirect('/')
        else:
            print("file's not ok1")
    else:
        print("file's not ok2")
        form = UploadFileForm()
    return render(request, 'upload/upload.html', {'form': form})


def base(request):
    return render(request, 'layout/base.html')


def demo(request):
    campaignDF = handler.getAllCampaign()
    context = {
        'campaignLength': len(campaignDF),
    }
    return render(request, 'dashboard/demo.html', context)
