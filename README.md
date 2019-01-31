# Resource Management in Cloud CLI

# 20 Design and Implementation
The whole software of Aggiestack is very similar like a Database command shell. It can accept user input of aggiestack command. Also it can accept a filename as command line arguement to process the commands in the input file. This is useful for batch processing and also useful for debug and testing. See the detailed run cases below.

The main idea of implementing the software is to store all the hardware, image, flavor information in a in-memory data structure inside the program and keep track of the free resouces when creating and deleting the instances and do other things such like evacuation of a rack. The design philosophy are similar like a memory allocator, but with speicial policy (for partC requirement). For the actuall implementation, I use OOP design in Python. The main class are Hardware, Image, Flavor, Instance and Rack. The resource information are stored in the class and the class provide method to manipulate with the resource information. See below for the detailed data structure design.
