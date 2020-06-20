import BBRhandler
import datafordeleren
import csvHandler
import emoweb
import logging
logging.basicConfig(filename='example.log',level=logging.DEBUG)
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')
#BBRhandler.calculateEnergyDemand(630)
#datafordeleren.getBygninrger(210, "210.csv", 900000)
#datafordeleren.getHusnummer(3310, "Ølsted.csv", 100*1000)
#datafordeleren.getAdres    ser("Ølsted.xlx½sx", "Husnummer", "Adresser.csv")

#emoweb.getBulding(emoweb.getLabelSerialIdentifierForBulding(101, 574938, 0))
#emoweb.getEnergyLabelForLabelSerialIdentifierFromTo(200053229, 200053239)
emoweb.getAllBuildingsInKommune(169)