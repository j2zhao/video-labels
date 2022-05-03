"""
Define Errors by shape and/or location in video

"""
import math

def define_location_error(x_center = None, y_center = None):
    """
    define errors function for location
    xcenter, and ycenter are two-value tuples that define ranges
    can be percentage or absolute
    """
    def error_funct(label):
        bb_center = ((label['bbox']['x1'] + label['bbox']['x2'])/2, (label['bbox']['y1'] + label['bbox']['y2'])/2)

        if "img_size" in label:
            img_size = label['img_size']
        else:
            img_size = None

        error = True
        if x_center != None:
            if (x_center[0] <= 1 or x_center[1] <= 1) and img_size == None:
                raise ValueError("Can't use percentage without image size")
            elif x_center[0] <= 1:
                x_center[0] = math.floor(x_center[0]*img_size[0])
            elif x_center[1] <= 1:
                x_center[1] = math.ceil(x_center[1]*img_size[1])
            
            if bb_center[0] < x_center[0] or bb_center[0] > x_center[1]:
                error = False
        
        if y_center != None:
            if (y_center[0] <= 1 or y_center[1] <= 1) and img_size == None:
                raise ValueError("Can't use percentage without image size")
            elif y_center[0] <= 1:
                y_center[0] = math.floor(y_center[0]*img_size[1])
            elif y_center[1] <= 1:
                y_center[1] = math.ceil(y_center[1]*img_size[1])
            if bb_center[1] < y_center[0] or bb_center[1] > y_center[1]:
                error = False
        return error
    return error_funct

def define_shape_error(min_width = None, max_width = None, min_length= None, max_length = None):
    """
    define errors function for shape
    
    """
    def error_funct(label):
        bb_size = (label['bbox']['x2'] - label['bbox']['x1'], label['bbox']['y2'] - label['bbox']['y1'])
        if "img_size" in label:
            img_size = label['img_size']
        else:
            img_size = None
        error = True

        if min_width != None:
            if min_width <= 1 and img_size == None:
                raise ValueError("Can't use percentage without image size")
            elif min_width <= 1:
                min_width = min_width*img_size[0]
            if bb_size[0] < min_width:
                error = False
        if max_width != None:
            if max_width <= 1 and img_size == None:
                raise ValueError("Can't use percentage without image size")
            elif max_width <= 1:
                max_width = max_width*img_size[0]
            if bb_size[0] > max_width:
                error = False

        if min_length != None:
            if min_length <= 1 and img_size == None:
                raise ValueError("Can't use percentage without image size")
            elif min_length <= 1:
                min_length = min_length*img_size[1]
            if bb_size[0] < min_length:
                error = False

        if max_length != None:
            if max_length <= 1 and img_size == None:
                raise ValueError("Can't use percentage without image size")
            elif max_length <= 1:
                max_length = max_length*img_size[1]
            if bb_size[0] > max_length:
                error = False
        return error
    return error_funct

def and_error(loc_funct, shape_funct):
    """
    define combination function
    """
    def error_funct(label):
        e1 = loc_funct(label)
        e2 = shape_funct(label)
        return e1 and e2
    return error_funct

def or_error(loc_funct, shape_funct):
    """
    define combination function
    """
    def error_funct(label):
        e1 = loc_funct(label)
        e2 = shape_funct(label)
        return e1 or e2
    return error_funct