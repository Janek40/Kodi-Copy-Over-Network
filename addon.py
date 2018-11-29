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



class MyWindow(xbmcgui.WindowDialog):
    def __init__(self):
	bt1 = self.add_button(340, 500, 220, 80, 'Bt1', '0xFF00FFFF', 6)	
	bt2 = self.add_button(340, 600, 220, 80, 'Bt2', '0xFF00FFFF', 6)
	bt3 = self.add_button(550, 500, 250, 80, 'Bt3', '0xFF00FFFF', 6)
	bt4 = self.add_button(550, 600, 250, 80, 'Bt4', '0xFF00FFFF', 6)
	bt5 = self.add_button(700, 500, 250, 80, 'Bt5', '0xFF00FFFF', 6)
	bt6 = self.add_button(700, 600, 250, 80, 'Bt6', '0xFF00FFFF', 6)
        
	bt1.setNavigation(bt1, bt2, bt1, bt3)
        bt2.setNavigation(bt1, bt2, bt2, bt4)
	bt3.setNavigation(bt3, bt4, bt1, bt5)
	bt4.setNavigation(bt3, bt4, bt2, bt6)
	bt5.setNavigation(bt5, bt6, bt3, bt5)
	bt6.setNavigation(bt5, bt6, bt4, bt6)
	self.setFocus(bt1)

        self.BT1 = bt1.getId()
	self.BT2 = bt2.getId()
	self.BT3 = bt3.getId()
	self.BT4 = bt4.getId()
	self.BT5 = bt5.getId()
	self.BT6 = bt6.getId()

	myList = xbmcgui.ControlList(360, 160, 300, 200)
	self.addControl(myList)
	myList.addItem("Bleach Episode 01")
        myList.addItem("Bleach Episode 02")
        myList.addItem("Bleach Episode 03")
        myList.addItem("Bleach Episode 04")
        myList.addItem("Bleach Episode 05")
        myList.addItem("Bleach Episode 06")
        myList.addItem("Bleach Episode 07")
	
	
	loc = addon.getAddonInfo('path') + '/resources/image.png'
        #self.addControl(xbmcgui.ControlImage (400, 200, 400, 400, loc))
    
    def add_button(self, x, y, xLen, yLen, text, focusedColor, alignment):
        actBtn = xbmcgui.ControlButton(x, y, xLen, yLen, text, focusedColor=focusedColor, alignment=alignment)
	self.addControl(actBtn)
	return actBtn
   
    def logMe(self, text):
	xbmc.log(text, level=xbmc.LOGNOTICE)
    
    def refresh_list(self):
	xbmc.log("Refreshing list", level=xbmc.LOGNOTICE)
    
    def copy_selected(self):
	xbmc.log("Copying selected", level=xbmc.LOGNOTICE)

    def onControl(self, control):
        buttonCode = int(control.getId())
	
	if buttonCode==self.BT1:
	    self.logMe("Bt1 pressed")
        elif buttonCode==self.BT2:
	    self.logMe("Bt2 pressed")
        elif buttonCode==self.BT3:
	    self.logMe("Bt3 pressed")
        elif buttonCode==self.BT4:
	    self.logMe("Bt4 pressed")
        elif buttonCode==self.BT5:
	    self.logMe("Bt5 pressed")
        elif buttonCode==self.BT6:
	    self.logMe("Bt6 pressed")

Win = MyWindow()
Win.doModal()
del Win
