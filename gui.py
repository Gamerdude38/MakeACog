'''
John Maurer

Description: A class used to construct the GUI used in Construct A Cog.
This class demonstrates the use of multi-class programming and organization
via the separation of game elements.

Variables:
currentScreen: Represents the GUI screen that is currently being displayed 
[Ranges from 0 to 3]
name: Stores the string typed in by the user in the DirectEntry box
'''

from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from direct.showbase import DirectObject
from direct.gui.DirectGui import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from cog import Cog
import sys,os

class ConstructACogGUI():
	def __init__(self):
		#Define variables and file path locations
		self.currentScreen = 0
		self.name = 'New Cog'
		self.currentDirectory = os.path.abspath(sys.path[0])
		self.pandaDirectory = Filename.fromOsSpecific(self.currentDirectory).getFullpath()
		
		#Define UI Background
		self.UIBackground = loader.loadModel(self.pandaDirectory + '/resources/gui/tt_m_gui_ups_panelBg.bam')
		self.UIBackground.reparentTo(aspect2d)
		self.UIBackground.setPos(-0.75,0,0)
		self.UIBackground.setScale(1,1,1.75)
		
		#Set the title text
		self.remingtonFont = loader.loadFont(self.pandaDirectory + '/resources/gui/vtRemingtonPortable.ttf')
		self.instructionText = OnscreenText(pos=(0,0.35),
											wordwrap=10,
											font=self.remingtonFont,
											parent=self.UIBackground,
											mayChange=True)
		
		#Establish where the buttons are located
		self.buttonMaps = loader.loadModel(self.pandaDirectory + '/resources/gui/tt_m_gui_mat_mainGui.bam')
		
		#Define the head selector, its title text, and its scroll buttons
		self.headSelector = OnscreenImage(image=self.buttonMaps.find('**/tt_t_gui_mat_shuffleFrame'),
											parent=self.UIBackground,
											scale=(0.7,1,0.5),
											pos=(0,0,0.18))
		
		self.headSelectorText = OnscreenText(text='Head',
											parent=self.headSelector,
											pos=(0,-0.04),
											scale=(0.15,0.15),
											fg=(255,255,255,1),
											font=self.remingtonFont)
		
		self.headLeftButton = DirectButton(geom = (self.buttonMaps.find('**/tt_t_gui_mat_shuffleArrowUp'),
											self.buttonMaps.find('**/tt_t_gui_mat_shuffleArrowDown')),
											relief=None,
											parent=self.headSelector,
											pos=(-0.33,0,0),
											command=self.headLeftClick)
		
		self.headRightButton = DirectButton(geom = (self.buttonMaps.find('**/tt_t_gui_mat_shuffleArrowUp'),
											self.buttonMaps.find('**/tt_t_gui_mat_shuffleArrowDown')),
											relief=None,
											parent=self.headSelector,
											pos=(0.33,0,0),
											scale=(-1,1,1),
											command=self.headRightClick)
		self.headSelector.hide()
		
		#Define the body selector, its title text, and its scroll buttons
		self.bodySelector = OnscreenImage(image=self.buttonMaps.find('**/tt_t_gui_mat_shuffleFrame'),
											parent=self.UIBackground,
											scale=(-0.7,1,0.5),
											pos=(0,0,0))
											
		self.bodySelectorText = OnscreenText(text='Body',
											parent=self.bodySelector,
											pos=(0,-0.04),
											scale=(-0.15,0.15),
											fg=(255,255,255,1),
											font=self.remingtonFont)
		
		self.bodyLeftButton = DirectButton(geom = (self.buttonMaps.find('**/tt_t_gui_mat_shuffleArrowUp'),
											self.buttonMaps.find('**/tt_t_gui_mat_shuffleArrowDown')),
											relief=None,
											parent=self.bodySelector,
											pos=(0.33,0,0),
											scale=(-1,1,1),
											command=self.bodyLeftClick)
		
		self.bodyRightButton = DirectButton(geom = (self.buttonMaps.find('**/tt_t_gui_mat_shuffleArrowUp'),
											self.buttonMaps.find('**/tt_t_gui_mat_shuffleArrowDown')),
											relief=None,
											parent=self.bodySelector,
											pos=(-0.33,0,0),
											command=self.bodyRightClick)
		self.bodySelector.hide()
		
		#Define the department selector, its title text, and its scroll buttons
		self.deptSelector = OnscreenImage(image=self.buttonMaps.find('**/tt_t_gui_mat_shuffleFrame'),
											parent=self.UIBackground,
											scale=(0.7,1,0.5),
											pos=(0,0,-0.18))
											
		self.deptSelectorText = OnscreenText(text='Dept.',
											parent=self.deptSelector,
											pos=(0,-0.04),
											scale=(0.15,0.15),
											fg=(255,255,255,1),
											font=self.remingtonFont)
		
		self.deptLeftButton = DirectButton(geom = (self.buttonMaps.find('**/tt_t_gui_mat_shuffleArrowUp'),
											self.buttonMaps.find('**/tt_t_gui_mat_shuffleArrowDown')),
											relief=None,
											parent=self.deptSelector,
											pos=(-0.33,0,0),
											command=self.deptLeftClick)
		
		self.deptRightButton = DirectButton(geom = (self.buttonMaps.find('**/tt_t_gui_mat_shuffleArrowUp'),
											self.buttonMaps.find('**/tt_t_gui_mat_shuffleArrowDown')),
											relief=None,
											parent=self.deptSelector,
											pos=(0.33,0,0),
											scale=(-1,1,1),
											command=self.deptRightClick)
		self.deptSelector.hide()
		
		#Define the name input
		self.nameEntryBackground = OnscreenImage(image=loader.loadModel(self.pandaDirectory + "/resources/gui/ChatPanel.bam"),
											parent=self.UIBackground,
											scale=(0.6,1,0.1),
											pos=(-0.3,0,0.2))
		
		self.nameEntry = DirectEntry(parent=self.nameEntryBackground,
											relief=None,
											text='',
											width=5.5,
											numLines=2,
											entryFont=self.remingtonFont,
											scale=(0.2,1,0.4),
											pos=(-0.05,0,-0.35),
											command=self.enterName,
											focusOutCommand=self.entryUnfocused,
											focus=False)
		self.nameEntryBackground.hide()
		
		#Define the screen changing buttons
		self.nextButton = DirectButton(geom = (self.buttonMaps.find('**/tt_t_gui_mat_nextUp'),
											self.buttonMaps.find('**/tt_t_gui_mat_nextDown')),
											relief=None,
											command=self.nextButtonClick,
											parent=self.UIBackground,
											scale=(0.4,1,0.25),
											pos=(0.3,0,-0.35))
		
		self.backButton = DirectButton(geom = (self.buttonMaps.find('**/tt_t_gui_mat_nextUp'),
											self.buttonMaps.find('**/tt_t_gui_mat_nextDown')),
											relief=None,
											command=self.backButtonClick,
											parent=self.UIBackground,
											scale=(-0.4,1,0.25),
											pos=(-0.3,0,-0.35))
		self.backButton.hide()
		
		#Call the Cog class to establish the Actor
		self.cog = Cog()
		
		#Change the current UI screen
		self.screenDirector()
		
	def headLeftClick(self):
		#switch to the previous head
		self.cog.previousHead()
		
	def headRightClick(self):
		#switch to the next head
		self.cog.nextHead()
		
	def bodyLeftClick(self):
		#switch to the previous body
		self.cog.previousBody()
		
	def bodyRightClick(self):
		#switch to the next body
		self.cog.nextBody()
		
	def deptLeftClick(self):
		#switch to the previous department
		self.cog.previousDept()
		
	def deptRightClick(self):
		#switch to the next department
		self.cog.nextDept()
		
	def enterName(self,text):
		#Assign the entry text to name, then switch to the next screen
		self.name = text
		self.currentScreen = 3
		
		#Change the current UI screen
		self.screenDirector()
	
	def setEntryFocus(self):
		#Determine if to focus or unfocus the DirectEntry depending if the screen is visible
		if self.currentScreen == 2:
			self.nameEntry['focus'] = True
		else:
			self.nameEntry['focus'] = False
			self.entryUnfocused()
		
		self.nameEntry.setFocus()
		
	def entryUnfocused(self):
		#Set whatever is currently in the box to the name variable
		self.name = self.nameEntry.get()

	def nextButtonClick(self):
		#Add 1 to the currentScreen, then switch to the new screen
		self.currentScreen += 1
		
		#Constrain current screen to always be less than 3
		if self.currentScreen > 3:
			self.currentScreen = 3
			return
		
		#Set the focus of the text entry box	
		self.setEntryFocus()
		
		#Change the current UI screen
		self.screenDirector()
		
	def backButtonClick(self):
		#Subtract 1 from the currentScreen, then switch to the new screen
		self.currentScreen -= 1
		
		#Constrain current screen to always be greater than 0
		if self.currentScreen < 0:
			self.currentScreen = 0
			return
		
		#Set the focus of the text entry box
		self.setEntryFocus()
		
		#Change the current UI screen
		self.screenDirector()
		
	def screenDirector(self):
		#Determine which screen to shift to
		if self.currentScreen == 0:
			self.welcomeScreen()
			
		elif self.currentScreen == 1:
			self.cogDesignScreen()
			
		elif self.currentScreen == 2:
			self.namingScreen()
			
		elif self.currentScreen == 3:
			self.finishedScreen()
		
		else:
			raise Exception('UH OH! currentScreen is not between 0 and 3! \
							The value of currentScreen is {}'.format(self.currentScreen))
			
	def welcomeScreen(self):
		#Show/hide respective GUI elements
		self.instructionText.setText('Salutations, new Cog. \
									Click the button below to continue.')
		self.backButton.hide()
		self.headSelector.hide()
		self.bodySelector.hide()
		self.deptSelector.hide()
		
		#Determine whether the cog should exit the scene if its in view already
		if(self.cog.isInView):
			self.cog.exitScene()
	
	def cogDesignScreen(self):
		#Show/hide respective GUI elements
		self.instructionText.setText('Select a design.')
		self.backButton.show()
		self.headSelector.show()
		self.bodySelector.show()
		self.deptSelector.show()
		self.nameEntryBackground.hide()
		
		#Determine whether the cog should reenter the scene if its in view already
		if(not self.cog.isInView):
			self.cog.enterScene()

	def namingScreen(self):
		#Show/hide respective GUI elements
		self.instructionText.setText('Type in a name.')
		self.nextButton.show()
		self.headSelector.hide()
		self.bodySelector.hide()
		self.deptSelector.hide()
		self.nameEntryBackground.show()
		
		#See if the cog is playing the victory animation and change to keep the animation smooth
		if self.cog.getAnimPlaying() == 'victory':
			self.cog.playNeutral()
	
	def finishedScreen(self):
		#Show/hide respective GUI elements
		self.instructionText.setText('Welcome to COGS, Inc., ' + self.name + '.\
									If you wish to make changes, click the back button.')
		self.nextButton.hide()
		self.nameEntryBackground.hide()
		
		#Have the cog dance
		self.cog.playVictory()
