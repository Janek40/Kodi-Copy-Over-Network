import sys
import urllib
import urlparse
import xbmcgui
import xbmcplugin
import xbmcaddon

ACTION_NAV_BACK = 92
ACTION_PREVIOUS_MENU = 10
ACTION_DOWN = 4
ACTION_UP = 3

addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'movies')
addon = xbmcaddon.Addon()

def logMe(text):
    xbmc.log(text, level=xbmc.LOGNOTICE)
    

class MyList():
    def __init__(self, window, x, y, width, height, color, alignment, maxLen):
	self.window = window
	self.x = x
	self.y = y
	self.width = width
	self.height = height
	self.color = color
	self.alignment = alignment
	self.maxLen = maxLen
	self.top     = []
	self.current = []
	self.bottom  = []
	self.heightOffset = 0
	self.heightOffsetPos = 0
	self.SCROLL_DOWN = False
	self.SCROLL_UP = False

	self.heightOffsets = []
	for x in range(maxLen):
	    self.heightOffsets.append(self.heightOffset)
            self.heightOffset = self.heightOffset + self.height/2

    def setControls(self, up, down, left, right):
        self.up = up
	self.down = down
	self.left = left
	self.right = right
	if left != None and right != None:
	    for x in self.top:
	        x.controlLeft(left)
		x.controlRight(right)
	    for x in self.current:
	        x.controlLeft(left)
		x.controlRight(right)
            for x in self.bottom:
	        x.controlLeft(left)
		x.controlRight(right)

	elif left != None:
	    for x in self.top:
	        x.controlLeft(left)
	    for x in self.current:
	        x.controlLeft(left)
            for x in self.bottom:
	        x.controlLeft(left)

        elif right != None:
            for x in self.top:
	        x.controlLeft(right)
            for x in self.current:
	        x.controlLeft(right)
            for x in self.bottom:
	        x.controlLeft(right)

	if up != None:
	    self.current[0].controlUp(up)
	
	if down != None:
	    if len(self.bottom)>0:
		bott = self.bottom[len(self.bottom)-1]
	        self.down.controlUp(bott)
            else:
	        bott = self.current[len(self.current)-1]
		down.controlUp(bott)

    def addItem(self, label, func):
	if self.maxLen>len(self.current):
	    if self.heightOffsetPos==self.maxLen:
	        self.heightOffsetPos = 0

	    btn = self.window.add_button(self.x, self.y+self.heightOffsets[self.heightOffsetPos], self.width, self.height, label, self.color, self.alignment, func)
	    self.heightOffsetPos = self.heightOffsetPos + 1

	    self.current.append(btn)
	    
	    if len(self.current)>1:
		self.current[len(self.current)-2].controlDown(btn)
	        btn.controlUp(self.current[len(self.current)-2])
	else:
	    btn = self.window.add_button(self.x, self.y+self.heightOffsets[self.maxLen-1], self.width, self.height, label, self.color, self.alignment, func)

	    self.bottom.append(btn)
	    btn.setVisible(False)
	    
    def notifyAction(self, action):
	actionId = action.getId()
        if actionId == ACTION_DOWN:
	    self.SCROLL_UP = False
	    if self.SCROLL_DOWN == True:
	        self.moveUp()
	    else:
	        itemId = self.window.getFocusId()
	        #If the focused item is the last in the list, then the next down press needs to scroll the list!
	        if itemId == self.current[len(self.current)-1].getId():
	            self.SCROLL_DOWN = True
        elif actionId == ACTION_UP:
	    self.SCROLL_DOWN = False
	    if self.SCROLL_UP == True:
	        self.moveDown()
	    else:
	        itemId = self.window.getFocusId()
		if itemId == self.current[0].getId():
		    self.SCROLL_UP = True

    def moveUp(self):
	if len(self.bottom)>0:
	    #hide the top item
	    topItem = self.current[0]
	    topItem.setVisible(False)
	    self.top.append(topItem)
	    del self.current[0]
	    #move up
	    for curr in self.current:
	        currY = curr.getY()
		newY = currY-self.height/2
		curr.setPosition(curr.getX(), newY)
	    #show the item in the bottom list
	    newBottom = self.bottom[0]
	    newBottom.setVisible(True)
	    self.window.setFocus(newBottom)
	    oldBottom = self.current[len(self.current)-1]
	    newBottom.controlUp(oldBottom)
	    oldBottom.controlDown(newBottom)
	    self.current.append(newBottom)
	    del self.bottom[0]
	else:
	    if self.down != None:
	        self.window.setFocus(self.down)
	    
    
    def moveDown(self):
        if len(self.top)>0:
	    #Move and hide the bottom item
	    bottomItem = self.current[len(self.current)-1]
	    bottomItem.controlDown(bottomItem)
	    bottomItem.setVisible(False)
	    self.bottom.insert(0, bottomItem)
	    del self.current[len(self.current)-1]
	    #Move down
	    for curr in self.current:
	        currY = curr.getY()
		newY = currY+self.height/2
		curr.setPosition(curr.getX(), newY)
	    
	    #Show and add the new top item
	    newTop = self.top[len(self.top)-1]
	    newTop.setVisible(True)
	    self.window.setFocus(newTop)
	    self.current.insert(0, newTop)
	    del self.top[len(self.top)-1]
	else:
	    if self.up != None:
	        self.window.setFocus(self.up)

    def getTail(self):
        return self.current[len(self.current)-1]

    def getHead(self):
        return self.current[0]

class MyWindow(xbmcgui.WindowDialog):
    def __init__(self):
        self.initial_setup()
	bt1 = self.add_button(340, 500, 220, 80, 'Bt1', '0xFF00FFFF', 6, self.refresh_list)	
	bt2 = self.add_button(340, 600, 220, 80, 'Bt2', '0xFF00FFFF', 6, self.refresh_list)
	bt3 = self.add_button(550, 500, 250, 80, 'Bt3', '0xFF00FFFF', 6, self.refresh_list)
	bt4 = self.add_button(550, 600, 250, 80, 'Bt4', '0xFF00FFFF', 6, self.refresh_list)
	bt5 = self.add_button(700, 500, 250, 80, 'Bt5', '0xFF00FFFF', 6, self.refresh_list)
	bt6 = self.add_button(700, 600, 250, 80, 'Bt6', '0xFF00FFFF', 6, self.refresh_list)
        
	myList = MyList(self, 360, 160, 350, 50, '0xFFDC143C', 6, 3)
	for x in range(4):
	    myList.addItem("Bleach Episode " + str(x+1), self.refresh_list)
        self.add_action_observer(myList)
	myList.setControls(None, bt1, None, None)
        
	self.setFocus(myList.getHead())

	#bt1.setNavigation(myList.getTail(), bt2, bt1, bt3)
        bt2.setNavigation(bt1, bt2, bt2, bt4)
	bt3.setNavigation(bt3, bt4, bt1, bt5)
	bt4.setNavigation(bt3, bt4, bt2, bt6)
	bt5.setNavigation(bt5, bt6, bt3, bt5)
	bt6.setNavigation(bt5, bt6, bt4, bt6)
	#self.setFocus(bt1)

		
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
