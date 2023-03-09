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

        compare_toggle = request.GET.get("compare").capitalize() == "True"

        periods_1 = request.GET.get("periods_1").split(",")
        years_1 = request.GET.get("years_1").split(",")

        periodrange_1 = handler.formPeriodRange(periods_1, years_1)

        summary = handler.queryByPeriodinRange(
            handler.getAllSummaryByPeriod, periodrange_1[0], periodrange_1[1], platform
        )

        platformCount = handler.queryByPeriodinRange(
            handler.getPlatformCountByPeriod, periodrange_1[0], periodrange_1[1], platform
        )

        # campaignCount = handler.getCampaignCountByPeriod(
        #     periods[page-1], years[page-1], platform)
        campaignCount = handler.intByPeriodinRange(
            handler.getCampaignCountByPeriod, periodrange_1[0], periodrange_1[1], platform
        )
        # siteTrafficCount = handler.getSitetrafficLengthByPeriod(
        #     periods[page-1], years[page-1], platform
        # )
        siteTrafficCount = handler.intByPeriodinRange(
            handler.getSitetrafficLengthByPeriod, periodrange_1[0], periodrange_1[1], platform
        )
        costPerResult = handler.queryByPeriodinRange(
            handler.getCostPerResultByPeriod, periodrange_1[0], periodrange_1[1], platform
        )

        # arraySummary = handler.formQueryArray(
        #     handler.getAllSummaryByPeriod, periods, years, platform
        # )
        # # Remove later
        summaryPerMonth = handler.getSummaryPerMonth(sdate, edate, platform)

        arraySummaryByPeriod = handler.formQueryArray(
            handler.getSummaryByPeriod, periodrange_1[0], periodrange_1[1], platform
        )

        if compare_toggle:
            periods_2 = request.GET.get("periods_2").split(",")
            years_2 = request.GET.get("years_2").split(",")
            periodrange_2 = handler.formPeriodRange(periods_2, years_2)

            summary_2 = handler.queryByPeriodinRange(
                handler.getAllSummaryByPeriod, periodrange_2[0], periodrange_2[1], platform
            )

            platformCount_2 = handler.queryByPeriodinRange(
                handler.getPlatformCountByPeriod, periodrange_2[0], periodrange_2[1], platform
            )

            campaignCount_2 = handler.intByPeriodinRange(
                handler.getCampaignCountByPeriod, periodrange_2[0], periodrange_2[1], platform
            )

            siteTrafficCount_2 = handler.intByPeriodinRange(
                handler.getSitetrafficLengthByPeriod, periodrange_2[0], periodrange_2[1], platform
            )
            costPerResult_2 = handler.queryByPeriodinRange(
                handler.getCostPerResultByPeriod, periodrange_2[0], periodrange_2[1], platform
            )

            arraySummaryByPeriod_2 = handler.formQueryArray(
                handler.getSummaryByPeriod, periodrange_2[0], periodrange_2[1], platform
            )

            summaryCompare = handler.percentageChange(summary, summary_2)
            CPRCompare = handler.percentageChange(
                costPerResult, costPerResult_2)
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
        # context["summaryARR"] = arraySummary
        context["compare"] = compare_toggle
        context["summaryByPeriodARR"] = arraySummaryByPeriod
        context["periods_1"] = ','.join(periods_1)
        context["years_1"] = ','.join(years_1)
        if compare_toggle:
            context["periods_2"] = ','.join(periods_2)
            context["years_2"] = ','.join(years_2)
            context["summary_2JSON"] = summary_2.to_json()
            context["platformCount_2JSON"] = platformCount_2.to_json()
            context["campaign_count_2"] = campaignCount_2
            context["sitetraffic_count_2"] = siteTrafficCount_2
            context["CPR_2JSON"] = costPerResult_2.to_json()
            context["arraySummaryByPeriod_2"] = arraySummaryByPeriod_2
            context["summaryCompareJSON"] = summaryCompare.to_json()
            context["CPRCompareJSON"] = CPRCompare.to_json()
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
