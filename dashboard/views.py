from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template import RequestContext

from .forms import UploadFileForm
from .models import Campaign, Document
import dashboard.scripts.handler as handler
import dashboard.scripts.dbmap as dbmap

# Create your views here.

PLATFORM_DEFAULT = "1,2,3,4,5,6,7"
SINGLE_SELECTOR_DEFAULT = "reach"
MULTIPLE_SELECTOR_DEFAULT = "reach,impression,engagement"


def dashboard(request):
    # http://localhost:8000/query/startdate=2023-1-1&enddate=2023-1-3

    sdate = request.GET.get("startdate")
    edate = request.GET.get("enddate")
    platform = request.GET.get("platform")
    single_selector = request.GET.get("ss")
    multiple_selector = request.GET.get("ms")

    if platform is not None:
        platform = platform.split(",")
        context_platform = ','.join(p for p in platform)
    else:
        context_platform = PLATFORM_DEFAULT

    if multiple_selector is not None:
        multiple_selector = multiple_selector.split(",")
        context_multiple_selector = ','.join(e for e in multiple_selector)
    else:
        context_multiple_selector = MULTIPLE_SELECTOR_DEFAULT

    if single_selector is None:
        single_selector = SINGLE_SELECTOR_DEFAULT

    summary = handler.getAllSummary(sdate, edate, platform)
    costPerResult = handler.getCostPerResult(sdate, edate, platform)
    summaryPerMonth = handler.getSummaryPerMonth(sdate, edate, platform)

    context = {
        "start_date": sdate,
        "end_date": edate,
        "platform": context_platform,
        "single_selector": single_selector,
        "multiple_selector": context_multiple_selector,
        "summaryJSON": summary.to_json(),
        "CPRJSON": costPerResult.to_json(),
        "summaryPMJSON": summaryPerMonth.to_json()

    }

    return render(request, 'dashboard/dashboard.html', context)


def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            type = request.POST.get("type")
            date = request.POST.get("date")

            # file function
            fileShape = handler.writeCSV(request.FILES['csvfile'])
            colLength = fileShape[1]
            rowLength = fileShape[0]

            print(colLength, rowLength)

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
                return HttpResponseRedirect('/upload-success')
            else:
                print("unmatch")

        else:
            print("file's not ok1")
    else:
        form = UploadFileForm()
    return render(request, 'upload/upload.html', {'form': form})


def uploadsuccess(request):
    type = request.GET.get("type")
    amount = request.GET.get("amount")
    campaignLenght = handler.getCampaignLength()
    siteTrafficLenght = handler.getSiteTrafficLength()
    context = {
        'campaignLength': campaignLenght,
        'siteTrafficLenght': siteTrafficLenght,
        'type': type,
        'amount': amount
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
