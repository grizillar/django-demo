from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template import RequestContext

from .forms import UploadFileForm
from .models import Campaign, Document
import dashboard.scripts.handler as handler

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
                print("match")
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
