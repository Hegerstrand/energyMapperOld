import httplib2 as http
import requests
import ssl
import json
import csv
import numpy
import pandas as pd

def getEnergyLabelForBulding(municipality, property, building):
    try:
        from urlparse import urlparse
    except ImportError:
        try:
            from urllib.parse import urlparse
        except ImportError:
            print("urlparse failed")


    headers = {
        'Authorization': 'Basic am9sbkBjb3dpLmNvbToxMjM0NTY3OA=='
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
    try:
        r = requests.get(url="https://emoweb.dk/EMOData/EMOData.svc/Ping", headers=headers)
        if r.status_code == 200:
            SearchEnergyLabelBBR = "https://emoweb.dk/EMOData/EMOData.svc/SearchEnergyLabelBBR/"
            bygning = str(municipality) + "/" + str(property) + "/" + str(building)
            BBRSearchResponse = requests.get(url=SearchEnergyLabelBBR + bygning, headers=headers)
            BBRcontent = json.loads(BBRSearchResponse.content)
            SearchResults = BBRcontent["SearchResults"]
            EnergimaerkeNr = SearchResults[0]["EnergyLabelSerialIdentifier"]

            FetchEnergyLabelDetails = "https://emoweb.dk/EMOData/EMOData.svc/FetchEnergyLabelDetails/"
            EnergyLabelDetailsResponse = requests.get(url=FetchEnergyLabelDetails + str(EnergimaerkeNr), headers=headers)
            EnergyLabelDetails = json.loads(EnergyLabelDetailsResponse.content)
            if EnergyLabelDetails["ResponseStatus"]["StatusCode"] == 3:

                Headings = []
                Headings.append("Nummer")
                Summary = []
                Summary.append(str(EnergimaerkeNr))

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
                Summary_writer.wr iterow(Summary)

                Proposal_csv_file = open(str(EnergimaerkeNr) + ".csv", 'w')
                Proposal_writer = csv.writer(Proposal_csv_file, delimiter=';', lineterminator='\n')
                Proposal_writer.writerow(ProposalHeadings)

                ProposalCalculation = []
                for proposal in ProposalOverview["Proposals"]:
                    ProposalCalculation = []
                    for heading in ProposalHeadings:
                        ProposalCalculation.append(proposal[heading])
                    Proposal_writer.writerow(ProposalCalculation)

    except ImportError:
        print("2")
    #response, content = h.request(target.geturl(), method, body, headers)



    # https://emoweb.dk/EMOData/EMOData.svc/Ping

        #https://emoweb.dk/EMOData/EMOData.svc/SearchEnergyLabelBBR/573/112576/0
        #https://emoweb.dk/emodata/emodata.svc/FetchEnergyLabelDetails/311022216/Investment=All,TL,BA

    # GET /FetchEnergyLabelDetails/{EntityIdentifier}
    #GET SearchEnergyLabelBBR/{municipality}/{property}/{building}


    #GET /EMOData/EMOData.svc/SearchEnergyLabelUID/{UID}
    #GET /EMOData/EMOData.svc/FetchEnergyLabelDetailsMultipleBuildings/{EntityIdentifier}


# /EMOData/EMOData.svc/
# http://energisparebygning.dk:8001/DIADEMService/DIADEMService.svc
# https://emoweb.dk/emodata/emodata.svc/