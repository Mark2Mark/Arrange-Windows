# encoding: utf-8

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
#	- Run with Option Key to include the MacroPanel
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


from GlyphsApp.plugins import *
from AppKit import NSScreen
import traceback

Version = "1.0"

class ArrangeWindows(GeneralPlugin):
	def settings(self):
		self.name = Glyphs.localize({'en': u'Arrange Windows', 'de': u'Arrange Windows'})
		self.nameAlt = Glyphs.localize({'en': u'Arrange Windows & Macro Panel', 'de': u'Arrange Windows & Macro Panel'})
	
	def start(self):
		try: 
			# new API in Glyphs 2.3.1-910
			targetMenu = WINDOW_MENU # EDIT_MENU # SCRIPT_MENU

			## Without the separator, it overwrites the `Kerning` menu entry, if put in WINDOW_MENU
			separator = NSMenuItem.separatorItem()
			Glyphs.menu[targetMenu].append(separator)

			newMenuItem = NSMenuItem(self.name, self.doArrangeWindows)

			newMenuItemAlt = NSMenuItem(self.nameAlt, self.doArrangeWindows)
			newMenuItemAlt.setKeyEquivalentModifierMask_(NSAlternateKeyMask)
			newMenuItemAlt.setAlternate_(True) # A Boolean value that marks the menu item as an alternate to the previous menu item.
			
			Glyphs.menu[targetMenu].append(newMenuItem)
			Glyphs.menu[targetMenu].append(newMenuItemAlt)
			

		except:
			print traceback.format_exc()
			# mainMenu = Glyphs.mainMenu()
			# s = objc.selector(self.doArrangeWindows,signature='v@:@')
			# newMenuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(self.name, s, "")
			# newMenuItem.setTarget_(self)
			# mainMenu.itemWithTag_(5).submenu().addItem_(newMenuItem)



	
	def doArrangeWindows(self, sender):

		screenHeight = NSScreen.mainScreen().frame().size.height
		screenWidth = NSScreen.mainScreen().frame().size.width

		optionKeyFlag = 524288
		optionKeyPressed = NSEvent.modifierFlags() & optionKeyFlag == optionKeyFlag

		includeMacroPanel = False
		if optionKeyPressed:
			includeMacroPanel = True

		if includeMacroPanel:
			allWindows = [x for x in Glyphs.windows() if x.class__().__name__ == "GSWindow" and x.document() or x.class__().__name__ == "GSMacroWindow"]
			Glyphs.showMacroWindow()
		else:
		 	allWindows = [x for x in Glyphs.windows() if x.class__().__name__ == "GSWindow" and x.document()]
		 	macroWindow = [x for x in Glyphs.windows() if x.class__().__name__ == "GSMacroWindow"][0]
		 	macroWindow.close()

		### just for debugging:
		# for x in Glyphs.windows():
		# 	className = x.class__().__name__
		# 	if className == "GSWindow":
		# 		print x.document()
		# 		help(x)
		#######################

		amount = len(allWindows)
		for i, x in enumerate(allWindows):
			share = screenWidth / amount-1
			point = screenWidth / amount*(i)
			x.setFrame_display_animate_(((point, 0), (share, screenHeight)), True, True) #x.setFrameOrigin_((point, 0))

	
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
	