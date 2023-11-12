from __future__ import print_function

import time
from sr.robot import *


a_th = 2.0
""" float: Threshold for the control of the orientation"""

d_th = 0.4
""" float: Threshold for the control of the linear distance"""

R = Robot()
""" instance of the class Robot"""

carried_tokens = list()
""" a constantly updated list of grabbed tokens"""

 

def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0



def scanner():

 """
 Function for scanning and finding the closest tokens that their codes do not belong to the carried_tokens list.
 the function relies on the method see() of the class Robot which returns an object whose attribute is info.code.
 
 retunrs :

 dist (float): distance of the closest token (-1 if no new code token is detected from outside the carried tokens list)
 rot_y (float): angle between the robot and the new token (-1 if no new code token is detected)
 identity(int): the code of the closest new token (-1 if no new code token is detected)
 
 """
 
 dist=100
 
 for token in R.see():
  if token.dist < dist and token.info.code not in carried_tokens:
    dist = token.dist 
    rot_y= token.rot_y
    identity= token.info.code 
   
 if dist == 100 : 
  return -1 , -1 ,-1
 else :
  return dist , rot_y , identity 
  
  
 
def find_familiar():

    """
    Function for scanning and finding the closest familiar tokens that their codes have been appended already into the carried_tokens list.
    the function relies on the method see() of the class Robot as well which returns an object whose attribute is info.code.
 
    retunrs :

    dist (float): distance of the closest familiar token (-1 if no familiar token is detected from the carried tokens list)
    rot_y (float): angle between the robot and the familiar token (-1 if no familiar token is detected)
 
    """

    dist = 100
    for token in R.see():
        if token.dist < dist and token.info.code in carried_tokens:
            dist = token.dist
            rot_y = token.rot_y

    if dist == 100:
        return -1, -1
    else:
        return dist, rot_y
   
  
def approach_grab():

         """

         function for approaching and dirving the robot towards the closest new token in order to grab it. 
         this function relies internally on the function scanner() to get the new token's destination info.
         it also uses the method R.grab() to grab the token once reaching it out.
   
         returns:
         identity(int): the code of the closest token so the carried_tokens list stays updated.

         """
         
	 ready= 1
	 " scanning for new boxes and trying to obtain their info"
	 dist, rot_y, identity = scanner() 
	 
	 while dist == -1 :
	  print (" i couldnt find a new target !")
	  print (" searching for a new target")
	  
	  turn (20,1)
	  dist , rot_y , identity = scanner()
	  
	 print(" oh I found a new one !")
	 while  dist > d_th  :
	    
	      if ready == 1:
		  drive (30,1) 
		  ready =0 
		  dist, rot_y , identity =scanner()
		  
	      elif - a_th <= rot_y <= a_th :
		  dist, rot_y , identity  = scanner()
		  drive(20,0.5)
		  ready=0
	      elif rot_y > a_th :
		   turn(2,1)
		   dist, rot_y , identity  = scanner()
		   
		   ready=1
	      elif rot_y < - a_th :
		   turn(-2,1)
		   dist, rot_y , identity  = scanner()
		   ready=1
	 print(" I should be able to grab it") 		       
	 R.grab() 
	 print("ITS HEAVY !!")
	 return identity 



def approach_release():


 """
 function for dirving the robot back towards the closest familiar token that its code has already been appended into the carried_token list, in order to release the curruntly held token next to it. 
 this function relies internally on the function find_familiar() to get the previously carried token's destination info.
 it also uses the method R.release() to release the token once reaching its destination out.

 """
         
 
 ready=1
 " scanning for box with a familiar tokens and obtaining its orientation"
 print(" where did I put that box !?")
 dist, rot_y = find_familiar()
 
 while dist == -1 :
  print (" I couldnt remember !")
  print (" searching again.....")
  
  turn (20,0.5)
  dist , rot_y  = find_familiar()
  
 print(" I remember how to go back") 
 while  dist > d_th + 0.3  :
    
      if ready == 1:
          drive (30,1) 
          ready =0 
          dist, rot_y  = find_familiar()
          
      elif - a_th <= rot_y <= a_th :
          dist, rot_y  = find_familiar()
          drive(20,0.5)
          ready=0
      elif rot_y > a_th :
           turn(2,1)
           dist, rot_y   = find_familiar()
           
           ready=1
      elif rot_y < - a_th :
           turn(-2,1)
           dist, rot_y   = find_familiar()
           ready=1
 print("FINALLY I CAN DROP IT")
 R.release()
 print(" the box has been dropped successfully")
 drive(-30,1)

 
 

def main():
        
        print(" LETS START !")  
	turn( 7,2)
	drive(10,2)

        "I scan the enviroment"   	
	dist, rot_y, identity = scanner()
	print("curruntly held tokens : ",carried_tokens)
	
	"I append the identity obtained into the carried_tokens list"  
	carried_tokens.append(identity) 
	print("update carried_tokens :",carried_tokens)
	
	while len ( carried_tokens ) < 6 :
	 
	 "I scan for a new token which isnt familiar within the token list , approach ,grab it and then obtain its code"
	 identity = approach_grab() 
	 	 
	 "I find the reference token again and head towards it in order to drop the currenlty held token"
	 approach_release() 
	 
	 "I append the last identity obtained so I can update the reference"
	 carried_tokens.append(identity)
        
        print(" I am done working for today !!! ")
	exit()
main()	
	  



	 
 
