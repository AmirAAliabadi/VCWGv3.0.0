# =================================================
# Developed by: Mojtaba Safdari, Mohammad Al Janaideh, and Amir A. Aliabadi
# Atmospheric Innovations Research (AIR) Laboratory, University of Guelph, Guelph, Canada
# Last update: March  2025
# =================================================

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import math

class FuzzyControlSystem:
    def __init__(self, TOU_Low_Summer, TOU_Medium_Summer, TOU_High_Summer, TOU_Low_Winter, TOU_Medium_Winter, TOU_High_Winter):
        self.TOU_Low_Summer = TOU_Low_Summer
        self.TOU_Medium_Summer = TOU_Medium_Summer
        self.TOU_High_Summer = TOU_High_Summer
        self.TOU_Low_Winter = TOU_Low_Winter
        self.TOU_Medium_Winter = TOU_Medium_Winter
        self.TOU_High_Winter = TOU_High_Winter

        self.initialize_fuzzy_systems()

    def initialize_fuzzy_systems(self):
        # Define fuzzy variables and membership functions
        self.occupancy = ctrl.Antecedent(np.arange(0, 1, 0.01), 'occupancy')
        self.price_Summer = ctrl.Antecedent(np.arange(0, 24, 1), 'price_Summer')
        self.price_Winter = ctrl.Antecedent(np.arange(0, 24, 1), 'price_Winter')
        self.w_Temp = ctrl.Consequent(np.arange(-1, 1, 0.01), 'w_Temp')
        self.w_Hum = ctrl.Consequent(np.arange(-1, 1, 0.01), 'w_Hum')
        self.w_Dehum = ctrl.Consequent(np.arange(-1, 1, 0.01), 'w_Dehum')

        # Define membership functions
        self.define_membership_functions()
        self.define_rules()
        self.create_control_systems()

    def define_membership_functions(self):
        self.occupancy['low'] = fuzz.trapmf(self.occupancy.universe, [0, 0, 0.01, 0.02])
        self.occupancy['medium'] = fuzz.trimf(self.occupancy.universe, [0.01, 0.02, 0.03])
        self.occupancy['high'] = fuzz.trapmf(self.occupancy.universe, [0.02, 0.03, 1, 1])

        self.price_Summer['low'] = fuzz.trapmf(self.price_Summer.universe, [self.TOU_Low_Summer[0], self.TOU_Low_Summer[0], self.TOU_Low_Summer[1], self.TOU_Low_Summer[1]]) + \
                                   fuzz.trapmf(self.price_Summer.universe, [self.TOU_Low_Summer[2], self.TOU_Low_Summer[2], self.TOU_Low_Summer[3], self.TOU_Low_Summer[3]])
        self.price_Summer['medium'] = fuzz.trapmf(self.price_Summer.universe, [self.TOU_Medium_Summer[0], self.TOU_Medium_Summer[0], self.TOU_Medium_Summer[1], self.TOU_Medium_Summer[1]]) + \
                                      fuzz.trapmf(self.price_Summer.universe, [self.TOU_Medium_Summer[2], self.TOU_Medium_Summer[2], self.TOU_Medium_Summer[3], self.TOU_Medium_Summer[3]])
        self.price_Summer['high'] = fuzz.trapmf(self.price_Summer.universe, [self.TOU_High_Summer[0], self.TOU_High_Summer[0], self.TOU_High_Summer[1], self.TOU_High_Summer[1]])

        self.price_Winter['low'] = fuzz.trapmf(self.price_Winter.universe, [self.TOU_Low_Winter[0], self.TOU_Low_Winter[0], self.TOU_Low_Winter[1], self.TOU_Low_Winter[1]]) + \
                                   fuzz.trapmf(self.price_Winter.universe, [self.TOU_Low_Winter[2], self.TOU_Low_Winter[2], self.TOU_Low_Winter[3], self.TOU_Low_Winter[3]])
        self.price_Winter['medium'] = fuzz.trapmf(self.price_Winter.universe, [self.TOU_Medium_Winter[0], self.TOU_Medium_Winter[0], self.TOU_Medium_Winter[1], self.TOU_Medium_Winter[1]]) + \
                                      fuzz.trapmf(self.price_Winter.universe, [self.TOU_Medium_Winter[2], self.TOU_Medium_Winter[2], self.TOU_Medium_Winter[3], self.TOU_Medium_Winter[3]])
        self.price_Winter['high'] = fuzz.trapmf(self.price_Winter.universe, [self.TOU_High_Winter[0], self.TOU_High_Winter[0], self.TOU_High_Winter[1], self.TOU_High_Winter[1]])

        self.w_Temp['NSSet'] = fuzz.trimf(self.w_Temp.universe, [-1, -1, -0.5])
        self.w_Temp['ZSet'] = fuzz.trimf(self.w_Temp.universe, [-.5, 0, .5])
        self.w_Temp['PSSet'] = fuzz.trimf(self.w_Temp.universe, [0.5, 1, 1])

        self.w_Hum['NB'] = fuzz.trimf(self.w_Hum.universe, [-1, -1, -0.5])
        self.w_Hum['Z'] = fuzz.trimf(self.w_Hum.universe, [-0.5, 0, 0.5])
        self.w_Hum['PB'] = fuzz.trimf(self.w_Hum.universe, [0.5, 1, 1])

        self.w_Dehum['NB'] = fuzz.trimf(self.w_Dehum.universe, [-1, -1, -0.5])
        self.w_Dehum['Z'] = fuzz.trimf(self.w_Dehum.universe, [-0.5, 0, 0.5])
        self.w_Dehum['PB'] = fuzz.trimf(self.w_Dehum.universe, [0.5, 1, 1])

    def define_rules(self):
        # Define rules for temperature control
        self.ruleH1 = ctrl.Rule(self.occupancy['low'], self.w_Temp['NSSet'])
        self.ruleH2 = ctrl.Rule(self.occupancy['medium'], self.w_Temp['ZSet'])
        self.ruleH3 = ctrl.Rule(self.occupancy['high'], self.w_Temp['PSSet'])

        # Define rules for cooling in summer
        self.ruleSC1 = ctrl.Rule(self.occupancy['low'] & self.price_Summer['low'], self.w_Temp['NSSet'])
        self.ruleSC2 = ctrl.Rule(self.occupancy['low'] & self.price_Summer['medium'], self.w_Temp['NSSet'])
        self.ruleSC3 = ctrl.Rule(self.occupancy['low'] & self.price_Summer['high'], self.w_Temp['NSSet'])
        self.ruleSC4 = ctrl.Rule(self.occupancy['medium'] & self.price_Summer['low'], self.w_Temp['ZSet'])
        self.ruleSC5 = ctrl.Rule(self.occupancy['medium'] & self.price_Summer['medium'], self.w_Temp['ZSet'])
        self.ruleSC6 = ctrl.Rule(self.occupancy['medium'] & self.price_Summer['high'], self.w_Temp['ZSet'])
        self.ruleSC7 = ctrl.Rule(self.occupancy['high'] & self.price_Summer['low'], self.w_Temp['PSSet'])
        self.ruleSC8 = ctrl.Rule(self.occupancy['high'] & self.price_Summer['medium'], self.w_Temp['PSSet'])
        self.ruleSC9 = ctrl.Rule(self.occupancy['high'] & self.price_Summer['high'], self.w_Temp['PSSet'])

        # Define rules for cooling in winter
        self.ruleWC1 = ctrl.Rule(self.occupancy['low'] & self.price_Winter['low'], self.w_Temp['NSSet'])
        self.ruleWC2 = ctrl.Rule(self.occupancy['low'] & self.price_Winter['medium'], self.w_Temp['NSSet'])
        self.ruleWC3 = ctrl.Rule(self.occupancy['low'] & self.price_Winter['high'], self.w_Temp['NSSet'])
        self.ruleWC4 = ctrl.Rule(self.occupancy['medium'] & self.price_Winter['low'], self.w_Temp['ZSet'])
        self.ruleWC5 = ctrl.Rule(self.occupancy['medium'] & self.price_Winter['medium'], self.w_Temp['ZSet'])
        self.ruleWC6 = ctrl.Rule(self.occupancy['medium'] & self.price_Winter['high'], self.w_Temp['ZSet'])
        self.ruleWC7 = ctrl.Rule(self.occupancy['high'] & self.price_Winter['low'], self.w_Temp['PSSet'])
        self.ruleWC8 = ctrl.Rule(self.occupancy['high'] & self.price_Winter['medium'], self.w_Temp['PSSet'])
        self.ruleWC9 = ctrl.Rule(self.occupancy['high'] & self.price_Winter['high'], self.w_Temp['PSSet'])

        # Define rules for weekend cooling
        self.ruleWend1 = ctrl.Rule(self.occupancy['low'], self.w_Temp['NSSet'])
        self.ruleWend2 = ctrl.Rule(self.occupancy['medium'], self.w_Temp['ZSet'])
        self.ruleWend3 = ctrl.Rule(self.occupancy['high'], self.w_Temp['PSSet'])

        # Define rules for dehumidification in summer
        self.ruleDHumS1 = ctrl.Rule(self.occupancy['low'] & self.price_Summer['low'], self.w_Dehum['NB'])
        self.ruleDHumS2 = ctrl.Rule(self.occupancy['low'] & self.price_Summer['medium'], self.w_Dehum['NB'])
        self.ruleDHumS3 = ctrl.Rule(self.occupancy['low'] & self.price_Summer['high'], self.w_Dehum['NB'])
        self.ruleDHumS4 = ctrl.Rule(self.occupancy['medium'] & self.price_Summer['low'], self.w_Dehum['NB'])
        self.ruleDHumS5 = ctrl.Rule(self.occupancy['medium'] & self.price_Summer['medium'], self.w_Dehum['Z'])
        self.ruleDHumS6 = ctrl.Rule(self.occupancy['medium'] & self.price_Summer['high'], self.w_Dehum['PB'])
        self.ruleDHumS7 = ctrl.Rule(self.occupancy['high'] & self.price_Summer['low'], self.w_Dehum['PB'])
        self.ruleDHumS8 = ctrl.Rule(self.occupancy['high'] & self.price_Summer['medium'], self.w_Dehum['PB'])
        self.ruleDHumS9 = ctrl.Rule(self.occupancy['high'] & self.price_Summer['high'], self.w_Dehum['PB'])

        # Define rules for dehumidification in winter
        self.ruleDHumW1 = ctrl.Rule(self.occupancy['low'] & self.price_Winter['low'], self.w_Dehum['NB'])
        self.ruleDHumW2 = ctrl.Rule(self.occupancy['low'] & self.price_Winter['medium'], self.w_Dehum['NB'])
        self.ruleDHumW3 = ctrl.Rule(self.occupancy['low'] & self.price_Winter['high'], self.w_Dehum['NB'])
        self.ruleDHumW4 = ctrl.Rule(self.occupancy['medium'] & self.price_Winter['low'], self.w_Dehum['NB'])
        self.ruleDHumW5 = ctrl.Rule(self.occupancy['medium'] & self.price_Winter['medium'], self.w_Dehum['Z'])
        self.ruleDHumW6 = ctrl.Rule(self.occupancy['medium'] & self.price_Winter['high'], self.w_Dehum['PB'])
        self.ruleDHumW7 = ctrl.Rule(self.occupancy['high'] & self.price_Winter['low'], self.w_Dehum['PB'])
        self.ruleDHumW8 = ctrl.Rule(self.occupancy['high'] & self.price_Winter['medium'], self.w_Dehum['PB'])
        self.ruleDHumW9 = ctrl.Rule(self.occupancy['high'] & self.price_Winter['high'], self.w_Dehum['PB'])

        # Define rules for weekend dehumidification
        self.ruleDHumWend1 = ctrl.Rule(self.occupancy['low'], self.w_Dehum['NB'])
        self.ruleDHumWend2 = ctrl.Rule(self.occupancy['medium'], self.w_Dehum['Z'])
        self.ruleDHumWend3 = ctrl.Rule(self.occupancy['high'], self.w_Dehum['PB'])

        # Define rules for humidification
        self.ruleHum1 = ctrl.Rule(self.occupancy['low'], self.w_Hum['NB'])
        self.ruleHum2 = ctrl.Rule(self.occupancy['medium'], self.w_Hum['Z'])
        self.ruleHum3 = ctrl.Rule(self.occupancy['high'], self.w_Hum['PB'])

    def create_control_systems(self):
        self.cooling_Summer_ctrl = ctrl.ControlSystem([self.ruleSC1, self.ruleSC2, self.ruleSC3, self.ruleSC4, self.ruleSC5, self.ruleSC6, self.ruleSC7, self.ruleSC8, self.ruleSC9])
        self.cooling_Winter_ctrl = ctrl.ControlSystem([self.ruleWC1, self.ruleWC2, self.ruleWC3, self.ruleWC4, self.ruleWC5, self.ruleWC6, self.ruleWC7, self.ruleWC8, self.ruleWC9])
        self.cooling_weekend_ctrl = ctrl.ControlSystem([self.ruleWend1, self.ruleWend2, self.ruleWend3])
        self.heating_ctrl = ctrl.ControlSystem([self.ruleH1, self.ruleH2, self.ruleH3])
        self.dehum_Summer_ctrl = ctrl.ControlSystem([self.ruleDHumS1, self.ruleDHumS2, self.ruleDHumS3, self.ruleDHumS4, self.ruleDHumS5, self.ruleDHumS6, self.ruleDHumS7, self.ruleDHumS8, self.ruleDHumS9])
        self.dehum_Winter_ctrl = ctrl.ControlSystem([self.ruleDHumW1, self.ruleDHumW2, self.ruleDHumW3, self.ruleDHumW4, self.ruleDHumW5, self.ruleDHumW6, self.ruleDHumW7, self.ruleDHumW8, self.ruleDHumW9])
        self.ruleDHumWend_ctrl = ctrl.ControlSystem([self.ruleDHumWend1, self.ruleDHumWend2, self.ruleDHumWend3])
        self.hum_ctrl = ctrl.ControlSystem([self.ruleHum1, self.ruleHum2, self.ruleHum3])

        self.cooling_Summer = ctrl.ControlSystemSimulation(self.cooling_Summer_ctrl)
        self.cooling_Winter = ctrl.ControlSystemSimulation(self.cooling_Winter_ctrl)
        self.cooling_weekend = ctrl.ControlSystemSimulation(self.cooling_weekend_ctrl)
        self.heating = ctrl.ControlSystemSimulation(self.heating_ctrl)
        self.dehum_Summer = ctrl.ControlSystemSimulation(self.dehum_Summer_ctrl)
        self.dehum_Winter = ctrl.ControlSystemSimulation(self.dehum_Winter_ctrl)
        self.DHumWend = ctrl.ControlSystemSimulation(self.ruleDHumWend_ctrl)
        self.hum = ctrl.ControlSystemSimulation(self.hum_ctrl)
    
    def TempSetpointHeatFun(self, Nocc, SmartTempSetPoint, simTime, SmartBuildingParam, MeteoData, canTemp, dayType):
        
        heatTempSetpointHighHigh = SmartBuildingParam.heatTempSetpointHighHigh      # [K]
        heatTempSetpointHigh = SmartBuildingParam.heatTempSetpointHigh              # [K]
        heatTempSetpointLow = SmartBuildingParam.heatTempSetpointLow                # [K]
        heatTempSetpointLowLow = SmartBuildingParam.heatTempSetpointLowLow          # [K]
        Season = SmartBuildingParam.Season  # Season Type: Winter 0, summer 1 for TOU pricing [-]
        
        # Energy Price in heating is constant, so TOU is not applicable
        self.heating.input['occupancy'] = Nocc
        self.heating.compute()
        w = self.heating.output['w_Temp']  # Weight factor from fuzzy logic [-]
        
        # Calculate the new setpoint based on the value of w
        if canTemp < heatTempSetpointLow:                               # [K]
            if w >= 0:
                SmartTempSetPoint = heatTempSetpointLow                 # [K]
            else:
                SmartTempSetPoint = canTemp                             # [K]
        elif canTemp > heatTempSetpointHigh:                            # [K]
            if w >= 0:
                SmartTempSetPoint = heatTempSetpointHigh                # [K]
            else:
                SmartTempSetPoint = canTemp                             # [K]
        else:
            SmartTempSetPoint = canTemp                                 # [K]
        
        new_Tempsetpoint = SmartTempSetPoint                            # [K]
        
        # Ensure the new setpoint does not go beyond the high-high and low-low setpoints (critical values)
        new_Tempsetpoint = min(max(new_Tempsetpoint, heatTempSetpointLowLow), heatTempSetpointHighHigh)  # [K]
        return new_Tempsetpoint, w                                      # [K], [-]
        
    def TempSetpointCoolFun(self, Nocc, SmartTempSetPoint, simTime, SmartBuildingParam, MeteoData, canTemp,
                            dayType):
        coolTempSetpointHighHigh = SmartBuildingParam.coolTempSetpointHighHigh          # [ K ]
        coolTempSetpointHigh = SmartBuildingParam.coolTempSetpointHigh                  # [ K ]
        coolTempSetpointLow = SmartBuildingParam.coolTempSetpointLow                    # [ K ]
        coolTempSetpointLowLow = SmartBuildingParam.coolTempSetpointLowLow              # [ K ]
        Season = SmartBuildingParam.Season  # Season Type: Winter 0 summer 1 for TOU pricing [ - ]
        
        # Weekday
        if dayType == 1:
            # Season Check for TOU
            # Summer
            if Season == 1:
                self.cooling_Summer.input['price_Summer'] = simTime.secDay / 3600
                self.cooling_Summer.input['occupancy'] = Nocc
                self.cooling_Summer.compute()
                w = self.cooling_Summer.output['w_Temp']
            # Winter
            else:
                self.cooling_Winter.input['price_Winter'] = simTime.secDay / 3600
                self.cooling_Winter.input['occupancy'] = Nocc
                self.cooling_Winter.compute()
                w = self.cooling_Winter.output['w_Temp']
        # weekend summer/winter
        else:
            self.cooling_weekend.input['occupancy'] = Nocc
            self.cooling_weekend.compute()
            w = self.cooling_weekend.output['w_Temp']               # [-]
        
        # Calculate the new setpoint based on the value of U
        if canTemp < coolTempSetpointLow:                           # [K]
            if w >= 0:
                SmartTempSetPoint = coolTempSetpointLow             # [K]
            else:
                SmartTempSetPoint = canTemp                         # [K]
        elif canTemp > coolTempSetpointHigh:                        # [K]
            if w >= 0:
                SmartTempSetPoint = coolTempSetpointHigh            # [K]
            else:
                SmartTempSetPoint = canTemp                         # [K]
        else:
            SmartTempSetPoint = canTemp                             # [K]
        
        new_Tempsetpoint = SmartTempSetPoint                        # [K]
        
        # Making sure the new setpoint does not go beyond and lower the highhigh and lowlow setpoints that are the critical values
        new_Tempsetpoint = min(max(new_Tempsetpoint, coolTempSetpointLowLow), coolTempSetpointHighHigh)  # [K]
        return new_Tempsetpoint, w
    
    def HumSetpointFun(self, Nocc, SmartRHSetPoint, SmartBuildingParam, canHum, T_indoor, MeteoData, simTime,
                       dayType):
        RHSetPointLow = SmartBuildingParam.RHSetPointLow             # [%]
        RHSetPointLowLow = SmartBuildingParam.RHSetPointLowLow       # [%]
        RHSetPointHigh = SmartBuildingParam.RHSetPointHigh           # [%]
        RHSetPointHighHigh = SmartBuildingParam.RHSetPointHighHigh   # [%]
        
        # Set point specific humidities [kgv kga^-1]
        # Tetens equation: Pg = 610.78 exp(17.27 T / (T+237.3)) with Pg [Pa] ant T [C]
        # Saturation pressure [Pa]
        SatPre = 610.78 * math.exp(17.27 * (T_indoor - 273.15) / ((T_indoor - 273.15) + 237.3))
        
        # Calculating Spec Hum for RH for constant setpoint thresholds [kgv kga^-1]
        SmartHumSetPoint = 0.622 * (SmartRHSetPoint / 100) * SatPre / (
                MeteoData.Pre - (SmartRHSetPoint / 100) * SatPre)
        LowHumSetPoint = 0.622 * (RHSetPointLow / 100) * SatPre / (
                MeteoData.Pre - (RHSetPointLow / 100) * SatPre)
        LowLowHumSetPoint = 0.622 * (RHSetPointLowLow / 100) * SatPre / (
                MeteoData.Pre - (RHSetPointLowLow / 100) * SatPre)
        HighHumSetPoint = 0.622 * (RHSetPointHigh / 100) * SatPre / (
                MeteoData.Pre - (RHSetPointHigh / 100) * SatPre)
        HighHighHumSetPoint = 0.622 * (RHSetPointHighHigh / 100) * SatPre / (
                MeteoData.Pre - (RHSetPointHighHigh / 100) * SatPre)
        
        # Calculate the value of w using the fuzzy control system
        self.hum.input['occupancy'] = Nocc  # [Person m^-2]
        self.hum.compute()
        w = self.hum.output['w_Hum']  # [-]
        
        # Calculate the new setpoint based on the value of U
        if canHum < LowHumSetPoint:  # [kgv kga^-1]
            if w >= 0:
                SmartHumSetPoint = LowHumSetPoint  # [kgv kga^-1]
            else:
                SmartHumSetPoint = canHum  # [kgv kga^-1]
        elif canHum > HighHumSetPoint:  # [kgv kga^-1]
            if w >= 0:
                SmartHumSetPoint = HighHumSetPoint  # [kgv kga^-1]
            else:
                SmartHumSetPoint = canHum  # [kgv kga^-1]
        else:
            SmartHumSetPoint = canHum  # [kgv kga^-1]
        
        new_Humsetpoint = SmartHumSetPoint  # [kgv kga^-1]
        # Making sure the new setpoint does not go beyond and lower the highhigh and lowlow setpoints that are the critical values
        new_Humsetpoint = min(max(new_Humsetpoint, LowLowHumSetPoint), HighHighHumSetPoint)  # [kgv kga^-1]
        return new_Humsetpoint, \
            LowHumSetPoint, LowLowHumSetPoint, HighHumSetPoint, HighHighHumSetPoint, \
            RHSetPointLow, RHSetPointLowLow, RHSetPointHigh, RHSetPointHighHigh, w  # [kgv kga^-1]/[kgv kga^-1]/%/ #@hum
    
    def DehumSetpointFun(self, Nocc, SmartRHSetPoint, SmartBuildingParam, canHum, T_indoor, MeteoData, simTime,
                         dayType):
        RHSetPointLow = SmartBuildingParam.RHSetPointLow             # [%]
        RHSetPointLowLow = SmartBuildingParam.RHSetPointLowLow       # [%]
        RHSetPointHigh = SmartBuildingParam.RHSetPointHigh           # [%]
        RHSetPointHighHigh = SmartBuildingParam.RHSetPointHighHigh   # [%]
        Season = SmartBuildingParam.Season  # Season Type: Winter 0 summer 1 for TOU pricing [ - ]
        
        # Set point specific humidities [kgv kga^-1]
        # Tetens equation: Pg = 610.78 exp(17.27 T / (T+237.3)) with Pg [Pa] ant T [C]
        # Saturation pressure [Pa]
        SatPre = 610.78 * math.exp(17.27 * (T_indoor - 273.15) / ((T_indoor - 273.15) + 237.3))
        
        # Calculating Spec Hum for RH for constant setpoint thresholds [kgv kga^-1]
        SmartHumSetPoint = 0.622 * (SmartRHSetPoint / 100) * SatPre / (
                MeteoData.Pre - (SmartRHSetPoint / 100) * SatPre)
        LowHumSetPoint = 0.622 * (RHSetPointLow / 100) * SatPre / (
                MeteoData.Pre - (RHSetPointLow / 100) * SatPre)
        LowLowHumSetPoint = 0.622 * (RHSetPointLowLow / 100) * SatPre / (
                MeteoData.Pre - (RHSetPointLowLow / 100) * SatPre)
        HighHumSetPoint = 0.622 * (RHSetPointHigh / 100) * SatPre / (
                MeteoData.Pre - (RHSetPointHigh / 100) * SatPre)
        HighHighHumSetPoint = 0.622 * (RHSetPointHighHigh / 100) * SatPre / (
                MeteoData.Pre - (RHSetPointHighHigh / 100) * SatPre)
        
        # Weekday or Weekend check
        if dayType == 1:  # Weekday
            # Season check
            if Season == 1:  # Summer
                self.dehum_Summer.input['price_Summer'] = simTime.secDay / 3600
                self.dehum_Summer.input['occupancy'] = Nocc
                self.dehum_Summer.compute()
                w = self.dehum_Summer.output['w_Dehum']  # [-]
            else:  # Winter
                self.dehum_Winter.input['price_Winter'] = simTime.secDay / 3600
                self.dehum_Winter.input['occupancy'] = Nocc
                self.dehum_Winter.compute()
                w = self.dehum_Winter.output['w_Dehum']
        
        # weekend summer/winter (If the price should be considered we should have different
        # weekend prices for summer and winter prices
        else:
            self.DHumWend.input['occupancy'] = Nocc
            self.DHumWend.compute()
            w = self.DHumWend.output['w_Dehum']     # [-]
        
        # Calculate the new setpoint based on the value of U
        if canHum < LowHumSetPoint:                 # [kgv kga^-1]
            if w >= 0:
                SmartHumSetPoint = LowHumSetPoint   # [kgv kga^-1]
            else:
                SmartHumSetPoint = canHum           # [kgv kga^-1]
        elif canHum > HighHumSetPoint:
            if w >= 0:
                SmartHumSetPoint = HighHumSetPoint  # [kgv kga^-1]
            else:
                SmartHumSetPoint = canHum           # [kgv kga^-1]
        else:
            SmartHumSetPoint = canHum               # [kgv kga^-1]
        
        new_DehumSetpoint = SmartHumSetPoint        # [kgv kga^-1]
        
        # Ensure the setpoint stays within the defined bounds
        new_DehumSetpoint = min(max(new_DehumSetpoint, LowLowHumSetPoint), HighHighHumSetPoint)  # [kgv kga^-1]
        return new_DehumSetpoint, w                                                              # [kgv kga^-1]