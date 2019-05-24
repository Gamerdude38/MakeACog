'''
John Maurer

Description: Description: A driver class for Construct A Cog, a program 
that demonstrates DirectGUI knowledge in conjuction with 3D rendering 
elements in Panda3D using models and other resources from the Toontown 
Rewritten Phase Files.
'''

from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from gui import ConstructACogGUI
import sys,os

class ConstructACog(ShowBase):
	def __init__(self):
		#Initialize the scene and disable Panda's free camera
		ShowBase.__init__(self)
		self.disableMouse()
		
		#Establish where the current directory of the running file is
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
		self.camera.setHpr(20,-8,0)
		
		#Create the GUI
		self.gui = ConstructACogGUI()
		
constructACog = ConstructACog()
constructACog.run()
