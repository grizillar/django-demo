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

    by = request.GET.get("by")
    platform = request.GET.get("platform")
    multiple_selector = request.GET.get("ms")
    page, sdate, edate, context_period, context_year = '', '', '', '', ''

    if platform is not None:
        platform = platform.split(",")
        context_platform = ','.join(p for p in platform)
    else:
        context_platform = PLATFORM_DEFAULT

    if multiple_selector is not None:
        multiple_selector = multiple_selector.split(",")
        context_multiple_selector = ','.join(e for e in multiple_selector)
    else:
        multiple_selector = MULTIPLE_SELECTOR_DEFAULT.split(",")
        context_multiple_selector = MULTIPLE_SELECTOR_DEFAULT

    possibleYear = handler.getPossibleYear()
    siteTrafficCount = handler.getSiteTrafficLength()

    if by == None:
        by = "date"

    if by == "date":
        sdate = request.GET.get("startdate")
        edate = request.GET.get("enddate")

        summary = handler.getAllSummary(sdate, edate, platform)
        costPerResult = handler.getCostPerResult(sdate, edate, platform)
        summaryPerMonth = handler.getSummaryPerMonth(sdate, edate, platform)

        # topCPRarray = []
        # for s in multiple_selector:
        #     if s in ["reach", "impression", "engagement"]:
        #         topCPRarray.append(handler.getTopCostPerCampaign(
        #             sdate, edate, platform, order=s).to_json())
        # topCPRarray = '|'.join(a for a in topCPRarray)

        # simpleCampaign = handler.getSimpleCampaign(sdate, edate, platform)
        platformCount = handler.getPlatformCount(sdate, edate, platform)
        campaignCount = handler.getCampaignCount(sdate, edate, platform)
        siteTrafficCount = handler.getSiteTrafficLength()

        # topCampaign = handler.getTopCampaign(sdate, edate, platform)

    if by == "period":
        sdate = request.GET.get("startdate")
        edate = request.GET.get("enddate")

        context_period = request.GET.get("periods")
        context_year = request.GET.get("years")
        page = int(request.GET.get("p"))
        periods = context_period.split(",")
        years = context_year.split(",")

        summary = handler.getAllSummaryByPeriod(
            periods[page-1], years[page-1], platform)
        platformCount = handler.getPlatformCountByPeriod(
            periods[page-1], years[page-1], platform)
        campaignCount = handler.getCampaignCountByPeriod(
            periods[page-1], years[page-1], platform)
        siteTrafficCount = handler.getSitetrafficLengthByPeriod(
            periods[page-1], years[page-1], platform
        )
        costPerResult = handler.getCostPerResultByPeriod(
            periods[page-1], years[page-1], platform)

        arraySummary = handler.formQueryArray(
            handler.getAllSummaryByPeriod, periods, years, platform
        )
        # Remove later
        summaryPerMonth = handler.getSummaryPerMonth(sdate, edate, platform)

        arraySummaryByPeriod = handler.formQueryArray(
            handler.getSummaryByPeriod, periods, years, platform
        )

    context = {
        "by": by,
        "page": page,
        "period": context_period,
        "year": context_year,
        "start_date": sdate,
        "end_date": edate,
        "platform": context_platform,
        "multiple_selector": context_multiple_selector,
        "summaryJSON": summary.to_json(),
        "CPRJSON": costPerResult.to_json(),
        "summaryPMJSON": summaryPerMonth.to_json(),
        "platformCountJSON": platformCount.to_json(),
        "campaign_count": campaignCount,
        "sitetraffic_count": siteTrafficCount,
        "possibleYearJSON": possibleYear.to_json(),
    }

    if by == "period":
        context["summaryARR"] = arraySummary
        context["summaryByPeriodARR"] = arraySummaryByPeriod

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
                    origin = handler.getSiteTrafficLength()
                    filetype = "sitetraffic"
                    handler.insertSiteTraffic(data)

                else:
                    origin = handler.getCampaignLength()
                    filetype = "campaign"
                    handler.insertCampaign(data)

                return HttpResponseRedirect(f'/upload-success?type={filetype}&origin={origin}&amount={rowLength}')
            else:
                print("unmatch")

        else:
            print("file's not ok1")
    else:
        form = UploadFileForm()
    return render(request, 'upload/upload.html', {'form': form})


def uploadsuccess(request):
    type = request.GET.get("type")
    origin = int(request.GET.get("origin"))
    amount = int(request.GET.get("amount"))
    database_amount = 0
    print(type)
    if type == "campaign":
        database_amount = handler.getCampaignLength()
    if type == "sitetraffic":
        database_amount = handler.getSiteTrafficLength()
    bad_amount = amount - (database_amount - origin)

    context = {
        'amount': amount,
        'origin': origin,
        'database_amount': database_amount,
        'bad_amount': bad_amount
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
