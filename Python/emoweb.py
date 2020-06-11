import httplib2 as http
import requests
import ssl
import json
import csv
import numpy
import pandas as pd

import datafordeleren

headers = {
    'Authorization': 'Basic am9sbkBjb3dpLmNvbToxMjM0NTY3OA=='
}


BBRHeadings = {
    'EnergyLabelSerialIdentifier',
    'BBRUseCode',
    'BuildingNumber',
    'CityName',
    'DEMOLink',
    'EnergyLabelClassification',
    'EnergyLabelTypeBasedOn',
    'EnergyLabelTypeUsage',
    'EntityIdentifier',
    'HasPdf',
    'HasXML',
    'HeatSupply',
    'HouseNumber',
    'IsHidden',
    'IsMixedUsage',
    'LabelStatus',
    'LabelStatusCode',
    'MunicipalityNumber',
    'PropertyNumber',
    'SchemaVersion',
    'StreetName',
    'SubmitterCompanyIdentifier',
    'SubmitterCompanyName',
    'SubmitterConsultantName',
    'ValidFrom',
    'ValidTo',
    'Wgs84Latitude',
    'Wgs84Longitude',
    'YearOfConstruction',
    'ZipCode'
}

def getAllBuildingsInKommune(kommuneNummer):
    try:
        from urlparse import urlparse
    except ImportError:
        try:
            from urllib.parse import urlparse
        except ImportError:
            print("urlparse failed")

    try:
        r = requests.get(url="https://emoweb.dk/EMOData/EMOData.svc/Ping", headers=headers)
        if r.status_code == 200:
            LabelSerialIdentifierList = []
            buildingInfo = []

            bygningsList = datafordeleren.getBygningsList(kommuneNummer)
            print("Going through list of " + str(len(bygningsList)) + " buildings")

            kommune_csv_file = open("BBRBygninger" + str(kommuneNummer) + ".csv", 'w')
            kommune_writer = csv.writer(kommune_csv_file, delimiter=';', lineterminator='\n')
            kommune_writer.writerow(BBRHeadings)
            for bygningsID in bygningsList:
                buildingInfo = []
                EjendomsNummer = datafordeleren.getEjendomsNummerOfBygning(bygningsID)
                if EjendomsNummer == None: continue

                building = getBulding(kommuneNummer, EjendomsNummer, 0)
                if building == None: continue

                for heading in BBRHeadings:
                    buildingInfo.append(building[heading])
                kommune_writer.writerow(buildingInfo)
                LabelSerialIdentifierList.append(building["EnergyLabelSerialIdentifier"])

        print("Collected EnergyLabelForLabelSerialIdentifier for " + str(len(LabelSerialIdentifierList)) + " buildings")
        getEnergyLabelForLabelSerialIdentifier(LabelSerialIdentifierList)
    except ImportError:
        print("Ping failed")



def getBulding(municipality, property, building):
    try:
        SearchEnergyLabelBBR = "https://emoweb.dk/EMOData/EMOData.svc/SearchEnergyLabelBBR/"
        query = str(municipality) + "/" + property + "/" + str(building)
        url = SearchEnergyLabelBBR + query + "/TL,BA"

        print(url)
        BBRSearchResponse = requests.get(url=url, headers=headers)

        if BBRSearchResponse.status_code == 200:
            BBRcontent = json.loads(BBRSearchResponse.content)
            searchResults = BBRcontent["SearchResults"]

            if len(searchResults) > 0:
                building = searchResults[0]
                return building
    except ImportError:
        print("getBulding " + query + " failed")


def getEnergyLabelForLabelSerialIdentifierFromTo(FromLabelSerialIdentifier,ToLabelSerialIdentifier):
    LabelSerialIdentifierList = range(FromLabelSerialIdentifier, ToLabelSerialIdentifier)
    getEnergyLabelForLabelSerialIdentifier(LabelSerialIdentifierList)


def getEnergyLabelForLabelSerialIdentifier(LabelSerialIdentifierList):
    try:
        from urlparse import urlparse
    except ImportError:
        try:
            from urllib.parse import urlparse
        except ImportError:
            print("urlparse failed")

    ProposalCalculationHeadings = {
        "AdditionalHeat",
        "AdditionalHeatCost",
        "CalculatedConsumption",
        "CalculatedEmission",
        "CalculatedEmissionLowering",
        "CalculatedEnergyConsumption",
        "CalculatedEnergySavings",
        "ElectricityPrice",
        "ExtraCostPrYear",
        "FixedCharge",
        "HeatSupply",
        "HeatSupplyCost",
        "TotalProfitableInvestment"
    }
    ProposalOverviewHeadings = {
        "ExtraCostPrYear",
        "ExtraCostPrYearForAllProposals",
        "ExtraCostPrYearForRecommendedProposals",
        "PossibleEnergyLabelForAllProfitableProposals",
        "PossibleEnergyLabelForAllProposals",
        "TotalProfitableInvestment",
        "TotalRecommendedInvestment"
    }

    ProposalHeadings = {
        "Investment",
        "Profitable",
        "ProposalHeadline",
        "ProposalID",
        "Recommended",
        "Savings",
        "SeebClassification",
        "SeebClassificationDescription",
    }
    try:
        r = requests.get(url="https://emoweb.dk/EMOData/EMOData.svc/Ping", headers=headers)
        if r.status_code == 200:

            SummaryHeadings = ["Nummer"]
            SummaryHeadings.extend(ProposalCalculationHeadings)
            SummaryHeadings.extend(ProposalOverviewHeadings)
            SummaryFile = open("Summary.csv", 'w')
            Summary_writer = csv.writer(SummaryFile, delimiter=';', lineterminator='\n')
            Summary_writer.writerow(SummaryHeadings)

            for LabelSerialIdentifier in LabelSerialIdentifierList:
                try:
                    print("Getting energy label for building with LabelSerialIdentifier: " + str(LabelSerialIdentifier))
                    FetchEnergyLabelDetails = "https://emoweb.dk/EMOData/EMOData.svc/FetchEnergyLabelDetails/"
                    try:
                        EnergyLabelDetailsResponse = requests.get(url=FetchEnergyLabelDetails + str(LabelSerialIdentifier), headers=headers)
                    except:
                        continue
                    if EnergyLabelDetailsResponse.status_code == 200:
                        try:
                            EnergyLabelDetails = json.loads(EnergyLabelDetailsResponse.content)
                        except ImportError:
                            print(str(LabelSerialIdentifier) + " did not return JSON format")
                            continue
                    else:
                        continue

                    if EnergyLabelDetails["ResponseStatus"]["StatusCode"] == 3:

                        Summary = []
                        Summary.append(str(LabelSerialIdentifier))

                        ProposalOverview = EnergyLabelDetails["ProposalOverview"]
                        for heading in ProposalCalculationHeadings:
                            Summary.append(EnergyLabelDetails["ProposalCalculation"][heading])
                        for heading in ProposalOverviewHeadings:
                            Summary.append(ProposalOverview[heading])

                        Summary_writer.writerow(Summary)
                        print("Wrote " + str(LabelSerialIdentifier) + ".csv  with " + str(len(ProposalOverview)) + " proposals.")

                        Proposal_csv_file = open(str(LabelSerialIdentifier) + ".csv", 'w')
                        Proposal_writer = csv.writer(Proposal_csv_file, delimiter=';', lineterminator='\n')
                        Proposal_writer.writerow(ProposalHeadings)

                        for proposal in ProposalOverview["Proposals"]:
                            ProposalCalculation = []
                            for heading in ProposalHeadings:
                                ProposalCalculation.append(proposal[heading])
                            Proposal_writer.writerow(ProposalCalculation)

                        print(str(LabelSerialIdentifier) + " written to Summary.csv.")
                    else:
                        print("Could not write " + str(LabelSerialIdentifier) + " with status code : " + str(EnergyLabelDetails["ResponseStatus"]["StatusCode"]) + ".")

                        if "ResponseStatus" in EnergyLabelDetails:
                            print(EnergyLabelDetails["ResponseStatus"]["StatusMessage"])

                except ImportError:
                    print("Getting energy label failed")

            SummaryFile.close()

        else:
            print("getEnergyLabelForLabelSerialIdentifier failed at ping")
    except ImportError:
        print("Ping failed")
