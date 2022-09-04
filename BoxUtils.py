from array import array


class OuterBox:
    def __init__(self):
        self.curr_height_min = 0

    #This function adds a package to the box such that the aspects commonly referenced for the box are fast.
    def add_package(x_placement : float, y_placement : float, dims : list):
        return None
    
    #This function creates a metric on which to compare performance for different agents. It's a rough estimate on the minimum bounding box for a 3d object with the aim of trading some accuracy for speed 
    #because of the large amount of simulations needed for getting a good result from an evolutionary algorithm. Additionally, this method allows a bias to be put on stacking in one direction so that later 
    #a bias against stacking higher rather than wider can be considered, a common preference in actual applications.
    def inner_bounding_box_volume():
        return None

    #This function creates a height map of a top-down view of the "partially filled box". This is the input for the agent to determine where it will "drop" the package. The relative aspect is that in order to 
    #normalize the input, the height at each spot is measured from the lowest height of the top of an uncovered box. 
    def top_down_relative_view():
        return None

