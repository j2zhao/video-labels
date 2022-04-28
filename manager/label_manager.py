
"""
Manager for Video Labels: convert into appropriate funmat
"""

from collections import defaultdict


class LabelManager(object):
    def __init__(self, true_labels, model_labels, match, img_dir) -> None:
        """initialize labels storage
        match function must return with this format
        format: {video: {index: {type: [{"image_name": str, attributes: blob, "bounding box": bbox, "errors": errors}]}}}
        
        """
        self.dire = img_dir
        self.labels = match(true_labels, model_labels)
        self.videos = list(true_labels.keys())
        self.video_num = len(self.videos)
        self.frames_num = 0
        self.bb_num = defaultdict(int)
        for video in self.videos:
            for i in range(len(self.labels[video])):
                self.frames_num += 1
                for type in self.labels[video][i]:
                    for j in range(len(self.labels[video][i][type])):
                        self.bb_num[type] += 1
                        self.labels[video][i][type][j]["error"] = {}
    
    def add_attribute(self, name, funct):
        """
        Add an attribute to the image functions
        """
        for video in self.videos:
            for i in range(len(self.labels[video])):
                for type in self.labels[video][i]:
                    for j in range(len(self.labels[video][i][type])):
                        self.labels[video][i][type][j][name] = funct(self.labels[video][i][type][j], self.dire)

    def eval_error(self, name, funct):
        """
        Returns number of attribute match for each type of bbox
        """
        errors = defaultdict(int)
        for video in self.videos:
            for i in range(len(self.labels[video])):
                for type in self.labels[video][i]:
                    for j in range(len(self.labels[video][i][type])):
                        self.labels[video][i][type][j]['error'][name] = funct(self.labels[video][i][type][j])
                        if self.labels[video][i][type][j]['error'][name] == True:
                            errors[type] += 1
        
        return errors
                            
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
