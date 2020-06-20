import httplib2 as http
import requests
import ssl
import json
import csv
import numpy
import pandas as pd
import time
import datafordeleren
import requests
import xml.etree.ElementTree as ET
from pathlib import Path
import logging

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
            csvFileName = 'BBR' + str(kommuneNummer) + '.csv'
            if Path(csvFileName).is_file():
                bygnignsData = pd.read_csv(csvFileName, encoding='latin1', header=0, quotechar='"', delimiter=";")
                bygningsList = bygnignsData["id_lokalId"]

            else:
                bygningsList = datafordeleren.getBygningsList(kommuneNummer)

            print("Going through list of " + str(len(bygningsList)) + " buildings")

            bygnigner_csv_file = open("BygningInfo" + str(kommuneNummer) + ".csv", 'w')
            bygning_writer = csv.writer(bygnigner_csv_file, delimiter=';', lineterminator='\n')
            allHeadings = []
            allHeadings.extend(DawaHeadings)
            allHeadings.extend(EmoDataHeadings)
            bygning_writer.writerow(allHeadings)
            for bygningsID in bygningsList:
                buildingInfo = []
                DawaBygning = datafordeleren.getDawaBygning(bygningsID)
                if DawaBygning == None or DawaBygning["BYG_ANVEND_KODE"] >= 600 or "ESREjdNr" not in DawaBygning:
                    continue

                EjendomsNummer = DawaBygning["ESREjdNr"]
                SearchforEnergyLabel = getLabelSerialIdentifier(kommuneNummer, EjendomsNummer, 0)
                if SearchforEnergyLabel == None: continue

                for heading in DawaHeadings:
                    buildingInfo.append(DawaBygning[heading])

                for heading in EmoDataHeadings:
                    buildingInfo.append(SearchforEnergyLabel[heading])

                bygning_writer.writerow(buildingInfo)
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
        time.sleep(6)
        try:
            BBRSearchResponse = requests.get(url=url, headers=headers)
        except:
            logging.warning("getLabelSerialIdentifier: SearchEnergyLabelBBR " + query + " failed")
            print("getLabelSerialIdentifier: SearchEnergyLabelBBR " + query + " failed")
            return

        if BBRSearchResponse.status_code == 200:
            BBRcontent = json.loads(BBRSearchResponse.content)
            searchResults = BBRcontent["SearchResults"]

            if len(searchResults) > 0:
                building = searchResults[0]
                return building
    except ImportError:
        logging.warning("getLabelSerialIdentifier: SearchEnergyLabelBBR " + query + " failed")
        print("getLabelSerialIdentifier: SearchEnergyLabelBBR " + query + " failed")
        return


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
                        logging.warning("getEnergyLabelForLabelSerialIdentifier: FetchEnergyLabelDetails " + str(LabelSerialIdentifier) + " failed")
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
                        ProposalOverview = EnergyLabelDetails["ProposalOverview"]

                        saveProposalOverviewInSummary(Summary_writer, LabelSerialIdentifier, EnergyLabelDetails, ProposalOverview)
                        saveProposalsAsCsv(LabelSerialIdentifier, ProposalOverview)
                        saveProposalsAsXml(LabelSerialIdentifier)

                    else:
                        print("Could not write " + str(LabelSerialIdentifier) + " with status code : " + str(EnergyLabelDetails["ResponseStatus"]["StatusCode"]) + ".")
                        logging.info("Could not write " + str(LabelSerialIdentifier) + " with status code : " + str(EnergyLabelDetails["ResponseStatus"]["StatusCode"]) + ".")

                        if "ResponseStatus" in EnergyLabelDetails:
                            print(EnergyLabelDetails["ResponseStatus"]["StatusMessage"])

                except ImportError:
                    print("Getting energy label failed")
                    logging.warning("Getting energy label" + str(LabelSerialIdentifier) + " failed")

            SummaryFile.close()

        else:
            print("getEnergyLabelForLabelSerialIdentifier failed at ping")
    except ImportError:
        print("Ping failed")


def saveProposalOverviewInSummary(Summary_writer, LabelSerialIdentifier,EnergyLabelDetails, ProposalOverview):

    Summary = []
    Summary.append(str(LabelSerialIdentifier))
    for heading in ProposalCalculationHeadings:
        Summary.append(EnergyLabelDetails["ProposalCalculation"][heading])
    for heading in ProposalOverviewHeadings:
        Summary.append(ProposalOverview[heading])

    Summary_writer.writerow(Summary)
    print(str(LabelSerialIdentifier) + " written to Summary.csv.")

def saveProposalsAsCsv(LabelSerialIdentifier, ProposalOverview):
    Proposal_csv_file = open(str(LabelSerialIdentifier) + ".csv", 'w')
    Proposal_writer = csv.writer(Proposal_csv_file, delimiter=';', lineterminator='\n')
    Proposal_writer.writerow(ProposalHeadings)

    for proposal in ProposalOverview["Proposals"]:
        ProposalCalculation = []
        for heading in ProposalHeadings:
            ProposalCalculation.append(proposal[heading])
        Proposal_writer.writerow(ProposalCalculation)
    print("Wrote " + str(LabelSerialIdentifier) + ".csv  with " + str(len(ProposalOverview)) + " proposals.")

def saveProposalsAsXml(LabelSerialIdentifier):
    FetchEnergyLabelXmlRaw = "https://emoweb.dk/emodata/emodata.svc/FetchEnergyLabelXmlRaw/"
    try:
        EnergyLabelXmlResponse = requests.get(
            url=FetchEnergyLabelXmlRaw + str(LabelSerialIdentifier), headers=headers)
    except:
        return
    xmlRoot = ET.fromstring(EnergyLabelXmlResponse.text)
    xmlTree = ET.ElementTree(xmlRoot)
    xmlTree.write(str(LabelSerialIdentifier) + ".xml")
    print(str(LabelSerialIdentifier) + ".xml saved.")