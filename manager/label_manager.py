
"""
Manager for Video Labels: convert into appropriate funmat
"""

from collections import defaultdict
from matplotlib import pyplot as plt
from torch import Def
import cv2
import os

class LabelManager(object):
    def __init__(self, true_labels, model_labels, match, base_dir, is_image = True) -> None:
        """initialize labels storage
        match function must return with this format
        format: {video: {index: {type: [{"image_name": str, attributes: blob, "bounding box": bbox, "errors": errors}]}}}
        
        """
        self.dire = base_dir
        self.labels = match(true_labels, model_labels)
        self.videos = list(true_labels.keys())
        self.video_num = len(self.videos)
        self.frames_num = 0
        self.bb_num = defaultdict(int)
        self.is_image = is_image
        self.label_sizes = {'tp':0 , 'fn': 0, 'fp': 0}
        for video in self.videos:
            for i in range(len(self.labels[video])):
                self.frames_num += 1
                for type in self.labels[video][i]:
                    for j in range(len(self.labels[video][i][type])):
                        self.label_sizes[type] += 1
                        self.bb_num[type] += 1
                        self.labels[video][i][type][j]["error"] = []
        
    
    def add_attribute(self, name, funct, need_img = False):
        """
        Add an attribute to the image functions
        """
        if not need_img:
            for video in self.videos:
                for i in range(len(self.labels[video])):
                    for type in self.labels[video][i]:
                        for j in range(len(self.labels[video][i][type])):
                            #self.labels[video][i][type][j][name] = funct(self.labels[video][i][type][j], self.dire)
                            self.labels[video][i][type][j][name] = funct(self.labels[video][i][type][j])
        
        else:
            if self.is_image:
                for video in self.videos:
                    for i in range(len(self.labels[video])):
                        for type in self.labels[video][i]:
                            for j in range(len(self.labels[video][i][type])):
                                #self.labels[video][i][type][j][name] = funct(self.labels[video][i][type][j], self.dire)
                                label = self.labels[video][i][type][j]
                                name = label['name']
                                dire = os.path.join(self.dir, name)
                                img = cv2.imread(dire)
                                self.labels[video][i][type][j][name] = funct(label, img)
            
            else:
                for video in self.videos:
                    dire = os.path.join(self.dir, video)
                    cap = cv2.VideoCapture(dire)
                    for i in range(len(self.labels[video])):
                        ret, frame = cap.read()
                        if not ret:
                            raise ValueError("Video Error")
                        for type in self.labels[video][i]:
                            for j in range(len(self.labels[video][i][type])):
                                #self.labels[video][i][type][j][name] = funct(self.labels[video][i][type][j], self.dire)
                                label = self.labels[video][i][type][j]
                                self.labels[video][i][type][j][name] = funct(label, frame)


    def eval_attribute(self, name, cat = 'continous'):
        if cat == 'continous':
            eval = defaultdict(list)

        elif cat == 'discrete':
            eval = defaultdict(dict)
            raise ValueError("Currently not supporting discrete") # add if needed

        for video in self.videos:
            for i in range(len(self.labels[video])):
                for type in self.labels[video][i]:
                    for j in range(len(self.labels[video][i][type])):
                        if cat == 'continous':
                            eval[type].append(self.labels[video][i][type][j][name])
                        else:
                            val = self.labels[video][i][type][j][name]
                            if val not in eval[type]:
                                eval[type][val] = 0
                            else:
                                eval[type][val] += 1

        if cat == 'continous':
            for type in eval:
                plt.hist(eval[type])
                plt.title("{}: {}".format(name, type))
                plt.show()

    def eval_error(self, name, funct, all = False):
        """
        Returns number of attribute match for each type of bbox
        """
        errors = defaultdict(int)
        label_sizes = defaultdict(int)
        
        for video in self.videos:
            for i in range(len(self.labels[video])):
                for type in self.labels[video][i]:
                    for j in range(len(self.labels[video][i][type])):
                        if not all and len(self.labels[video][i][type][j]['error']) != 0:
                            continue
                        
                        label_sizes[type] += 1
                        error = funct(self.labels[video][i][type][j])
                        if error:
                            errors[type] += 1
                            self.labels[video][i][type][j]['error'].append(name) 
        return errors, label_sizes

    def remove_error(self, name):
        pass
    
    def fetch_no_errors(self):
        """
        fetch a subset of labels with no error explainations
        """
        no_errors = {}
        for video in self.videos:
            no_errors[video] = []
            for i in range(len(self.labels[video])):
                flabels = {}
                for type in self.labels[video][i]:
                    flabels[type] = []
                    for j in range(len(self.labels[video][i][type])):
                        if len(self.labels[video][i][type][j]['error']) == 0:
                            flabels[type].append(self.labels[video][i][type][j])

                no_errors.video.append(flabels)
        return no_errors

    def get_metric(self, metric_funct):
        metrics = {}
        for video in self.videos:
            metrics[video] = []
            for i in range(len(self.labels[video])):
                m = metric_funct(self.labels[video][i])
                metrics[video].append(m)
        
        return metrics        