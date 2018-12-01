import sys
import urllib
import urlparse
import xbmcgui
import xbmcplugin
import xbmcaddon

ACTION_NAV_BACK = 92
ACTION_PREVIOUS_MENU = 10

addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'movies')
addon = xbmcaddon.Addon()

def logMe(text):
    xbmc.log(text, level=xbmc.LOGNOTICE)
    

class MyListItem():
    def __init__(self, button, number):
        self.button = button
	self.number = number

    def getButton(self):
        return self.button

    def getNumber(self):
        return self.number


class MyList():
    def __init__(self, window, x, y, width, height, color, alignment, maxLen, up, down, left, right):
	self.window = window
	self.x = x
	self.y = y
	self.width = width
	self.height = height
	self.color = color
	self.alignment = alignment
	self.maxLen = maxLen
	self.up = up
	self.down = down
	self.left = left
	self.right = right
	self.top     = []
	self.current = []
	self.bottom  = []
	self.count = 0
	self.heightOffset = 0

    def addItem(self, label, func):
	btn = self.window.add_button(self.x, self.y+self.heightOffset, self.width, self.height, label, self.color, self.alignment, func)
        itm = MyListItem(btn, self.count)
	self.count = self.count + 1
	
	if self.maxLen>len(self.current):
	    self.heightOffset = self.heightOffset + self.height/2
	    self.current.append(itm)
	    
	    if self.current==1:
	        if self.up != None:
	            btn.controlUp(self.up)
	        if self.down != None:
	            btn.controlDown(self.down)
	        if self.left != None:
	            btn.controlLeft(self.left)
	        if self.right != None:
	            btn.controlRight(self.right)
	    else:
	        #Get the button above it, and set that button's DOWN to this
	        self.current[itm.getNumber()-1].getButton().controlDown(btn)
	        #Set this new button's up to the previous button
	        btn.controlUp(self.current[itm.getNumber()-1].getButton())
	        if self.down != None:
	            btn.controlDown(self.down)
	        if self.left != None:
	            btn.controlLeft(self.left)
	        if self.right != None:
	            btn.controlRight(self.right)
	else:
	    self.bottom.append(itm)
	    
    def notifyAction(self, action):
        logMe("success!")       

    def getTail(self):
        return self.current[len(self.current)-1].getButton()

    def getHead(self):
        return self.current[0].getButton()

class MyWindow(xbmcgui.WindowDialog):
    def __init__(self):
        self.initial_setup()
	bt1 = self.add_button(340, 500, 220, 80, 'Bt1', '0xFF00FFFF', 6, self.refresh_list)	
	bt2 = self.add_button(340, 600, 220, 80, 'Bt2', '0xFF00FFFF', 6, self.refresh_list)
	bt3 = self.add_button(550, 500, 250, 80, 'Bt3', '0xFF00FFFF', 6, self.refresh_list)
	bt4 = self.add_button(550, 600, 250, 80, 'Bt4', '0xFF00FFFF', 6, self.refresh_list)
	bt5 = self.add_button(700, 500, 250, 80, 'Bt5', '0xFF00FFFF', 6, self.refresh_list)
	bt6 = self.add_button(700, 600, 250, 80, 'Bt6', '0xFF00FFFF', 6, self.refresh_list)
        
	myList = MyList(self, 360, 160, 350, 50, '0xFFDC143C', 6, 3, None, bt1, None, None)
	myList.addItem("Bleach Episode 01", self.refresh_list)
	myList.addItem("Bleach Episode 02", self.refresh_list)
	myList.addItem("Bleach Episode 03", self.refresh_list)
	myList.addItem("Bleach Episode 04", self.refresh_list)
	myList.addItem("Bleach Episode 05", self.refresh_list)
        self.add_action_observer(myList)

	bt1.setNavigation(myList.getTail(), bt2, bt1, bt3)
        bt2.setNavigation(bt1, bt2, bt2, bt4)
	bt3.setNavigation(bt3, bt4, bt1, bt5)
	bt4.setNavigation(bt3, bt4, bt2, bt6)
	bt5.setNavigation(bt5, bt6, bt3, bt5)
	bt6.setNavigation(bt5, bt6, bt4, bt6)
	self.setFocus(bt1)

		
	loc = addon.getAddonInfo('path') + '/resources/image.png'
        #self.addControl(xbmcgui.ControlImage (400, 200, 400, 400, loc))
    
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
