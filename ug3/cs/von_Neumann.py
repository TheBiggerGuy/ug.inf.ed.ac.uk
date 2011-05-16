import curses
import wrapper
from time import sleep

class Uicli(object):
  
  def __init__(self, screen):
    self.__screen = screen
    self.__screen.nodelay(True)
    self._running = True
  
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
    
    self.__screen.addstr(15, 2, "Q - Quit")
    self.__screen.refresh()
    
    try:
      if self.__screen.getkey() in ["Q", "q"]:
        self._running = False
    except curses.error:
      pass
  
  def isRunning(self):
    return self._running
  
  def __del__(self):
    self.__screen.clear()
    self._running = False

class RandomWithStats(object):
  
  def __init__(self, sqew):
    self._sqew = sqew
    
    self.__zeroCount = 0
    self.__oneCount  = 0
  
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
  
  def __init__(self, rand):
    RandomWithStats.__init__(self, sqew=0)
    self._rand = rand
    self._lastBytes = (0, 0)
  
  def getBool(self):
    n1 = n2 = 0
    while n1 == n2:
      n1 = self._rand.getBool()
      n2 = self._rand.getBool()
    self._lastBytes = n1, n2
    if n1 == 1:
      self._incOne()
      return 1
    else:
      self._incZero()
      return 0
  
  def getLastBytes(self):
    return self._lastBytes

def main(screen):
  rand  = Urandom()
  white = Whitening(rand)
  ui = Uicli(screen)

  zeroCount = 0
  oneCount = 0
  while ui.isRunning():
    byte = white.getBool()
    ui.refresh(byte, rand, white)
    sleep(0.05)

if __name__ == "__main__":
  wrapper.wrapper(main)

