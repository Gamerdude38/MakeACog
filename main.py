'''
John Maurer

Description: A driver class for Make A Cog, a program that demonstrates 
DirectGUI  knowledge in conjuction with 3D rendering elements in Panda3D 
using models and other resources from the Toontown Rewritten Phase 
Files.

Screen Numbers
0: Welcome screen
1: Cog body
2: Cog head
3: Cog department
4: Name
5: Finished!
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
		ShowBase.__init__(self)
		self.disableMouse()
		
		self.currentScreen = 0
		self.currentDirectory = os.path.abspath(sys.path[0])
		self.pandaDirectory = Filename.fromOsSpecific(self.currentDirectory).getFullpath()
			
		self.remingtonFont = loader.loadFont(self.pandaDirectory + '/models/vtRemingtonPortable.ttf')
		self.buttonMaps = loader.loadModel(self.pandaDirectory + '/models/create_a_toon_gui.bam')
		
		#Load the main terrain to be used
		self.terrain = self.loader.loadModel(self.pandaDirectory + '/models/tt_m_ara_cmg_quadrant1.bam')
		self.terrain.reparentTo(self.render)
		
		#Add enclosing walls
		self.walls = self.loader.loadModel(self.pandaDirectory + '/models/tt_m_ara_cmg_level.bam')
		self.walls.reparentTo(self.terrain)
		self.walls.setHpr(90,0,0)
		self.walls.setScale(0.33,0.33,1)
		
		#Set up the fixed camera position
		self.camera.setPos(10,-15,7)
		self.camera.setHpr(20,-7,0)
		
		#Define the UI elements
		self.UIBackground = self.loader.loadModel(self.pandaDirectory + '/models/dialog_box_gui.bam')
		self.UIBackground.reparentTo(self.aspect2d)
		self.UIBackground.setPos(-0.75,0,0)
		self.UIBackground.setScale(1,1,1.5)
		
		self.instructionText = OnscreenText(text='Hi there! Welcome to Make a Cog! Click the button below to continue.', pos=(0,0.4), wordwrap=10, font=self.remingtonFont, parent=self.UIBackground, mayChange=True)
		
		self.nextButton = DirectButton(geom = (self.buttonMaps.find('**/CrtAtoon_Btn3_UP'), self.buttonMaps.find('**/CrtAtoon_Btn3_DN'), self.buttonMaps.find('**/CrtAtoon_Btn3_RLVR')), relief=None)
		self.nextButton['command'] = self.nextButtonClick
		self.nextButton.reparentTo(self.UIBackground)
		self.nextButton.setPos(0.3,0,-0.4)
		self.nextButton.setScale(0.75,1,0.5)
		
		self.backButton = DirectButton(geom = (self.buttonMaps.find('**/CrtAtoon_Btn3_UP'), self.buttonMaps.find('**/CrtAtoon_Btn3_DN'), self.buttonMaps.find('**/CrtAtoon_Btn3_RLVR')), relief=None)
		self.backButton['command'] = self.backButtonClick
		self.backButton.reparentTo(self.UIBackground)
		self.backButton.setPos(-0.3,0,-0.4)
		self.backButton.setScale(-0.75,-1,0.5)
		
	def welcomeScreen(self):
		self.instructionText.setText('Salutations, new Cog. Welcome to Make a Cog! Click the button below to continue.')
		self.backButton.hide()
	
	def cogBodyScreen(self):
		self.instructionText.setText('Select a body type.')
		self.backButton.show()

	def cogHeadScreen(self):
		self.instructionText.setText('Select a head.')

	def cogDepScreen(self):
		self.instructionText.setText('Choose your department.')

	def namingScreen(self):
		self.instructionText.setText('Type in a name.')
		self.nextButton.show()
	
	def finishedScreen(self):
		self.instructionText.setText('Welcome to COGS, Inc., new cog. If you wish to make changes, click the back button.')
		self.nextButton.hide()

	def nextButtonClick(self):
		self.currentScreen += 1
		
		if self.currentScreen > 5:
			self.currentScreen = 5
			return
			
		self.screenDirector()
		
	def backButtonClick(self):
		self.currentScreen -= 1
		
		if self.currentScreen < 0:
			self.currentScreen = 0
			return
			
		self.screenDirector()
		
	def screenDirector(self):
		if self.currentScreen == 0:
			self.welcomeScreen()
		elif self.currentScreen == 1:
			self.cogBodyScreen()
		elif self.currentScreen == 2:
			self.cogHeadScreen()
		elif self.currentScreen == 3:
			self.cogDepScreen()
		elif self.currentScreen == 4:
			self.namingScreen()
		elif self.currentScreen == 5:
			self.finishedScreen()
			
makeACog = MakeACog()
makeACog.run()
