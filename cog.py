'''
John Maurer

Description: A class used to create a Cog Actor that can be changed during
runtime

Variables:
currentHead: Represents the 32 different cog heads available [0-31]
currentBody: Represents the 3 different cog body types [0-2]
currentDept: Represents the 4 different cog departments, plus the waiter
suit [0-4]
'''

from direct.actor.Actor import Actor
from direct.interval.LerpInterval import LerpPosInterval,LerpHprInterval
from direct.interval.ActorInterval import ActorInterval
from direct.interval.IntervalGlobal import *
from panda3d.core import *
import sys,os

class Cog():
	def __init__(self):
		#Define variables to keep track of the current head, body, and department
		self.currentBody = 0
		self.currentHead = 22
		self.currentDept = 0
		
		#Define a boolean to determine if the cog is in view
		self.isInView = False
		
		#Establish current file path location
		self.currentDirectory = os.path.abspath(sys.path[0])
		self.pandaDirectory = Filename.fromOsSpecific(self.currentDirectory).getFullpath()
		
		#Create the cog head and body (mainly to allow it to be 
		#destroyed later in replacement of the proper body)
		self.cog = Actor(self.pandaDirectory + '/resources/cogs/models/tt_a_ene_cga_zero.bam',{
						'neutral':(self.pandaDirectory + '/resources/cogs/animations/tt_a_ene_cga_neutral.bam'),
						'walk':(self.pandaDirectory + '/resources/cogs/animations/tt_a_ene_cga_walk.bam')
						})
		self.head = loader.loadModel(self.pandaDirectory + '/resources/cogs/models/suitA-heads.bam')
		
		#Determine the body type and set the head
		self.determineBody()
		
	def determineBody(self):
		#Destroy the current body to unrender it
		self.cog.delete()
		self.cog.removeNode()
		
		#Determine the new cog body type
		if self.currentBody == 0:
			self.cog = Actor(self.pandaDirectory + '/resources/cogs/models/tt_a_ene_cga_zero.bam',{
						'neutral':(self.pandaDirectory + '/resources/cogs/animations/tt_a_ene_cga_neutral.bam'),
						'walk':(self.pandaDirectory + '/resources/cogs/animations/tt_a_ene_cga_walk.bam')
						})
		elif self.currentBody == 1:
			self.cog = Actor(self.pandaDirectory + '/resources/cogs/models/tt_a_ene_cgb_zero.bam',{
						'neutral':(self.pandaDirectory + '/resources/cogs/animations/tt_a_ene_cgb_neutral.bam'),
						'walk':(self.pandaDirectory + '/resources/cogs/animations/tt_a_ene_cgb_walk.bam')
						})
		elif self.currentBody == 2:
			self.cog = Actor(self.pandaDirectory + '/resources/cogs/models/tt_a_ene_cgc_zero.bam',{
						'neutral':(self.pandaDirectory + '/resources/cogs/animations/tt_a_ene_cgc_neutral.bam'),
						'walk':(self.pandaDirectory + '/resources/cogs/animations/tt_a_ene_cgc_walk.bam')
						})
		else:
			raise Exception('UH OH! currentBody is not between 0 and 2! The value of currentBody is {}'.format(self.currentBody))
		
		self.cog.reparentTo(render)
		
		if self.isInView:
			self.cog.loop('neutral')
			self.cog.setPos(6, 2, 0)
			self.cog.setHpr(180, 0, 0)
		else:
			self.resetCogPos()
			
		#Define the lerp for the cog's movement and animations
		self.walkIn = self.cog.posInterval(2, pos=(6, 2, 0))
		self.walkOut = self.cog.posInterval(2, pos=(15, 2, 0))
		self.turnToCam = self.cog.hprInterval(1, hpr=(180, 0, 0))
		self.turnAway = self.cog.hprInterval(1, hpr=(270, 0, 0))
		
		#Define the sequences
		#Note: If you want to loop an animation after a sequence plays, 
		#you have to append the Func(self.actor.loop, 'animName') to the end of the function.
		self.enterView = Sequence(self.walkIn, self.turnToCam, Func(self.cog.loop, 'neutral'))
		self.exitView = Sequence(Func(self.cog.loop, 'walk'), self.turnAway, self.walkOut)
		
		#Call the other methods to reattach and reapply the head and department textures
		self.determineHead()
		self.determineDept()
			
	def determineHead (self):
		#Destroy the current head to unrender it
		self.head.removeNode()
		
		#Set up a boolean to make sure the cog is or isn't a flunky
		hasGlasses = False
		
		#Determine the cog head type
		if self.currentHead <= 12:
			self.headList = loader.loadModel(self.pandaDirectory + '/resources/cogs/models/suitA-heads.bam')
			
			if self.currentHead == 0:
				self.head = self.headList.find('**/backstabber')
			elif self.currentHead == 1:
				self.head = self.headList.find('**/bigcheese')
			elif self.currentHead == 2:
				self.head = self.headList.find('**/bigwig')
			elif self.currentHead == 3:
				self.head = self.headList.find('**/headhunter')
			elif self.currentHead == 4:
				self.head = self.headList.find('**/legaleagle')
			elif self.currentHead == 5:
				self.head = self.headList.find('**/numbercruncher')
			elif self.currentHead == 6:
				#name dropper
				self.head = self.headList.find('**/numbercruncher')
				self.head.setTexture(loader.loadTexture(self.pandaDirectory + \
									'/resources/cogs/textures/name-dropper.jpg'), 1)
			elif self.currentHead == 7:
				self.head = self.headList.find('**/pennypincher')
			elif self.currentHead == 8:
				self.head = self.headList.find('**/yesman')
			elif self.currentHead == 9:
				#robber baron
				self.head = self.headList.find('**/yesman')
				self.head.setTexture(loader.loadTexture(self.pandaDirectory + \
									'/resources/cogs/textures/robber-baron.jpg'), 1)
			elif self.currentHead == 10:
				self.head = self.headList.find('**/twoface')
			elif self.currentHead == 11:
				#mingler
				self.head = self.headList.find('**/twoface')
				self.head.setTexture(loader.loadTexture(self.pandaDirectory + \
									'/resources/cogs/textures/mingler.jpg'), 1)
			else:
				#double talker
				self.head = self.headList.find('**/twoface')
				self.head.setTexture(loader.loadTexture(self.pandaDirectory + \
									'/resources/cogs/textures/double-talker.jpg'), 1)
				
		elif self.currentHead <= 20:
			self.headList = loader.loadModel(self.pandaDirectory + '/resources/cogs/models/suitB-heads.bam')
			
			if self.currentHead == 13:
				self.head = self.headList.find('**/ambulancechaser')
			elif self.currentHead == 14:
				self.head = self.headList.find('**/beancounter')
			elif self.currentHead == 15:
				self.head = self.headList.find('**/loanshark')
			elif self.currentHead == 16:
				self.head = self.headList.find('**/movershaker')
			elif self.currentHead == 17:
				#bloodsucker
				self.head = self.headList.find('**/movershaker')
				self.head.setTexture(loader.loadTexture(self.pandaDirectory + \
									'/resources/cogs/textures/blood-sucker.jpg'), 1)
			elif self.currentHead == 18:
				self.head = self.headList.find('**/pencilpusher')
			elif self.currentHead == 19:
				self.head = self.headList.find('**/telemarketer')
			else:
				#spin doctor
				self.head = self.headList.find('**/telemarketer')
				self.head.setTexture(loader.loadTexture(self.pandaDirectory + \
									'/resources/cogs/textures/spin-doctor.jpg'), 1)
			
		elif self.currentHead <= 29:
			self.headList = loader.loadModel(self.pandaDirectory + '/resources/cogs/models/suitC-heads.bam')
			
			if self.currentHead == 21:
				#actually a short change
				self.head = self.headList.find('**/coldcaller')
			elif self.currentHead == 22:
				#cold caller needs to be recolored
				self.head = self.headList.find('**/coldcaller')
				self.head.setColor(0, 0, 255, 1)
			elif self.currentHead == 23:
				self.head = self.headList.find('**/flunky')
				hasGlasses = True
			elif self.currentHead == 24:
				#corporate raider
				self.head = self.headList.find('**/flunky')
				self.head.setTexture(loader.loadTexture(self.pandaDirectory + \
									'/resources/cogs/textures/corporate-raider.jpg'), 1)
			elif self.currentHead == 25:
				self.head = self.headList.find('**/gladhander')
			elif self.currentHead == 26:
				self.head = self.headList.find('**/micromanager')
			elif self.currentHead == 27:
				self.head = self.headList.find('**/moneybags')
			elif self.currentHead == 28:
				self.head = self.headList.find('**/tightwad')
			else:
				#bottom feeder
				self.head = self.headList.find('**/tightwad')
				self.head.setTexture(loader.loadTexture(self.pandaDirectory + \
									'/resources/cogs/textures/bottom-feeder.jpg'), 1)
		else:
			raise Exception('UH OH! currentHead is not between 0 and 31! The value of currentBody is {}'.format(self.currentHead))
		
		#Attach the head to the model
		self.head.reparentTo(self.cog.find('**/def_head'))
		
		if hasGlasses:
			self.glasses = self.headList.find('**/glasses')
			self.glasses.reparentTo(self.head)
			
						
	def determineDept(self):
		#Determine the cog department and set the textures of the suit
		if self.currentDept == 0:
			self.cog.findAllMatches('**/torso').setTexture(loader.loadTexture(self.pandaDirectory + '/resources/cogs/textures/s_blazer.jpg'), 1)
			
			self.cog.findAllMatches('**/arms').setTexture(loader.loadTexture(self.pandaDirectory + '/resources/cogs/textures/s_sleeve.jpg'), 1)
			
			self.cog.findAllMatches('**/legs').setTexture(loader.loadTexture(self.pandaDirectory + '/resources/cogs/textures/s_leg.jpg'), 1)
			
		elif self.currentDept == 1:
			self.cog.findAllMatches('**/torso').setTexture(loader.loadTexture(self.pandaDirectory + '/resources/cogs/textures/m_blazer.jpg'), 1)
			
			self.cog.findAllMatches('**/arms').setTexture(loader.loadTexture(self.pandaDirectory + '/resources/cogs/textures/m_sleeve.jpg'), 1)
			
			self.cog.findAllMatches('**/legs').setTexture(loader.loadTexture(self.pandaDirectory + '/resources/cogs/textures/m_leg.jpg'), 1)
			
		elif self.currentDept == 2:
			self.cog.findAllMatches('**/torso').setTexture(loader.loadTexture(self.pandaDirectory + '/resources/cogs/textures/l_blazer.jpg'), 1)
			
			self.cog.findAllMatches('**/arms').setTexture(loader.loadTexture(self.pandaDirectory + '/resources/cogs/textures/l_sleeve.jpg'), 1)
			
			self.cog.findAllMatches('**/legs').setTexture(loader.loadTexture(self.pandaDirectory + '/resources/cogs/textures/l_leg.jpg'), 1)
			
		elif self.currentDept == 3:
			self.cog.findAllMatches('**/torso').setTexture(loader.loadTexture(self.pandaDirectory + '/resources/cogs/textures/c_blazer.jpg'), 1)
			
			self.cog.findAllMatches('**/arms').setTexture(loader.loadTexture(self.pandaDirectory + '/resources/cogs/textures/c_sleeve.jpg'), 1)
			
			self.cog.findAllMatches('**/legs').setTexture(loader.loadTexture(self.pandaDirectory + '/resources/cogs/textures/c_leg.jpg'), 1)
		
		elif self.currentDept == 4:
			self.cog.findAllMatches('**/torso').setTexture(loader.loadTexture(self.pandaDirectory + '/resources/cogs/textures/waiter_m_blazer.jpg'), 1)
			
			self.cog.findAllMatches('**/arms').setTexture(loader.loadTexture(self.pandaDirectory + '/resources/cogs/textures/waiter_m_sleeve.jpg'), 1)
			
			self.cog.findAllMatches('**/legs').setTexture(loader.loadTexture(self.pandaDirectory + '/resources/cogs/textures/waiter_m_leg.jpg'), 1)
				
		else:
			raise Exception('UH OH! currentDept is not between 0 and 4! The value of currentDept is {}'.format(self.currentDept))
			
	
	def nextHead(self):
		#Keep the head variable within the range and switch to the next head
		if self.currentHead >= 29:
			self.currentHead = 0
		else:
			self.currentHead += 1
			
		self.determineHead()
	
	def previousHead(self):
		#Keep the head variable within the range and switch to the previous head
		if self.currentHead <= 0:
			self.currentHead = 29
		else:
			self.currentHead -= 1
			
		self.determineHead()
		
	def nextBody(self):
		#Keep the head variable within the range and switch to the next body
		if self.currentBody >= 2:
			self.currentBody = 0
		else:
			self.currentBody += 1
			
		self.determineBody()
		
	def previousBody(self):
		#Keep the head variable within the range and switch to the previous body
		if self.currentBody <= 0:
			self.currentBody = 2
		else:
			self.currentBody -= 1
			
		self.determineBody()
		
	def nextDept(self):
		#Keep the head variable within the range and switch to the next department
		if self.currentDept >= 4:
			self.currentDept = 0
		else:
			self.currentDept += 1
			
		self.determineDept()
	
	def previousDept(self):
		#Keep the head variable within the range and switch to the previous department
		if self.currentDept <= 0:
			self.currentDept = 4
		else:
			self.currentDept -= 1
			
		self.determineDept()
			
	def resetCogPos(self):
		#Sets the cog's position to its starting location outside the scene
		self.cog.loop('walk')
		self.cog.setHpr(90,0,0)
		self.cog.setPos(15,2,0)
	
	def enterScene(self):
		#Establish the sequence for the cog to walk in the scene
		self.resetCogPos()
		self.enterView.start()
		
		self.isInView = True
	
	def exitScene(self):
		#Establish the sequence for the cog to walk out of the scene
		self.exitView.start()
		
		self.isInView = False
