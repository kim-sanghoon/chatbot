"""
chatbot/identifier2ont.py

It converts tokenized natural language input to corresponding ontology class.
"""

def id2trigger(_object, _action=''):
    ontDict = {
        'air conditioner': {
            'enable': 'CoolingSystemEnabledTrigger',
            'disable': 'CoolingSystemDisabledTrigger',
            'increase': 'TemperatureSetToTrigger',
            'decrease': 'TemperatureSetToTrigger',
            'set': 'TemperatureSetToTrigger',
            '': 'CoolingSystemEnabledTrigger'
        },
        'air purifier': {
            'enable': 'AirPurifierEnabledTrigger',
            'disable': 'AirPurifierDisabledTrigger',
            'increase': 'SensedAirQualityIncreasedTrigger',
            'decrease': 'SensedAirQualityDecreasedTrigger',
            '': 'SensedAirQualityDecreasedTrigger'
        },
        'thermostat': {
            'enable': 'SensedTemperatureDecreasedTrigger',
            'disable': 'SensedTemperatureIncreasedTrigger',
            'increase': 'SensedTemperatureIncreasedTrigger',
            'decrease': 'SensedTemperatureDecreasedTrigger',
            'set': 'TemperatureSetToTrigger',
            '': 'TemperatureSetToTrigger'
        },
        'heater': {
            'enable': 'HeatingSystemEnabledTrigger',
            'disable': 'HeatingSystemDisabledTrigger',
            'increase': 'TemperatureSetToTrigger',
            'decrease': 'TemperatureSetToTrigger',
            'set': 'TemperatureSetToTrigger',
            '': 'HeatingSystemEnabledTrigger'
        },
        'TV': {
            'enable': 'StartedWatchingTvTrigger',
            'disable': 'StoppedWatchingTvTrigger',
            'set': 'StartedWatchingTvTrigger',
            'make': 'StartedWatchingTvTrigger'

        },
        'shade': {
            'enable': 'ShadingSystemEnabledTrigger',
            'disable': 'ShadingSystemDisabledTrigger',
            'increase': 'ShadeSetToTrigger',
            'decrease': 'ShadeSetToTrigger',
            'set': 'ShadeSetToTrigger',
            '': 'ShadingSystemEnabledTrigger'
        },
        'light': {
            'enable': 'LightingSystemEnabledTrigger',
            'disable': 'LightingSystemDisabledTrigger',
            'increase': 'SensedLightingIncreasedTrigger',
            'decrease': 'SensedLightingDecreasedTrigger',
            '': 'LightingSystemEnabledTrigger'
        },
        'humidifier': {
            'increase': 'SensedHumidityIncreasedTrigger',
            'decrease': 'SensedHumididtyDecreasedTrigger',
            'set': 'HumiditySetToTrigger',
            '': 'HumiditySetToTrigger'
        },
        'window': {
            'open': 'WindowFrameOpenedTrigger',
            'close': 'WindowFrameClosedTrigger',
            'enable': 'WindowFrameOpenedTrigger',
            'disable': 'WindowFrameClosedTrigger',
            '': 'WindowFrameOpenedTrigger'
        },
        'security': {
            'enable': 'SecuritySystemEnabledTrigger',
            'disable': 'SecuritySystemDisabledTrigger',
            'set': 'SecuritySystemEnabledTrigger',
            '': 'SecuritySystemEnabledTrigger'
        },
        'alarm': {
            'enable': 'AddedAlarmTrigger',
            'disable': 'DeletedAlarmTrigger',
            'set': 'AddedAlarmTrigger',
            '': 'AddedAlarmTrigger'
        },
        'noise': {
            'enable': 'SensedNoiseLevelIncreasedTrigger',
            'disable': 'SensedNoiseLevelDecreasedTrigger',
            'increase': 'SensedNoiseLevelIncreasedTrigger',
            'decrease': 'SensedNoiseLevelDecreasedTrigger',
            '': 'SensedNoiseLevelIncreasedTrigger'
        },
        'air pressure': {
            'enable': 'SensedAirPressureIncreasedTrigger',
            'disable': 'SensedAirPressureDecreasedTrigger',
            'increase': 'SensedAirPressureIncreasedTrigger',
            'decrease': 'SensedAirPressureDecreasedTrigger',
            '': 'SensedAirPressureIncreasedTrigger'
        },
        'audio': {
            'enable': 'StartedListeningMusicTrigger',
            'disable': 'StoppedListeningMusicTrigger',
            'increase': 'VolumeIncreasedTrigger',
            'decrease': 'VolumeDecreasedTrigger',
            '': 'StartedListeningMusicTrigger'
        },
        'self': {
            'come': 'GPSEnterAreaTrigger',
            'leave': 'GPSExitAreaTrigger'
        },
        'that': {
            '': ''
        },
        'time': {
            '':'EveryTimeTrigger'
        },
        'weather': {
            '': 'WeatherConditionsTrigger'
        },
        'computer': {
            'enable': 'ComputerTurnedOnTrigger',
            'disable': 'ComputerTurnedOffTrigger'
        },
        'chatbot': {
            'invoke': 'VoiceCommandTrigger',
            '': 'VoiceCommandTrigger'
        }
    }

    if _object not in ontDict:
        raise RuntimeError('Not supported object - ' + _object)
    else:
        # This looks weird, but Python calls every id2trigger() while initializing ontDict in id2action()
        # Therefore, returning None is needed otherwise it will cause tricky error.
        ret = ontDict[_object]
        if _action not in ret:
            return None
        else:
            return ret[_action]

def id2action(_object, _action):
    ontDict = {
        'air conditioner': {
            'enable': 'EnableCoolingSystemAction',
            'disable': 'DisableCoolingSystemAction',
            'increase': 'SetTemperatureAction',
            'decrease': 'SetTemperatureAction',
            'set': 'SetTemperatureAction',
            'check': id2trigger(_object)
        },
        'air purifier': {
            'enable': 'EnableAirPurifierSystemAction',
            'disable': 'DisableAirPurifierSystemAction',
            'increase': 'EnableAirPurifierSystemAction',
            'decrease': 'DisableAirPurifierSystemAction',
            'check': id2trigger(_object)
        },
        'thermostat': {
            'enable': 'SetTemperatureAction',
            'disable': 'SetTemperatureAction',
            'increase': 'SetTemperatureAction',
            'decrease': 'SetTemperatureAction',
            'set': 'SetTemperatureAction',
            'check': id2trigger(_object)
        },
        'heater': {
            'enable': 'EnableHeatingSystemAction',
            'disable': 'DisableHeatingSystemAction',
            'increase': 'SetTemperatureAction',
            'decrease': 'SetTemperatureAction',
            'set': 'SetTemperatureAction',
            'check': id2trigger(_object)
        },
        'TV': {
            'enable': 'StartWatchingTvAction',
            'disable': 'StopWatchingTvAction',
            'set': 'StartWatchingTvAction',
            'make': 'StartWatchingTvAction',
            'check': id2trigger(_object)
        },
        'shade': {
            'open': 'DisableShadingSystemAction',
            'close': 'EnableShadingSystemAction',
            'enable': 'EnableShadingSystemAction',
            'disable': 'DisableShadingSystemAction',
            'increase': 'SetShadingAction',
            'decrease': 'SetShadingAction',
            'set': 'SetShadingAction',
            'check': id2trigger(_object)
        },
        'light': {
            'enable': 'EnableLightingSystemAction',
            'disable': 'DisableLightingSystemAction',
            'increase': 'SetLightingAction',
            'decrease': 'SetLightingAction',
            'set': 'SetLightingAction',
            'check': id2trigger(_object)
        },
        'humidifier': {
            'enable': 'EnableHumidifierSystemAction',
            'disable': 'DisableHumidifierSystemAction',
            'increase': 'SetHumidityAction',
            'decrease': 'SetHumidityAction',
            'set': 'SetHumidityAction',
            'make': 'SetHumidityAction',
            'check': id2trigger(_object)
        },
        'window': {
            'open': 'OpenWindowFrameAction',
            'close': 'CloseWindowFrameAction',
            'enable': 'OpenWindowFrameAction',
            'disable': 'CloseWindowFrameAction',
            'check': id2trigger(_object)
        },
        'security': {
            'enable': 'EnableSecuritySystemAction',
            'disable': 'DisableSecuritySystemAction',
            'increase': 'EnableSecuritySystemAction',
            'decrease': 'DisableSecuritySystemAction',
            'set': 'EnableSecuritySystemAction',
            'make': 'EnableSecuritySystemAction',
            'check': id2trigger(_object)
        },
        'alarm': {
            'enable': 'AddAlarmAction',
            'disable': 'TurnAlarmOffAction',
            'set': 'AddAlarmAction',
            'make': 'AddAlarmAction',
            'check': id2trigger(_object)
        },
        'noise': {
            'disable': 'TurnAlarmOffAction',
            'decrease': 'TurnAlarmOffAction',
            'check': id2trigger(_object)
        },
        'audio': {
            'enable': 'StartListeningMusicAction',
            'disable': 'StopListeningMusicAction',
            'increase': 'IncreaseVolumeAction',
            'decrease': 'DecreaseVolumeAction',
            'check': id2trigger(_object)
        },
        'self': {
            'remind': 'AddAlarmAction'
        },
        'that': {
            'enable': 'TurnEntireDeviceOnAction',
            'disable': 'TurnEntireDeviceOffAction'
        },
        'computer': {
            'enable': 'TurnComputerOnAction',
            'disable': 'TurnComputerOffAction'
        }
    }

    if _object not in ontDict:
        raise RuntimeError('Not supported object - ' + _object)
    return ontDict[_object][_action]