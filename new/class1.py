# from Pmax import *
# from Debug import *
# from Params import *
# from Eprom import *
from ipmp.emu.pmax.SiaPacket import SiaPacket as SiaPacket
from ipmp.emu.pmax.pmaxemulator import Params as Params
from ipmp.emu.pmax.pmaxemulator import Debug as Debug
from ipmp.emu.pmax.pmaxemulator import PictureSender as PictureSender


import socket, threading, time

Debug.level = 2
# CONFIGURATION AREA
Params.host = '94.125.125.197' # IPMP Server IP
Params.media = 'GSM'          # no need to change  
concurancy = 1                # how much panels will simultaniously send events <= 50
start_serial = 0xA00000       # start serial for panel's bunch
pmax_count = 1                # total amount of pmax panels
cycles = 10
ACCOUNT = '777711'          
INDEX = 12                 # Start index for film

zones = [3, 23]               # Zones


def worker(pm, zones, idxbase):
    print 'Running thread for %s' % pm.serial
    
    ps = PictureSender(Params.host, pm.serial)

    for z in zones:
        index = idxbase + zones.index(z)
        pm.ReportCIDEvent('1110 00 %03d' % z, index)
        time.sleep(1) # delay for averting of `pending event` IPMP message

        # V3.5.x ?????????? DEPENDS ON panel protocol version
        z = int(str(z), 16)
        # ===================================================
        if ps.SendMovie(index, z, filmType=0):
            print 'Film index %d from %s sent successfuly (zone=%d)' % (index, pm.serial, z)
        else:
            print 'Film index %d from %s FAILED, (zone=%d)' % (index, pm.serial, z)


class pmax(object):

    def __init__(self, serial, account):
        self._serial = serial
        self.account = account

    @property
    def serial(self):
        return '%06X' % self._serial

    @serial.setter
    def serial(self, value):
        self._serial = value

    def ReportCIDEvent(self, cid_code, index=None, jade=None):
        data = "#" + self.account + "|" + cid_code
        xdata = []
        if not index is None:
            xdata.append('Ix%02X' % index)
        if jade:
            xdata.append('Zx' + jade)


        packet = SiaPacket().Format(id_="ADM-CID",
                                    pref=self.serial,
                                    acct=self.account,
                                    data=data,
                                    xdata=xdata)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((Params.host, Params.port))
        self.sock.send(packet)
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
        except socket.error:
            pass



while cycles > 0:
    INDEX += len(zones)
    print '==== CYCLES LEFT --%d-- =====' % cycles
    pmaxes = []
    pmax_processed = 0
    while pmax_processed < pmax_count:
        for i in range(concurancy):
            if len(pmaxes) >= pmax_count:
                break
            pmaxes.append(threading.Thread(target=worker, args=[pmax(start_serial + i + pmax_processed, ACCOUNT), zones, INDEX]))
            pmaxes[i].start()


        for i in range(len(pmaxes)): 
            pmaxes[i].join()
            pmax_processed += 1

        del pmaxes[:]
            
    cycles -= 1







