import BBRhandler
import datafordeleren
import csvHandler
import emoweb

#BBRhandler.calculateEnergyDemand(630)
#datafordeleren.getBygninger(210, "210.csv", 900000)
#datafordeleren.getHusnummer(3310, "Ølsted.csv", 100*1000)
#datafordeleren.getAdres    ser("Ølsted.xlx½sx", "Husnummer", "Adresser.csv")
emoweb.getEnergyLabelForLabelSerialIdentifier(emoweb.getLabelSerialIdentifierForBulding(101, 574938, 0))