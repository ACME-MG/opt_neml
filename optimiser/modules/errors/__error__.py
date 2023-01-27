"""
 Title:         Error
 Description:   Contains the basic structure for an error class
 Author:        Janzen Choi

"""

# The Error Class
class Error:

    # Constructor
    def __init__(self, name, exp_curves):
        self.name = name
        self.exp_curves = exp_curves

    # Returns the name of the error
    def get_name(self):
        return self.name

    # Returns the experimental curve
    def get_exp_curves(self):
        return self.exp_curves

    # Prepares the object for evaluation (placeholder)
    def prepare(self):
        raise NotImplementedError
    
    # Returns an error (placeholder)
    def get_value(self):
        raise NotImplementedError