import xbmc, xbmcgui, xbmcaddon

ACTION_NAV_BACK = 92
ACTION_PREVIOUS_MENU = 10

#addon_handle = int(sys.argv[1])
addon = xbmcaddon.Addon()

def logMe(text):
    xbmc.log(text, level=xbmc.LOGNOTICE)
    
from List import List
class MyWindow(xbmcgui.Window):
    def __init__(self):
	self.show()
	self.initial_setup()
	bt1 = self.add_button(340, 200, 220, 80, 'Bt1', '0xFF00FFFF', 6, self.refresh_list)	
	bt2 = self.add_button(100, 300, 220, 80, 'Bt2', '0xFF00FFFF', 6, self.refresh_list)
	bt3 = self.add_button(650, 300, 250, 80, 'Bt3', '0xFF00FFFF', 6, self.refresh_list)
	bt4 = self.add_button(340, 500, 250, 80, 'Bt4', '0xFF00FFFF', 6, self.refresh_list)
        
	myList = List(self, 360, 300, 350, 50, '0xFFDC143C', 6, 10)
	for x in range(10):
	    myList.addItem("Bleach Episode " + str(x+1), self.refresh_list)
        self.add_action_observer(myList)
	myList.setControls(bt1, bt4, bt2, bt3)
        
	self.setFocus(myList.getHead())

	#loc = addon.getAddonInfo('path') + '/resources/image.png'
        #self.addControl(xbmcgui.ControlImage (0, 0, 400, 400, loc))
    
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
   
    def refresh_list(self):
	xbmc.log("Refreshing list", level=xbmc.LOGNOTICE)
    
    def copy_selected(self):
	xbmc.log("Copying selected", level=xbmc.LOGNOTICE)

    def onControl(self, control):
	self.buttons[control.getId()]()

Win = MyWindow()
Win.doModal()
del Win
xbmc.executebuiltin("XBMC.Container.Update(path,replace)")
xbmc.executebuiltin("XBMC.ActivateWindow(Home)")
