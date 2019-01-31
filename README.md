# Resource Management in Cloud CLI

## Design and Implementation

### Overview
The main idea of implementing the software is to store all the hardware, image, flavor information in a in-memory data structure inside the program and keep track of the free resouces when creating and deleting the instances and do other things such like evacuation of a rack. It can accept user input of aggiestack command. Also it can accept a filename as command line arguement to process the commands in the input file. This is useful for batch processing and also useful for debug and testing. The design philosophy are similar like a memory allocator, but with speicial policy. For the actual implementation, I used OOP design in Python. The main class are Hardware, Image, Flavor, Instance and Rack. The resource information are stored in the class and the class provide method to manipulate with the resource information. See below for the detailed data structure design.

### Data Structures

#### Hardware
The Hardware class maintain two lists (use dictionary in python), one rack list and one machine list. The machine name/rack name as key and a dictionary for detailed information such as name, mem, vcpus, etc as value. The class provide many basic methods such as insert/delete rack/machine, get a machine information, listing the hardware information and etc. The program keep track of two Hardware entity one for configured hardware information, the other for the free resource information for creating and deleting instances.

#### Rack
The Rack class maintain a list of image using as the information of image cache in the Rack storage server. This class is used for the allocating policy (creating instance). The image cache information can be retrived from the Rack class using rack name.

#### Image
Image class is similar like Hardware, it maintains a list (using dictionary) of image records.

#### Flavor
Flavor class is also similar like Hardware, it maintains a list (using dictionary) of flavor records. Which used to retrive the detailed flavor information.

#### Instance
Instance class keep track of all the instances created. It keep the information of instance name, which rack/machine it sits on and also the image and flavor information. This class is used when creating and removing instances and also migrating/listing instances.
