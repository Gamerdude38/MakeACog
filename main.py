'''
John Maurer

Description: A driver class for Make A Cog, a program that demonstrates 
DirectGUI  knowledge in conjuction with 3D rendering elements in Panda3D 
using models and other resources from the Toontown Rewritten Phase 
Files.

Screen Numbers
0: Welcome screen
1: Design Screen
2: Name
3: Finished!
'''


from direct.actor.Actor import Actor
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from direct.showbase import DirectObject
from direct.gui.DirectGui import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
import sys,os

class MakeACog(ShowBase):
	def __init__(self):
		#Initialize the scene and disable Panda's free camera
		ShowBase.__init__(self)
		self.disableMouse()
		
		#Define tracking variables and file location where the models are stored
		self.currentScreen = 0
		self.currentHead = 0
		self.currentBody = 0
		self.currentDept = 0
		self.name = 'New Cog'
		self.currentDirectory = os.path.abspath(sys.path[0])
		self.pandaDirectory = Filename.fromOsSpecific(self.currentDirectory).getFullpath()
		
		#Load the main terrain to be used
		self.terrain = self.loader.loadModel(self.pandaDirectory + '/resources/terrain/tt_m_ara_cmg_quadrant1.bam')
		self.terrain.reparentTo(self.render)
		
		#Add enclosing walls
		self.walls = self.loader.loadModel(self.pandaDirectory + '/resources/terrain/tt_m_ara_cmg_level.bam')
		self.walls.reparentTo(self.terrain)
		self.walls.setHpr(90,0,0)
		self.walls.setScale(0.33,0.33,1)
		
		#Set up the fixed camera position
		self.camera.setPos(10,-15,7)
		self.camera.setHpr(20,-7,0)
		
		#Define UI Background
		self.UIBackground = self.loader.loadModel(self.pandaDirectory + '/resources/gui/tt_m_gui_ups_panelBg.bam')
		self.UIBackground.reparentTo(self.aspect2d)
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
		
		#Define the cog actor
		self.cog = Actor(self.pandaDirectory + '/resources/cogs/models/tt_a_ene_cga_zero.bam',{
						'neutral':(self.pandaDirectory + '/resources/cogs/animations/tt_a_ene_cga_neutral.bam'),
						'walk':(self.pandaDirectory + '/resources/cogs/animations/tt_a_ene_cga_walk.bam')
						})
		self.cog.reparentTo(render)
		self.cog.loop('walk')
		self.cog.setHpr(90,0,0)
		self.cog.setPos(15,2,0)
		
		#Establish the scene
		self.screenDirector()
		
		self.oobe()
		
	def headLeftClick(self):
		print('Left Head Click!')
	def headRightClick(self):
		print('Right Head Click!')
	def bodyLeftClick(self):
		print('Left Body Click!')
	def bodyRightClick(self):
		print('Right Body Click!')
	def deptLeftClick(self):
		print('Left Department Click!')
	def deptRightClick(self):
		print('Right Department Click!')
		
	def enterName(self, text):
		#Assign the entry text to name, then switch to the next screen
		self.name = text
		self.currentScreen = 3
		
		self.screenDirector()
	
	def setEntryFocus(self):
		#Determine if to focus or unfocus the DirectEntry depending if the screen is visible
		if self.currentScreen == 2:
			self.nameEntry['focus'] = True
		else:
			self.nameEntry['focus'] = False
		
		self.nameEntry.setFocus()
		
	def entryUnfocused(self):
		self.name = self.nameEntry.get()

	def nextButtonClick(self):
		#Add 1 to the currentScreen, then switch to the new string
		self.currentScreen += 1
		
		self.setEntryFocus()
		
		#Constrain current screen to always be less than 3
		if self.currentScreen > 3:
			self.currentScreen = 3
			return
			
		self.screenDirector()
		
	def backButtonClick(self):
		#Subtract 1 from the currentScreen, then switch to the new string
		self.currentScreen -= 1
		
		self.setEntryFocus()
		
		#Constrain current screen to always be greater than 0
		if self.currentScreen < 0:
			self.currentScreen = 0
			return
			
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
			
	def welcomeScreen(self):
		self.instructionText.setText('Salutations, new Cog. \
									Click the button below to continue.')
		self.backButton.hide()
		self.headSelector.hide()
		self.bodySelector.hide()
		self.deptSelector.hide()
	
	def cogDesignScreen(self):
		self.instructionText.setText('Select a design.')
		self.backButton.show()
		self.headSelector.show()
		self.bodySelector.show()
		self.deptSelector.show()
		self.nameEntryBackground.hide()

	def namingScreen(self):
		self.instructionText.setText('Type in a name.')
		self.nextButton.show()
		self.headSelector.hide()
		self.bodySelector.hide()
		self.deptSelector.hide()
		self.nameEntryBackground.show()
	
	def finishedScreen(self):
		self.instructionText.setText('Welcome to COGS, Inc., new cog.\
									If you wish to make changes, click the back button.')
		self.nextButton.hide()
		self.nameEntryBackground.hide()
			
makeACog = MakeACog()
makeACog.run()
