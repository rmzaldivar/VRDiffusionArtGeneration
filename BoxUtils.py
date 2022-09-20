import numpy as np


class OuterBox:
    def __init__(self):
        self.curr_height_min = 0
        self.curr_box = np.zeros((1000,1000))

    def add_package(self, x_placement : float, y_placement : float, package_dims : tuple):
        """
        This function adds a package to the box such that the aspects commonly referenced for the box are fast.

        x_placement: Float in range (0,1000) to normalize problem input. Represents center of package in x coordinate
        y_placement: Float in range (0,1000) to normalize problem input. Represents center of package in y coordinate
        dims: A tuple of 3 numbers (x,y,z) scaled with respect to overall box size that represent the 3 dimensions of a package.
        """
        #check for invalid box size, shouldn't happen if everything else is working right
        if package_dims[0] > 1000 or package_dims[1] > 1000:
            return False

        #first confirm original center is valid for the package size
        #otherwise shift center to conform to overall box size
        if x_placement-package_dims[0]/2 < 0: 
            x_placement += x_placement-package_dims[0]//2
        if x_placement+package_dims[0]/2 > 1000:
            x_placement -= x_placement-package_dims[0]//2

        if y_placement-package_dims[1]/2 < 0: 
            y_placement += y_placement-package_dims[0]//2
        if y_placement+package_dims[1]/2 > 1000:
            y_placement -= y_placement-package_dims[0]//2

        #add value of height to the block of values covered by the new package
        self.curr_box[x_placement-package_dims[0]/2:x_placement+package_dims[0]/2+1][y_placement-package_dims[1]/2:y_placement+package_dims[1]/2] += package_dims[2]
        
        return True
    
    #This function creates a metric on which to compare performance for different agents. It's a rough estimate on the minimum bounding box for a 3d object with the aim of trading some accuracy for speed 
    #because of the large amount of simulations needed for getting a good result from an evolutionary algorithm. Additionally, this method allows a bias to be put on stacking in one direction so that later 
    #a bias against stacking higher rather than wider can be considered, a common preference in actual applications.
    def inner_bounding_box_volume(self):
        return None

