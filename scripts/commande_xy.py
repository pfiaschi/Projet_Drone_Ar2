#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from ardrone_autonomy.msg import Navdata # for receiving navdata feedback
from nav_msgs.msg	import Odometry
# variables globales
#altitudeRef = 400 # altitude ref en mm
XRef = 700
YRef = 900
commande = Twist()

# initialisation du noeud
rospy.init_node('commande_xy', anonymous=True)

# declaration d'un publisher sur le topic de commande
pubCommande = rospy.Publisher('/cmd_vel', Twist, queue_size=10)


# fonction de lecture de la mesure et d'envoi de la commande
def calculCommandeXY(odo):
	# lecture donnee altitude
	 X = odo.pose.pose.position.x
	 Y = odo.pose.pose.position.y
	# affichage sur la console (pour info)
	rospy.loginfo(rospy.get_caller_id() + "posX (mm) = %f", odo.pose.pose.position.x)
	rospy.loginfo(rospy.get_caller_id() + "posY (mm) = %f", odo.pose.pose.position.y)

	# calcul de la commande
	
	
	commande.linear.x =(XRef-odo.pose.pose.position.x)*0.001
	commande.linear.y =(YRef-odo.pose.pose.position.y)*0.001
	# --------------------


	# envoi de la commande
	pubCommande.publish(commande)	


# declaration d'un subscriber : appelle claculCommandeZ a chq arrivee d'une donnee sur le topic Navdata
rospy.Subscriber("/ardrone/odometry", Odometry, calculCommandeXY)



# fonction main executee en boucle 
if __name__ == '__main__':

	rospy.spin()

