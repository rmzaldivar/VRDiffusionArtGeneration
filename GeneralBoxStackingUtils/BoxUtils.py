import numpy as np

class OuterBox:
    """
    This class defines an outer box object that represents the container all 
    boxes are to be stored in. It's represented as a 2D numpy array where each 
    value is the height at each point in the container as seen by a viewer 
    seeing the container from the top down. 
    """
    def __init__(self):
        self.curr_container = np.zeros((1000,1000))

    def add_package(self, x_placement : float, y_placement : float, package_dims : tuple):
        """
        This function adds a package to the box such that the aspects commonly referenced 
        for the box are fast.

        :param x_placement: Float in range (0,1000) to normalize problem input. Represents center 
            of package in x coordinate
        :param y_placement: Float in range (0,1000) to normalize problem input. Represents center 
            of package in y coordinate
        :param dims: A tuple of 3 numbers (x,y,z) scaled with respect to overall box size that 
            represent the 3 dimensions of a package.
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

        #check if there is a stable foundation for a box by seeing if the area it would be placed
        #on is all the same height. Disincentivize this by a factor if not
        off_balance_factor = 1
        if np.all(self.curr_container[x_placement-package_dims[0]/2:x_placement+package_dims[0]/2+1][y_placement-package_dims[1]/2:y_placement+package_dims[1]/2]
                    == self.curr_container[x_placement-package_dims[0]/2][y_placement-package_dims[1]/2]):
                    off_balance_factor = 10
        
        #add value of height to the block of values covered by the new package
        self.curr_container[x_placement-package_dims[0]/2:x_placement+package_dims[0]/2+1][y_placement-package_dims[1]/2:y_placement+package_dims[1]/2] += off_balance_factor * package_dims[2]
        
        return True
    
    def inner_bounding_box_volume(self, height_bias = 1):
        """
        This function creates a metric on which to compare performance for different agents.
        It's a rough estimate on the minimum bounding box for a 3d object with the aim of 
        trading some accuracy for speed because of the large amount of simulations needed for 
        getting a good result from an evolutionary algorithm. Additionally, this method allows 
        a bias to be put on stacking in one direction so that later a bias against stacking 
        higher rather than wider can be considered, a common preference in actual applications.
        
        :param height_bias: A value that can be increased to incentivize placing boxes in a
        wider configuration rather than taller to simulate how this should be done in real
        scenarios to have better balance
        """
        container_dims = self.curr_container.shape

        #find overall height first
        bounding_box_height = height_bias * np.amax(self.curr_container)

        #check how many rows are empty from left to right and then vice versa to get
        #the width
        l2r_zero_cols = 0
        for col in self.curr_container.T:
            if np.all(col == 0):
                l2r_zero_cols += 1
            else:
                break
        r2l_zero_cols = 0
        for col in np.flipud(self.curr_container).T:
            if np.all(col == 0):
                r2l_zero_cols += 1
            else:
                break
        bounding_box_width = container_dims[1] - l2r_zero_cols - r2l_zero_cols
        if bounding_box_width < 0:
            bounding_box_width = 0

        #check how many columns are empty from top to bottom and then vice versa
        #to get the length
        t2b_zero_rows = 0
        for row in self.curr_container:
            if np.all(row == 0):
                t2b_zero_rows += 1
            else:
                break
        b2t_zero_rows = 0
        for row in np.flipud(self.curr_container):
            if np.all(row == 0):
                b2t_zero_rows += 1
            else:
                break
        bounding_box_length = container_dims[0] - t2b_zero_rows - b2t_zero_rows
        if bounding_box_length < 0:
            bounding_box_length = 0

        return bounding_box_height * bounding_box_width * bounding_box_length

