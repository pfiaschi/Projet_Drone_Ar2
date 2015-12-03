#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from ardrone_autonomy.msg import Navdata # for receiving navdata feedback

# variables globales
altitudeRef = 500 # altitude ref en mm
altitudeRefMin = 500
altitudeRefMax = 1500

commande = Twist()
valid = 0
counter = 0
Valid_Top = 0

# initialisation du noeud
rospy.init_node('commande_z', anonymous=True)

# declaration d'un publisher sur le topic de commande
pubCommande = rospy.Publisher('/cmd_vel', Twist, queue_size=10)


# fonction de lecture de la mesure et d'envoi de la commande
def calculCommandeZ(data):
	global altitudeRef
	global counter
	global Valid_Top
	# lecture donnee altitude
	altitude = data.altd    
	# affichage sur la console (pour info)
	rospy.loginfo(rospy.get_caller_id() + "altitude (mm) = %f", data.altd)

	# calcul de la commande
	
	
	commande.linear.z =(altitudeRef-data.altd)*0.001
	
	# --------------------

	
	# envoi de la commande
	
	if counter == 100:
		counter = 0
		
	if altitudeRef == altitudeRefMin:
		Valid_Top = 1
	if altitudeRef == altitudeRefMax:
		Valid_Top = 0 
	if altitude <= (altitudeRef + 40) and altitude >= (altitudeRef - 40):
		counter = counter + 1
	if Valid_Top == 1 and counter == 100:
		altitudeRef = altitudeRef + 200
	if Valid_Top == 0 and counter == 100:
		altitudeRef = altitudeRef - 200
		
		
	
	
	
	
	pubCommande.publish(commande)
	
# declaration d'un subscriber : appelle claculCommandeZ a chq arrivee d'une donnee sur le topic Navdata
rospy.Subscriber("/ardrone/navdata", Navdata, calculCommandeZ)




# fonction main executee en boucle 
if __name__ == '__main__':

	rospy.spin()

