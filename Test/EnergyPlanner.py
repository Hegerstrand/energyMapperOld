import BBRhandler
import sys

if(len(sys.argv)>0):
    print ('Running:', str(sys.argv.pop(0)), '.')

kommunekoder = sys.argv
if(len(kommunekoder)>0):
    kommunekode = kommunekoder.pop(0)
    print ('This version only support one kommunekode. Running EnergyPlanner for kommune:', str(kommunekode), '.')
    BBRhandler.calculateEnergyDemand(kommunekode)
else:
    print("No kommunekode found. sys.argv: ", sys.argv)