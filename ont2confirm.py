"""
chatbot/ont2confirm.py

It convert ontology class to corresponding natural language.
Unlike ont2nl.py, this generates an implicit confirmation for the add_command.
"""

from mashup import *
from datetime import datetime
import dateutil.parser
import random

confirmDict = {
    # Actions list
    'EnableCoolingSystemAction': 'Turning on the air conditioner',
    'DisableCoolingSystemAction': 'Turning off the air conditioner',
    'SetTemperatureAction': 'Setting the temperature to 26 degrees Celcius',
    'EnableAirPurifierSystemAction': 'Turning on the air purifier',
    'DisableAirPurifierSystemAction': 'Turning off the air purifier',
    'EnableHeatingSystemAction': 'Turning on the heater',
    'DisableHeatingSystemAction': 'Turning off the heater',
    'StartWatchingTvAction': 'Turning on the TV',
    'StopWatchingTvAction': 'Turning off the TV',
    'EnableShadingSystemAction': 'Closing the curtain',
    'DisableShadingSystemAction': 'Opening the curtain',
    'SetShadingAction': 'Changing the curtain position',
    'EnableLightingSystemAction': 'Turning on the lights',
    'DisableLightingSystemAction': 'Turning off the lights',
    'SetLightingAction': 'Changing the light setting',
    'EnableHumidifierSystemAction': 'Turning on the humidifier',
    'DisableHumidifierSystemAction': 'Turning off the humidifier',
    'SetHumidityAction': 'Changing the humidifier setting',
    'OpenWindowFrameAction': 'Opening the windows',
    'CloseWindowFrameAction': 'Closing the windows',
    'EnableSecuritySystemAction': 'Enabling the security system',
    'DisableSecuritySystemAction': 'Diabling the security system',
    'AddAlarmAction': 'Adding a notification',
    'TurnAlarmOffAction': 'Turning off the notification',
    'StartListeningMusicAction': 'Start playing the audio',
    'StopListeningMusicAction': 'Stop playing the audio',
    'IncreaseVolumeAction': 'Increasing the volume',
    'DecreaseVolumeAction': 'Decreasing the volume',
    'TurnEntireDeviceOnAction': 'Turning on the entire devices in this area',
    'TurnEntireDeviceOffAction': 'Turning off the entire devices in this area',
    'TurnComputerOnAction': 'Turning on the computer',
    'TurnComputerOffAction': 'Turning off the computer',

    # Triggers list
    'CoolingSystemEnabledTrigger': 'the air conditioner is turned on. ',
    'CoolingSystemDisabledTrigger': 'the air conditioner is turned off. ',
    'TemperatureSetToTrigger': 'the temperature setting is changed. ',
    'AirPurifierEnabledTrigger': 'the air purifier is turned on. ',
    'AirPurifierDisabledTrigger': 'the air purifier is turned off. ',
    'SensedAirQualityIncreasedTrigger': 'the air quality becomes good. ',
    'SensedAirQualityDecreasedTrigger': 'the air quality becomes bad. ',
    'SensedTemperatureDecreasedTrigger': 'the temperature decreases. ',
    'SensedTemperatureIncreasedTrigger': 'the temperature increases. ',
    'HeatingSystemEnabledTrigger': 'the heater is turned on. ',
    'HeatingSystemDisabledTrigger': 'the heater is turned off. ',
    'StartedWatchingTvTrigger': 'the TV is turned on. ',
    'StoppedWatchingTvTrigger': 'the TV is turned off. ',
    'ShadingSystemEnabledTrigger': 'the curtain is closed. ',
    'ShadingSystemDisabledTrigger': 'the curtain is opened. ',
    'ShadeSetToTrigger': 'the curtain position is changed. ',
    'LightingSystemEnabledTrigger': 'the lights are turned on. ',
    'LightingSystemDisabledTrigger': 'the lights are turned off. ',
    'SensedLightingIncreasedTrigger': 'the lights are bright. ',
    'SensedLightingDecreasedTrigger': 'the lights are dark. ',
    'SensedHumidityIncreasedTrigger': 'the room is humid. ',
    'SensedHumididtyDecreasedTrigger': 'the room is not humid. ',
    'HumiditySetToTrigger': 'the humidifier setting is changed. ',
    'WindowFrameOpenedTrigger': 'the windows are opened. ',
    'WindowFrameClosedTrigger': 'the windows are closed. ',
    'SecuritySystemEnabledTrigger': 'the security system is activated. ',
    'SecuritySystemDisabledTrigger': 'the security system is deactivated. ',
    'AddedAlarmTrigger': 'a notification is added. ',
    'DeletedAlarmTrigger': 'a notification is deleted. ',
    'SensedNoiseLevelIncreasedTrigger': 'noise becomes loud. ',
    'SensedNoiseLevelDecreasedTrigger': 'noise becomes quiet. ',
    'SensedAirPressureIncreasedTrigger': 'the air pressure is high. ',
    'SensedAirPressureDecreasedTrigger': 'the air pressure is low. ', 
    'StartedListeningMusicTrigger': 'the audio started playing. ',
    'StoppedListeningMusicTrigger': 'the audio stopped playing. ',
    'VolumeIncreasedTrigger': 'the volume is increased. ',
    'VolumeDecreasedTrigger': 'the volume is decreased. ',
    'GPSEnterAreaTrigger': 'you enter the area. ',
    'GPSExitAreaTrigger': 'you leave the area. ',
    'EveryTimeTrigger': 'the time is ',
    'WeatherConditionsTrigger': 'the weather condition is raining. ',
    'ComputerTurnedOnTrigger': 'the computer is turned on. ',
    'ComputerTurnedOffTrigger': 'the computer is turned off. ',
    'VoiceCommandTrigger': 'the voice command is activated. '
}

# Check if the number of triggers is more than two
initialTriggerMet = False

# Exhaustive information has been provided
firstAppend = True

def craft_trigger(node):
    global initialTriggerMet

    ret = ' if ' + confirmDict[node.category]

    if not initialTriggerMet:
        initialTriggerMet = True
    else:
        ret = 'Checking ' + ret

    if node.category == 'EveryTimeTrigger':
        timeObj = dateutil.parser.isoparse(node.raw['time'])

        hour, minute, pm = timeObj.hour % 12, timeObj.minute, timeObj.hour >= 12
        if hour == 0:
            hour = 12
            
        ret += str(hour) + " "
        if minute != 0:
            ret += str(minute) + " "
        ret += "PM. " if pm else "AM. "

    return ret


def speak_add_command(m, resp=True):
    global firstAppend

    g = m.graph
    node = None

    ret = ""

    if g.number_of_nodes() < 3:
        node = m.first

        while node is not None:
            if 'Trigger' in node.category:
                ret += craft_trigger(node)
            else:
                ret = confirmDict[node.category] + ret

            nextNode = list(g.neighbors(node))
            if len(nextNode) > 0:
                node = nextNode[0]
            else:
                break   
    else:
        node = m.last

        while node is not None:
            if 'Trigger' in node.category:
                ret += craft_trigger(node)
            else:
                ret += confirmDict[node.category] + ". "

            nextNode = list(g.neighbors(node))
            if len(nextNode) > 0:
                node = nextNode[0]
            else:
                break    
    
    if firstAppend:
        firstAppend = False
        
        ret += "<break time='700ms'/> Got it, tell me if you have more commands to add, or just say I'm done."
    else:
        responses = [
            "<break time='700ms'/> Okay, anything else to add?",
            "<break tiem='700ms'/> Great, anything else?",
            "<break time='700ms'/> Got it, anything else?",
            "<break time='700ms'/> Sure, is there anything else?",
        ]

        if resp:
            ret += random.choice(responses)

    return '<speak>' + ret + '</speak>'

def confirm_init():
    global initialTriggerMet
    global firstAppend

    initialTriggerMet = False
    firstAppend = True
