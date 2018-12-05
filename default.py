import xbmc, xbmcgui, xbmcaddon

ACTION_NAV_BACK = 92
ACTION_PREVIOUS_MENU = 10
ACTION_NAV_BACK = 92
ACTION_PREVIOUS_MENU = 10
ACTION_DOWN = 4
ACTION_UP = 3
ACTION_LEFT = 1
ACTION_RIGHT = 2


#addon_handle = int(sys.argv[1])
addon = xbmcaddon.Addon()

def logMe(text):
    xbmc.log(text, level=xbmc.LOGNOTICE)
    

class MyMover():
    def __init__(self, currBtn, inc):
        self.currBtn = currBtn
	self.inc = inc
    
    def notifyAction(self, action):
        actionId = action.getId()
	ans = False
	if actionId == ACTION_DOWN:
	    self.currBtn.setPosition(self.currBtn.getX(), self.currBtn.getY()+self.inc)
	    ans = True
	elif actionId == ACTION_UP:
	    self.currBtn.setPosition(self.currBtn.getX(), self.currBtn.getY()-self.inc)
	    ans = True
        elif actionId == ACTION_LEFT:
	    self.currBtn.setPosition(self.currBtn.getX()-self.inc, self.currBtn.getY())
	    ans = True
        elif actionId == ACTION_RIGHT:
	    self.currBtn.setPosition(self.currBtn.getX()+self.inc, self.currBtn.getY())
	    ans = True
        
	if ans == True:
	    logMe("X: " + str(self.currBtn.getX()) + ", Y: " + str(self.currBtn.getY()))

from List import List
class MyWindow(xbmcgui.Window):
    def __init__(self):
	self.show()
	self.setCoordinateResolution(0)
	self.initial_setup()
	
	self.minX = -55
	self.minY = -20
	#640x480
	#self.maxX = 584
	#self.maxY = 700
	#1920x1080
	self.maxX = 1920-self.abs(self.minX)
	self.maxY = 1080-self.abs(self.minY)
        

	refreshList = self.add_button(self.minX, self.minY, 220, 80, 'Refresh List', '0xFF00FFFF', 6, self.refresh_list)	
	downloadSelected = self.add_button(self.minX+self.getWidth()/2, self.minY, 370, 80, 'Download Selected', '0xFF00FFFF', 6, self.stub)
	deselectAll = self.add_button(650, 300, 250, 80, 'Deselect All', '0xFF00FFFF', 6, self.stub)
	changeDestinationFolder = self.add_button(340, 500, 250, 80, 'Change Destination Folder', '0xFF00FFFF', 6, self.stub)
	DEBUG_OTHER = self.add_button(650, 300, 250, 80, 'DEBUG_OTHER', '0xFF00FFFF', 6, self.stub)
	
	#self.add_action_observer(MyMover(refreshList2, 10))
	#-85
	#-10
	myList = List(self, self.minX+self.getWidth()/2, self.minY, 350, 50, '0xFFDC143C', 6, 10)
	for x in range(10):
	    myList.addItem("Bleach Episode " + str(x+1), self.refresh_list)
        self.add_action_observer(myList)
	#myList.setControls(bt1, bt4, bt2, bt3)

	self.setFocus(myList.getHead())

	#loc = addon.getAddonInfo('path') + '/resources/image.png'
        #self.addControl(xbmcgui.ControlImage (0, 0, 400, 400, loc))
    
    def abs(self, val):
        if val < 0:
	    return val*-1
	else:
	    return val

    def initial_setup(self):
	self.buttons = {}
	self.ActionObservers = []
    
    def add_action_observer(self, observer):
        self.ActionObservers.append(observer)

    def onAction(self, action):
        actionId = action.getId()
	if actionId == ACTION_PREVIOUS_MENU or actionId == ACTION_NAV_BACK:
	    self.close()
	else:
	    for ob in self.ActionObservers:
	        ob.notifyAction(action)

	    
    def add_button(self, x, y, xLen, yLen, text, focusedColor, alignment, func):
        actBtn = xbmcgui.ControlButton(x, y, xLen, yLen, text, focusedColor=focusedColor, alignment=alignment)
	self.addControl(actBtn)
	self.buttons[actBtn.getId()] = func
	return actBtn
    
    def stub(self):
        logMe("Something was pressed")

    def refresh_list(self):
	xbmc.log("Refreshing list", level=xbmc.LOGNOTICE)
    
    def downloadSelected(self):
	xbmc.log("Downloading selected", level=xbmc.LOGNOTICE)

    def onControl(self, control):
	self.buttons[control.getId()]()

Win = MyWindow()
Win.doModal()
del Win
#xbmc.executebuiltin("XBMC.Container.Update(path,replace)")
xbmc.executebuiltin("XBMC.ActivateWindow(Home)")
