#!C:/Users/shaha/AppData/Local/Microsoft/WindowsApps/python3.exe
#!/usr/bin/env python3


import sys
import xmlrpc.client
import logging
#import tf.transformations as tf
import tensorflow as tf
from time import sleep
"""
This is an example how to use the XML-RPC interface of horstFX
"""



class Client:
    #def __init__(self, user="horstFX", password="WZA3P9", url="127.0.0.1:8080/xml-rpc"):
    def __init__(self, user="horstFX", password="WZA3P9", url="192.168.11.11:8080/xml-rpc"):
    #def __init__(self, user="horstFX", password="WZA3P9", url="LAPTOP-5OEMQ0QA:8080/xml-rpc"):
        self.URL = url   # changed - moved @ to lower line with whole address
        '''Username and password (only needed for some calls, including RobotMoveCalls)'''
        self.USERNAME = user
        self.PASSWORD = password
        '''Construct a client with the HorstFX server url, username and password '''
        self.client = xmlrpc.client.ServerProxy("http://" + self.USERNAME + ":" + self.PASSWORD + "@" + self.URL)
        print("Initialized xmlrpc client for user '" + self.USERNAME + "'")


    """ Example call to get the robot position"""
    def getCurrentRobotPositionV(self):
        pos = self.client.HorstFX.Robotcontrol.getCurrentRobotPosition()
        x = pos.get("x")
        y = pos.get("y")
        z = pos.get("z")
        return x, y, z

    def getModifiedRobotPosition(self):
        pos = self.client.HorstFX.Robotcontrol.getCurrentRobotPosition()
        x = pos.get("x")
        y = pos.get("y")
        z = float(pos.get("z")) + 999999
        print(f"Modified Robot Position: x={x}, y={y}, z={z}")
        print("x: " + str(pos.get("x")) + " y: " + str(pos.get("y")) + " z: " + str(pos.get("z")))
        print(z)
        return x, y, z

    def getCurrentRobotPosition(self):
        pos = self.client.HorstFX.Robotcontrol.getCurrentRobotPosition()
        print ("q0: " + str(pos.get('q0')) + " q1: " + str(pos.get("q1")) + " q2: " + str(pos.get("q2")) + " q3: " + str(pos.get("q3")) +
               "\nrx: " + str(pos.get("rx")) + " ry: " + str(pos.get("ry")) + " rz: " + str(pos.get("rz")) +
               "\nx: " + str(pos.get("x")*1000) + "mm y: " + str(pos.get("y")*1000) + "mm  z: " + str(pos.get("z")*1000) + "mm")




    """ Example call to get the current robot joint position"""  # HERE! v1
    def getCurrentRobotJoints(self):
        joints = self.client.HorstFX.Robotcontrol.getCurrentRobotJoints()
        print ("j1: " + str(joints.get('j1')) + " j2: " + str(joints.get('j2')) + " j3: " + str(joints.get('j3')) +
               " j4: " + str(joints.get('j4')) + " j5: " + str(joints.get('j5')) + " j6: " + str(joints.get('j6')))



    """ Example call to move the robot (joint movement)"""
    def moveJoint(self, x, y, z, q0, q1, q2, q3, speed):
        "Convert to mm from m"
        result = self.client.HorstFX.Robotcontrol.moveJoint(x, y, z, q0, q1, q2, q3, speed) #speed
        return result


        return result

    """ Example call to move the robot (linear movement)"""
    def moveLinear(self, x, y, z, q0, q1, q2, q3, speed):
        result = self.client.HorstFX.Robotcontrol.moveLinear(x, y, z, q0, q1, q2, q3, speed) #speed
        return result

    def move(self, move_array=[]):

        result = self.client.HorstFX.Robotcontrol.moveAdvanced(move_array)
        return result

    def moveAdvanced(self, value):   #!!! Not finished
        result = self.client.HorstFX.Robotcontrol.moveAdvanced(value)
        return result

    def moveTrajectory(self, trajectory_joints=[], error_on_constraints_violation=True):

        result = self.client.HorstFX.v5.Robotcontrol.moveTrajectory(trajectory_joints, error_on_constraints_violation)
        return result

    """ change mode"""

    def checkTrajectories(self, trajectories):   #!!!
        result = self.client.HorstFX.Robotcontrol.checkTrajectories(trajectories)
        return result

    def checkJointViaPointPaths(self, viaPointPaths):   #!!!
        result = self.client.HorstFX.Robotcontrol.checkJointViaPointPaths(viaPointPaths)
        return result

    """"Trajectories will be stored for execution,
            which needs to be triggered by calling execTraj"""

    def checkCartesianViaPointPaths(self, viaPointPaths):   #!!!
        result = self.client.HorstFX.Robotcontrol.checkCartesianViaPointPaths(viaPointPaths)
        return result

    """"Trajectories will be stored for execution,
            which needs to be triggered by calling execTraj"""

    def executeTrajectories(self):   #!!!
        result = self.client.HorstFX.Robotcontrol.executeTrajectories()
        return result


    """ Example call to get Inputs"""
    def getInput(self, input):
        result = self.client.HorstFX.Robotcontrol.getInput(input)
        return result


    """ Example call to set Outputs"""
    def setOutput(self, output_name, value):
        result = self.client.HorstFX.Robotcontrol.setOutput(output_name, value)
        return result

    """ Example call to set the tool"""
    def setTool(self, tool_name):
        result = self.client.HorstFX.Robotcontrol.setTool(tool_name)
        return result

    def getToolOffset(self):   #!!!
        result = self.client.HorstFX.Robotcontrol.getToolOffset()
        return result



    """ Example call to set the variable nextPose
    saves the given pose (position + orientation) inside variable nextPose,
the value of the variable will be overridden"""
    def nextPose(self, x, y, z, q0, q1, q2, q3):
        result = self.client.HorstFX.Variable.nextPose(x, y, z, q0, q1, q2, q3)
        return result

    """ reads the variable nextPose, returns a map with coords """
    def getNextPose(self):
        result = self.client.HorstFX.Variable.getNextPose()
        return result

    """ saves the given joints inside variable nextJoints, the value of the 
variable will be overridden - we can read them in Text Programming via getNextJoints()"""
    def nextJoints(self, joint1, joint2, joint3, joint4, joint5, joint6):
        result = self.client.HorstFX.Variable.nextJoints(joint1, joint2, joint3, joint4, joint5, joint6)
        return result

    """ Returns the current joint angles of the variable nextJoints."""
    def getNextJoints(self):
        result = self.client.HorstFX.Variable.getNextJoints()
        return result

    """ Example call to set the register"""
    def setRegister(self, registerIndex, value):
        result = self.client.HorstFX.Variable.setRegister(registerIndex, float(value))
        return result

    """ Example call to get the given register value"""
    def getRegister(self, registerIndex):
        result = self.client.HorstFX.Variable.getRegister(registerIndex)
        return result

    def setFloatRegister(self, registerIndex, value):
        result = self.client.HorstFX.Variable.setFloatRegister(registerIndex, value)
        return result

    def getFloatRegister(self, registerIndex):
        result = self.client.HorstFX.Variable.getFloatRegister(registerIndex)
        return result
    
    "we can read them in Text Programming via getIntRegister(index)"
    def setIntRegister(self, registerIndex, value):
        result = self.client.HorstFX.Variable.ssetIntRegister(registerIndex, value)
        return result

    def getIntRegister(self, registerIndex):
        result = self.client.HorstFX.Variable.setIntRegister(registerIndex)
        return result

    def setBoolRegister(self, registerIndex, value):
        result = self.client.HorstFX.Variable.setBoolRegister(registerIndex, value)
        return result

    def getBoolRegister(self, registerIndex):
        result = self.client.HorstFX.Variable.getBoolRegister(registerIndex)
        return result

    """ Start a predefined program written by user (put in str)"""
    def execute(self, script):
        result = self.client.HorstFX.Program.execute(script)
        return result

    """ Example call to pause a program"""
    def pause(self):
        result = self.client.HorstFX.Program.pause()
        return result

    """ Example call to find out if a program is running"""
    def isRunning(self):
        result = self.client.HorstFX.Program.isRunning()
        return result

    """ Example call to abort a program"""
    def abort(self):
        result = self.client.HorstFX.Program.abort()
        return result

    """ Example call to proceed a program"""
    def proceed(self):
        result = self.client.HorstFX.Program.proceed()
        return result

    """ Example call to proceed a program"""
    def play(self):
        result = self.client.HorstFX.Program.play()
        return result

    """ Example call to proceed a program"""
    def getGlobalSpeed(self):
        result = self.client.HorstFX.Program.getGlobalSpeed()
        return result

    """ Example call to proceed a program"""
    def setGlobalSpeed(self, value):
        result = self.client.HorstFX.Program.setGlobalSpeed(value)
        return result

    """ This method returns the status of the robot. """  # HERE! .v4.
    def safetyStatus(self):
        result = self.client.HorstFX.Safety.status()
        return result

    """ This method confirms the emergency stop (Nothalt)"""
    def confirmEmergencyStop(self):
        result = self.client.HorstFX.Safety.confirmEmergencyStop()
        return result

    """ This method confirms the external emergency stop (externer Nothalt)"""
    def confirmExternalEmergencyStop(self):
        result = self.client.HorstFX.Safety.confirmExternalEmergencyStop()
        return result

    """ This method confirms the internal errors"""
    def confirmInternalError(self):
        result = self.client.HorstFX.v4.Safety.confirmInternalError()
        return result

    """ This method confirms the change of the operating mode"""
    def confirmChangeOperatingMode(self):
        result = self.client.HorstFX.v4.Safety.confirmChangeOperatingMode()
        return result

    """ This method gets the path and name of the currently loaded program. Path starts with save directory"""
    def programName(self):
        result = self.client.HorstFX.Activity.getCurrentProgramName()
        return result

    """ This method switches to another activity identified by its ID."""
    def switchActivity(self, value):
        result = self.client.HorstFX.Activity.switchActivity(value)
        return result

    """ This method switches to the programming activity and loads a program 
identified by its path and name."""
    def switchActivitySpecial(self, fileName):
        result = self.client.HorstFX.Activity.switchActivity(fileName)
        return result

    """ This method gets the ID of the current activity."""
    def getCurrentActivityID(self):
        result = self.client.HorstFX.Activity.getCurrentActivityID()
        return result

    """ This method gets the ID of the currently shown pop-up."""
    def getShownPopUpID(self):
        result = self.client.HorstFX.Activity.getShownPopUpID()
        return result

    """ Choose button 1"""
    def option1(self):
        result = self.client.HorstFX.Activity.executeOption1()
        return result

    """ Choose button 2"""
    def option2(self):
        result = self.client.HorstFX.Activity.executeOption2()
        return result

    """ Choose button 3"""
    def option3(self):
        result = self.client.HorstFX.Activity.executeOption3()
        return result

    """ This method return if joints are initialized"""
    def getInitialization(self):
        result = self.client.HorstFX.Initialization.getJointInit()
        return result

    """ starts/continues the auto-init of the robot. As the process takes some 
time to finish and collisions can occur during the process it is 
recommended to use the timeout to specify how long the robot should 
move until the next call confirms the continuation of the process
"""
    def automaticInitialize(self, timeout):
        result = self.client.HorstFX.Initialization.automatic(timeout)
        return result

    def movejointsInitialize(self, jointIdx, jointAngle):  # THROWS
        result = self.client.HorstFX.Initialization.moveJoint(jointIdx, jointAngle)
        return result

    def stopInitialize(self):
        result = self.client.HorstFX.Initialization.stop()
        return result



#client = Client()
#client.safetyStatus()


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)
