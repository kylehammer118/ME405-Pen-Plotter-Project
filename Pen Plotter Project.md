# Pen Plotter Project

#### Project Contents 

1. Introduction 
2. Mechanical Design 
3. Manufacturing
4. Electrical Design
5. Code Design
6. Key Features
7. Reflection 

------

**Introduction**

For this project we were tasked with designing a 2.5 DOF robot to draw shapes and plot user generated files from programs such as inkscape. Our design consists of 2 stepper motors and a linear actuator. One stepper motor drives a belt and pulley system that attaches to a whiteboard. The other stepper rotates an arm with a pen at the end which draws on the whiteboard. The linear actuator moves the pen up and down to make contact and break contact with the board. The actuator is located at the end of the arm. Our design also features an LCD display which displays messages to the user and shows the progress of the selected drawing as it is being run. 

------

**Mechanical Design** 

------

**Parts List**

| Part                                      | Price [$] | Quantity | Source     | Link                                                         |
| ----------------------------------------- | --------- | -------- | ---------- | ------------------------------------------------------------ |
| 1"  Aluminum Square Stock- 48"            | 24        | 2        | Home Depot | https://www.homedepot.com/p/Everbilt-1-in-x-48-in-Aluminum-Square-Tube-with-1-16-in-Thick-801307/204273940 |
| Linear Actuator 0.8"                      | 30        | 1        | Amazon     | https://www.amazon.com/dp/B07ZJ4B3WW?psc=1&ref=ppx_yo2ov_dt_b_product_details |
| I2C Serial LCD Screen                     | 12        | 1        | Amazon     | https://www.amazon.com/SunFounder-Serial-Module-Display-Arduino/dp/B019K5X53O/ref=asc_df_B019K5X53O/?tag=hyprod-20&linkCode=df0&hvadid=312760964359&hvpos=&hvnetw=g&hvrand=8567627865970401505&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9060121&hvtargid=pla-563014027379&th=1 |
| Particle Board  (24"x24")                 | 5         | 1        | Home Depot | N/A                                                          |
| Bearings (4mm inner diameter)             | 11        | 1        | Amazon     | https://www.amazon.com/dp/B08JKF33W8?psc=1&ref=ppx_yo2ov_dt_b_product_details |
| Stainless Steel Screws and  Nuts (metric) | 16        | 1        | Amazon     | https://www.amazon.com/dp/B094NHTRLS?ref=ppx_yo2ov_dt_b_product_details&th=1 |
| Whiteboard  (8.5"x11") and Pen            | 5.5       | 1        | Amazon     | https://www.amazon.com/gp/product/B00PRYQA4E/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&th=1 |
| Elbow brackets for M3 bolts               | 8         |          | Home Depot | N/A                                                          |
| Total                                     | 135.5     |          |            |                                                              |

------

**Manufacturing Plan - Mechanical** 

1. 3D print all connector parts. Pictures of these can be found in the 3D print section. Fusion and scad files have been provided in Github
2. Cut aluminum square stock to the following lengths
   - 2x 3.5” 
   - 2x 20.25”
   - 2x 9.5”
   - 1x 4.75”
   - 1x 15.5”
3. Sand off any burs on the square stock on a belt sander
4. Perform a rough assembly of the design to determine where to drill holes into the square stock. This includes press fitting the stock into the flanges and elbows and holding the elbow brackets on and positions of the stepper motors. 
5. Drill all holes in square stock and 3D printed parts using drill press
6. To assemble the base 
   1. Drill holes in the particle board and bolt flanges to the particle board
   2. Assemble square stock frame and place into flanges
   3. Bolt stepper motors into square stock 
   4. Put 3D printed gears onto stepper shaft and rotating shaft (through bearings) 
   5. Use JB weld or other similar strength adhesive to attach the whiteboard to the belt Stretch belt around the gearsWe suggest not drilling holes for the flange that sits under the bearings until you can judge how much tension you want to put in the belt then place the flange properly. 
7. Arm assembly
   1. Bolt through the hole at the end of the linear actuator and attach to Pen holder 3D printed part Slide the pen through the hole in the pen holder Press fit actuator into arm attachment 3D printed part Ensure pen can slide through the hole for itDrill arm attachment into square tube for the arm Drill square tube onto gear attachment Drill holes through counterweight and attach to square tube using angle bracketsMount Microcontroller to the board Attach __ to microcontrollers Drill through particle board and bolt m3 bolts into ___

------

**Wiring Diagram**

**![img](https://lh4.googleusercontent.com/uPaN4ypytM9g5GnSsKol537hxS--PnCq5q55aGC4sOGV7iI6UvT8GOqwdcnGNsN6-TmGR-n56NzcDjoij4Ma_5jXwfAT3W0KuBbiyo9Nw9bTrAQSWjg1bANHrenD-g5Fl6AAbUcr60SY6a2sAg)**

**Electrical Parts/Equipment:**

1. Nucleo STML476RG
2. Shoe of Brian
3. X-NUCLEO-IHM04A1 dual brush DC motor driver expansion board for STM32 Nucleo
4. Dual Motor Driver BoardTMC4210 TMC2208Capacitor 
5. 2x Power Supply = HP 6543A DC Power Supply
6. Linear Actuator 
7. 2x Stepper Motors
8. I2C Serial LCD Screen 
9. Wiring
10. Wire cutters 
11. Soldering Iron

All wiring done using the screw terminals located on the Shoe of Brian, Motor Driver Board and X-Nucleo. Only modifications we made were to the Stepper driver board assembly. To start we were given the motor driver board with surface mount components pre-soldered. We soldered the pins for connections with the Shoe of Brian and limit switches as well as the capacitor and the connections to the two MOT chips. We then attached a heat sink to the top of each chip using adhesive.  For the connections between the Shoe of Brian and the stepper driver board we used pre-crimped wires that were put into a rectangular wiring harness to keep our wiring organized. Our wiring can be seen in the pictures and wiring diagram below. ![img](https://lh5.googleusercontent.com/46g2O8rAmkTF9slxGz8ttIcdbdXMP8dxX1wTpi_BlpJW_dvxci9uOe0qdQjToW_SJ5q1uwQD92End4CDpe8ssxa9EuhFcqLeURIJeYhg-_JI6GRzeoTMJ5bAldeLWA3NMrGqHOq-qfwQ84xPOA) Figure 1: Shoe of Brian screw terminal connections from Stepper Board ![img](https://lh5.googleusercontent.com/F0RLznJNnCOLJWGZkLkg8QlTD59ahWz0zd8kFcjosl3Ucxy_zIjiyYs3-BhqA8trTb-rEH4B-jtdMqAJ6qzG1IJfnhLHSpDBtUmq_rbCU5-uPiQTxRp1q0IIrSXUPR-l6U_XdvwAlY5ceZ1Ohg) Figure 2: Wiring harness connections on the Stepper Board.  

To connect the stepper motors, we had to modify them. We stripped off the PCB that they came with by heating the pads and then applying a levering force. We checked which wires are in phase with a multimeter and soldered them directly to the 4 exposed terminals and then paired them to put into matching screw terminals (1A & 1B, 2A & 2B). We twisted together each wire pair that was in phase to keep track of them easier. We connected the power supply to the Ground and MVIN screw terminals on the stepper board. ![img](https://lh4.googleusercontent.com/-nN8b4qPCy3afz24eKBNzc0EZcDEAeinMZb7DPxQHjCvpf9JHXTqPcOX-tDCd4IbKNwllHBioV1Gf8WRO_lzuLUzCWfpvvC2vFTkS54INVVkfr7lHWa_mXfqe0aXU9HYlz7Dz8PlD3lKWpUmGw) Figure 4: Stepper Motor Soldered Connections. 