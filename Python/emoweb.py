import httplib2 as http
import requests
import ssl
import json
import csv
import numpy
import pandas as pd
import time

import datafordeleren

headers = {
    'Authorization': 'Basic am9sbkBjb3dpLmNvbToxMjM0NTY3OA=='
}

DawaHeadings = {
    "Bygning_id",
    "BYG_ANVEND_KODE",
    "OPFOERELSE_AAR",
    "OMBYG_AAR",
    "BYG_ARL_SAML",
    "BYG_BOLIG_ARL_SAML",
    "ERHV_ARL_SAML",
    "ESREjdNr"
}

EmoDataHeadings = {
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

# For et kommunekode findes samtlige bygninger fra BBR. For hver bygning findes ESR ejendomsnr (ESREjdNr).
# ESR ejendomsnr og kommunekode benyttes sammen til findes LabelSerialIdentifier ved /SearchEnergyLabelBBR
# LabelSerialIdentifier bruges til at hente /FetchEnergyLabelDetails
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
            allHeadings = []
            allHeadings.extend(DawaHeadings)
            allHeadings.extend(EmoDataHeadings)
            kommune_writer.writerow(allHeadings)
            for bygningsID in bygningsList:
                time.sleep(6)
                buildingInfo = []
                DawaBygning = datafordeleren.getDawaBygning(bygningsID)
                if DawaBygning == None or DawaBygning["BYG_ANVEND_KODE"] >= 600: continue

                EjendomsNummer = DawaBygning["ESREjdNr"]
                SearchforEnergyLabel = getLabelSerialIdentifier(kommuneNummer, EjendomsNummer, 0)
                if SearchforEnergyLabel == None: continue

                for heading in DawaHeadings:
                    buildingInfo.append(DawaBygning[heading])

                for heading in EmoDataHeadings:
                    buildingInfo.append(SearchforEnergyLabel[heading])

                kommune_writer.writerow(buildingInfo)
                LabelSerialIdentifierList.append(SearchforEnergyLabel["EnergyLabelSerialIdentifier"])

        print("Collected EnergyLabelForLabelSerialIdentifier for " + str(len(LabelSerialIdentifierList)) + " buildings")
        getEnergyLabelForLabelSerialIdentifier(LabelSerialIdentifierList)
    except ImportError:
        print("Ping failed")



# kommunekode og ESR ejendomsnr (property) benyttes sammen til findes LabelSerialIdentifier ved /SearchEnergyLabelBBR
def getLabelSerialIdentifier(municipality, property, building):
    try:
        SearchEnergyLabelBBR = "https://emoweb.dk/EMOData/EMOData.svc/SearchEnergyLabelBBR/"
        query = str(municipality) + "/" + property + "/" + str(building)
        url = SearchEnergyLabelBBR + query + "/TL,BA"

        BBRSearchResponse = requests.get(url=url, headers=headers)

        if BBRSearchResponse.status_code == 200:
            BBRcontent = json.loads(BBRSearchResponse.content)
            searchResults = BBRcontent["SearchResults"]

            if len(searchResults) > 0:
                building = searchResults[0]
                return building
    except ImportError:
        print("getBulding " + query + " failed")


# LabelSerialIdentifier fra/til bruges til at hente /FetchEnergyLabelDetails
def getEnergyLabelForLabelSerialIdentifierFromTo(FromLabelSerialIdentifier,ToLabelSerialIdentifier):
    LabelSerialIdentifierList = range(FromLabelSerialIdentifier, ToLabelSerialIdentifier)
    getEnergyLabelForLabelSerialIdentifier(LabelSerialIdentifierList)


# En liste af LabelSerialIdentifier bruges til at hente /FetchEnergyLabelDetails
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
