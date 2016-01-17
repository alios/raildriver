Quick Start
===========

Get python 3 (32 bit) ([Python](https://www.haskell.org/downloads/windows) for Windows).
Make sure to take the 32 bit Version, to be able to link to the `raildriver.dll`.

On the Machine that runs your `raildriver.dll` compatible simulator
(f.e. TrainSimulator 201x) run `connectRaildriver.py`.

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


Configuration
=============

In the future there will be a configuration file, till then you can tweak some
parameters by editing the `connectRaildriver.py` file.

The following parameters can be changed.

|-----------|--------------------------------------|---------------|
| variable  | Description                          | Default value |
|-----------|--------------------------------------|---------------|
| dllPath   | The location of the `raildirver.dll` | TS default    |
|-----------|--------------------------------------|---------------|
| sleepTime | The polling interval                 | 50Hz          |
|-----------|--------------------------------------|---------------|
| logLevel  | the log level                        | logging.INFO  |
|-----------|--------------------------------------|---------------|
| tcpPort   | the TCP port to listen on            | 22222         |
|-----------|--------------------------------------|---------------|


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


TODO
====

* Add support for a config file (YAML)
* Add support for writing data to the simulator
** Sending JSON dictitionaries ```{ "key1": value, "key2": value }```
* Add support for "special values" like longitude, latitude





