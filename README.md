Quick Start
===========

Get python 3 (32 bit) ([Python](https://www.haskell.org/downloads/windows) for Windows).
Make sure to take the 32 bit Version, to be able to link to the `raildriver.dll`.

On the Machine that runs your `raildriver.dll` compatible simulator
(f.e. TrainSimulator 201x) run `connectRaildriver.py`.)

It will open a tcp port 22222 waiting for incomming connections.

For testing try to connect using the telnet tool `telnet <ip> 22222`.

If a simulator instance is running you should immediatly see comming data in.


Basic Protocol
==============

All data is packets are JSON UTF-8 Encoded Byte Strings. Each JSON Strucuture is
follwed by a newline character. 

On initial connect (or if the loco has changed), the client will receive:
* The LocoInfo structure (containing loco name, availible values and their min and max.
* A value dictionary with all values

From that on the client will receive update packets, containting a value dictionary,
but only containing those values which have actually changed since last packet.

If the loco changes it will start again from the beginning.

See below for examples of the packets.


Configuration
=============

In the future there will be a configuration file, till then you can tweak some
parameters by editing the `connectRaildriver.py` file.

The following parameters can be changed.

| variable  | Description                          | Default value |
|-----------|--------------------------------------|---------------|
| dllPath   | The location of the `raildirver.dll` | TS default    |
| sleepTime | The polling interval                 | 50Hz          |
| logLevel  | the log level                        | logging.INFO  |
| tcpPort   | the TCP port to listen on            | 22222         |


To change one of these from their default value, you have to add them to the constructor
of the `RaildriverServer` f.e., change the `main()` function in `connectRaildriver.py`
to 

```python

def main():
  rd = Raildriver.Raildriver(logLevel = logging.DEBUG,
                             dllPath = 'C://TS//raildriver.dll',
                             tcpPort = 22223)
  rd.runRaildriver()

```

Make sure to quote backslashes `\\`. If you want to change the loglevel like above,
you have to import the `logging` module at the beginning of the file like:

```python

import logging

```


TODO
====

* Add support for a config file (YAML)
* Add support for writing data to the simulator
** Sending JSON dictitionaries ```{ "key1": value, "key2": value }```
* Add support for "special values" like longitude, latitude



Example LocoInfo
================

This is an example of the very first packet you receive on connect or loco change.

```json
{
  "producer": "DTG", 
  "model": "DB Baureihe 101 Engine", 
  "product": "CologneKoblenz",
  "minmax": {"TractionDial": [-300.0, 300.0], "VirtualDynamicBrake": [0.0, 1.0], "VirtualPantographControl": [0.0, 1.0], "CMD_G": [0.0, 1.0], "PZB_Warning": [0.0, 1.0], "LZB_DistanceBar": [-1.0, 4000.0], "Dummy": [0.0, 1.0], "PZB_500Hz": [0.0, 1.0], "PZB_70": [0.0, 1.0], "PZB_1000Hz": [0.0, 1.0], "Accelerometer": [-320.0, 320.0], "PZB_Restriction": [0.0, 85.0], "SifaLight": [0.0, 1.0], "LZB_Buzzer": [0.0, 1.0], "BrakePipePressureBAR": [0.0, 12.0], "PZB": [0.0, 4.0], "PZB_Emergency": [0.0, 1.0], "LZB_Speed": [-1.0, 250.0], "PZB_B40": [0.0, 1.0], "AWSReset": [0.0, 1.0], "CMD_Acknowledge": [0.0, 1.0], "PZB_55": [0.0, 1.0], "VirtualBrake": [0.0, 1.0], "PZB_DistantPassed": [-1.0, 4.0], "CMD_S": [0.0, 1.0], "EngineBrakeControl": [0.0, 1.0], "CMD_SpeedH": [-1.0, 9.0], "AWSWarnCount": [0.0, 1.0], "Sifa": [0.0, 1.0], "SimpleChangeDirection": [-1.0, 1.0], "SimpleThrottle": [0.0, 1.0], "CMD_Override": [0.0, 1.0], "LZB_Auto": [0.0, 1.0], "VirtualThrottle": [0.0, 1.0], "Horn": [0.0, 1.0], "PantographControl": [0.0, 1.0], "Ammeter": [-600.0, 600.0], "MainReservoirPressureBAR": [0.0, 12.0], "PZB_85": [0.0, 1.0], "PZB_1000Hz_Control": [-1.0, 1250.0], "CMD_SpeedU": [-1.0, 9.0], "Startup": [-1.0, 1.0], "Headlights": [0.0, 2.0], "TrainBrakeControl": [0.0, 1.0], "LZB_DistanceH": [-1.0, 9.0], "PantographID": [0.0, 3.0], "SpeedometerKPH": [0.0, 250.0], "PantographSwitch": [-1.0, 1.0], "AmmeterNeedle": [0.0, 600.0], "Wipers": [0.0, 1.0], "Current": [0.0, 100000.0], "LocoBrakeCylinderPressureBAR": [0.0, 10.0], "AFB_Speed": [0.0, 250.0], "PZB_500Hz_Control": [-1.0, 250.0], "LZB_End": [0.0, 1.0], "EmergencyBrake": [0.0, 1.0], "TractiveEffort": [-1000.0, 10000.0], "HandBrake": [0.0, 1.0], "Regulator": [0.0, 1.0], "CMD_SpeedT": [-1.0, 9.0], "LZB_DistanceK": [-1.0, 9.0], "CompressorState": [0.0, 1.0], "LZB_Distance": [-1.0, 10000.0], "LZB_Ending": [0.0, 1.0], "AFB": [0.0, 1.0], "PZB_RestrictiveMode": [-1.0, 15.0], "Sander": [0.0, 1.0], "Reverser": [-1.0, 1.0], "DoorsOpenClose": [0.0, 1.0], "CMD_Free": [0.0, 1.0], "SifaAlarm": [0.0, 1.0], "VirtualEngineBrakeControl": [-1.0, 1.0], "LZB_SpeedWarning": [0.0, 250.0], "CabLight": [0.0, 1.0], "DynamicBrake": [0.0, 1.0], "PantographVoltage": [0.0, 20.0], "PZB_2000Hz_Control": [-1.0, 1.0], "LZB": [0.0, 1.0], "SifaReset": [0.0, 1.0]},
  "keys": ["TractiveEffort", "Current", "CompressorState", "MainReservoirPressureBAR", "BrakePipePressureBAR", "LocoBrakeCylinderPressureBAR", "LocoBrakeCylinderPressureBAR", "TractionDial", "Ammeter", "AmmeterNeedle", "SpeedometerKPH", "Accelerometer", "VirtualThrottle", "Regulator", "Reverser", "SimpleChangeDirection", "SimpleThrottle", "VirtualBrake", "TrainBrakeControl", "PantographControl", "VirtualPantographControl", "PantographID", "PantographSwitch", "PantographVoltage", "Horn", "Startup", "Sander", "HandBrake", "Headlights", "VirtualDynamicBrake", "DynamicBrake", "Wipers", "EmergencyBrake", "DoorsOpenClose", "VirtualEngineBrakeControl", "EngineBrakeControl", "AWSReset", "AWSWarnCount", "AFB", "AFB_Speed", "CMD_SpeedU", "CMD_SpeedT", "CMD_SpeedH", "Sifa", "SifaReset", "SifaLight", "SifaAlarm", "PZB", "CMD_Override", "CMD_Free", "CMD_Acknowledge", "PZB_1000Hz_Control", "PZB_500Hz_Control", "PZB_2000Hz_Control", "PZB_DistantPassed", "PZB_RestrictiveMode", "PZB_55", "PZB_70", "PZB_85", "PZB_B40", "PZB_500Hz", "PZB_1000Hz", "PZB_Restriction", "CMD_S", "CMD_G", "PZB_Warning", "PZB_Emergency", "LZB", "LZB_Auto", "LZB_Ending", "LZB_End", "LZB_Buzzer", "LZB_Speed", "LZB_SpeedWarning", "LZB_Distance", "LZB_DistanceH", "LZB_DistanceK", "LZB_DistanceBar", "Dummy", "CabLight"]
}
```

Example Update 
==============
The following is actually a "full" record with all variable as you would receive it on initial
connect.

```json
{
  "TractionDial": 172.62261962890625,
  "VirtualDynamicBrake": 0.0,
  "VirtualPantographControl": 1.0, 
  "CMD_G": 0.0, 
  "PZB_Warning": 0.0, 
  "LZB_DistanceBar": -1.0, 
  "Dummy": 0.0, 
  "PZB_500Hz": 0.0, 
  "PZB_70": 0.0, 
  "PZB_1000Hz": 0.0, 
  "Accelerometer": 172.60235595703125, 
  "PZB_Restriction": 0.0, 
  "SifaLight": 1.0, 
  "LZB_Buzzer": 0.0, 
  "BrakePipePressureBAR": 4.998698711395264, 
  "PZB": 0.0, "PZB_Emergency": 0.0, 
  "LZB_Speed": -1.0, 
  "PZB_B40": 0.0, 
  "AWSReset": 0.0, 
  "CMD_Acknowledge": 0.0, 
  "PZB_55": 0.0, 
  "VirtualBrake": 0.0, 
  "PZB_DistantPassed": -1.0, 
  "CMD_S": 0.0, 
  "EngineBrakeControl": 0.0, 
  "CMD_SpeedH": -1.0, 
  "AWSWarnCount": 0.0, 
  "Sifa": 0.0, 
  "SimpleChangeDirection": 1.0, 
  "SimpleThrottle": 0.800000011920929, 
  "CMD_Override": 0.0, 
  "LZB_Auto": 0.0, 
  "VirtualThrottle": 0.6000000238418579, 
  "Horn": 0.0, "PantographControl": 1.0, 
  "Ammeter": 194.0355224609375, 
  "MainReservoirPressureBAR": 9.98742389678955, 
  "PZB_85": 0.0, "PZB_1000Hz_Control": -1.0, 
  "CMD_SpeedU": -1.0, 
  "Startup": 1.0, 
  "Headlights": 0.0, 
  "TrainBrakeControl": 0.0, 
  "LZB_DistanceH": -1.0, 
  "PantographID": 2.0, 
  "SpeedometerKPH": 34.20183563232422, 
  "PantographSwitch": 0.0, 
  "AmmeterNeedle": 194.05905151367188, 
  "Wipers": 0.0, 
  "Current": 194.0127410888672, 
  "LocoBrakeCylinderPressureBAR": 0.0, 
  "AFB_Speed": 0.0, 
  "PZB_500Hz_Control": -1.0, 
  "LZB_End": 0.0, 
  "EmergencyBrake": 0.0, 
  "TractiveEffort": 172.60235595703125, 
  "HandBrake": 0.0, 
  "Regulator": 0.6000000238418579, 
  "CMD_SpeedT": -1.0, 
  "LZB_DistanceK": -1.0, 
  "CompressorState": 0.0, 
  "LZB_Distance": -1.0, 
  "LZB_Ending": 0.0, 
  "AFB": 0.0, 
  "PZB_RestrictiveMode": -1.0, 
  "Sander": 0.0, 
  "Reverser": 1.0, 
  "DoorsOpenClose": 0.0, 
  "CMD_Free": 0.0, 
  "SifaAlarm": 0.0, 
  "VirtualEngineBrakeControl": 0.0, 
  "LZB_SpeedWarning": 0.0, 
  "CabLight": 1.0, 
  "DynamicBrake": 0.0, 
  "PantographVoltage": 0.0, 
  "PZB_2000Hz_Control": -1.0, 
  "LZB": 0.0, 
  "SifaReset": 0.0
}
```

Following packets contain only those values which actually update

```json

{
  "TractionDial": 172.45770263671875, 
  "Accelerometer": 172.4319610595703, 
  "Current": 193.8212127685547, 
  "Ammeter": 193.85015869140625, 
  "SpeedometerKPH": 34.942012786865234, 
  "AmmeterNeedle": 193.86778259277344, 
  "TractiveEffort": 172.4319610595703
}

```