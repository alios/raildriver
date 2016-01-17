# Copyright (c) 2016, Markus Barenhoff
# 
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
# 
#     * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
# 
#     * Neither the name of Markus Barenhoff nor the names of other
#       contributors may be used to endorse or promote products derived
#       from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import ctypes
import threading
import logging
import time
import json
import socket
import signal
import sys
import select

class LocoInfo:
    def __init__(self, producer, product, model, keys, minmax):
        self.producer = producer
        self.product = product
        self.model = model
        self.keys = keys
        self.minmax = minmax

class RaildriverServer(threading.Thread):

    def __init__(self, dllPath, sleepTime):        
        threading.Thread.__init__(self)

        self.sleepTime = sleepTime
        self.running = True
        self.locoInfo = None
        self.values = dict()
        self.dataLock = threading.RLock()
        
        self.clientSockets = []
        self.clientSocketsLock = threading.Lock()
        
        self.api = RaildriverAPI(dllPath)
        self.api.SetRailSimConnected(True)
        self.api.SetRailDriverConnected(True)
        self.getLocoInfoUpdate()
        logging.debug("api loaded: %s" % self.api.rdDll)

        self.setName("RaildriverServer");

    def broadcastClients(self, data):
        brokenSockets = []

        self.clientSocketsLock.acquire()
        for c in self.clientSockets:
            try:
                c.sendall(data.encode("utf-8"));
            except socket.error as e:
                logging.debug("unable to send data to client: %s" % repr(e))
                c.close()
                brokenSockets.append(c)

        for c in brokenSockets:
            self.clientSockets.remove(c)
        self.clientSocketsLock.release()
                
        
    def disconnect(self):
        for c in self.clientSockets:
            c.shutdown(socket.SHUT_RDWR)
            c.close()
            
        self.api.SetRailDriverConnected(False)
        self.api.SetRailSimConnected(False)
        
    def updatedValues(self):
        updates = dict()
        
        info = self.locoInfo
        if not info: return updates

        self.dataLock.acquire()
        
        for key in info.keys:
            i = info.keys.index(key)
            val = self.api.GetControllerValue(i,0)
            if ((key in self.values) and (self.values[key] == val)):
                continue;
            else:
                updates[key] = val
                self.values[key] = val

        self.dataLock.release()
        return updates
        
    def getLocoInfoUpdate(self):

        # if nothing has changed, and we already have a LocoInfo, return None
        if (not self.api.GetRailSimLocoChanged() and self.locoInfo):
            return None;

        # get loco name               
        locoName = self.api.GetLocoName()
        if not locoName: return None
        
        (producer, product, model) = locoName
        if (not producer or not product or not model): return None

        # get controller list
        cl = self.api.GetControllerList()

        # get min/max values
        minmax = dict();
        for key in cl:
            i = cl.index(key)
            min_val = self.api.GetControllerValue(i, 1)
            max_val = self.api.GetControllerValue(i, 2)
            minmax[key] = (min_val, max_val)

        self.dataLock.acquire()
        self.locoInfo = LocoInfo(producer, product, model, cl, minmax)
        self.values = dict()
        self.updatedValues()
        self.dataLock.release()
        
        return self.locoInfo
    
    def run(self):
        logging.info("Raildriver Server started")
        while self.running:
            
            infoUpdate = self.getLocoInfoUpdate()
            if (infoUpdate):
                logging.debug("got new loco: %s", repr(infoUpdate))
                self.broadcastClients(json.dumps(infoUpdate.__dict__) + "\n")
                
            updates = self.updatedValues();
            if (updates):
                logging.debug("got new values: %s", repr(updates))
                self.broadcastClients(json.dumps(updates) + "\n")
                
            time.sleep(self.sleepTime)
            
        logging.info("Shutting down Raildriver Server")    
        self.disconnect()


class Raildriver:

    def __init__(self,
                 dllPath = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\RailWorks\\plugins\\RailDriver.dll",
                 sleepTime = 1/50,
                 logLevel = logging.INFO,
                 tcpPort = 22222):
        
        logging.basicConfig(level=logging.INFO)
        logging.info("Starting up Raildriver")

        self.server = RaildriverServer(dllPath = dllPath, sleepTime = sleepTime)
        
        self.s = socket.socket()
        host = socket.gethostname()
        self.s.bind((host, tcpPort))
        self.s.listen(5)
        logging.debug("listening on %s on port %d." % (host, tcpPort));

        signal.signal(signal.SIGINT, self.signal_handler)

    def runRaildriver(self):
        self.server.start()

        while True:
            ready = select.select((self.s,), (), (), 0.5)
            if (ready[0]):
                self.server.dataLock.acquire()
                self.server.clientSocketsLock.acquire()

                try: 
                    (c, caddr) = self.s.accept()
                    logging.info("new client connection from %s port %d" % caddr);

                    locoInfo = self.server.locoInfo
                    if (locoInfo): 
                        c.sendall((json.dumps(locoInfo.__dict__) + "\n").encode("utf-8"));
                        c.sendall((json.dumps(self.server.values) + "\n").encode("utf-8"));                
                    self.server.clientSockets.append(c)
                except socket.error as e:
                    logging.error("error while accpeting new client connection: %s",
                                  repr(e))
                
                self.server.clientSocketsLock.release()
                self.server.dataLock.release()

    def signal_handler(self, signal, frame):
        self.s.close()
        self.server.running = False
        self.server.join()
        sys.exit();



class RaildriverAPI:

    def __init__(self, libpath):
        self.rdDll = ctypes.CDLL(libpath)

        self.SetRailSimConnected_c = self.rdDll.SetRailSimConnected
        self.SetRailSimConnected_c.restype = None
        self.SetRailSimConnected_c.argtypes = [ctypes.c_bool]

        self.SetRailDriverConnected_c = self.rdDll.SetRailDriverConnected
        self.SetRailDriverConnected_c.restype = None
        self.SetRailDriverConnected_c.argtypes = [ctypes.c_bool]
        
        self.GetRailSimLocoChanged_c = self.rdDll.GetRailSimLocoChanged
        self.GetRailSimLocoChanged_c.restype = ctypes.c_bool
        self.GetRailSimLocoChanged_c.argtypes = None

        self.GetLocoName_c = self.rdDll.GetLocoName
        self.GetLocoName_c.restype = ctypes.c_char_p
        self.GetLocoName_c.argtypes = None

        self.GetControllerList_c = self.rdDll.GetControllerList
        self.GetControllerList_c.restype = ctypes.c_char_p
        self.GetControllerList_c.argtypes = None

        self.GetControllerValue_c = self.rdDll.GetControllerValue
        self.GetControllerValue_c.restype = ctypes.c_float
        self.GetControllerValue_c.argtypes = [ctypes.c_int, ctypes.c_int]

    def SetRailSimConnected(self, connected):
        """connect or disconnect to the API. Must be called first with True"""
        self.SetRailSimConnected_c(connected)

    def SetRailDriverConnected(self, connected):
        """connect or disconnect to Raildriver."""
        self.SetRailDriverConnected_c(connected)
        
    def GetRailSimLocoChanged(self):
        """returns if Loco has changed since last call"""
        return self.GetRailSimLocoChanged_c()

    def GetLocoName(self):
        """returns a tuple with 3 elements of the loko name [Producer, Product,Loco Name]"""
        resp = self.GetLocoName_c().decode("utf-8")
        if resp: return tuple(resp.split('.:.'))
        else: return None

    def GetControllerList(self):
        """returns a list of all controllers of the current loco"""
        ctls = self.GetControllerList_c().decode("utf-8")
        if ctls: return ctls.split("::")
        else: return []

    def GetControllerValue(self, vid, t):
        """get the next new/changed value, where
           t=0 (value), t=1 (min), t=2 (max)
         """
        return self.GetControllerValue_c(vid, t)
