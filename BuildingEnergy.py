# =================================================
# Developed by: Mojtaba Safdari and Amir A. Aliabadi
# Atmospheric Innovations Research (AIR) Laboratory, University of Guelph, Guelph, Canada
# Last update: Nov 2024
# =================================================

from psychrometrics import psychrometrics, moist_air_density
import FuzzySetpoint
import logging
import numpy
import copy
import math
import Read_Input
from Simparam import SimParam
from PMV import calculate_pmv
from FuzzySetpoint import FuzzyControlSystem

class Building(object):

    TEMPERATURE_COEFFICIENT_CONFLICT_MSG = "FATAL ERROR!"

    def __init__(self,floorHeight,intHeatNight,intHeatDay,intHeatFRad,\
            intHeatFLat,infil,vent,glazingRatio,uValue,shgc,\
            condType,cop,\
             coolCap,heatEff,initialTemp,\
             initialTempSetPoint, initialSmartRHSetPoint):

        self.floorHeight =float(floorHeight)                   # floor height [m]
        self.intHeat = intHeatNight                            # timestep internal sensible heat gain per unit floor area [W m^-2]
        self.intHeatNight = intHeatNight                       # nighttime internal heat gain per unit floor area [W m^-2]
        self.intHeatDay = intHeatDay                           # daytime internal heat gain per unit floor area [W m^-2]
        self.intHeatFRad = intHeatFRad                         # internal gain radiant fraction
        self.intHeatFLat = intHeatFLat                         # internal gain latent fraction
        self.infil = infil                                     # infiltration Air Change per Hour (ACH) [hr^-1]
        self.vent = vent                                       # ventilation rate per unit floor area [m^3 s^-1 m^-2]
        self.glazingRatio = glazingRatio                       # glazing ratio [-]
        self.uValue = uValue                                   # window U-value [W m^-2 K^-1] including film coefficient
        self.shgc = shgc                                       # window Solar Heat Gain Coefficient (SHGC), fraction of radiation that is admitted through a window [-]
        self.condType = condType                               # cooling condensation system type: AIR, WATER
        self.cop = cop                                         # COP of cooling system (nominal)
        self.heatEff = heatEff                                 # heating system capacity [-]
        self.mSys = coolCap/1004./(298.15-14-273.15)           # HVAC supply mass flowrate [kg s^-1 m^-2]
        self.indoorTemp = initialTemp                          # Indoor Air Temperature [K]
        self.indoorHum = 0.006                                 # Indoor specific humidity [kgv kga^-1] fixed at 40% RH at 20C
        self.copAdj = cop                                      # adjusted COP per temperature
        self.canyon_fraction = 1.0                             # Default canyon fraction [-]
        self.sensWaste = 0                                     # Total Sensible Waste [W m^-2]
        self.TempSetPointHeat= initialTempSetPoint             # initial value for setpoint when Smart control disabled-under heating mode [K]
        self.TempSetPointCool= initialTempSetPoint             # initial value for setpoint when Smart control disabled-under cooling mode [K]
        self.T_smart = initialTempSetPoint                     # Initial temperature setpoint when smart controler is ON [K]
        self.SmartRHSetPoint = initialSmartRHSetPoint          # initial value for setpoint when Smart control enabled-under both cooling and heating mode [%]
        self.Type = "null"                                     # DOE reference building type
        self.Era = "null"                                      # pre80, pst80, new
        self.Zone = "null"                                     # Climate zone number

        # Logger will be disabled by default unless explicitly called in tests
        self.logger = logging.getLogger(__name__)

    def __repr__(self):
        return "BuildingType: {a}, Era: {b}, Zone: {c}".format(
            a=self.Type,
            b=self.Era,
            c=self.Zone
            )

    def is_near_zero(self,val,tol=1e-14):
        return abs(float(val)) < tol

    def BEMCalc(self,canTemp,canHum,BEM,MeteoData,ParCalculation,simTime,Geometry_m,FractionsRoof,SWR,SmartBuildingParam,TOU):
        
        self.coolTempSetpointDay = SmartBuildingParam.coolTempSetpointDay      # [K]
        self.coolTempSetpointNight = SmartBuildingParam.coolTempSetpointNight  # [K]
        self.heatTempSetpointDay = SmartBuildingParam.heatTempSetpointDay      # [K]
        self.heatTempSetpointNight = SmartBuildingParam.heatTempSetpointNight  # [K]
        self.dehumRHSetpointDay = SmartBuildingParam.dehumRHSetpointDay        # [%]
        self.dehumRHSetpointNight = SmartBuildingParam.dehumRHSetpointNight    # [%]
        self.humRHSetpointDay = SmartBuildingParam.humRHSetpointDay            # [%]
        self.humRHSetpointNight = SmartBuildingParam.humRHSetpointNight        # [%]
        self.T_can = canTemp                                                   # Canyon temperature [K]
        
        self.TOU_Low_Summer = TOU.TOU_Low_Summer                               # [hr] Low price hours for summer
        self.TOU_Medium_Summer = TOU.TOU_Medium_Summer                         # [hr] Medium price hours for summer
        self.TOU_High_Summer = TOU.TOU_High_Summer                             # [hr] High price hours for summer
        self.TOU_Low_Winter = TOU.TOU_Low_Winter                               # [hr] Low price hours for winter
        self.TOU_Medium_Winter = TOU.TOU_Medium_Winter                         # [hr] Medium price hours for winter
        self.TOU_High_Winter = TOU.TOU_High_Winter                             # [hr] High price hours for winter
        
        fuzzy_system = FuzzyControlSystem(self.TOU_Low_Summer, self.TOU_Medium_Summer, self.TOU_High_Summer,
                                          self.TOU_Low_Winter, self.TOU_Medium_Winter, self.TOU_High_Winter)

        # calculating the outdoor relative hum based on outdoor temp
        _Tdb, _w, _phi, _h, _Tdp, _v = psychrometrics(self.T_can, canHum, MeteoData.Pre)
        self.outdoorRH_Outtemp = _phi                                           # Indoor relative humidity[%]

        # calculating the Outdoor relative hum based on indoor temp
        _Tdb, _w, _phi, _h, _Tdp, _v = psychrometrics(self.indoorTemp, canHum, MeteoData.Pre)
        self.outdoorRH_Intemp = _phi                                            # Indoor relative humidity[%]

        self.logger.debug("Logging at {} {}".format(__name__, self.__repr__()))

        # Building Energy Model
        self.ElecTotal = 0.0                                       # total electricity consumption [W m^-2]
        self.nFloor = max(Geometry_m.Height_canyon/float(self.floorHeight),1)   # At least one floor
        self.sensCoolDemand = 0.0                                  # building sensible cooling demand per unit building footprint area [W m^-2]
        self.sensHeatDemand = 0.0                                  # building sensible heating demand per unit building footprint area [W m^-2]
        self.sensWaterHeatDemand = 0.0                             # building sensible water heating demand per unit building footprint area [W m^-2]
        self.coolConsump  = 0.0                                    # cooling energy consumption per unit building footprint area OR per unit floor area [W m^-2]
        self.heatConsump  = 0.0                                    # heating energy consumption per unit floor area [W m^-2]
        self.sensWaste = 0.0                                       # Total Sensible waste heat per unit building footprint area including cool, heat, dehum, water, and gas [W m^-2]
        self.sensWasteCoolHeatLatent = 0.0                         # Sensible waste heat per unit building footprint area only including cool, heat, and dehum [W m-2]
        self.dehumDemand  = 0.0                                    # Latent Energy demand for dehumidification of air per unit building footprint area [W m^-2]
        self.humDemand = 0.0                                       # Latent heat demand for humidification of air per unit building footprint area [W m^-2]
        self.Qhvac = 0.0                                           # Total heat removed (sensible + latent) [W m^-2]
        self.elecDomesticDemand = 0.0                              # Electricity demand for appliances and lighting (not for energy) per building footprint area [W m^-2]
        self.ThermostatMode = SmartBuildingParam.SmartThermostat   # Thermostat Mode:  1: smart 0: no smart
        self.HumidistatMode = SmartBuildingParam.SmartHumidistat   # Humidistat Mode:  1: smart 0: no smart

        # Moist air density given dry bulb temperature, humidity ratio, and pressure [kgv m^-3]
        dens =  moist_air_density(MeteoData.Pre,self.indoorTemp,self.indoorHum)
        # evaporation efficiency in the condenser for evaporative cooling devices
        evapEff = 1.
        # total ventilation volumetric flow rate per building footprint area [m^3 s^-1 m^-2]
        volVent = self.vent * self.nFloor
        # total infiltration volumetric flow rate per building footprint area [m^3 s^-1 m^-2]
        volInfil = self.infil * Geometry_m.Height_canyon / 3600.
        # Interior wall temperature [K]
        T_wall = (BEM.wallSun.Tint+BEM.wallShade.Tint)/2
        self.WallTemp =  T_wall
        # Solar water heating per building footprint area per hour [kg s^-1 m^-2] (Change of units [hr^-1] to [s^-1]
        massFlowRateSWH = BEM.SWH * self.nFloor/3600.
        # Interior roof temperature [K]
        T_ceil = FractionsRoof.fimp*BEM.roofImp.Tint+FractionsRoof.fveg*BEM.roofVeg.Tint
        T_mass = BEM.mass.Text                                 # Outer layer [K]
        T_indoor = self.indoorTemp                             # Indoor temp (initial) [K]

        # Normalize areas to building foot print [m^2 m^-2]
        # Facade (exterior) area per unit building footprint area [m^2 m^-2]
        facArea = 2*Geometry_m.Height_canyon/numpy.sqrt(Geometry_m.Width_roof*Geometry_m.Width_roof)
        wallArea = facArea*(1.-self.glazingRatio)              # Wall area per unit building footprint area [m^2 m^-2]
        winArea = facArea*self.glazingRatio                    # Window area per unit building footprint area [m^2 m^-2]
        massArea = 2*self.nFloor-1                             # ceiling and floor (top & bottom) per unit building footprint area [m^2 m^-2]
        ceilingArea = 1                                        # ceiling area per unit building footprint area [m^2 m^-2]; must be equal to 1

        # Set temperature set points according to night/day set points in building schedule & simTime; need the time in [hr]
        isEqualNightStart = self.is_near_zero((simTime.secDay/3600.) - ParCalculation.nightStart)

        # Daytype
        if self.is_near_zero(simTime.julian % 7):
            self.dayType = 3                                   # Sunday [-]
        elif self.is_near_zero(simTime.julian % 7 - 6.):
            self.dayType = 2                                   # Saturday [-]
        else:
            self.dayType = 1                                   # Weekday [-]

        # Day or night (Night)
        if simTime.secDay/3600. < ParCalculation.nightEnd or (simTime.secDay/3600. > ParCalculation.nightStart or isEqualNightStart):
            self.logger.debug("{} Night set points @{}".format(__name__,simTime.secDay/3600.))

            # Set point temperatures [K]
            # If ThermostatMode = 0 temperature sepoint controller is off and else it is on
            # When the contoller is off the setpoints are equal to the fixed day/night heating and cooling setpoints
            if self.ThermostatMode == 0:
                self.TempSetPointHeat = self.heatTempSetpointNight
                T_heat = self.TempSetPointHeat
                self.TempSetPointCool = self.coolTempSetpointNight
                T_cool = self.TempSetPointCool

                # Writing NaN for smart parameters when the setpoints are not controlled
                self.coolTempSetpointHighHigh = numpy.NaN       # [ K ]
                self.coolTempSetpointHigh = numpy.NaN           # [ K ]
                self.coolTempSetpointLow = numpy.NaN            # [ K ]
                self.coolTempSetpointLowLow = numpy.NaN         # [ K ]

                self.heatTempSetpointHighHigh = numpy.NaN       # [ K ]
                self.heatTempSetpointHigh = numpy.NaN           # [ K ]
                self.heatTempSetpointLow = numpy.NaN            # [ K ]
                self.heatTempSetpointLowLow = numpy.NaN         # [ K ]

                self.wTemp = numpy.NaN  # [-]
            
            # When the humidistat is on the controller adjusts the setpoint based on inputs and fuzzy logic controller
            # Here we calculate and adjust both heating and cooling setpoints [K] but only one of them is being used finally based
            # on the building loads
            # Here w represents the variations of the controller output for setpoint adjustment [-]
            else:
                self.TempSetPointHeat, self.wTemp = fuzzy_system.TempSetpointHeatFun(self.Nocc, self.TempSetPointHeat, simTime, SmartBuildingParam, MeteoData, canTemp, self.dayType)
                T_heat = self.TempSetPointHeat
                self.TempSetPointCool, self.wTemp = fuzzy_system.TempSetpointCoolFun(self.Nocc, self.TempSetPointCool, simTime, SmartBuildingParam, MeteoData, canTemp, self.dayType)
                T_cool = self.TempSetPointCool

            # RH night [%]
            # If HumidistatMode = 0 humidity sepoint controller is off and else it is on
            # When the controller is off the setpoints are equal to the fixed day/night setpoints [%]
            if self.HumidistatMode == 0:
                RH_dehum = self.dehumRHSetpointNight           # [%]
                RH_hum= self.humRHSetpointDay                  # [%]

                # Set point specific humidities [kgv kga^-1]
                # Tetens equation: Pg = 610.78 exp(17.27 T / (T+237.3)) with Pg [Pa] ant T [C]
                # Saturation pressure [Pa]
                Pg_cool = 610.78 * math.exp(17.27 * (T_cool - 273.15) / ((T_cool - 273.15) + 237.3))
                Pg_heat = 610.78 * math.exp(17.27 * (T_heat - 273.15) / ((T_heat - 273.15) + 237.3))
                # Specific humidity set points [kgv kga^-1]
                q_dehum = 0.622 * (RH_dehum/ 100) * Pg_cool / (MeteoData.Pre - (RH_dehum / 100) * Pg_cool)
                q_hum= 0.622 * (RH_hum / 100) * Pg_heat / (MeteoData.Pre - (RH_hum / 100) * Pg_heat)

                # Writing NaN for smart parameters when the setpoints are not controlled
                self.SmartHumSetPoint = numpy.NaN               # [kgv kga^-1]
                self.SmartDehumSetPoint = numpy.NaN             # [kgv kga^-1]

                self.HighHumSetPoint = numpy.NaN                # [kgv kga^-1]
                self.HighHighHumSetPoint = numpy.NaN            # [kgv kga^-1]
                self.LowHumSetPoint = numpy.NaN                 # [kgv kga^-1]
                self.LowLowHumSetPoint = numpy.NaN              # [kgv kga^-1]

                self.SmartRHSetPoint = numpy.NaN                # [%]
                self.SmartRHHumSetPoint = numpy.NaN             # [%]
                self.SmartRHDehumSetPoint = numpy.NaN           # [%]

                self.LowRHSetPoint = numpy.NaN                  # [%]
                self.LowLowRHSetPoint = numpy.NaN               # [%]
                self.HighRHSetPoint = numpy.NaN                 # [%]
                self.HighHighRHSetPoint = numpy.NaN             # [%]

                self.wHum = numpy.NaN                           # [-]

            else:
                # Humidity Control is on and the new thresholds and variable setpoints are calculated
                self.SmartHumSetPoint, self.LowHumSetPoint, self.LowLowHumSetPoint, self.HighHumSetPoint, self.HighHighHumSetPoint,\
                self.LowRHSetPoint, self.LowLowRHSetPoint, self.HighRHSetPoint, self.HighHighRHSetPoint, self.wHum = \
                    fuzzy_system.HumSetpointFun( self.Nocc, self.SmartRHSetPoint, SmartBuildingParam, canHum, T_indoor, MeteoData, simTime, self.dayType)
                q_hum = self.SmartHumSetPoint                   # [kgv kga^-1]
                self.SmartDehumSetPoint, self.wHum = \
                    fuzzy_system.DehumSetpointFun(self.Nocc, self.SmartRHSetPoint, SmartBuildingParam, canHum, T_indoor, MeteoData, simTime, self.dayType)
                q_dehum =  self.SmartDehumSetPoint              # [kgv kga^-1]

                # calculating the smart setpoint relative hum
                _Tdb, _w, _phi, _h, _Tdp, _v = psychrometrics(T_indoor, self.SmartHumSetPoint, MeteoData.Pre)
                # Indoor relative humidity [%]
                self.SmartRHHumSetPoint = _phi
                RH_hum = self.SmartRHHumSetPoint

                # calculating the smart setpoint relative dehum
                _Tdb, _w, _phi, _h, _Tdp, _v = psychrometrics(T_indoor, self.SmartDehumSetPoint, MeteoData.Pre)
                # Indoor relative humidity [%]
                self.SmartRHDehumSetPoint = _phi
                RH_dehum = self.SmartRHDehumSetPoint

            self.outdoorHum = canHum                              # [kgv kga^-1]

            # Internal heat per unit building footprint area [W m^-2]
            self.intHeat = self.intHeatNight * self.nFloor
        #Day
        else:
            self.logger.debug("{} Day set points @{}".format(__name__,simTime.secDay/3600.))

            # If ThermostatMode = 0 temperature sepoint controller is off and else it is on
            # When the contoller is off the setpoints are equal to the fixed day heating and cooling setpoints
            if self.ThermostatMode == 0:
                self.TempSetPointHeat = self.heatTempSetpointDay
                T_heat = self.TempSetPointHeat
                self.TempSetPointCool = self.coolTempSetpointDay
                T_cool = self.TempSetPointCool

                # Writing NaN for smart parameters when the setpoints are not controlled
                self.T_smart = numpy.NaN                        # [ K ]
                self.coolTempSetpointHighHigh = numpy.NaN       # [ K ]
                self.coolTempSetpointHigh = numpy.NaN           # [ K ]
                self.coolTempSetpointLow = numpy.NaN            # [ K ]
                self.coolTempSetpointLowLow = numpy.NaN         # [ K ]

                self.heatTempSetpointHighHigh = numpy.NaN       # [ K ]
                self.heatTempSetpointHigh = numpy.NaN           # [ K ]
                self.heatTempSetpointLow = numpy.NaN            # [ K ]
                self.heatTempSetpointLowLow = numpy.NaN         # [ K ]

                self.wTemp = numpy.NaN  # [-]

            #Smart
            else:
                self.TempSetPointHeat , self.wTemp = fuzzy_system.TempSetpointHeatFun(self.Nocc, self.TempSetPointHeat, simTime,SmartBuildingParam, MeteoData, canTemp, self.dayType)
                T_heat = self.TempSetPointHeat
                self.TempSetPointCool , self.wTemp = fuzzy_system.TempSetpointCoolFun(self.Nocc, self.TempSetPointCool, simTime, SmartBuildingParam, MeteoData, canTemp, self.dayType)
                T_cool = self.TempSetPointCool

            #Relative humidity setpoint during the day [%]
            if self.HumidistatMode == 0:
                RH_dehum = self.dehumRHSetpointDay
                RH_hum = self.humRHSetpointDay

                # Set point specific humidities [kgv kga^-1]
                # Tetens equation: Pg = 610.78 exp(17.27 T / (T+237.3)) with Pg [Pa] ant T [C]
                # Saturation pressure [Pa]
                Pg_cool = 610.78 * math.exp(17.27 * (T_cool - 273.15) / ((T_cool - 273.15) + 237.3))
                Pg_heat = 610.78 * math.exp(17.27 * (T_heat - 273.15) / ((T_heat - 273.15) + 237.3))
                # Specific humidity set points [kgv kga^-1]
                q_dehum = 0.622 * (RH_dehum / 100) * Pg_cool / (MeteoData.Pre - (RH_dehum/ 100) * Pg_cool)
                q_hum = 0.622 * (RH_hum/ 100) * Pg_heat / (MeteoData.Pre - (RH_hum / 100) * Pg_heat)
                
                # Writing NaN for smart parameters when the setpoints are not controlled
                self.SmartHumSetPoint = numpy.NaN               # [kgv kga^-1]
                self.SmartDehumSetPoint = numpy.NaN             # [kgv kga^-1]

                self.LowHumSetPoint = numpy.NaN                 # [kgv kga^-1]
                self.LowLowHumSetPoint = numpy.NaN              # [kgv kga^-1]
                self.HighHumSetPoint = numpy.NaN                # [kgv kga^-1]
                self.HighHighHumSetPoint = numpy.NaN            # [kgv kga^-1]

                self.SmartRHSetPoint = numpy.NaN                # [%]
                self.SmartRHHumSetPoint = numpy.NaN             # [%]
                self.SmartRHDehumSetPoint = numpy.NaN           # [%]

                self.LowRHSetPoint = numpy.NaN                  # [%]
                self.LowLowRHSetPoint = numpy.NaN               # [%]
                self.HighRHSetPoint = numpy.NaN                 # [%]
                self.HighHighRHSetPoint = numpy.NaN             # [%]

                self.wHum = numpy.NaN                           # [-]

            # Night HumidistatMode == 1
            else:
                self.SmartHumSetPoint, self.LowHumSetPoint, self.LowLowHumSetPoint, self.HighHumSetPoint, self.HighHighHumSetPoint,\
                self.LowRHSetPoint, self.LowLowRHSetPoint, self.HighRHSetPoint, self.HighHighRHSetPoint, self.wHum = \
                    fuzzy_system.HumSetpointFun(self.Nocc, self.SmartRHSetPoint, SmartBuildingParam, canHum, T_indoor, MeteoData, simTime, self.dayType)   # [kgv kga^-1]
                q_hum = self.SmartHumSetPoint                   # [kgv kga^-1]

                self.SmartDehumSetPoint , self.wHum= \
                    fuzzy_system.DehumSetpointFun(self.Nocc, self.SmartRHSetPoint, SmartBuildingParam, canHum, T_indoor, MeteoData, simTime, self.dayType)
                q_dehum = self.SmartDehumSetPoint               # [kgv kga^-1]

                # calculating the smart setpoint relative hum
                _Tdb, _w, _phi, _h, _Tdp, _v = psychrometrics(T_indoor, self.SmartHumSetPoint, MeteoData.Pre)
                # Indoor relative humidity [%]
                self.SmartRHHumSetPoint = _phi
                RH_hum = self.SmartRHHumSetPoint

                # calculating the smart setpoint relative dehum
                _Tdb, _w, _phi, _h, _Tdp, _v = psychrometrics(T_indoor, self.SmartDehumSetPoint, MeteoData.Pre)
                # Indoor relative humidity [%]
                self.SmartRHDehumSetPoint = _phi
                RH_dehum = self.SmartRHDehumSetPoint
                
            # Internal heat per unit building footprint area [W m^-2]
            self.intHeat = self.intHeatDay*self.nFloor

        # Initialize building envelop loads to NaN
        self.wallheatload = numpy.NaN       # [W m^-2]
        self.massheatload = numpy.NaN       # [W m^-2]
        self.winheatload = numpy.NaN        # [W m^-2]
        self.ceilingheatload = numpy.NaN    # [W m^-2]
        self.infilheatload = numpy.NaN      # [W m^-2]
        self.ventheatload = numpy.NaN       # [W m^-2]

        self.wallcoolload = numpy.NaN       # [W m^-2]
        self.masscoolload = numpy.NaN       # [W m^-2]
        self.wincoolload = numpy.NaN        # [W m^-2]
        self.ceilingcoolload = numpy.NaN    # [W m^-2]
        self.infilcoolload = numpy.NaN      # [W m^-2]
        self.ventcoolload = numpy.NaN       # [W m^-2]

        # Indoor convection heat transfer coefficients
        # wall convective heat transfer coefficient [W m^-2 K^-1]
        zac_in_wall = 3.076
        # other surfaces convective heat transfer coefficient [W m^-2 K^-1]
        zac_in_mass = 0.948

        # Assume the same convective heat transfer coefficient regardless of temperature difference
        zac_in_ceil = 0.948

        # -------------------------------------------------------------
        # Heat fluxes [W m^-2]
        # -------------------------------------------------------------
        # Solar Heat Gain on windows per building footprint area [W m^-2]:
        # = radiation intensity [W m^-2] * Solar Heat Gain Coefficient (SHGC) * window area per unit building foot print area [m^2 m^-2]
        SWRinWall = (SWR.SWRin.SWRinWallSun + SWR.SWRin.SWRinWallShade)/2
        self.QWindowSolar = (SWRinWall * self.shgc * winArea)

        # Latent heat load per unit building footprint area [W m^-2]
        QLintload = self.intHeat * self.intHeatFLat

        self.sensCoolDemand = max(
            wallArea*zac_in_wall*(T_wall-T_cool) +                        # wall load per unit building footprint area [W m^-2]
            massArea*zac_in_mass*(T_mass-T_cool) +                        # other surfaces load per unit building footprint area [W m^-2]
            winArea*self.uValue*(self.T_can-T_cool) +                     # window load due to temperature difference per unit building footprint area [W m^-2]
            ceilingArea*zac_in_ceil*(T_ceil-T_cool) +                     # ceiling load per unit building footprint area [W m^-2]
            self.intHeat +                                                # internal load per unit building footprint area [W m^-2]
            volInfil*dens*ParCalculation.cp_atm*(self.T_can-T_cool) +     # infiltration load per unit building footprint area [W m^-2]
            volVent*dens*ParCalculation.cp_atm*(self.T_can-T_cool) +      # ventilation load per unit building footprint area [W m^-2]
            self.QWindowSolar,                                            # solar load through window per unit building footprint area
            0.)

        self.sensHeatDemand = max(
            -(wallArea*zac_in_wall*(T_wall-T_heat) +                      # wall load per unit building footprint area [W m^-2]
            massArea*zac_in_mass*(T_mass-T_heat) +                        # other surfaces load per unit building footprint area [W m^-2]
            winArea*self.uValue*(self.T_can-T_heat) +                     # window load due to temperature difference per unit building footprint area [W m^-2]
            zac_in_ceil*(T_ceil-T_heat) +                                 # ceiling load per unit building footprint area [W m^-2]
            self.intHeat +                                                # internal load per unit building footprint area [W m^-2]
            volInfil*dens*ParCalculation.cp_atm*(self.T_can-T_heat) +     # infiltration load per unit building footprint area [W m^-2]
            volVent*dens*ParCalculation.cp_atm*(self.T_can-T_heat) +      # ventilation load per unit building footprint area [W m^-2]
            self.QWindowSolar),                                           # solar load through window per unit building footprint area [W m^-2]
            0.)

        self.dehumDemand = max(
            volInfil * dens * ParCalculation.Lv * (canHum - q_dehum) +    # Moisture load from infiltration
            volVent * dens *ParCalculation.Lv * (canHum - q_dehum) +      # Moisture load from ventilation
            QLintload,                                                    # Internal sources of moisture (people, equipment)
            0.
        )

        self.humDemand = max(
            -(volInfil * dens * ParCalculation.Lv * (canHum - q_hum) +    # Moisture load from infiltration
              volVent * dens * ParCalculation.Lv *(canHum - q_hum) +      # Moisture load from ventilation
              QLintload),                                                 # Internal sources of moisture
            0.
        )
        
        # System under dehumidification
        if self.dehumDemand > 0:                                          # [W m^-2]
            self.q_Setpoint = q_dehum                                     # [kgv kga^-1]
            self.RH_Setpoint = RH_dehum                                   # [%]
            self.humDemand = 0                                            # [W m^-2]
        # System under humidification
        elif self.humDemand > 0:                                          # [W m^-2]
            self.q_Setpoint = q_hum                                       # [kgv kga^-1]
            self.RH_Setpoint = RH_hum                                     # [%]
            self.dehumDemand = 0                                          # [W m^-2]
        # System in neutral mode
        else:
            self.q_Setpoint = numpy.NaN                                   # [kgv kga^-1]
            self.RH_Setpoint = numpy.NaN                                  # [%]
        # dehumDemand>0 and humDemand<0
        self.LatentLoad = self.dehumDemand - self.humDemand               # [W m^-2]
        
        # -------------------------------------------------------------
        # HVAC system (cooling demand = [W m^-2] bld footprint)
        # -------------------------------------------------------------
        # If the canyon air temperature is greater than 288 K building energy system is under cooling mode
        if self.sensCoolDemand > 0. and self.T_can > 288.:                              #[W m^-2]

            # QL: Latent heat per unit floor area [W m^-2] from infiltration & ventilation
            # volInfil and volVent: volumetric rate of infiltration or ventilation per unit area [m^3 s^-1 m^-2]
            # ParCalculation.Lv: latent heat of evaporation [J kgv^-1]
            # dens: density [kga m^-3]
            # canHum: canyon specific humidity [kgv kga^-1]
            # q_cool, q_heat, or q_smart: indoor specific humidity set point [kgv kga^-1]

            self.T_smart = T_cool                                                       # [ K ]

            # Wall cooling load per unit building footprint area [W m^-2]
            self.wallcoolload = wallArea * zac_in_wall * (T_wall - T_cool)
            # Other surfaces (mass) cooling load per unit building footprint area [W m^-2]
            self.masscoolload = massArea * zac_in_mass * (T_mass - T_cool)
            # Window cooling load due to temperature difference per unit building footprint area [W m^-2]
            self.wincoolload = winArea * self.uValue * (self.T_can - T_cool)
            # Ceiling cooling load per unit building footprint area [W m^-2]
            self.ceilingcoolload = ceilingArea * zac_in_ceil * (T_ceil - T_cool)
            # Infiltration cooling load per unit building footprint area [W m^-2]
            self.infilcoolload = volInfil * dens * ParCalculation.cp_atm * (self.T_can - T_cool)
            # Ventilation cooling load per unit building footprint area [W m^-2]
            self.ventcoolload = volVent * dens * ParCalculation.cp_atm * (self.T_can - T_cool)

            # Calculate input work required by the refrigeration cycle per unit building footprint area [W m^-2]
            # COP = QL/Win or Win = QL/COP
            self.coolConsump = (max(self.sensCoolDemand+self.dehumDemand,0.0))/self.copAdj

            # Calculate waste heat from HVAC system per unit building footprint area [W m^-2]
            # Using 1st law of thermodynamics QH = Win + QL
            if (self.condType == 'AIR'):
                self.sensWasteCoolHeatLatent = max(self.sensCoolDemand+self.dehumDemand,0)+self.coolConsump
                self.latWaste = 0.0
            # We have not tested this option; it must be investigated further
            elif (self.condType == 'WAT'):
                self.sensWasteCoolHeatLatent = max(self.sensCoolDemand+self.dehumDemand,0)+self.coolConsump*(1.-evapEff)
                self.latWaste = max(self.sensCoolDemand+self.dehumDemand,0)+self.coolConsump*evapEff

            self.sensHeatDemand = 0                                                      # [W m^-2]
            
            # Reading constant setpoint thresholds for saving in output
            if self.ThermostatMode == 1:
                self.coolTempSetpointHighHigh = SmartBuildingParam.coolTempSetpointHighHigh  # [ K ]
                self.coolTempSetpointHigh = SmartBuildingParam.coolTempSetpointHigh          # [ K ]
                self.coolTempSetpointLow = SmartBuildingParam.coolTempSetpointLow            # [ K ]
                self.coolTempSetpointLowLow = SmartBuildingParam.coolTempSetpointLowLow      # [ K ]
            
            # NaN heating calculations under cooling for in saving outputs
            self.heatTempSetpointHighHigh = numpy.NaN                                    # [ K ]
            self.heatTempSetpointHigh = numpy.NaN                                        # [ K ]
            self.heatTempSetpointLow = numpy.NaN                                         # [ K ]
            self.heatTempSetpointLowLow = numpy.NaN                                      # [ K ]
            self.wallheatload = numpy.NaN                                                # [W m^-2]
            self.massheatload = numpy.NaN                                                # [W m^-2]
            self.winheatload = numpy.NaN                                                 # [W m^-2]
            self.ceilingheatload = numpy.NaN                                             # [W m^-2]
            self.infilheatload = numpy.NaN                                               # [W m^-2]
            self.ventheatload = numpy.NaN                                                # [W m^-2]

        # -------------------------------------------------------------
        # HVAC system (heating demand = [W m^-2] bld footprint)
        # -------------------------------------------------------------
        # If the canyon air temperature is less than 288 K building energy system is under heating mode
        # Under heating mode, there is no dehumidification
        elif self.sensHeatDemand > 0. and self.T_can < 288.:

            self.T_smart = T_heat                                                        # [ K ]

            # Wall heating load per unit building footprint area [W m^-2]
            self.wallheatload = wallArea * zac_in_wall * (T_wall - T_heat)
            # Other surfaces (mass) heating load per unit building footprint area [W m^-2]
            self.massheatload = massArea * zac_in_mass * (T_mass - T_heat)
            # Window heating load due to temperature difference per unit building footprint area [W m^-2]
            self.winheatload = winArea * self.uValue * (self.T_can - T_heat)
            # Ceiling heating load per unit building footprint area [W m^-2]
            self.ceilingheatload = ceilingArea * zac_in_ceil * (T_ceil - T_heat)
            # Infiltration heating load per unit building footprint area [W m^-2]
            self.infilheatload = volInfil * dens * ParCalculation.cp_atm * (self.T_can - T_heat)
            # Ventilation heating load per unit building footprint area [W m^-2]
            self.ventheatload = volVent * dens * ParCalculation.cp_atm * (self.T_can - T_heat)

            # Calculate the energy consumption of the heating system per unit building footprint area [W m^-2] from heating demand divided by efficiency
            self.heatConsump  = (self.sensHeatDemand + self.humDemand) / self.heatEff
            # Calculate waste heat from HVAC system per unit building footprint area [W m^-2]
            # Using 1st law of thermodynamics QL = Win - QH
            self.sensWasteCoolHeatLatent = self.heatConsump - (self.sensHeatDemand + self.humDemand)
            self.sensCoolDemand = 0.0                                                       # [W m^-2]

            # Reading constant setpoint thresholds for saving in output
            if self.ThermostatMode == 1:
                self.heatTempSetpointHighHigh = SmartBuildingParam.heatTempSetpointHighHigh     # [ K ]
                self.heatTempSetpointHigh = SmartBuildingParam.heatTempSetpointHigh             # [ K ]
                self.heatTempSetpointLow = SmartBuildingParam.heatTempSetpointLow               # [ K ]
                self.heatTempSetpointLowLow = SmartBuildingParam.heatTempSetpointLowLow         # [ K ]
            
            # NaN cooling calculations under heating for in saving outputs
            self.coolTempSetpointHighHigh = numpy.NaN                                       # [ K ]
            self.coolTempSetpointHigh = numpy.NaN                                           # [ K ]
            self.coolTempSetpointLow = numpy.NaN                                            # [ K ]
            self.coolTempSetpointLowLow = numpy.NaN                                         # [ K ]
            self.wallcoolload = numpy.NaN                                                   # [W m^-2]
            self.masscoolload = numpy.NaN                                                   # [W m^-2]
            self.wincoolload = numpy.NaN                                                    # [W m^-2]
            self.ceilingcoolload = numpy.NaN                                                # [W m^-2]
            self.infilcoolload = numpy.NaN                                                  # [W m^-2]
            self.ventcoolload = numpy.NaN                                                   # [W m^-2]

        else:
            
            # Writing NaN for smart parameters when the setpoints are under no control
            self.SmartHumSetPoint = numpy.NaN           # [kgv kga^-1]
            self.SmartDehumSetPoint = numpy.NaN         # [kgv kga^-1]

            self.LowHumSetPoint =  numpy.NaN            # [kgv kga^-1]
            self.LowLowHumSetPoint =  numpy.NaN         # [kgv kga^-1]
            self.HighHumSetPoint =  numpy.NaN           # [kgv kga^-1]
            self.HighHighHumSetPoint =  numpy.NaN       # [kgv kga^-1]

            self.SmartRHSetPoint = numpy.NaN            # [%]
            self.SmartRHHumSetPoint = numpy.NaN         # [%]
            self.SmartRHDehumSetPoint = numpy.NaN       # [%]

            self.LowRHSetPoint = numpy.NaN              # [%]
            self.LowLowRHSetPoint = numpy.NaN           # [%]
            self.HighRHSetPoint = numpy.NaN             # [%]
            self.HighHighRHSetPoint = numpy.NaN         # [%]
            
            self.T_smart = numpy.NaN                    # [ K ]
            self.coolTempSetpointHighHigh = numpy.NaN   # [ K ]
            self.coolTempSetpointHigh = numpy.NaN       # [ K ]
            self.coolTempSetpointLow = numpy.NaN        # [ K ]
            self.coolTempSetpointLowLow = numpy.NaN     # [ K ]

            self.heatTempSetpointHighHigh = numpy.NaN   # [ K ]
            self.heatTempSetpointHigh = numpy.NaN       # [ K ]
            self.heatTempSetpointLow = numpy.NaN        # [ K ]
            self.heatTempSetpointLowLow = numpy.NaN     # [ K ]

            self.wTemp = numpy.NaN                      # [-]
            self.wHum = numpy.NaN                       # [-]

        # -------------------------------------------------------------
        # Evolution of the internal temperature and humidity
        # -------------------------------------------------------------
        # Rearrange the building sensible heat load equation to solve for the indoor air temperature
        # Explicit terms which either do not contain Tin or contain Tin from previous iteration [W m^-2]
        Q = -self.intHeat - self.QWindowSolar - self.sensHeatDemand + self.sensCoolDemand

        H1 = (T_wall*wallArea*zac_in_wall +
            T_mass*massArea*zac_in_mass +
            T_ceil*ceilingArea*zac_in_ceil +
            self.T_can*winArea*self.uValue +
            self.T_can*volInfil * dens * ParCalculation.cp_atm +
            self.T_can*volVent * dens * ParCalculation.cp_atm)
        # Implicit terms in eq. 2 which directly contain coefficient for newest Tin to be solved (Bueno et al., 2012)
        H2 = (wallArea*zac_in_wall +
            massArea*zac_in_mass +
            ceilingArea * zac_in_ceil +
            winArea*self.uValue +
            volInfil * dens * ParCalculation.cp_atm +
            volVent * dens * ParCalculation.cp_atm)

        # Assumes air temperature of control volume is sum of surface boundary temperatures
        # weighted by area and heat transfer coefficient + generated heat
        # Calculate indoor air temperature [K]
        self.indoorTemp = (H1 - Q)/H2

        # Rearrange the building latent heat load equation to solve for the indoor air specific humidity
        # QLinfil + QLvent = self.dehumDemand - QLintload (left hand side has qin but right hand side does not)
        # Explicit terms which either do not contain qin or contain qin from previous iteration
        QL = self.dehumDemand - self.humDemand - QLintload
        HL1 = volInfil * dens * ParCalculation.Lv *canHum + volVent * dens * ParCalculation.Lv * canHum
        # Implicit terms which directly contain coefficient for newest qin to be solved
        HL2 = volInfil * dens *ParCalculation.Lv+ volVent * dens * ParCalculation.Lv
        # Calculate indoor specific humidity [kgv kga^-1]
        self.indoorHum = (HL1 - QL) / HL2

        # Calculate relative humidity ((Pw/Pws)*100) using pressure, indoor temperature, humidity
        _Tdb, _w, _phi, _h, _Tdp, _v = psychrometrics(self.indoorTemp, self.indoorHum, MeteoData.Pre)
        # Indoor relative humidity [%]
        self.indoorRH = _phi

        # Calculate MRT using area-weighted mean surface temperatures of walls, ceiling, and floor
        A_wall = wallArea                                                    # Wall area per unit building footprint area [m^2/m^2]
        A_ceil = ceilingArea                                                 # Ceiling area per unit building footprint area [m^2/m^2]
        A_mass = massArea                                                    # Floor/thermal mass area per unit building footprint area [m^2/m^2]

        T_mrt = (T_wall * A_wall + T_ceil * A_ceil + T_mass * A_mass) / (A_wall + A_ceil + A_mass)       #Radiant Temperature [K]
        
        # Determine clothing insulation (clo) based on the season
        Season = SmartBuildingParam.Season  # Season Type: Winter 0 summer 1
        if Season == 0:                     # Winter
            clo = 1.0                       # Higher insulation for winter
        elif Season == 1:                   # Summer
            clo = 0.5                       # Lower insulation for summer
        
        # PMV  and PPD calculation
        #-0.5 to +0.5: Comfortable (target zone).< -0.5: Cool/cold discomfort.> +0.5: Warm/hot discomfort.
        self.PMV, self.PPD = calculate_pmv(self.indoorTemp - 273.15, self.indoorRH, Met=1.0, Clo = clo , v = 0.1, T_r = T_mrt - 273.15)

        # Heat fluxes of elements [W m^-2]
        # (will be used for element calculation)
        # Wall heat flux per unit wall area [W m^-2]
        self.fluxWall = zac_in_wall * (T_indoor - T_wall)
        # Top ceiling heat flux per unit ceiling or building footprint area [W m^-2]
        self.fluxRoof = zac_in_ceil * (T_indoor - T_ceil)
        # Inner horizontal heat flux per unit floor area [W m^-2]
        self.fluxMass = zac_in_mass * (T_indoor - T_mass) + self.intHeat * self.intHeatFRad/massArea

        # Calculate heat fluxes per unit floor area [W m^-2] (These are for record keeping only)
        self.fluxSolar = self.QWindowSolar/self.nFloor                                                  # [W m^-2]
        self.fluxWindow = winArea * self.uValue *(self.T_can - T_indoor)/self.nFloor                    # [W m^-2]
        self.fluxInterior = self.intHeat * self.intHeatFRad *(1.-self.intHeatFLat)/self.nFloor          # [W m^-2]
        self.fluxInfil= volInfil * dens * ParCalculation.cp_atm *(self.T_can - T_indoor)/self.nFloor    # [W m^-2]
        self.fluxVent = volVent * dens * ParCalculation.cp_atm *(self.T_can - T_indoor)/self.nFloor     # [W m^-2]

        # Total Electricity consumption per unit floor area [W m^-2] which is equal to
        # cooling consumption + electricity consumption + lighting
        self.ElecTotal = self.coolConsump/self.nFloor + BEM.Elec + BEM.Light                            # [W m^-2]
        # electricity demand other than cooling consumption per building footprint area [W m^-2]
        self.elecDomesticDemand = self.nFloor * (BEM.Elec + BEM.Light)                                  # [W m^-2]
        # Sensible hot water heating demand [W m^-2]
        CpH20 = 4200.           # heat capacity of water [J Kg^-1 K^-1]
        T_hot = 49 + 273.15     # Service water temp (assume no storage) [K]
        self.sensWaterHeatDemand = massFlowRateSWH * CpH20 * (T_hot - MeteoData.waterTemp)              # [W m^-2]

        # Calculate total sensible waste heat to canyon per unit building footprint area [W m^-2]
        # which can be determined from sensible waste to canyon, energy consumption for domestic hot water and gas consumption
        # Sensible hot water heating demand
        self.sensWaterHeatDemand = massFlowRateSWH * CpH20 * (T_hot - MeteoData.waterTemp)              # [W m^-2]
        # Waste heat of water heating
        self.QWater = (1 / self.heatEff - 1.) * self.sensWaterHeatDemand                                # [W m^-2]
        self.QGas = BEM.Gas * (1 - self.heatEff) * self.nFloor                                          # [W m^-2]
        self.sensWaste = self.sensWasteCoolHeatLatent + self.QWater + self.QGas                         # [W m^-2]
        # Calculate total gas consumption per unit floor area [W m^-2] which is equal to gas consumption per unit floor area +
        # energy consumption for domestic hot water per unit floor area + energy consumption of the heating system per unit floor area
        self.GasTotal = BEM.Gas + (massFlowRateSWH*CpH20*(T_hot - MeteoData.waterTemp)/self.nFloor)/self.heatEff + self.heatConsump/self.nFloor
