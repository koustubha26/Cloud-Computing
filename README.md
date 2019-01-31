# Resource Management in Cloud CLI

## Design and Implementation

### Overview
The main idea of implementing the software is to store all the hardware, image, flavor information in an in-memory data structure inside the program and keep track of the free resources when creating and deleting the instances and do other things like evacuation of a rack. It can accept user input of aggiestack command. Also, it can accept a filename as command line arguement to process the commands in the input file. This is useful for debugging and testing. The design is similar to a memory allocator, but with special policy. For the actual implementation, I used OOP design in Python. The main class are Hardware, Image, Flavor, Instance and Rack. The resource information are stored in the class and the class provides methods to manipulate the resource information. See below for the resources handled through data structure design.

### Resources

#### Hardware
The Hardware class maintain two lists (use dictionary in python), one rack list and one machine list. The machine name/rack name is the key and a dictionary for detailed information such as name, mem, vcpus, etc serves as value. The class provide many basic methods such as insert/delete rack/machine, get a machine information, listing the hardware information etc. The program keep track of two hardware entity one for configured hardware information, the other for the free resource information for creating and deleting instances.

#### Rack
The Rack class maintain a list of image using as the information of image cache in the Rack storage server. This class is used for the allocating policy (creating instance). The image cache information can be retrived from the Rack class using rack name.

#### Image
Image class is similar like Hardware class. It maintains a list (using dictionary) of image records.

#### Flavor
Flavor class is also similar like Hardware class. It maintains a list (using dictionary) of flavor records which is used to retrive the detailed flavor information.

#### Instance
Instance class keep track of all the instances created. It keep the information of instance name, which rack/machine it sits on and also the image and flavor information. This class is used when creating and removing instances and also migrating/listing instances.

## Mechanism
The whole create process is a exhaustive search algorithm with certain priorities. First, it will find whether there are rack that contains the image for the new instance, if exist, try to create a instance on that rack using first fit algorithm for finding a physical machine. If no machine can serve the instance, add the rack into a unavail_rack list. Second, if the rack which contains the image is out of resources, find a rack with the maximum space in the rack storage server (for storing the image cache). If no space for holding the new image, remove the oldest image in the image cache. This is done by mainting a LRU list for the image cache. Then, try to create a server on that rack. If no machine can fit for that instance, put that rack into the unavail_rack list. Third, keep looping until all the rack is checked, if all of the rack is unavailable, reporting error message that not enough resources available.
