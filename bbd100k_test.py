"""
test LabelManager for bbd100k

"""
from numpy import append
from manager.label_manager import LabelManager
from manager.match import match_object
from manager import simple_attributes
from manager.position_error import *

from discontinuity_errors.breaks import *
# define labels/LabelManager

true_labels = [] # replace with true labels bdd100k
yolo_labels = [] # replace with yolo labels bdd100k

manager = LabelManager(true_labels, yolo_labels, match_object, img_dir = "") # replace img_dir with image directory

# add attributes -> from simple attributes
manager.add_attribute('img_size', simple_attributes.img_size)
manager.add_attribute('img_color', simple_attributes.avg_bb_wrapper(simple_attributes.img_color))
manager.add_attribute('img_lumin', simple_attributes.avg_bb_wrapper(simple_attributes.img_lumin))
manager.add_attribute('img_edges', simple_attributes.avg_bb_wrapper(simple_attributes.img_edges))

# evaluate position errors -> dashboard error
loc_error = define_location_error(x_center=(0.8, 1))

shape_error = define_shape_error(min_width=0.75)

dashboard_error = and_error(loc_error, shape_error)
errors, label_size = manager.eval_error("dashboard_error", dashboard_error)

print(errors) # evaluate errors based on these criteria (maybe more), and see if we 
print(label_size) # TODO: add more

# evaluate breaks -> try breaks function, and display kpi

metrics  = manager.get_metric(metric_funct)

breaks = find_breaks(manager.labels, metrics)

# TODO: evaluate how efficient we are at finding breaks -> with visualization and metrics -> maybe play around with hyper parameters


# display KPI to evaluate if RDD works -> play around with all parameters
display_kpi(manager.labels, video="", start_frame= 0, kpi_funct=avg_kpi, attribute='img_color') #video -> video name to display, start_frame +> where to display -> find by hand
