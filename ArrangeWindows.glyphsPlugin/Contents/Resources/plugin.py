# encoding: utf-8

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
# - Run with Option Key to include the MacroPanel.
# - Run with Shift Key to Arrange 2 Fonts to 2 Screens.
#
#
# --> let me know if you have ideas for improving
# --> Mark Froemberg aka Mark2Mark @ GitHub
# --> www.markfromberg.com
#
# ToDo:
#	- Tiles for 3 or 4 fonts
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from GlyphsApp import *
from GlyphsApp.plugins import *
from AppKit import NSScreen, NSAnimationEaseIn, NSViewAnimationEndFrameKey
import traceback



# class MFWindow(NSWindow):
# 	def init(self):
# 		return self
# 	def animationResizeTime_(self, rect):
# 		return 0.2

screens = NSScreen.screens()
screenCount = len(screens)

specialWindowName = "Skedge 1.2"

class ArrangeWindows(GeneralPlugin):
	def settings(self):
		self.name = Glyphs.localize({'en': u'Arrange Windows', 'de': u'Verteile Fenster', 'ko': u'창 정렬'})
		self.nameAlt = Glyphs.localize({'en': u'Arrange Windows & Macro Panel', 'de': u'Verteile Fenster & Macro Panel'})
		self.nameAltScreens = Glyphs.localize({'en': u'Arrange Windows on Screens', 'de': u'Verteile Fenster auf Monitore'})
	
	def start(self):
		try: 
			# new API in Glyphs 2.3.1-910
			targetMenu = WINDOW_MENU # EDIT_MENU # SCRIPT_MENU

			## Without the separator, it overwrites the `Kerning` menu entry, if put in WINDOW_MENU
			separator = NSMenuItem.separatorItem()
			Glyphs.menu[targetMenu].append(separator)

			newMenuItem = NSMenuItem(self.name, self.doArrangeWindows)

			# Alt 1
			newMenuItemAlt = NSMenuItem(self.nameAlt, self.doArrangeWindows)
			newMenuItemAlt.setKeyEquivalentModifierMask_(NSAlternateKeyMask)
			newMenuItemAlt.setAlternate_(True) # A Boolean value that marks the menu item as an alternate to the previous menu item.

			# Alt 2
			if screenCount == 2:
				newMenuItemAltScreens = NSMenuItem(self.nameAltScreens, self.doArrangeWindowsOnScreens)
				newMenuItemAltScreens.setKeyEquivalentModifierMask_(NSShiftKeyMask)
				newMenuItemAltScreens.setAlternate_(True) # A Boolean value that marks the menu item as an alternate to the previous menu item.			
			
			Glyphs.menu[targetMenu].append(newMenuItem)
			Glyphs.menu[targetMenu].append(newMenuItemAlt)
			if screenCount == 2:
				Glyphs.menu[targetMenu].append(newMenuItemAltScreens)
			

		except:
			print traceback.format_exc()
			# mainMenu = Glyphs.mainMenu()
			# s = objc.selector(self.doArrangeWindows,signature='v@:@')
			# newMenuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(self.name, s, "")
			# newMenuItem.setTarget_(self)
			# mainMenu.itemWithTag_(5).submenu().addItem_(newMenuItem)


	def distribute(self, allWindows, screenWidth, screenHeight):
		amount = len(allWindows)
		for i, window in enumerate(allWindows):
			
			# Optional: deminiaturize:
			# if window.isMiniaturized():
			# 	window.deminiaturize_(True)

			share = screenWidth / amount-1
			point = screenWidth / amount*(i)
			
			newRect = ((point, 0), (share, screenHeight))

			# window = MFWindow.alloc().init() ## Subclass, dont do that!
			#window.animationResizeTime_( newRect )
			window.setFrame_display_animate_(newRect, True, True) #window.setFrameOrigin_((point, 0))
			# window.animator().setAlphaValue_(0.0)




			

	
	def doArrangeWindows(self, sender):

		screenHeight = NSScreen.mainScreen().frame().size.height
		screenWidth = NSScreen.mainScreen().frame().size.width

		optionKeyFlag = 524288
		optionKeyPressed = NSEvent.modifierFlags() & optionKeyFlag == optionKeyFlag

		includeMacroPanel = False
		if optionKeyPressed:
			includeMacroPanel = True

		if includeMacroPanel:
			#allWindows = [x for x in Glyphs.windows() if x.class__().__name__ == "GSWindow" and x.document() or x.class__().__name__ == "GSMacroWindow"] # A: Without special window
			allWindows = [x for x in Glyphs.windows() if x.class__().__name__ == "GSWindow" and x.document() or x.class__().__name__ == "GSMacroWindow" or specialWindowName in x.title() ] # B: With special window
			Glyphs.showMacroWindow()
		else:
			#allWindows = [x for x in Glyphs.windows() if x.class__().__name__ == "GSWindow" and x.document()] # A: Without special window
			allWindows = [x for x in Glyphs.windows() if x.class__().__name__ == "GSWindow" and x.document() or specialWindowName in x.title() ] # B: With special window
			macroWindow = [x for x in Glyphs.windows() if x.class__().__name__ == "GSMacroWindow"][0]
			macroWindow.close()
			
		self.distribute(allWindows, screenWidth, screenHeight)

		### just for debugging:
		# for x in Glyphs.windows():
		# 	className = x.class__().__name__
		# 	if className == "GSWindow":
		# 		print x.document()
		# 		help(x)
		#######################



	def doArrangeWindowsOnScreens(self, sender):
		allWindows = [x for x in Glyphs.windows() if x.class__().__name__ == "GSWindow" and x.document()]
		macroWindow = [x for x in Glyphs.windows() if x.class__().__name__ == "GSMacroWindow"][0]

		if screenCount == len(allWindows) == 2: # only limited to exactly 2
			macroWindow.close()

			w1, w2 = allWindows[0], allWindows[1]
			s1, s2 = screens[0].frame(), screens[1].frame()
			
			s1Rect = ((s1.origin.x, s1.origin.x), (s1.size.width, s1.size.height))
			w1.setFrame_display_animate_(s1Rect, True, True)

			s2Rect = ((s2.origin.x, s2.origin.x), (s2.size.width, s2.size.height))
			w2.setFrame_display_animate_(s2Rect, True, True)
		else:
			Message("You need exactly 2 fonts to be open.", "", OKButton="OK")

	
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
	
