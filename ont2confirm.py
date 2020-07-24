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
    'EnableCoolingSystemAction': 'Turning the air conditioner on',
    'DisableCoolingSystemAction': 'Turning the air conditioner off',
    'SetTemperatureAction': 'Changing the temperature setting',
    'EnableAirPurifierSystemAction': 'Turning the air purifier on',
    'DisableAirPurifierSystemAction': 'Turning the air purifier off',
    'EnableHeatingSystemAction': 'Turning the heater on',
    'DisableHeatingSystemAction': 'Turning the heater off',
    'StartWatchingTvAction': 'Turning the TV on',
    'StopWatchingTvAction': 'Turning the TV off',
    'EnableShadingSystemAction': 'Closing the shade',
    'DisableShadingSystemAction': 'Opening the shade',
    'SetShadingAction': 'Changing the shade position',
    'EnableLightingSystemAction': 'Turning the lights on',
    'DisableLightingSystemAction': 'Turning the lights off',
    'SetLightingAction': 'Changing the light setting',
    'EnableHumidifierSystemAction': 'Turning the humidifier on',
    'DisableHumidifierSystemAction': 'Turning the humidifier off',
    'SetHumidityAction': 'Changing the humidifier setting',
    'OpenWindowFrameAction': 'Opening the windows',
    'CloseWindowFrameAction': 'Closing the windows',
    'EnableSecuritySystemAction': 'Activating the security system',
    'DisableSecuritySystemAction': 'Deactivating the security system',
    'AddAlarmAction': 'Adding an alarm',
    'TurnAlarmOffAction': 'Turning the alarm off',
    'StartListeningMusicAction': 'Start playing the audio',
    'StopListeningMusicAction': 'Stop playing the audio',
    'IncreaseVolumeAction': 'Increasing the volume',
    'DecreaseVolumeAction': 'Decreasing the volume',
    'TurnEntireDeviceOnAction': 'Turning entire devices on in this area',
    'TurnEntireDeviceOffAction': 'Turning entire devices off in this area',
    'TurnComputerOnAction': 'Turning the computer on',
    'TurnComputerOffAction': 'Turning the computer off',

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
    'ShadingSystemEnabledTrigger': 'the shade is closed. ',
    'ShadingSystemDisabledTrigger': 'the shade is opened. ',
    'ShadeSetToTrigger': 'the shade position is changed. ',
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
    'AddedAlarmTrigger': 'an alarm is added. ',
    'DeletedAlarmTrigger': 'an alarm is deleted. ',
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
    'WeatherConditionsTrigger': 'the weather condition is met. ',
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
        
        ret += "Got it, tell me if you have more commands to add, or just say I'm done."
    else:
        responses = [
            "Okay, anything else to add?",
            "Consider it done, anything else?",
            "Added to the mashup, anything else?",
            "Sure, is there anything else?",
        ]

        if resp:
            ret += random.choice(responses)

    return ret

def confirm_init():
    global initialTriggerMet
    global firstAppend

    initialTriggerMet = False
    firstAppend = True