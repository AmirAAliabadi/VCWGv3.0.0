#Calculate monthly building performance metrics and save to file
import random
import sys
import os
import numpy
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def BEMMonthly(Input_file, TimeStep, num_Steps):

    #Define file names
    fileName = Input_file

    #Constants
    HeatingValue = 37000            # Energy in a cubic meter of natural gas [kJ m^-3]
    SpinUpDays = 3                  # Number of days to ignore data
    SpinUpHours = SpinUpDays * 24   # Number of hours to ignore data

    #Load all data in a matrix
    data = numpy.loadtxt(fileName)

    Hour = data[:,0]
    sensCoolDemand = data[:, 1]
    sensHeatDemand = data[:, 2]
    dehumDemand = data[:, 3]
    coolConsump = data[:, 4]
    sensWasteCoolHeatDehum = data[:, 5]
    heatConsump = data[:, 6]
    indoorTemp = data[:, 7]
    QWater = data[:, 8]
    QGas = data[:, 9]
    sensWaste = data[:, 10]
    elecDomesticDemand = data[:, 11]
    sensWaterHeatDemand = data[:, 12]
    Nocc = data[:, 13]
    TempSetPointHeat = data[:, 14]
    TempSetPointCool = data[:, 15]
    IndoorHumidity = data[:, 16]
    OutdoorHumidity = data[:, 17]

    #Averaging some of above variables over a months (skipping spinuphours)
    # Tindoor_average = numpy.mean(indoorTemp[SpinUpHours:])
    # OccuPre_average = numpy.mean(Nocc[SpinUpHours:])
    # SmartSetPointHeat_average = numpy.mean(SmartSetPointHeat [SpinUpHours:])
    # SmartSetPointCool_average = numpy.mean(SmartSetPointCool[SpinUpHours:])

        # heating demand is partitioned into Q_hp or sensible heating demand
        # so to calculate total building sensible heating demand they must be added
    TotalSensHeatDemand = (numpy.sum(sensHeatDemand[SpinUpHours:])) / 1000
    TotalGasConsumpHeat = ((numpy.sum(heatConsump[SpinUpHours:])) / 1000) * 3600 / HeatingValue
    TotalElecHeatDemand = 0

    TotalSensCoolDemand = numpy.sum(sensCoolDemand[SpinUpHours:])/1000
    TotalElecCoolDemand = numpy.sum(coolConsump[SpinUpHours:])/1000

    # sensible water heating demand is partitioned into Q_waterSaved or sensible water heating demand
    # so to calculate total building sensible water heating demand they must be added
    TotalSensWaterHeatDemand = (numpy.sum(sensWaterHeatDemand[SpinUpHours:])) / 1000
    TotalGasConsumpWaterHeat = ((numpy.sum(QWater[SpinUpHours:])) / 1000) * 3600 / HeatingValue

    TotalElecDomesticDemand = numpy.sum(elecDomesticDemand[SpinUpHours:]) / 1000
    TotalElecProducedPV = 0
    TotalElecProducedWT = 0

    TotalDehumDemand = (numpy.sum(abs(dehumDemand[SpinUpHours:]))) / 1000

#Spinup hours should be considered here later
    TimeStepAvgResMatrix=numpy.zeros((num_Steps,data.shape[1]))
    # Loop over each column
    for j in range(data.shape[1]):
        # Loop over each time step
        for i in range(num_Steps):
            start_index = i * TimeStep
            end_index = start_index + TimeStep
            Out_average = numpy.nanmean(data[start_index:end_index, j])
            TimeStepAvgResMatrix[i, j] = Out_average


    return TimeStepAvgResMatrix