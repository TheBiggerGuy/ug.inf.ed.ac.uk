import curses
from time import sleep

class Uicli(object):
  
  __screen = None
  
  def __init__(self):
    self.__screen = curses.initscr()
    self.__screen.keypad(1)
    curses.noecho()
    curses.cbreak()
    #curses.wrapper.wrapper(
  
  def refresh(self, lastNum, rand, white):
    self.__screen.clear()
    self.__screen.border(0)
    
    self.__screen.addstr(1, 2, "Guy Taylor (s0700260)")
    self.__screen.addstr(3, 2, "Last random Number")
    n1, n2 = white.getLastBytes()
    self.__screen.addstr(4, 8, "{n1}, {n2} => {sr}".format(n1=n1, n2=n2, sr=lastNum))
    self.__screen.addstr(6, 2, "Averages")
    self.__screen.addstr(7, 8, "Input Stream : #{n:<5}  {per:<15}%  (intended sqew of {sqew})".format(
                          n=rand.getTotal(),
                          per=(rand.genAcutualSqew()*100), sqew=rand.getSqew()*100
                          )
                        )
    self.__screen.addstr(8, 8, "Output Stream: #{n:<5}  {per:<15}%".format(
                          n=white.getTotal(),
                          per=(white.genAcutualSqew()*100)
                          )
                        )
    self.__screen.addstr(10, 2, "Efficency")
    self.__screen.addstr(11, 8, "{per:<15}%".format(per=(white.getTotal()/(rand.getTotal()+0.0))*100))
    self.__screen.refresh()
  
  def __del__(self):
    self.__screen.clear()
    #curses.endwin()

class RandomWithStats(object):
  __zeroCount = 0
  __oneCount  = 0
  _sqew      = 0
  
  def __init__(self, sqew=64):
    self._sqew = sqew
  
  def getBool(self):
    pass
  
  def getTotal(self):
    return self.__zeroCount + self.__oneCount
  
  def getSqew(self):
    return (self._sqew/256.0)
  
  def genAcutualSqew(self):
    return self.__oneCount / (self.__zeroCount + self.__oneCount+0.0)
  
  def _incZero(self):
    self.__zeroCount += 1
  
  def _incOne(self):
    self.__oneCount += 1

class Urandom(RandomWithStats):
  
  _dev = None
  
  def __init__(self, sqew=64):
    RandomWithStats.__init__(self, sqew=sqew)
    self._dev = open("/dev/urandom", mode="r")
  
  def getBool(self):
    n = ord(self._dev.read(1))
    if n > (128 - self._sqew):
      self._incOne()
      return 1
    else:
      self._incZero()
      return 0
  
  def __del__(self):
    if self.__dev != None:
      self.__dev.close()

class Whitening(RandomWithStats):
  
  _rand = None
  _lastBytes = (0, 0)
    
  def __init__(self, rand):
    self._rand = rand
  
  def getBool(self):
    n1 = n2 = 0
    while n1 == n2:
      n1 = rand.getBool()
      n2 = rand.getBool()
    self._lastBytes = n1, n2
    if n1 == 1:
      self._incOne()
      return 1
    else:
      self._incZero()
      return 0
  
  def getLastBytes(self):
    return self._lastBytes

rand  = Urandom()
white = Whitening(rand)
sreen = Uicli()

zeroCount = 0
oneCount = 0
while True:
  byte = white.getBool()
  sreen.refresh(byte, rand, white)
  sleep(0.05)

curses.endwin()
