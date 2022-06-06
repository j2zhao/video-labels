
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

        self.label_sizes = {'tp':0 , 'fn': 0, 'fp': 0}
        for video in self.videos:
            for i in range(len(self.labels[video])):
                self.frames_num += 1
                for type in self.labels[video][i]:
                    for j in range(len(self.labels[video][i][type])):
                        self.label_sizes[type] += 1
                        self.bb_num[type] += 1
                        self.labels[video][i][type][j]["error"] = []

        
    
    def add_attribute(self, name, funct):
        """
        Add an attribute to the image functions
        """
        for video in self.videos:
            for i in range(len(self.labels[video])):
                for type in self.labels[video][i]:
                    for j in range(len(self.labels[video][i][type])):
                        self.labels[video][i][type][j][name] = funct(self.labels[video][i][type][j], self.dire)

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