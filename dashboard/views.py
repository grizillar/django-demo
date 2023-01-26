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
            date = request.POST.get("date")

            # file function
            colLength = handler.writeCSV(request.FILES['csvfile'])

            if handler.colCheck(colLength, type):
                if type == "FB":
                    data = dbmap.FBTransform()
                if type == "LP":
                    data = dbmap.LPTransform()
                if type == "LM":
                    data = dbmap.LMTransform()
                if type == "GC":
                    data = dbmap.GCTransform()
                if type == "GS":
                    data = dbmap.GSTransform()

                # Config apply here
                if date:
                    handler.applyDate(data, date)

                if type == "GS":
                    handler.insertSiteTraffic(data)
                else:
                    handler.insertCampaign(data)
            else:
                print("unmatch")

            return HttpResponseRedirect('/upload-success')
        else:
            print("file's not ok1")
    else:
        form = UploadFileForm()
    return render(request, 'upload/upload.html', {'form': form})


def uploadsuccess(request):
    campaignDF = handler.getAllCampaign()
    context = {
        'campaignLength': len(campaignDF),
    }
    return render(request, 'upload/upload-success.html', context)


def base(request):
    return render(request, 'layout/base.html')


def demo(request):
    campaignDF = handler.getAllCampaign()
    context = {
        'campaignLength': len(campaignDF),
    }
    return render(request, 'dashboard/demo.html', context)
