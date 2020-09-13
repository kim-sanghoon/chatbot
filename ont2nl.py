"""
chatbot/ont2nl.py

It convert ontology class to corresponding natural language.
"""

from mashup import *
from datetime import datetime
import dateutil.parser

nlDict = {
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
    'ShadingSystemEnabledTrigger': 'the curtains are closed. ',
    'ShadingSystemDisabledTrigger': 'the curtains are opened. ',
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
    'VoiceCommandTrigger': 'the voice command is activated. ',
    # Actions list
    'EnableCoolingSystemAction': 'the air conditioner will be turned on. ',
    'DisableCoolingSystemAction': 'the air conditioner will be turned off. ',
    'SetTemperatureAction': 'the temperature setting will be changed to 26 degrees Celcius. ',
    'EnableAirPurifierSystemAction': 'the air purifier will be turned on. ',
    'DisableAirPurifierSystemAction': 'the air purifier will be turned off. ',
    'EnableHeatingSystemAction': 'the heater will be turned on. ',
    'DisableHeatingSystemAction': 'the heater will be turned off. ',
    'StartWatchingTvAction': 'the TV will be turned on. ',
    'StopWatchingTvAction': 'the TV will be turned off. ',
    'EnableShadingSystemAction': 'the curtains will be closed. ',
    'DisableShadingSystemAction': 'the curtains will be opened. ',
    'SetShadingAction': 'the curtain position will be changed. ',
    'EnableLightingSystemAction': 'the lights will be turned on. ',
    'DisableLightingSystemAction': 'the lights will be turned off. ',
    'SetLightingAction': 'the lights setting will be changed. ',
    'EnableHumidifierSystemAction': 'the humidifier will be turned on. ',
    'DisableHumidifierSystemAction': 'the humidifier will be turned off. ',
    'SetHumidityAction': 'the humidifier setting will be changed. ',
    'OpenWindowFrameAction': 'the windows will be opened. ',
    'CloseWindowFrameAction': 'the windows will be closed. ',
    'EnableSecuritySystemAction': 'the security system will be activated. ',
    'DisableSecuritySystemAction': 'the security system will be deactivated. ',
    'AddAlarmAction': 'a notification for you will be added. ',
    'TurnAlarmOffAction': 'the notification will be turned off. ',
    'StartListeningMusicAction': 'the audio will start playing. ',
    'StopListeningMusicAction': 'the audio will stop playing. ',
    'IncreaseVolumeAction': 'the volume will be increased. ',
    'DecreaseVolumeAction': 'the volume will be decreased. ',
    'TurnEntireDeviceOnAction': 'entire devices in the area will be turned on. ',
    'TurnEntireDeviceOffAction': 'entire devices in the area will be turned off. ',
    'TurnComputerOnAction': 'the computer will be turned on. ',
    'TurnComputerOffAction': 'the computer will be turned off. '
}

# TODO: Double triggers are not supported.
def speak_mashup(m):
    g = m.graph
    node = m.first

    ret = ""
    initWords, i = ["If ", "First, ", "Second, ", "Third, ", "Next, ", "After that, ", "Then, ", "Finally, "], 0

    while node is not None:
        ret, i = ret + initWords[i], i + 1 if i < len(initWords) else i
        ret += nlDict[node.category]

        if node.category == 'EveryTimeTrigger':
            timeObj = dateutil.parser.isoparse(node.raw['time'])

            hour, minute, pm = timeObj.hour % 12, timeObj.minute, timeObj.hour >= 12
            if hour == 0:
                hour = 12
            
            ret += str(hour) + " "
            if minute != 0:
                ret += str(minute) + " "
            ret += "PM. " if pm else "AM. "

        ret += '<break time="700ms">'
        nextNode = list(g.neighbors(node))
        if len(nextNode) > 0:
            node = nextNode[0]
        else:
            break
    
    return '<speak>' + ret
