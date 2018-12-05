import xbmc, xbmcgui, xbmcaddon

ACTION_NAV_BACK = 92
ACTION_PREVIOUS_MENU = 10
ACTION_DOWN = 4
ACTION_UP = 3
ACTION_LEFT = 1
ACTION_RIGHT = 2

def logMe(text):
    xbmc.log(text, level=xbmc.LOGNOTICE)
    

class List():
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
	self.up = None
	self.down = None
	self.left = None
	self.right = None

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
	    self.left.controlRight(self.current[0])
	    self.right.controlLeft(self.current[0])

	elif left != None:
	    for x in self.top:
	        x.controlLeft(left)
	    for x in self.current:
	        x.controlLeft(left)
            for x in self.bottom:
	        x.controlLeft(left)
	    self.left.controlRight(self.current[0])

        elif right != None:
            for x in self.top:
	        x.controlLeft(right)
            for x in self.current:
	        x.controlLeft(right)
            for x in self.bottom:
	        x.controlLeft(right)
	    self.right.controlLeft(self.current[0])
	
	if up != None:
	    self.up.controlDown(self.current[0])
	
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
		idx = len(self.current)-2
		self.current[idx].controlDown(btn)
	        btn.controlUp(self.current[idx])

	else:
	    btn = self.window.add_button(self.x, self.y+self.heightOffsets[self.maxLen-1], self.width, self.height, label, self.color, self.alignment, func)
	    btn.setVisible(False)
	    self.bottom.append(btn)
	    if len(self.bottom)>1:
	        idx = len(self.bottom)-2
		self.bottom[idx].controlDown(btn)
		btn.controlUp(self.bottom[idx])
            else:
	        self.current[len(self.current)-1].controlDown(btn)
		btn.controlUp(self.current[len(self.current)-1])

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
	elif actionId == ACTION_LEFT or actionId == ACTION_RIGHT:
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
	        currY = curr.getY()-self.height/2
		curr.setPosition(curr.getX(), currY)
	    #Set the left thing
	    if self.left != None:
	        self.left.controlRight(self.current[0])
	    if self.right != None:
	        self.right.controlLeft(self.current[0])
	    #show the item in the bottom list
	    newBottom = self.bottom[0]
	    newBottom.setVisible(True)
	    self.window.setFocus(newBottom)
	    self.current.append(newBottom)
	    del self.bottom[0]
	else:
	    if self.down != None:
	        self.window.setFocus(self.down)
	    
    
    def moveDown(self):
        if len(self.top)>0:
	    idxCurr = len(self.current)-1
	    idxTopp = len(self.top)-1
	    #Move and hide the bottom item
	    bottomItem = self.current[idxCurr]
	    bottomItem.setVisible(False)
	    self.bottom.insert(0, bottomItem)
	    del self.current[idxCurr]
	    #Move down
	    for curr in self.current:
	        currY = curr.getY()+self.height/2
		curr.setPosition(curr.getX(), currY)
	    
	    #Show and add the new top item
	    newTop = self.top[idxTopp]
	    newTop.setVisible(True)
	    self.window.setFocus(newTop)
	    self.current.insert(0, newTop)
	    del self.top[idxTopp]
	    if self.left != None:
	        self.left.controlRight(self.current[0])
	    if self.right != None:
	        self.right.controlLeft(self.current[0])
	else:
	    if self.up != None:
	        self.window.setFocus(self.up)

    def getTail(self):
        return self.current[len(self.current)-1]

    def getHead(self):
        return self.current[0]