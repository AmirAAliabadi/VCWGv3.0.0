import numpy
import os

"""
Write output
Developed by Mohsen Moradi and Amir A. Aliabadi
Atmospheric Innovations Research (AIR) Laboratory, University of Guelph, Guelph, Canada
Originally developed by Naika Meili
Last update: February 2021
"""

def Write_Forcing(case,ForcingData,time,Output_dir, month_name):

    timeseriesFilename = os.path.join(Output_dir,"Forcing" + case + month_name + ".txt")
    outputFile_Forcing = open(timeseriesFilename, "w")
    outputFile_Forcing.write("#### \t Vertical City Weather Generator (VCWG)  \t #### \n")
    outputFile_Forcing.write("# Forcing parameters near surface or top of the domain based on user's choice \n")
    outputFile_Forcing.write("# 0:time [hr] 1:T [K] 2:S [m s^-1] 3:RH [-] 4:q [kg kg^-1] 5:Pressure [Pa] 6:Rain [mm s^-1] \n")
    for i in range(len(time)):
        outputFile_Forcing.write("%i %f %f %f %f %f %f \n"
                                 % (i, ForcingData[i].Tatm, ForcingData[i].Uatm,ForcingData[i].rel_hum,
                                    ForcingData[i].q_atm, ForcingData[i].Pre,ForcingData[i].Rain))
    outputFile_Forcing.close()

def Write_EB(case,FractionsRoof,FractionsGround,ParTree,RSMParam, EBRoofData,EBCanyonData,EBRuralData,UCMData,time,Output_dir, month_name):

    timeseriesFilename = os.path.join(Output_dir,"SWR"+case+  month_name +".txt")
    outputFile_SWR = open(timeseriesFilename, "w")
    outputFile_SWR.write("#### \t Vertical City Weather Generator (VCWG)  \t #### \n")
    outputFile_SWR.write("# Shortwave radiative fluxes at the surfaces \n")
    outputFile_SWR.write("# 0:time [hr] 1:SWRabsRoofImp [W m^-2] 2:SWRabsRoofVeg [W m^-2] 3:SWRabsTotalRoof [W m^-2] 4:SWRabsGroundImp [W m^-2] "
                         "5:SWRabsGroundBare [W m^-2] 6:SWRabsGroundVeg [W m^-2] 7:SWRabsTree [W m^-2] 8:SWRabsWallSun [W m^-2] "
                         "9:SWRabsWallShade [W m^-2] 10:SWRabsTotalGround [W m^-2] 11:SWRabsTotalCanyon [W m^-2] 12:SWRabsTotalUrban [W m^-2] "
                         "13:SWRinRoofImp [W m^-2] 14:SWRinRoofVeg [W m^-2] 15:SWRinTotalRoof [W m^-2] 16:SWRinGroundImp [W m^-2] 17:SWRinGroundBare [W m^-2] "
                         "18:SWRinGroundVeg [W m^-2] 19:SWRinTree [W m^-2] 20:SWRinWallSun [W m^-2] 21:SWRinWallShade [W m^-2] 22:SWRinTotalGround [W m^-2] "
                         "23:SWRinTotalCanyon [W m^-2] 24:SWRinTotalUrban [W m^-2] 25:SWRoutRoofImp [W m^-2] 26:SWRoutRoofVeg [W m^-2] 27:SWRoutTotalRoof [W m^-2] "
                         "28:SWRoutGroundImp [W m^-2] 29:SWRoutGroundBare [W m^-2] 30:SWRoutGroundVeg [W m^-2] 31:SWRoutTree [W m^-2] 32:SWRoutWallSun [W m^-2] "
                         "33:SWRoutWallShade [W m^-2] 34:SWRoutTotalGround [W m^-2] 35:SWRoutTotalCanyon [W m^-2] 36:SWRoutTotalUrban [W m^-2] "
                         "37:SWRinRural [W m^-2] 38:SWRoutRural [W m^-2] 39:SWRabsRural [W m^-2] \n")
    for i in range(len(time)):

        #Write NaN if an urban feature is non-existent
        if not int(FractionsRoof.fimp > 0) == 1:
            EBRoofData[i].SWR.SWRabsRoofImp = numpy.NaN
            EBRoofData[i].SWR.SWRinRoofImp = numpy.NaN
            EBRoofData[i].SWR.SWRoutRoofImp = numpy.NaN
        if not int(FractionsRoof.fveg > 0) == 1:
            EBRoofData[i].SWR.SWRabsRoofVeg = numpy.NaN
            EBRoofData[i].SWR.SWRinRoofVeg = numpy.NaN
            EBRoofData[i].SWR.SWRoutRoofVeg = numpy.NaN
        if not int(FractionsGround.fimp > 0) == 1:
            EBCanyonData[i].SWR.SWRabs.SWRabsGroundImp = numpy.NaN
            EBCanyonData[i].SWR.SWRin.SWRinGroundImp = numpy.NaN
            EBCanyonData[i].SWR.SWRout.SWRoutGroundImp = numpy.NaN
        if not int(FractionsGround.fveg > 0) == 1:
            EBCanyonData[i].SWR.SWRabs.SWRabsGroundVeg = numpy.NaN
            EBCanyonData[i].SWR.SWRin.SWRinGroundVeg = numpy.NaN
            EBCanyonData[i].SWR.SWRout.SWRoutGroundVeg = numpy.NaN
        if not int(FractionsGround.fbare > 0) == 1:
            EBCanyonData[i].SWR.SWRabs.SWRabsGroundBare = numpy.NaN
            EBCanyonData[i].SWR.SWRin.SWRinGroundBare = numpy.NaN
            EBCanyonData[i].SWR.SWRout.SWRoutGroundBare = numpy.NaN
        if not int(ParTree.trees == 1) == 1:
            EBCanyonData[i].SWR.SWRabs.SWRabsTree = numpy.NaN
            EBCanyonData[i].SWR.SWRin.SWRinTree = numpy.NaN
            EBCanyonData[i].SWR.SWRout.SWRoutTree = numpy.NaN
        if RSMParam.Rural_Model_name == 'Forcing_extFile':
            EBRuralData[i].EnergyFlux.SWRinRural = numpy.NaN
            EBRuralData[i].EnergyFlux.SWRoutRural = numpy.NaN
            EBRuralData[i].EnergyFlux.SWRabsRural = numpy.NaN

        outputFile_SWR.write("%i %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f \n"
                             % (i,EBRoofData[i].SWR.SWRabsRoofImp,EBRoofData[i].SWR.SWRabsRoofVeg,EBRoofData[i].SWR.SWRabsTotalRoof,
                                EBCanyonData[i].SWR.SWRabs.SWRabsGroundImp,EBCanyonData[i].SWR.SWRabs.SWRabsGroundBare,
                                EBCanyonData[i].SWR.SWRabs.SWRabsGroundVeg,EBCanyonData[i].SWR.SWRabs.SWRabsTree,
                                EBCanyonData[i].SWR.SWRabs.SWRabsWallSun,EBCanyonData[i].SWR.SWRabs.SWRabsWallShade,
                                EBCanyonData[i].SWR.SWRabs.SWRabsTotalGround,EBCanyonData[i].SWR.SWRabs.SWRabsTotalCanyon,
                                EBCanyonData[i].SWR.SWRabsTotalUrban,EBRoofData[i].SWR.SWRinRoofImp,EBRoofData[i].SWR.SWRinRoofVeg,
                                EBRoofData[i].SWR.SWRinTotalRoof,EBCanyonData[i].SWR.SWRin.SWRinGroundImp,EBCanyonData[i].SWR.SWRin.SWRinGroundBare,
                                EBCanyonData[i].SWR.SWRin.SWRinGroundVeg,EBCanyonData[i].SWR.SWRin.SWRinTree,EBCanyonData[i].SWR.SWRin.SWRinWallSun,
                                EBCanyonData[i].SWR.SWRin.SWRinWallShade,EBCanyonData[i].SWR.SWRin.SWRinTotalGround,
                                EBCanyonData[i].SWR.SWRin.SWRinTotalCanyon,EBCanyonData[i].SWR.SWRinTotalUrban,
                                EBRoofData[i].SWR.SWRoutRoofImp,EBRoofData[i].SWR.SWRoutRoofVeg,EBRoofData[i].SWR.SWRoutTotalRoof,
                                EBCanyonData[i].SWR.SWRout.SWRoutGroundImp,EBCanyonData[i].SWR.SWRout.SWRoutGroundBare,
                                EBCanyonData[i].SWR.SWRout.SWRoutGroundVeg,EBCanyonData[i].SWR.SWRout.SWRoutTree,
                                EBCanyonData[i].SWR.SWRout.SWRoutWallSun,EBCanyonData[i].SWR.SWRout.SWRoutWallShade,
                                EBCanyonData[i].SWR.SWRout.SWRoutTotalGround,EBCanyonData[i].SWR.SWRout.SWRoutTotalCanyon,
                                EBCanyonData[i].SWR.SWRoutTotalUrban,EBRuralData[i].EnergyFlux.SWRinRural,EBRuralData[i].EnergyFlux.SWRoutRural,
                                EBRuralData[i].EnergyFlux.SWRabsRural))
    outputFile_SWR.close()


    timeseriesFilename = os.path.join(Output_dir,"LWR"+case+month_name+".txt")
    outputFile_LWR = open(timeseriesFilename, "w")
    outputFile_LWR.write("#### \t Vertical City Weather Generator (VCWG)  \t #### \n")
    outputFile_LWR.write("# Longwave radiative fluxes at the surfaces \n")
    outputFile_LWR.write("# 0:time [hr] 1:LWRabsRoofImp [W m^-2] 2:LWRabsRoofVeg [W m^-2] 3:LWRabsTotalRoof [W m^-2] 4:LWRabsGroundImp [W m^-2] "
                         "5:LWRabsGroundBare [W m^-2] 6:LWRabsGroundVeg [W m^-2] 7:LWRabsTree [W m^-2] 8:LWRabsWallSun [W m^-2] "
                         "9:LWRabsWallShade [W m^-2] 10:LWRabsTotalGround [W m^-2] 11:LWRabsTotalCanyon [W m^-2] 12:LWRabsTotalUrban [W m^-2] "
                         "13:LWRinRoofImp [W m^-2] 14:LWRinRoofVeg [W m^-2] 15:LWRinTotalRoof [W m^-2] 16:LWRinGroundImp [W m^-2] 17:LWRinGroundBare [W m^-2] "
                         "18:LWRinGroundVeg [W m^-2] 19:LWRinTree [W m^-2] 20:LWRinWallSun [W m^-2] 21:LWRinWallShade [W m^-2] 22:LWRinTotalGround [W m^-2] "
                         "23:LWRinTotalCanyon [W m^-2] 24:LWRinTotalUrban [W m^-2] 25:LWRoutRoofImp [W m^-2] 26:LWRoutRoofVeg [W m^-2] 27:LWRoutTotalRoof [W m^-2] "
                         "28:LWRoutGroundImp [W m^-2] 29:LWRoutGroundBare [W m^-2] 30:LWRoutGroundVeg [W m^-2] 31:LWRoutTree [W m^-2] 32:LWRoutWallSun [W m^-2] "
                         "33:LWRoutWallShade [W m^-2] 34:LWRoutTotalGround [W m^-2] 35:LWRoutTotalCanyon [W m^-2] 36:LWRoutTotalUrban [W m^-2] "
                         "37:LWRinRural [W m^-2] 38:LWRoutRural [W m^-2] 39:LWRabsRural [W m^-2] \n")
    for i in range(len(time)):

        #Write NaN if an urban feature is non-existent
        if not int(FractionsRoof.fimp > 0) == 1:
            EBRoofData[i].LWR.LWRabsRoofImp = numpy.NaN
            EBRoofData[i].LWR.LWRinRoofImp = numpy.NaN
            EBRoofData[i].LWR.LWRoutRoofImp = numpy.NaN
        if not int(FractionsRoof.fveg > 0) == 1:
            EBRoofData[i].LWR.LWRabsRoofVeg = numpy.NaN
            EBRoofData[i].LWR.LWRinRoofVeg = numpy.NaN
            EBRoofData[i].LWR.LWRoutRoofVeg = numpy.NaN
        if not int(FractionsGround.fimp > 0) == 1:
            EBCanyonData[i].LWR.LWRabs.LWRabsGroundImp = numpy.NaN
            EBCanyonData[i].LWR.LWRin.LWRinGroundImp = numpy.NaN
            EBCanyonData[i].LWR.LWRout.LWRoutGroundImp = numpy.NaN
        if not int(FractionsGround.fveg > 0) == 1:
            EBCanyonData[i].LWR.LWRabs.LWRabsGroundVeg = numpy.NaN
            EBCanyonData[i].LWR.LWRin.LWRinGroundVeg = numpy.NaN
            EBCanyonData[i].LWR.LWRout.LWRoutGroundVeg = numpy.NaN
        if not int(FractionsGround.fbare > 0) == 1:
            EBCanyonData[i].LWR.LWRabs.LWRabsGroundBare = numpy.NaN
            EBCanyonData[i].LWR.LWRin.LWRinGroundBare = numpy.NaN
            EBCanyonData[i].LWR.LWRout.LWRoutGroundBare = numpy.NaN
        if not int(ParTree.trees == 1) == 1:
            EBCanyonData[i].LWR.LWRabs.LWRabsTree = numpy.NaN
            EBCanyonData[i].LWR.LWRin.LWRinTree = numpy.NaN
            EBCanyonData[i].LWR.LWRout.LWRoutTree = numpy.NaN
        if RSMParam.Rural_Model_name == 'Forcing_extFile':
            EBRuralData[i].EnergyFlux.LWRinRural = numpy.NaN
            EBRuralData[i].EnergyFlux.LWRoutRural = numpy.NaN
            EBRuralData[i].EnergyFlux.LWRabsRural = numpy.NaN

        outputFile_LWR.write("%i %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f \n"
                             % (i,EBRoofData[i].LWR.LWRabsRoofImp,EBRoofData[i].LWR.LWRabsRoofVeg,EBRoofData[i].LWR.LWRabsTotalRoof,
                                EBCanyonData[i].LWR.LWRabs.LWRabsGroundImp,EBCanyonData[i].LWR.LWRabs.LWRabsGroundBare,
                                EBCanyonData[i].LWR.LWRabs.LWRabsGroundVeg,EBCanyonData[i].LWR.LWRabs.LWRabsTree,
                                EBCanyonData[i].LWR.LWRabs.LWRabsWallSun,EBCanyonData[i].LWR.LWRabs.LWRabsWallShade,
                                EBCanyonData[i].LWR.LWRabs.LWRabsTotalGround,EBCanyonData[i].LWR.LWRabs.LWRabsTotalCanyon,
                                EBCanyonData[i].LWR.LWRabsTotalUrban,EBRoofData[i].LWR.LWRinRoofImp,EBRoofData[i].LWR.LWRinRoofVeg,
                                EBRoofData[i].LWR.LWRinTotalRoof,EBCanyonData[i].LWR.LWRin.LWRinGroundImp,EBCanyonData[i].LWR.LWRin.LWRinGroundBare,
                                EBCanyonData[i].LWR.LWRin.LWRinGroundVeg,EBCanyonData[i].LWR.LWRin.LWRinTree,EBCanyonData[i].LWR.LWRin.LWRinWallSun,
                                EBCanyonData[i].LWR.LWRin.LWRinWallShade,EBCanyonData[i].LWR.LWRin.LWRinTotalGround,
                                EBCanyonData[i].LWR.LWRin.LWRinTotalCanyon,EBCanyonData[i].LWR.LWRinTotalUrban,
                                EBRoofData[i].LWR.LWRoutRoofImp,EBRoofData[i].LWR.LWRoutRoofVeg,EBRoofData[i].LWR.LWRoutTotalRoof,
                                EBCanyonData[i].LWR.LWRout.LWRoutGroundImp,EBCanyonData[i].LWR.LWRout.LWRoutGroundBare,
                                EBCanyonData[i].LWR.LWRout.LWRoutGroundVeg,EBCanyonData[i].LWR.LWRout.LWRoutTree,
                                EBCanyonData[i].LWR.LWRout.LWRoutWallSun,EBCanyonData[i].LWR.LWRout.LWRoutWallShade,
                                EBCanyonData[i].LWR.LWRout.LWRoutTotalGround,EBCanyonData[i].LWR.LWRout.LWRoutTotalCanyon,
                                EBCanyonData[i].LWR.LWRoutTotalUrban,EBRuralData[i].EnergyFlux.LWRinRural,EBRuralData[i].EnergyFlux.LWRoutRural,
                                EBRuralData[i].EnergyFlux.LWRabsRural))
    outputFile_LWR.close()

    timeseriesFilename = os.path.join(Output_dir,"Hfluxes"+case+month_name+".txt")
    outputFile_Hflux = open(timeseriesFilename, "w")
    outputFile_Hflux.write("#### \t Vertical City Weather Generator (VCWG)  \t #### \n")
    outputFile_Hflux.write("# Sensible heat fluxes at the surfaces \n")
    outputFile_Hflux.write("# 0:time [hr] 1:HfluxRoofImp [W m^-2] 2:HfluxRoofVeg [W m^-2] 3:HfluxRoof [W m^-2] 4:HfluxGroundImp [W m^-2] "
                           "5:HfluxGroundBare [W m^-2] 6:HfluxGroundVeg [W m^-2] 7:HfluxGround [W m^-2] 8:HfluxTree [W m^-2] "
                           "9:HfluxWallSun [W m^-2] 10:HfluxWallShade [W m^-2] 11:HfluxCanyon [W m^-2] 12:HfluxRural [W m^-2] "
                           "13:HfluxUrban [W m^-2] \n")
    for i in range(len(time)):

        #Write NaN if an urban feature is non-existent
        if not int(FractionsRoof.fimp > 0) == 1:
            EBRoofData[i].Hflux.HfluxRoofImp = numpy.NaN
        if not int(FractionsRoof.fveg > 0) == 1:
            EBRoofData[i].Hflux.HfluxRoofVeg = numpy.NaN
        if not int(FractionsGround.fimp > 0) == 1:
            EBCanyonData[i].Hflux.HfluxGroundImp = numpy.NaN
        if not int(FractionsGround.fveg > 0) == 1:
            EBCanyonData[i].Hflux.HfluxGroundVeg = numpy.NaN
        if not int(FractionsGround.fbare > 0) == 1:
            EBCanyonData[i].Hflux.HfluxGroundBare = numpy.NaN
        if not int(ParTree.trees == 1) == 1:
            EBCanyonData[i].Hflux.HfluxTree = numpy.NaN
        if RSMParam.Rural_Model_name == 'Forcing_extFile':
            EBRuralData[i].EnergyFlux.HfluxRural = numpy.NaN

        outputFile_Hflux.write("%i %f %f %f %f %f %f %f %f %f %f %f %f %f\n"
                             % (i,EBRoofData[i].Hflux.HfluxRoofImp,EBRoofData[i].Hflux.HfluxRoofVeg,EBRoofData[i].Hflux.HfluxRoof,
                                EBCanyonData[i].Hflux.HfluxGroundImp,EBCanyonData[i].Hflux.HfluxGroundBare,EBCanyonData[i].Hflux.HfluxGroundVeg,
                                EBCanyonData[i].Hflux.HfluxGround,EBCanyonData[i].Hflux.HfluxTree,EBCanyonData[i].Hflux.HfluxWallSun,
                                EBCanyonData[i].Hflux.HfluxWallShade,EBCanyonData[i].Hflux.HfluxCanyon,EBRuralData[i].EnergyFlux.HfluxRural,
                                UCMData[i].UrbanFlux_H))
    outputFile_Hflux.close()

    timeseriesFilename = os.path.join(Output_dir,"LEfluxes"+case+month_name+".txt")
    outputFile_LEfluxes = open(timeseriesFilename, "w")
    outputFile_LEfluxes.write("#### \t Vertical City Weather Generator (VCWG)  \t #### \n")
    outputFile_LEfluxes.write("# Latent heat fluxes at the surfaces \n")
    outputFile_LEfluxes.write("# 0:time [hr] 1:LEfluxRoofImp [W m^-2] 2:LEfluxRoofVegInt [W m^-2] 3:LEfluxRoofVegPond [W m^-2] 4:LEfluxRoofVegSoil [W m^-2] "
                              "5:LTEfluxRoofVeg [W m^-2] 6:LEfluxRoofVeg [W m^-2] 7:LEfluxRoof [W m^-2] 8:LEfluxGroundImp [W m^-2] "
                              "9:LEfluxGroundBarePond [W m^-2] 10:LEfluxGroundBareSoil [W m^-2] 11:LEfluxGroundBare 12:LEfluxGroundVegInt "
                              "13:LEfluxGroundVegPond [W m^-2] 14:LEfluxGroundVegSoil [W m^-2] 15:LTEfluxGroundVeg [W m^-2] "
                              "16:LEfluxGroundVeg [W m^-2] 17:LEfluxGround [W m^-2] 18:LEfluxTreeInt [W m^-2] 19:LTEfluxTree [W m^-2] "
                              "20:LEfluxTree [W m^-2] 21:LEfluxWallSun [W m^-2] 22:LEfluxWallShade [W m^-2] 23:LEfluxCanyon [W m^-2] "
                              "24:LEfluxRural [W m^-2] 25:LEfluxUrban [W m^-2] \n")
    for i in range(len(time)):

        #Write NaN if an urban feature is non-existent
        if not int(FractionsRoof.fimp > 0) == 1:
            EBRoofData[i].LEflux.LEfluxRoofImp = numpy.NaN
        if not int(FractionsRoof.fveg > 0) == 1:
            EBRoofData[i].LEflux.LEfluxRoofVegInt = numpy.NaN
            EBRoofData[i].LEflux.LEfluxRoofVegPond = numpy.NaN
            EBRoofData[i].LEflux.LEfluxRoofVegSoil = numpy.NaN
            EBRoofData[i].LEflux.LTEfluxRoofVeg = numpy.NaN
            EBRoofData[i].LEflux.LEfluxRoofVeg = numpy.NaN
        if not int(FractionsGround.fimp > 0) == 1:
            EBCanyonData[i].LEflux.LEfluxGroundImp = numpy.NaN
        if not int(FractionsGround.fveg > 0) == 1:
            EBCanyonData[i].LEflux.LEfluxGroundVegInt = numpy.NaN
            EBCanyonData[i].LEflux.LEfluxGroundVegPond = numpy.NaN
            EBCanyonData[i].LEflux.LEfluxGroundVegSoil = numpy.NaN
            EBCanyonData[i].LEflux.LTEfluxGroundVeg = numpy.NaN
            EBCanyonData[i].LEflux.LEfluxGroundVeg = numpy.NaN
        if not int(FractionsGround.fbare > 0) == 1:
            EBCanyonData[i].LEflux.LEfluxGroundBarePond = numpy.NaN
            EBCanyonData[i].LEflux.LEfluxGroundBareSoil = numpy.NaN
            EBCanyonData[i].LEflux.LEfluxGroundBare = numpy.NaN
        if not int(ParTree.trees == 1) == 1:
            EBCanyonData[i].LEflux.LEfluxTreeInt = numpy.NaN
            EBCanyonData[i].LEflux.LTEfluxTree = numpy.NaN
            EBCanyonData[i].LEflux.LEfluxTree = numpy.NaN
        if RSMParam.Rural_Model_name == 'Forcing_extFile':
            EBRuralData[i].EnergyFlux.LEfluxRural = numpy.NaN

        outputFile_LEfluxes.write("%i %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f \n"
                             % (i,EBRoofData[i].LEflux.LEfluxRoofImp,EBRoofData[i].LEflux.LEfluxRoofVegInt,
                                EBRoofData[i].LEflux.LEfluxRoofVegPond,EBRoofData[i].LEflux.LEfluxRoofVegSoil,
                                EBRoofData[i].LEflux.LTEfluxRoofVeg,EBRoofData[i].LEflux.LEfluxRoofVeg,EBRoofData[i].LEflux.LEfluxRoof,
                                EBCanyonData[i].LEflux.LEfluxGroundImp,EBCanyonData[i].LEflux.LEfluxGroundBarePond,
                                EBCanyonData[i].LEflux.LEfluxGroundBareSoil,EBCanyonData[i].LEflux.LEfluxGroundBare,
                                EBCanyonData[i].LEflux.LEfluxGroundVegInt,EBCanyonData[i].LEflux.LEfluxGroundVegPond,
                                EBCanyonData[i].LEflux.LEfluxGroundVegSoil,EBCanyonData[i].LEflux.LTEfluxGroundVeg,
                                EBCanyonData[i].LEflux.LEfluxGroundVeg,EBCanyonData[i].LEflux.LEfluxGround,EBCanyonData[i].LEflux.LEfluxTreeInt,
                                EBCanyonData[i].LEflux.LTEfluxTree,EBCanyonData[i].LEflux.LEfluxTree,EBCanyonData[i].LEflux.LEfluxWallSun,
                                EBCanyonData[i].LEflux.LEfluxWallShade,EBCanyonData[i].LEflux.LEfluxCanyon,
                                EBRuralData[i].EnergyFlux.LEfluxRural,UCMData[i].UrbanFlux_LE))
    outputFile_LEfluxes.close()

    timeseriesFilename = os.path.join(Output_dir,"Gfluxes"+case+month_name+".txt")
    outputFile_Gfluxes = open(timeseriesFilename, "w")
    outputFile_Gfluxes.write("#### \t Vertical City Weather Generator (VCWG)  \t #### \n")
    outputFile_Gfluxes.write("# Conductive heat fluxes at the surfaces \n")
    outputFile_Gfluxes.write("# 0:time [hr] 1:GfluxRoofImp [W m^-2] 2:GfluxRoofVeg [W m^-2] 3:GfluxRoof [W m^-2] 4:GfluxGroundImp [W m^-2] "
                             "5:GfluxGroundBare [W m^-2] 6:GfluxGroundVeg [W m^-2] 7:GfluxGround [W m^-2] 8:GfluxWallSun [W m^-2] "
                             "9:GfluxWallShade [W m^-2] 10:GfluxRural [W m^-2] \n")
    for i in range(len(time)):

        #Write NaN if an urban feature is non-existent
        if not int(FractionsRoof.fimp > 0) == 1:
            EBRoofData[i].Gflux.GfluxRoofImp = numpy.NaN
        if not int(FractionsRoof.fveg > 0) == 1:
            EBRoofData[i].Gflux.GfluxRoofVeg = numpy.NaN
        if not int(FractionsGround.fimp > 0) == 1:
            EBCanyonData[i].Gflux.GfluxGroundImp = numpy.NaN
        if not int(FractionsGround.fveg > 0) == 1:
            EBCanyonData[i].Gflux.GfluxGroundVeg = numpy.NaN
        if not int(FractionsGround.fbare > 0) == 1:
            EBCanyonData[i].Gflux.GfluxGroundBare = numpy.NaN
        if RSMParam.Rural_Model_name == 'Forcing_extFile':
            EBRuralData[i].EnergyFlux.GfluxRural = numpy.NaN

        outputFile_Gfluxes.write("%i %f %f %f %f %f %f %f %f %f %f \n"
                             % (i,EBRoofData[i].Gflux.GfluxRoofImp,EBRoofData[i].Gflux.GfluxRoofVeg,EBRoofData[i].Gflux.GfluxRoof,
                                EBCanyonData[i].Gflux.GfluxGroundImp,EBCanyonData[i].Gflux.GfluxGroundBare,EBCanyonData[i].Gflux.GfluxGroundVeg,
                                EBCanyonData[i].Gflux.GfluxGround,EBCanyonData[i].Gflux.GfluxWallSun,EBCanyonData[i].Gflux.GfluxWallShade,
                                EBRuralData[i].EnergyFlux.GfluxRural))
    outputFile_Gfluxes.close()

    timeseriesFilename = os.path.join(Output_dir,"Efluxes"+case+month_name+".txt")
    outputFile_Efluxes = open(timeseriesFilename, "w")
    outputFile_Efluxes.write("#### \t Vertical City Weather Generator (VCWG)  \t #### \n")
    outputFile_Efluxes.write("# Evaporative fluxes at the surfaces \n")
    outputFile_Efluxes.write("# 0:time [hr] 1:EfluxRoofImp [kg m^-2 s^-1] 2:LEfluxRoofVegInt [kg m^-2 s^-1] 3:EfluxRoofVegPond [kg m^-2 s^-1] 4:EfluxRoofVegSoil [kg m^-2 s^-1] "
                             "5:TEfluxRoofVeg [kg m^-2 s^-1] 6:EfluxRoofVeg [kg m^-2 s^-1] 7:EfluxRoof [kg m^-2 s^-1] 8:EfluxGroundImp [kg m^-2 s^-1]"
                             "9:EfluxGroundBarePond [kg m^-2 s^-1] 10:EfluxGroundBareSoil [kg m^-2 s^-1] 11:EfluxGroundBare [kg m^-2 s^-1] 12:EfluxGroundVegInt [kg m^-2 s^-1] "
                             "13:EfluxGroundVegPond [kg m^-2 s^-1] 14:EfluxGroundVegSoil [kg m^-2 s^-1] 15:TEfluxGroundVeg [kg m^-2 s^-1] "
                             "16:EfluxGroundVeg [kg m^-2 s^-1] 17:EfluxGround [kg m^-2 s^-1] 18:EfluxTreeInt [kg m^-2 s^-1] 19:TEfluxTree [kg m^-2 s^-1] "
                             "20:EfluxTree [kg m^-2 s^-1] 21:EfluxWallSun [kg m^-2 s^-1] 22:EfluxWallShade [kg m^-2 s^-1] \n")
    for i in range(len(time)):

        #Write NaN if an urban feature is non-existent
        if not int(FractionsRoof.fimp > 0) == 1:
            EBRoofData[i].Eflux.EfluxRoofImp = numpy.NaN
        if not int(FractionsRoof.fveg > 0) == 1:
            EBRoofData[i].Eflux.EfluxRoofVegInt = numpy.NaN
            EBRoofData[i].Eflux.EfluxRoofVegPond = numpy.NaN
            EBRoofData[i].Eflux.EfluxRoofVegSoil = numpy.NaN
            EBRoofData[i].Eflux.TEfluxRoofVeg = numpy.NaN
            EBRoofData[i].Eflux.EfluxRoofVeg = numpy.NaN
        if not int(FractionsGround.fimp > 0) == 1:
            EBCanyonData[i].Eflux.EfluxGroundImp = numpy.NaN
        if not int(FractionsGround.fveg > 0) == 1:
            EBCanyonData[i].Eflux.EfluxGroundVegInt = numpy.NaN
            EBCanyonData[i].Eflux.EfluxGroundVegPond = numpy.NaN
            EBCanyonData[i].Eflux.EfluxGroundVegSoil = numpy.NaN
            EBCanyonData[i].Eflux.TEfluxGroundVeg = numpy.NaN
            EBCanyonData[i].Eflux.EfluxGroundVeg = numpy.NaN
        if not int(FractionsGround.fbare > 0) == 1:
            EBCanyonData[i].Eflux.EfluxGroundBarePond = numpy.NaN
            EBCanyonData[i].Eflux.EfluxGroundBareSoil = numpy.NaN
            EBCanyonData[i].Eflux.EfluxGroundBare = numpy.NaN
        if not int(ParTree.trees == 1) == 1:
            EBCanyonData[i].Eflux.EfluxTreeInt = numpy.NaN
            EBCanyonData[i].Eflux.TEfluxTree = numpy.NaN
            EBCanyonData[i].Eflux.EfluxTree = numpy.NaN

        outputFile_Efluxes.write("%i %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f \n"
                             % (i,EBRoofData[i].Eflux.EfluxRoofImp,EBRoofData[i].Eflux.EfluxRoofVegInt,EBRoofData[i].Eflux.EfluxRoofVegPond,
                                EBRoofData[i].Eflux.EfluxRoofVegSoil,EBRoofData[i].Eflux.TEfluxRoofVeg,EBRoofData[i].Eflux.EfluxRoofVeg,
                                EBRoofData[i].Eflux.EfluxRoof,EBCanyonData[i].Eflux.EfluxGroundImp,EBCanyonData[i].Eflux.EfluxGroundBarePond,
                                EBCanyonData[i].Eflux.EfluxGroundBareSoil,EBCanyonData[i].Eflux.EfluxGroundBare,EBCanyonData[i].Eflux.EfluxGroundVegInt,
                                EBCanyonData[i].Eflux.EfluxGroundVegPond,EBCanyonData[i].Eflux.EfluxGroundVegSoil,EBCanyonData[i].Eflux.TEfluxGroundVeg,
                                EBCanyonData[i].Eflux.EfluxGroundVeg,EBCanyonData[i].Eflux.EfluxGround,EBCanyonData[i].Eflux.EfluxTreeInt,
                                EBCanyonData[i].Eflux.TEfluxTree,EBCanyonData[i].Eflux.EfluxTree,EBCanyonData[i].Eflux.EfluxWallSun,
                                EBCanyonData[i].Eflux.EfluxWallShade))
    outputFile_Efluxes.close()

def Write_Tsurf(case,FractionsRoof,FractionsGround,ParTree,RoofImpData,RoofVegData,GroundImpData,GroundBareData,GroundVegData,WallSunData,WallShadeData,EBCanyonData,
                RuralData,RuralGroundImpData,RuralGroundBareData,RuralGroundVegData,RSMParam,time,Output_dir, month_name):
    if RSMParam.Rural_Model_name == 'Forcing_extFile':
        TextRural = [0 for i in range(len(RuralGroundVegData))]
    else:
        if RuralData[0] is not None:
            TextRural = [RuralData[i].Text for i in range(len(RuralData))]
        else:
            TextRural = [RSMParam.fimp*RuralGroundImpData[i].Text+RSMParam.fbare*RuralGroundBareData[i].Text+
                         RSMParam.fveg*RuralGroundVegData[i].Text for i in range(len(RuralGroundVegData))]

    timeseriesFilename = os.path.join(Output_dir,"Tsurf" + case +  month_name + ".txt")
    outputFile_Tsurf = open(timeseriesFilename, "w")
    outputFile_Tsurf.write("#### \t Vertical City Weather Generator (VCWG)  \t #### \n")
    outputFile_Tsurf.write("# Temperature at the surfaces \n")
    outputFile_Tsurf.write(
        "# 0:time [hr] 1:TRoofImp [K] 2:TRoofVeg [K] 3:TGroundImp [K] 4:TGroundBare [K] 5:TGroundVeg [K] "
        "6:TWallSun [K] 7:TWallShade [K] 8:TTree [K] 9:TRural [K]\n")
    for i in range(len(time)):

        #Write NaN if an urban feature is non-existent
        if not int(FractionsRoof.fimp > 0) == 1:
            RoofImpData[i].Text = numpy.NaN
        if not int(FractionsRoof.fveg > 0) == 1:
            RoofVegData[i].Text = numpy.NaN
        if not int(FractionsGround.fimp > 0) == 1:
            GroundImpData[i].Text = numpy.NaN
        if not int(FractionsGround.fveg > 0) == 1:
            GroundVegData[i].Text = numpy.NaN
        if not int(FractionsGround.fbare > 0) == 1:
            GroundBareData[i].Text = numpy.NaN
        if not int(ParTree.trees == 1) == 1:
            EBCanyonData[i].Ttree = numpy.NaN
        if RSMParam.Rural_Model_name == 'Forcing_extFile':
            TextRural[i] = numpy.NaN

        outputFile_Tsurf.write("%i %f %f %f %f %f %f %f %f %f \n"
                               % (i,RoofImpData[i].Text,RoofVegData[i].Text,GroundImpData[i].Text,GroundBareData[i].Text,
                                  GroundVegData[i].Text,WallSunData[i].Text,WallShadeData[i].Text,EBCanyonData[i].Ttree,
                                  TextRural[i]))
    outputFile_Tsurf.close()

def Write_WB(case,FractionsRoof,FractionsGround,ParTree, WBRoofData,WBCanyonData,time,Output_dir, month_name):

    # Generate output text file for leakage
    timeseriesFilename = os.path.join(Output_dir,"Leakage" + case +  month_name + ".txt")
    outputFile_Lk = open(timeseriesFilename, "w")
    outputFile_Lk.write("#### \t Vertical City Weather Generator (VCWG)  \t #### \n")
    outputFile_Lk.write("# Water leakage from roof and ground \n")
    outputFile_Lk.write(
        "# 0:time [hr] 1:LkRoofImp [mm s^-1] 2:LkRoofVeg [mm s^-1] 3:LkRoof [mm s^-1] 4:LkGroundImp [mm s^-1] 5:LkGroundBare [mm s^-1] "
        "6:LkGroundVeg [mm s^-1] 7:LkGround [mm s^-1] \n")
    for i in range(len(time)):

        #Write NaN if an urban feature is non-existent
        if not int(FractionsRoof.fimp > 0) == 1:
            WBRoofData[i].Leakage.LkRoofImp = numpy.NaN
        if not int(FractionsRoof.fveg > 0) == 1:
            WBRoofData[i].Leakage.LkRoofVeg = numpy.NaN
        if not int(FractionsGround.fimp > 0) == 1:
            WBCanyonData[i].Leakage.LkGroundImp = numpy.NaN
        if not int(FractionsGround.fveg > 0) == 1:
            WBCanyonData[i].Leakage.LkGroundVeg = numpy.NaN
        if not int(FractionsGround.fbare > 0) == 1:
            WBCanyonData[i].Leakage.LkGroundBare = numpy.NaN

        outputFile_Lk.write("%i %f %f %f %f %f %f %f \n"
                            % (i, WBRoofData[i].Leakage.LkRoofImp,WBRoofData[i].Leakage.LkRoofVeg,WBRoofData[i].Leakage.LkRoof,
                               WBCanyonData[i].Leakage.LkGroundImp,WBCanyonData[i].Leakage.LkGroundBare,WBCanyonData[i].Leakage.LkGroundVeg,
                               WBCanyonData[i].Leakage.LkGround))
    outputFile_Lk.close()

    # Generate output text file for dInt_dt
    timeseriesFilename = os.path.join(Output_dir,"InterceptionChange" + case +month_name+ ".txt")
    outputFile_dInt = open(timeseriesFilename, "w")
    outputFile_dInt.write("#### \t Vertical City Weather Generator (VCWG)  \t #### \n")
    outputFile_dInt.write("# Change in water interception at roof and ground \n")
    outputFile_dInt.write(
        "# 0:time [hr] 1:dInt_dtRoofImp [mm s^-1] 2:dInt_dtRoofVegPlant [mm s^-1] 3:dInt_dtRoofVegGround [mm s^-1]"
        " 4:dInt_dtRooftot [mm s^-1] 5:dInt_dtGroundImp [mm s^-1] 6:dInt_dtGroundBare [mm s^-1] 7:dInt_dtGroundVegPlant [mm s^-1] "
        "8:dInt_dtGroundVegGround [mm s^-1] 9:dInt_dtTree [mm s^-1] \n")
    for i in range(len(time)):

        # Write NaN if an urban feature is non-existent
        if not int(FractionsRoof.fimp > 0) == 1:
            WBRoofData[i].dInt_dt.dInt_dtRoofImp = numpy.NaN
        if not int(FractionsRoof.fveg > 0) == 1:
            WBRoofData[i].dInt_dt.dInt_dtRoofVegPlant = numpy.NaN
            WBRoofData[i].dInt_dt.dInt_dtRoofVegGround = numpy.NaN
        if not int(FractionsGround.fimp > 0) == 1:
            WBCanyonData[i].dInt_dt.dInt_dtGroundImp = numpy.NaN
        if not int(FractionsGround.fveg > 0) == 1:
            WBCanyonData[i].dInt_dt.dInt_dtGroundVegPlant = numpy.NaN
            WBCanyonData[i].dInt_dt.dInt_dtGroundVegGround = numpy.NaN
        if not int(FractionsGround.fbare > 0) == 1:
            WBCanyonData[i].dInt_dt.dInt_dtGroundBare = numpy.NaN
        if not int(ParTree.trees == 1) == 1:
            WBCanyonData[i].dInt_dt.dInt_dtTree = numpy.NaN

        outputFile_dInt.write("%i %f %f %f %f %f %f %f %f %f \n"
                              % (i, WBRoofData[i].dInt_dt.dInt_dtRoofImp,WBRoofData[i].dInt_dt.dInt_dtRoofVegPlant,
                                 WBRoofData[i].dInt_dt.dInt_dtRoofVegGround,WBRoofData[i].dInt_dt.dInt_dtRooftot,
                                 WBCanyonData[i].dInt_dt.dInt_dtGroundImp,WBCanyonData[i].dInt_dt.dInt_dtGroundBare,
                                 WBCanyonData[i].dInt_dt.dInt_dtGroundVegPlant,WBCanyonData[i].dInt_dt.dInt_dtGroundVegGround,
                                 WBCanyonData[i].dInt_dt.dInt_dtTree))
    outputFile_dInt.close()

    # Generate output text file for Infiltration
    timeseriesFilename = os.path.join(Output_dir,"Infiltration" + case +month_name+ ".txt")
    outputFile_Inf = open(timeseriesFilename, "w")
    outputFile_Inf.write("#### \t Vertical City Weather Generator (VCWG)  \t #### \n")
    outputFile_Inf.write("# Infiltration at roof and ground \n")
    outputFile_Inf.write(
        "# 0:time [hr] 1:fRoofVeg [mm s^-1] 2:fGroundBare [mm s^-1] 3:fGroundVeg [mm s^-1] 4:fGroundImp [mm s^-1] \n")
    for i in range(len(time)):

        # Write NaN if an urban feature is non-existent
        if not int(FractionsRoof.fveg > 0) == 1:
            WBRoofData[i].fRoofVeg = numpy.NaN
        if not int(FractionsRoof.fimp > 0) == 1:
            WBRoofData[i].fRoofVeg = numpy.NaN
        if not int(FractionsGround.fimp > 0) == 1:
            WBCanyonData[i].Infiltration.fGroundImp = numpy.NaN
        if not int(FractionsGround.fveg > 0) == 1:
            WBCanyonData[i].Infiltration.fGroundVeg = numpy.NaN
        if not int(FractionsGround.fbare > 0) == 1:
            WBCanyonData[i].Infiltration.fGroundBare = numpy.NaN

        outputFile_Inf.write("%i %f %f %f %f \n"
                             % (i, WBRoofData[i].fRoofVeg,WBCanyonData[i].Infiltration.fGroundBare,
                                WBCanyonData[i].Infiltration.fGroundVeg,WBCanyonData[i].Infiltration.fGroundImp))
    outputFile_Inf.close()

    # Generate output text file for Runoff
    timeseriesFilename = os.path.join(Output_dir,"Runoff" + case +month_name+ ".txt")
    outputFile_Runoff = open(timeseriesFilename, "w")
    outputFile_Runoff.write("#### \t Vertical City Weather Generator (VCWG)  \t #### \n")
    outputFile_Runoff.write("# Runoff at roof and ground \n")
    outputFile_Runoff.write(
        "# 0:time [hr] 1:QRoofImp [mm s^-1] 2:QRoofVegDrip [mm s^-1] 3:QRoofVegPond [mm s^-1] 4:QRoofVegSoil [mm s^-1] 5:QGroundImp [mm s^-1] "
        "6:QGroundBarePond [mm s^-1] 7:QGroundBareSoil [mm s^-1] 8:QTree [mm s^-1] 9:QGroundVegDrip [mm s^-1] 10:QGroundVegPond [mm s^-1] "
        " 11:QGroundVegSoil [mm s^-1], 12:RunoffGroundTot [mm s^-1]\n")
    for i in range(len(time)):

        # Write NaN if an urban feature is non-existent
        if not int(FractionsRoof.fimp > 0) == 1:
            WBRoofData[i].Runoff.QRoofImp = numpy.NaN
        if not int(FractionsRoof.fveg > 0) == 1:
            WBRoofData[i].Runoff.QRoofVegDrip = numpy.NaN
            WBRoofData[i].Runoff.QRoofVegPond = numpy.NaN
            WBRoofData[i].Runoff.QRoofVegSoil = numpy.NaN
            WBRoofData[i].Runoff.QRoofVegDrip = numpy.NaN
            WBRoofData[i].Runoff.QRoofVegPond = numpy.NaN
            WBRoofData[i].Runoff.QRoofVegSoil = numpy.NaN
        if not int(FractionsGround.fimp > 0) == 1:
            WBCanyonData[i].Runoff.QGroundImp = numpy.NaN
        if not int(FractionsGround.fveg > 0) == 1:
            WBCanyonData[i].Runoff.QGroundVegDrip = numpy.NaN
            WBCanyonData[i].Runoff.QGroundVegPond = numpy.NaN
            WBCanyonData[i].Runoff.QGroundVegSoil = numpy.NaN
        if not int(FractionsGround.fbare > 0) == 1:
            WBCanyonData[i].Runoff.QGroundBarePond = numpy.NaN
            WBCanyonData[i].Runoff.QGroundBareSoil = numpy.NaN
        if not int(ParTree.trees == 1) == 1:
            WBCanyonData[i].Runoff.QTree = numpy.NaN

        outputFile_Runoff.write("%i %f %f %f %f %f %f %f %f %f %f %f %f \n"
                                % (i,WBRoofData[i].Runoff.QRoofImp,WBRoofData[i].Runoff.QRoofVegDrip,WBRoofData[i].Runoff.QRoofVegPond,
                                   WBRoofData[i].Runoff.QRoofVegSoil,WBCanyonData[i].Runoff.QGroundImp,WBCanyonData[i].Runoff.QGroundBarePond,
                                   WBCanyonData[i].Runoff.QGroundBareSoil,WBCanyonData[i].Runoff.QTree,WBCanyonData[i].Runoff.QGroundVegDrip,
                                   WBCanyonData[i].Runoff.QGroundVegPond,WBCanyonData[i].Runoff.QGroundVegSoil,WBCanyonData[i].Runoff.RunoffGroundTot))
    outputFile_Runoff.close()

    # Generate output text file for Runon
    timeseriesFilename = os.path.join(Output_dir,"Runon" + case +month_name+ ".txt")
    outputFile_Runon = open(timeseriesFilename, "w")
    outputFile_Runon.write("#### \t Vertical City Weather Generator (VCWG)  \t #### \n")
    outputFile_Runon.write("# Runon at roof and ground \n")
    outputFile_Runon.write(
        "# 0:time [hr] 1:RunonRoofTot [mm s^-1] 2:RunoffRoofTot [mm s^-1] 3:RunonGroundTot [mm s^-1] 4:RunoffGroundTot [mm s^-1] 5:RunonUrban [mm s^-1] "
        "6:RunoffUrban [mm s^-1]\n")
    for i in range(len(time)):
        outputFile_Runon.write("%i %f %f %f %f %f %f \n"
                               % (i,WBRoofData[i].RunonRoofTot,WBRoofData[i].RunoffRoofTot,WBCanyonData[i].Runon.RunonGroundTot,
                                  WBCanyonData[i].Runoff.RunoffGroundTot,WBCanyonData[i].Runon.RunonUrban,WBCanyonData[i].Runoff.RunoffUrban))
    outputFile_Runon.close()

    # Generate output text file for dVwater
    timeseriesFilename = os.path.join(Output_dir,"SoilWaterVolumeChange" + case +month_name+ ".txt")
    outputFile_dVwater = open(timeseriesFilename, "w")
    outputFile_dVwater.write("#### \t Vertical City Weather Generator (VCWG)  \t #### \n")
    outputFile_dVwater.write("# Change in water volume of soil \n")
    outputFile_dVwater.write(
        "# 0:time [hr] 1:dVRoofSoilVeg_dt [mm s^-1] 2:dVGroundSoilImp_dt [mm s^-1] 3:dVGroundSoilBare_dt [mm s^-1] 4:dVGroundSoilVeg_dt [mm s^-1] "
        "5:dVGroundSoilTot_dt \n")
    for i in range(len(time)):

        # Write NaN if an urban feature is non-existent
        if not int(FractionsGround.fimp > 0) == 1:
            WBCanyonData[i].dVwater_dt.dVGroundSoilImp_dt = numpy.NaN
        if not int(FractionsGround.fveg > 0) == 1:
            WBCanyonData[i].dVwater_dt.dVGroundSoilVeg_dt = numpy.NaN
        if not int(FractionsGround.fbare > 0) == 1:
            WBCanyonData[i].dVwater_dt.dVGroundSoilBare_dt = numpy.NaN

        outputFile_dVwater.write("%i %f %f %f %f %f \n"
                                 % (i,WBRoofData[i].dVRoofSoil_dt,WBCanyonData[i].dVwater_dt.dVGroundSoilImp_dt,
                                    WBCanyonData[i].dVwater_dt.dVGroundSoilBare_dt,WBCanyonData[i].dVwater_dt.dVGroundSoilVeg_dt,
                                    WBCanyonData[i].dVwater_dt.dVGroundSoilTot_dt))
    outputFile_dVwater.close()

    # Generate output text file for WB_OtherParam
    timeseriesFilename = os.path.join(Output_dir,"OtherWaterTerms" + case +month_name+ ".txt")
    outputFile_WB_OtherParam = open(timeseriesFilename, "w")
    outputFile_WB_OtherParam.write("#### \t Vertical City Weather Generator (VCWG)  \t #### \n")
    outputFile_WB_OtherParam.write("# Other water terms \n")
    outputFile_WB_OtherParam.write(
        "# 0:time [hr] 1:RainGround [mm s^-1] 2:Anthropogenic_Bare [mm s^-1] 3:Anthropogenic_Veg [mm s^-1] 4:Egveg_Soil [kg m^-2 s^-1] "
        "5:Egimp_soil [kg m^-2 s^-1] 6:Rd_gimp [mm] 7:Rd_gveg [mm] 8:Rd_gbare [mm] 9:Anthropogenic_Roof [mm s^-1] 10: Etot [mm s^-1] 11:StorageTot [mm s^-1] \n")
    for i in range(len(time)):

        # Write NaN if an urban feature is non-existent
        ## Check if these terms are appropriately set to NaN
        if not int(FractionsGround.fimp > 0) == 1:
            WBCanyonData[i].Egimp_soil1 = numpy.NaN
            WBCanyonData[i].Rd.Rd_gimp = numpy.NaN
        if not int(FractionsGround.fveg > 0) == 1:
            WBCanyonData[i].Anth_gveg = numpy.NaN
            WBCanyonData[i].Egveg_Soil1 = numpy.NaN
            WBCanyonData[i].Rd.Rd_gveg = numpy.NaN
        if not int(FractionsGround.fbare > 0) == 1:
            WBCanyonData[i].Anth_gbare = numpy.NaN
            WBCanyonData[i].Rd.Rd_gbare = numpy.NaN

        outputFile_WB_OtherParam.write("%i %f %f %f %f %f %f %f %f %f %f %f \n"
                                 % (i,WBCanyonData[i].RainGround,WBCanyonData[i].Anth_gbare,WBCanyonData[i].Anth_gveg,WBCanyonData[i].Egveg_Soil1,
                                    WBCanyonData[i].Egimp_soil1,WBCanyonData[i].Rd.Rd_gimp,WBCanyonData[i].Rd.Rd_gveg,WBCanyonData[i].Rd.Rd_gbare,
                                    WBRoofData[i].Anthp,WBCanyonData[i].EfluxCanyon,WBCanyonData[i].WaterStorageCanyon))
    outputFile_WB_OtherParam.close()

    # Generate output text file for TE
    timeseriesFilename = os.path.join(Output_dir,"Transpiration" + case +month_name+ ".txt")
    outputFile_TE = open(timeseriesFilename, "w")
    outputFile_TE.write("#### \t Vertical City Weather Generator (VCWG)  \t #### \n")
    outputFile_TE.write("# Transpiration from low and high vegetation \n")
    outputFile_TE.write(
        "# 0:time [hr] 1:TEgveg_imp [kg m^-2 s^-1] 2:TEtree_imp [kg m^-2 s^-1] 3:TEgveg_bare [kg m^-2 s^-1] 4:TEtree_bare [kg m^-2 s^-1]"
        " 5:TEgveg_veg [kg m^-2 s^-1] 6:TEtree_veg [kg m^-2 s^-1]\n")
    for i in range(len(time)):

        # Write NaN if an urban feature is non-existent
        ## Check if these terms are appropriately set to NaN
        if not int(FractionsGround.fimp > 0) == 1:
            WBCanyonData[i].TE.TEgveg_imp = numpy.NaN
            WBCanyonData[i].TE.TEtree_imp = numpy.NaN
        if not int(FractionsGround.fveg > 0) == 1:
            WBCanyonData[i].TE.TEgveg_veg = numpy.NaN
            WBCanyonData[i].TE.TEtree_veg = numpy.NaN
        if not int(FractionsGround.fbare > 0) == 1:
            WBCanyonData[i].TE.TEgveg_bare = numpy.NaN
            WBCanyonData[i].TE.TEtree_bare = numpy.NaN

        outputFile_TE.write("%i %f %f %f %f %f %f \n"
                                       % (i,WBCanyonData[i].TE.TEgveg_imp,WBCanyonData[i].TE.TEtree_imp,WBCanyonData[i].TE.TEgveg_bare,
                                          WBCanyonData[i].TE.TEtree_bare,WBCanyonData[i].TE.TEgveg_veg,WBCanyonData[i].TE.TEtree_veg))
    outputFile_TE.close()

    # Generate output text file for WBIndv
    timeseriesFilename = os.path.join(Output_dir,"WaterBalanceResiduals" + case +month_name+ ".txt")
    outputFile_WB = open(timeseriesFilename, "w")
    outputFile_WB.write("#### \t Vertical City Weather Generator (VCWG)  \t #### \n")
    outputFile_WB.write("# Water balance residual terms \n")
    outputFile_WB.write(
        "# 0:time [hr] 1:WB_In_tree [mm s^-1] 2:WB_In_gveg [mm s^-1] 3:WB_In_gimp [mm s^-1] 4:WB_In_gbare [mm s^-1] 5:WB_Pond_gveg [mm s^-1]"
        " 6:WB_Soil_gimp [mm s^-1] 7:WB_Soil_gbare [mm s^-1] 8:WB_Soil_gveg [mm s^-1] \n")
    for i in range(len(time)):

        # Write NaN if an urban feature is non-existent
        ## Check if these terms are appropriately set to NaN
        if not int(FractionsGround.fimp > 0) == 1:
            WBCanyonData[i].WBIndv.WB_In_gimp = numpy.NaN
            WBCanyonData[i].WBIndv.WB_Soil_gimp = numpy.NaN
        if not int(FractionsGround.fveg > 0) == 1:
            WBCanyonData[i].WBIndv.WB_In_gveg = numpy.NaN
            WBCanyonData[i].WBIndv.WB_Pond_gveg = numpy.NaN
            WBCanyonData[i].WBIndv.WB_Soil_gveg = numpy.NaN
        if not int(FractionsGround.fbare > 0) == 1:
            WBCanyonData[i].WBIndv.WB_In_gbare = numpy.NaN
            WBCanyonData[i].WBIndv.WB_Soil_gbare = numpy.NaN
        if not int(ParTree.trees == 1) == 1:
            WBCanyonData[i].WBIndv.WB_In_tree = numpy.NaN

        outputFile_WB.write("%i %f %f %f %f %f %f %f %f \n"
                            % (i,WBCanyonData[i].WBIndv.WB_In_tree,WBCanyonData[i].WBIndv.WB_In_gveg,WBCanyonData[i].WBIndv.WB_In_gimp,
                               WBCanyonData[i].WBIndv.WB_In_gbare,WBCanyonData[i].WBIndv.WB_Pond_gveg,WBCanyonData[i].WBIndv.WB_Soil_gimp,
                               WBCanyonData[i].WBIndv.WB_Soil_gbare,WBCanyonData[i].WBIndv.WB_Soil_gveg))
    outputFile_WB.close()

    # Generate output text file for SoilPotW
    timeseriesFilename = os.path.join(Output_dir,"SoilWaterPotential" + case +month_name+ ".txt")
    outputFile_SoilPotW = open(timeseriesFilename, "w")
    outputFile_SoilPotW.write("#### \t Vertical City Weather Generator (VCWG)  \t #### \n")
    outputFile_SoilPotW.write("# Soil water potential \n")
    outputFile_SoilPotW.write(
        "# 0:time [hr] 1:SoilPotWGroundTot_H [MPa] 2:SoilPotWGroundTot_L [MPa] \n")
    for i in range(len(time)):

        outputFile_SoilPotW.write("%i %f %f \n"
                            % (i,WBCanyonData[i].SoilPotW.SoilPotWGroundTot_H,WBCanyonData[i].SoilPotW.SoilPotWGroundTot_L))
    outputFile_SoilPotW.close()

def Write_TdeepProfiles(var_string,FractionsGround,SurfType,Surface,z_depth_ground,time,case,Output_dir, month_name):
    # SurfType = 1 (GroundImp), 2 (GroundVeg), 3 (GroundBare)
    Header0 = "#0:z [m] "
    Values_format0 = " %f "
    for io in range(0, len(time)):
        Header = Header0 + str(io + 1) + ":" + var_string + "\t"
        Header0 = Header
        Values_format = Values_format0 + " %f "
        Values_format0 = Values_format
    Values_format_all = Values_format + str('\n')
    ProfilesFilename = os.path.join(Output_dir,var_string+"_profiles"+case+  month_name +".txt")
    outputFileProf = open(ProfilesFilename, "w")
    outputFileProf.write("#### \t Vertical City Weather Generator (VCWG)  \t #### \n")
    outputFileProf.write("# "+var_string+" profile in the urban area \n")
    outputFileProf.write(Header + "\n")
    for i in range(0, len(z_depth_ground)):

        Values = [Surface[j].layerTemp[i] for j in range(0, len(time))]

        # Write NaN if an urban feature is non-existent
        if (SurfType == 1) and (not int(FractionsGround.fimp > 0) == 1):
            Values = [numpy.NaN for j in range(0, len(time))]
        if (SurfType == 2) and (not int(FractionsGround.fveg > 0) == 1):
            Values = [numpy.NaN for j in range(0, len(time))]
        if (SurfType == 3) and (not int(FractionsGround.fbare > 0) == 1):
            Values = [numpy.NaN for j in range(0, len(time))]

        # Insert depth value [m] after writing the layer temperatures
        Values.insert(0, z_depth_ground[i])

        outputFileProf.write(Values_format_all
                                      % (tuple(Values)))
    outputFileProf.close()

def Write_1Dprofiles(var_string,SiteModel,object_var,var,z,time,case,Output_dir, month_name):
    Header0 = "#0:z [m] "
    Values_format0 = "%f "
    for io in range(0, len(time)):
        Header = Header0 + str(io + 1) + ":" + var_string
        Header0 = Header
        Values_format = Values_format0 + " %f "
        Values_format0 = Values_format
    Values_format_all = Values_format + str('\n')
    ProfilesFilename = os.path.join(Output_dir,var_string+"_profiles"+case+  month_name +".txt")
    outputFileProf = open(ProfilesFilename, "w")
    outputFileProf.write("#### \t Vertical City Weather Generator (VCWG)  \t #### \n")
    outputFileProf.write("# " + var_string + "profile in the urban area \n")
    outputFileProf.write(Header + "\n")
    for i in range(0, len(z)-1):
        Values = [getattr(getattr(SiteModel[j],object_var),var)[i] for j in range(0, len(time))]
        Values.insert(0, z[i])
        outputFileProf.write(Values_format_all
                                % (tuple(Values)))
    outputFileProf.close()

def Write_Ruralprofiles(var_string,RuralModelName,SiteModel,var,z,time,case,Output_dir, month_name):
    Header0 = "#0:z [m] "
    Values_format0 = "%f "
    for io in range(0, len(time)):
        Header = Header0 + str(io + 1) + ":" + var_string
        Header0 = Header
        Values_format = Values_format0 + " %f "
        Values_format0 = Values_format
    Values_format_all = Values_format + str('\n')
    ProfilesFilename = os.path.join(Output_dir,var_string+"_profiles"+case+  month_name +".txt")
    outputFileProf = open(ProfilesFilename, "w")
    outputFileProf.write("#### \t Vertical City Weather Generator (VCWG)  \t #### \n")
    outputFileProf.write("# " + var_string + "\n")
    outputFileProf.write(Header + "\n")
    for i in range(0, len(z)-1):
        Values = [getattr(SiteModel[j],var)[i] for j in range(0, len(time))]

        # Write NaN if a rural model is not used
        if (RuralModelName == 'Forcing_extFile'):
            Values = [numpy.NaN for j in range(0, len(time))]

        Values.insert(0, z[i])

        outputFileProf.write(Values_format_all
                                % (tuple(Values)))
    outputFileProf.close()

BEMvariables = {
        'sensCoolDemand': 'Sensible Cooling Demand [W m^-2]',
        'sensHeatDemand': 'Sensible Heating Demand [W m^-2]',
        'dehumDemand': 'Dehumidification Demand [W m^-2]',
        'humDemand': 'humidification Demand [W m^-2]',
        'LatentLoad': 'Latent Load Demand [W m^-2]',
        'coolConsump': 'Cooling Consumption [W m^-2]',
        'elecDomesticDemand': 'Domestic Electricity Demand [W m^-2]',
        'sensWaterHeatDemand': 'Sensible Water Heating Demand [W m^-2]',
        'ElecTotal': 'Total Electricity [W m^-2]',
        'sensWasteCoolHeatLatent': 'Sensible Waste (Cooling/Heating/Dehumidification/Humidification) [W m^-2]',
        'heatConsump': 'Heating Consumption [W m^-2]',
        'sensWaste': 'Sensible Waste [W m^-2]',

        'intHeat': 'Internal Heat [W m^-2]',
        'fluxWall': 'Wall Flux [W m^-2]',
        'fluxRoof': 'Roof Flux [W m^-2]',
        'fluxMass': 'Mass Flux [W m^-2]',
        'fluxSolar': 'Solar Flux [W m^-2]',
        'fluxWindow': 'Window Flux [W m^-2]',
        'fluxInterior': 'Interior Flux [W m^-2]',
        'fluxInfil': 'Infiltration Flux [W m^-2]',
        'fluxVent': 'Ventilation Flux [W m^-2]',

        'intHeat': 'Internal Heat [W m^-2]',
        'QWindowSolar': 'Solar Load through Windows [W m^-2]',
        'wallcoolload': 'Wall Cooling Load [W m^-2]',
        'masscoolload': 'Mass Cooling Load [W m^-2]',
        'wincoolload': 'Window Cooling Load [W m^-2]',
        'ceilingcoolload': 'Ceiling Cooling Load [W m^-2]',
        'infilcoolload': 'Infiltration Cooling Load [W m^-2]',
        'ventcoolload': 'Ventilation Cooling Load [W m^-2]',

        'wallheatload': 'Wall Heating Load [W m^-2]',
        'massheatload': 'Mass Heating Load [W m^-2]',
        'winheatload': 'Window Heating Load [W m^-2]',
        'ceilingheatload': 'Ceiling Heating Load [W m^-2]',
        'infilheatload': 'Infiltration Heating Load [W m^-2]',
        'ventheatload': 'Ventilation Heating Load [W m^-2]',

        'QWater': 'Water Load [W m^-2]',
        'QGas': 'Gas Load [W m^-2]',
        'GasTotal': 'Total Gas [W m^-2]',
        'Qhvac': 'HVAC Load [W m^-2]',

        'Nocc': 'Number of Occupants [P m^-2]',

        'ThermostatMode': 'Thermostat Mode [-]',
        'T_smart': 'Temperature Set Point [K]',
        'TempSetPointHeat': 'Heating Set Point Temperature [K]',
        'TempSetPointCool': 'Cooling Set Point Temperature [K]',
        'indoorTemp': 'Indoor Temperature [K]',
        'T_can': 'Outdoor Temperature [K]',
        'coolTempSetpointHighHigh':'Cooling HH Setpoint [K]',
        'coolTempSetpointHigh':'Cooling H Setpoint [K]',
        'coolTempSetpointLow':'Cooling L Setpoint [K]',
        'coolTempSetpointLowLow':'Cooling LL Setpoint [K]',
        'heatTempSetpointHighHigh':'Heating HH Setpoint [K]',
        'heatTempSetpointHigh':'Heating H Setpoint [K]',
        'heatTempSetpointLow':'Heating L Setpoint [K]',
        'heatTempSetpointLowLow':'Heating LL Setpoint [K]',

        'HumidistatMode': 'Humidistat Mode [-]',
        'RH_Setpoint': 'Indoor RH Set Point [%]',
        'SmartRHDehumSetPoint': 'Indoor Dehum RH Set Point [%]',
        'SmartRHHumSetPoint': 'Indoor Hum RH Set Point [%]',
        'LowRHSetPoint': 'L RH comf range [%]',
        'HighRHSetPoint': 'H RH comf range [%]',
        'LowLowRHSetPoint': 'LL RH comf range [%]',
        'HighHighRHSetPoint': 'HH RH comf range [%]',
        'indoorRH': 'Indoor Relative Humidity [%]',
        'outdoorRH_Outtemp': 'Outdoor RH (outtemp) [%]',
        'outdoorRH_Intemp': 'Outdoor RH (intemp) [%]',

        'q_Setpoint': 'Indoor Specific Hum/Dehum Set Point [kga kgv^-1]',
        'SmartDehumSetPoint': 'Indoor Specific Dehum Set Point [kga kgv^-1]',
        'SmartHumSetPoint': 'Indoor Specific Hum Set Point [kga kgv^-1]',
        'LowHumSetPoint': 'L SH comf range [kga kgv^-1]',
        'HighHumSetPoint': 'H SH comf range [kga kgv^-1]',
        'LowLowHumSetPoint': 'LL SH comf range [kga kgv^-1]',
        'HighHighHumSetPoint': 'HH SH comf range [kga kgv^-1]',
        'indoorHum': 'Indoor Humidity [kgv kga^-1]',
        'outdoorHum': 'Outdoor Humidity [kgv kga^-1]',

        'WallTemp': 'Temperature of the wall [K]',

        'PMV': 'PMV Thermal Comfort [-]',
        'PPD': 'PPD Thermal Comfort [%]',

        'wTemp': 'Temperature w Factor  [-]',
        'wHum': 'Humidity w Factor  [-]'
    }
def Write_BEM(BEMData, time, case, Output_dir, month_name):
    # Initialize all the variables in a dictionary


    data = {var: numpy.zeros(len(BEMData)) for var in BEMvariables}

    # Process each BEMData
    for i in range(len(BEMData)):
        BEM = BEMData[i]
        for j in range(len(BEM)):
            for var in BEMvariables:
                building_value = getattr(BEM[j].building, var)
                if numpy.isnan(building_value):
                    data[var][i] = 'NaN'  # Set the value to 'NaN' as a string
                else:
                    data[var][i] += BEM[j].frac * building_value

    # Generate output text file for BEM
    timeseriesFilename = os.path.join(Output_dir, "BEM" + case + month_name + ".txt")
    with open(timeseriesFilename, "w") as outputFile_BEM:
        outputFile_BEM.write("#### \t Vertical City Weather Generator (VCWG)  \t #### \n")
        outputFile_BEM.write("# Building energy model terms \n")
        outputFile_BEM.write(
            "# time [hr] " + " ".join([f"{i}:{desc}" for i, desc in enumerate(BEMvariables.values())]) + " \n")

        for i in range(len(time)):
            outputFile_BEM.write("%i " % i + " ".join(
                [f"{data[var][i]:.6f}" if isinstance(data[var][i], (int, float)) else 'NaN' for var in
                 BEMvariables]) + "\n")
