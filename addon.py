import sys
import urllib
import urlparse
import xbmcgui
import xbmcplugin
import xbmcaddon


addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'movies')
addon = xbmcaddon.Addon()

ACTION_CLOSE  = 10
ACTION_UP     = 3
ACTION_DOWN   = 4
ACTION_LEFT   = 1
ACTION_RIGHT  = 2
ACTION_SELECT = 7

POS_LEFT   = 1
POS_MIDDLE = 2
POS_RIGHT  = 3



class ButtonObj():
    def __init__(self, btn, func):
       self.btn = btn
       self.func = func
       self.column = column

    def getButton(self):
        return self.btn

    def getFunction(self):
        return self.func


class MyWindow(xbmcgui.WindowDialog):
    def __init__(self):
	self.setup_initial()
	self.add_button(340, 500, 220, 80, 'Refresh list', '0xFF00FFFF', 6, self.refresh_list).setEnabled(True)
	self.add_button(340, 600, 220, 80, 'Refresh list', '0xFF00FFFF', 6, self.refresh_list)
	self.add_button(550, 500, 250, 80, 'Copy selected', '0xFF00FFFF', 6, self.copy_selected)
	self.add_button(550, 600, 250, 80, 'Copy selected', '0xFF00FFFF', 6, self.copy_selected)
	self.add_button(700, 500, 250, 80, 'Ignore me', '0xFF00FFFF', 6, self.copy_selected)
	self.add_button(700, 600, 250, 80, 'Ignore me', '0xFF00FFFF', 6, self.copy_selected)
	#self.buttons[0].getButton().setEnabled(True)

	myList = xbmcgui.ControlList(360, 160, 300, 200)
	self.addControl(myList)
	myList.addItem("Bleach Episode 01")
        myList.addItem("Bleach Episode 02")
        myList.addItem("Bleach Episode 03")
        myList.addItem("Bleach Episode 04")
        myList.addItem("Bleach Episode 05")
        myList.addItem("Bleach Episode 06")
        myList.addItem("Bleach Episode 07")
	
	xbmc.log("Length: " + str(myList.size()), level=xbmc.LOGNOTICE)
	
	loc = addon.getAddonInfo('path') + '/resources/image.png'
        #self.addControl(xbmcgui.ControlImage (400, 200, 400, 400, loc))
    

    def add_button(self, x, y, xLen, yLen, text, focusedColor, alignment, myFunc):
        btn = ButtonObj(xbmcgui.ControlButton(x, y, xLen, yLen, text, focusedColor=focusedColor, alignment=alignment), myFunc)
	#self.buttons.append(btn)
	self.numButtons = self.numButtons + 1
	self.addControl(btn.getButton())
	btn.getButton().setEnabled(False)
	return btn.getButton()

   
    def press_button(self):
        btn = self.buttons[self.buttonPosition]
        func = btn.getFunction()
	func()

    def stub(self):
	xbmc.log("Stub", level=xbmc.LOGNOTICE)
    
    def refresh_list(self):
	xbmc.log("Refreshing list", level=xbmc.LOGNOTICE)
    
    def copy_selected(self):
	xbmc.log("Copying selected", level=xbmc.LOGNOTICE)

    def onAction(self, action):
        action_id = action.getId()
        xbmc.log(str(action_id), level=xbmc.LOGNOTICE)
	if action_id==ACTION_CLOSE:
	    self.close()
	elif action_id==ACTION_DOWN:
	    self.request_down()
	elif action_id==ACTION_UP:
            self.request_up()
	elif action_id==ACTION_SELECT:
	    self.press_button()

Win = MyWindow()
Win.doModal()
del Win
