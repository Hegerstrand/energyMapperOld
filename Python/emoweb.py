import httplib2 as http
import requests
import ssl
import json
import csv
import numpy
import pandas as pd

headers = {
    'Authorization': 'Basic am9sbkBjb3dpLmNvbToxMjM0NTY3OA=='
}

def getLabelSerialIdentifierForBulding(municipality, property, building):
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
            SearchEnergyLabelBBR = "https://emoweb.dk/EMOData/EMOData.svc/SearchEnergyLabelBBR/"
            bygning = str(municipality) + "/" + str(property) + "/" + str(building)
            BBRSearchResponse = requests.get(url=SearchEnergyLabelBBR + bygning, headers=headers)
            BBRcontent = json.loads(BBRSearchResponse.content)
            SearchResults = BBRcontent["SearchResults"]
            LabelSerialIdentifier = SearchResults[0]["EnergyLabelSerialIdentifier"]

        return LabelSerialIdentifier

    except ImportError:
        print("Ping failed")

def getEnergyLabelForLabelSerialIdentifier(LabelSerialIdentifier):
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
            FetchEnergyLabelDetails = "https://emoweb.dk/EMOData/EMOData.svc/FetchEnergyLabelDetails/"
            EnergyLabelDetailsResponse = requests.get(url=FetchEnergyLabelDetails + str(LabelSerialIdentifier), headers=headers)
            EnergyLabelDetails = json.loads(EnergyLabelDetailsResponse.content)
            if EnergyLabelDetails["ResponseStatus"]["StatusCode"] == 3:

                Headings = []
                Headings.append("Nummer")
                Summary = []
                Summary.append(str(LabelSerialIdentifier))

                ProposalOverview = EnergyLabelDetails["ProposalOverview"]
                for heading in ProposalCalculationHeadings :
                    Headings.append(heading)
                    Summary.append(EnergyLabelDetails["ProposalCalculation"][heading])
                for heading in ProposalOverviewHeadings :
                    Headings.append(heading)
                    Summary.append(ProposalOverview[heading])

                csv_file = open("Energimærker.csv", 'w')
                Summary_writer = csv.writer(csv_file, delimiter=';', lineterminator='\n')
                Summary_writer.writerow(Headings)
                Summary_writer.writerow(Summary)

                Proposal_csv_file = open(str(LabelSerialIdentifier) + ".csv", 'w')
                Proposal_writer = csv.writer(Proposal_csv_file, delimiter=';', lineterminator='\n')
                Proposal_writer.writerow(ProposalHeadings)

                ProposalCalculation = []
                for proposal in ProposalOverview["Proposals"]:
                    ProposalCalculation = []
                    for heading in ProposalHeadings:
                        ProposalCalculation.append(proposal[heading])
                    Proposal_writer.writerow(ProposalCalculation)

    except ImportError:
        print("Ping failed")
