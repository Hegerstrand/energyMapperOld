cd C:\Users\JOLN\Documents\GitHub\energyMapper\Test
python EnergyPlanner.py %1
@rem cd MapInfo
@rem mapinfopro /k EnergyMapper.mbx
@rem exit
@echo Please run EnergyMapper.mbx from within EnergyPro
@pause