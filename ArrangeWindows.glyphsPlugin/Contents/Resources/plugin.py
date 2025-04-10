# encoding: utf-8
from __future__ import division, print_function, unicode_literals

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# - Run with Option Key to include the MacroPanel.
# - Run with Shift Key to Arrange 2 Fonts to 2 Screens.
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


import objc
from GlyphsApp import Glyphs, Message, WINDOW_MENU, NSMenuItem
from GlyphsApp.plugins import GeneralPlugin
from AppKit import NSScreen, NSEvent, NSAlternateKeyMask, NSShiftKeyMask
import traceback

# class MFWindow(NSWindow):
# 	def init(self):
# 		return self
# 	def animationResizeTime_(self, rect):
# 		return 0.2

screens = NSScreen.screens()
screenCount = len(screens)
specialWindowName = "Skedge"


class ArrangeWindows(GeneralPlugin):

	@objc.python_method
	def settings(self):
		self.name = Glyphs.localize({
			'en': 'Arrange Windows',
			'de': 'Fenster anordnen',
			'fr': 'Organiser les fenêtres',
			'es': 'Organizar ventanas',
		})
		self.nameAlt = Glyphs.localize({
			'en': 'Arrange Windows & Macro Panel',
			'de': 'Fenster & Macro Panel anordnen',
			'fr': 'Organiser les fenêtres et le panneau des macros',
			'es': 'Organizar ventanas y el panel de macros',
		})
		self.nameAltScreens = Glyphs.localize({
			'en': 'Arrange Windows Across Screens',
			'de': 'Verteile Fenster auf Monitore',
			'fr': 'Organiser les fenêtres à travers les écrans',
			'es': 'Organizar ventanas en pantallas',
		})

	@objc.python_method
	def start(self):
		try:
			# new API in Glyphs 2.3.1-910
			targetMenu = WINDOW_MENU  # EDIT_MENU # SCRIPT_MENU

			## Without the separator, it overwrites the `Kerning` menu entry, if put in WINDOW_MENU
			separator = NSMenuItem.separatorItem()
			Glyphs.menu[targetMenu].append(separator)
			if Glyphs.buildNumber >= 3320:
				from GlyphsApp.UI import MenuItem
				newMenuItem = MenuItem(self.name, action=self.doArrangeWindows_, target=self)
				newMenuItemAlt = MenuItem(self.nameAlt, action=self.doArrangeWindows_, target=self)
			else:
				newMenuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(self.name, self.doArrangeWindows_, "")
				newMenuItem.setTarget_(self)
				newMenuItemAlt = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(self.nameAlt, self.doArrangeWindows_, "")
				newMenuItemAlt.setTarget_(self)

			newMenuItemAlt.setKeyEquivalentModifierMask_(NSAlternateKeyMask)
			newMenuItemAlt.setAlternate_(True)  # A Boolean value that marks the menu item as an alternate to the previous menu item.

			Glyphs.menu[targetMenu].append(newMenuItem)
			Glyphs.menu[targetMenu].append(newMenuItemAlt)

			# Alt 2
			if screenCount == 2:
				if Glyphs.buildNumber >= 3320:
					newMenuItemAltScreens = MenuItem(self.nameAltScreens, action=self.doArrangeWindowsOnScreens_, target=self)
				else:
					newMenuItemAltScreens = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(self.nameAltScreens, self.doArrangeWindowsOnScreens_, "")
					newMenuItemAltScreens.setTarget_(self)

				newMenuItemAltScreens.setKeyEquivalentModifierMask_(NSShiftKeyMask)
				newMenuItemAltScreens.setAlternate_(True)  # A Boolean value that marks the menu item as an alternate to the previous menu item.

				Glyphs.menu[targetMenu].append(newMenuItemAltScreens)

		except:
			print(traceback.format_exc())

	@objc.python_method
	def distribute(self, allWindows, screenWidth, screenHeight):
		amount = len(allWindows)
		for i, window in enumerate(allWindows):

			# Optional: deminiaturize:
			# if window.isMiniaturized():
			# 	window.deminiaturize_(True)

			share = screenWidth / amount - 1
			point = screenWidth / amount * i
			newRect = ((point, 0), (share, screenHeight))

			# window = MFWindow.alloc().init() ## Subclass, dont do that!
			# window.animationResizeTime_(newRect)
			window.setFrame_display_animate_(newRect, True, True)  # window.setFrameOrigin_((point, 0))
			# window.animator().setAlphaValue_(0.0)

	def doArrangeWindows_(self, sender):
		screenHeight = NSScreen.mainScreen().frame().size.height
		screenWidth = NSScreen.mainScreen().frame().size.width

		optionKeyFlag = 524288
		optionKeyPressed = NSEvent.modifierFlags() & optionKeyFlag == optionKeyFlag

		includeMacroPanel = False
		if optionKeyPressed:
			includeMacroPanel = True

		if includeMacroPanel:
			# allWindows = [x for x in Glyphs.windows() if x.class__().__name__ == "GSWindow" and x.document() or x.class__().__name__ == "GSMacroWindow"]  # A: Without special window
			allWindows = [x for x in Glyphs.windows() if x.class__().__name__ == "GSWindow" and x.document() or x.class__().__name__ == "GSMacroWindow" or specialWindowName in x.title()]  # B: With special window
			Glyphs.showMacroWindow()
		else:
			# allWindows = [x for x in Glyphs.windows() if x.class__().__name__ == "GSWindow" and x.document()]  # A: Without special window
			allWindows = [x for x in Glyphs.windows() if x.class__().__name__ == "GSWindow" and x.document() or specialWindowName in x.title()]  # B: With special window
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

	def doArrangeWindowsOnScreens_(self, sender):
		allWindows = [x for x in Glyphs.windows() if x.class__().__name__ == "GSWindow" and x.document()]
		macroWindow = [x for x in Glyphs.windows() if x.class__().__name__ == "GSMacroWindow"][0]

		if screenCount == len(allWindows) == 2:  # only limited to exactly 2
			macroWindow.close()

			w1, w2 = allWindows[0], allWindows[1]
			s1, s2 = screens[0].frame(), screens[1].frame()

			s1Rect = ((s1.origin.x, s1.origin.x), (s1.size.width, s1.size.height))
			w1.setFrame_display_animate_(s1Rect, True, True)

			s2Rect = ((s2.origin.x, s2.origin.x), (s2.size.width, s2.size.height))
			w2.setFrame_display_animate_(s2Rect, True, True)
		else:
			Message(
				title=Glyphs.localize({
					'en': "Wrong Number of Fonts",
					'de': 'Falsche Anzahl Schriften',
					'fr': 'Nombre des polices incorrecte',
					'es': 'Numero de fuentes incorrecto',
				}),
				message=Glyphs.localize({
					'en': "You need exactly two fonts to be open.",
					'de': 'Es müssen genau zwei Schriftdateien geöffnet sein.',
					'fr': 'Il faut que exactement deux fichiers .glyphs sont ouverts.',
					'es': 'Exactamente dos archivos de fuentes deben estar abiertos.',
				}),
				OKButton="OK",
			)

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
