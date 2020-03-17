import BBRhandler
import sys

if(len(sys.argv)>0):
    try:
        kommunekode = sys.argv[1]
    except sys.argv as msg:
        print(msg)
else:
    print("Not found: sys.argv")

if int(kommunekode) > 100:
    try:
        print ('Running EnergyPlanner for kommune:', str(kommunekode), '.')
        BBRhandler.calculateEnergyDemand(int(kommunekode))
    except kommunekode as msg:
        print(msg)

else:
    print('This version only support one kommunekode', sys.argv)