"""
Match function for LabelManager

"""

def get_iou(bb1, bb2):
    # determine the coordinates of the intersection rectangle
    x_left = max(bb1['x1'], bb2['x1'])
    x_right = min(bb1['x2'], bb2['x2'])
    y_top = max(bb1['y1'], bb2['y1'])
    y_bottom = min(bb1['y2'], bb2['y2'])

    if x_right < x_left or y_bottom < y_top:
        return 0.0

    # The intersection of two axis-aligned bounding boxes is always an
    # axis-aligned bounding box
    intersection_area = (x_right - x_left) * (y_bottom - y_top)

    # compute the area of both AABBs
    bb1_area = (bb1['x2'] - bb1['x1']) * (bb1['y2'] - bb1['y1'])
    bb2_area = (bb2['x2'] - bb2['x1']) * (bb2['y2'] - bb2['y1'])

    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = intersection_area / float(bb1_area + bb2_area - intersection_area)
    return iou

def match_object(true_labels, model_labels, iou = 0.8, obj = "car"):
    """
    divide labels into: true positive, false positive, false negative
    """
    labels = {}
    for video in true_labels:
        labels[video] = [] 
        # TODO: Change testing to match this format  
        keys = set(true_labels[video].keys())
        keys = keys.union(set(model_labels[video].keys()))
        max_key = 0
        for key in keys:
            if key > max_key:
                max_key = key

        for i in range(max_key):
            flabels = {'tp': [], 'fn': [], 'fp': []}
            if i not in true_labels[video] and i not in model_labels[video]:
                pass
            elif i in true_labels[video] and i not in model_labels[video]:
                for label in true_labels[video][i]['labels']:
                    if label["category"] != obj:
                        continue
                    lb = {'name': true_labels[video][i]['name'], 'bbox':label['box2d']}
                    if "attributes" in label:
                        for key in label["attributes"]:
                            lb[key] = label["attributes"][key]
                    for key in label:
                        if key != "attributes" and key !="box2d":
                            lb[key] = label[key]
                    flabels['fn'].append(lb)
            elif i in model_labels[video] and i not in true_labels[video]:
                for label in model_labels[video][i]['labels']:
                    if label["category"] != obj:
                        continue
                    lb = {'name': model_labels[video][i]['name'], 'bbox':label['box2d'], 'category': label["category"]}
                    flabels['fp'].append(lb)
            else:
                matched = []
                for label in true_labels[video][i]['labels']:
                    if label["category"] != obj:
                        continue
                    bbox1 = label['box2d']
                    temp = False
                    for j, label2 in enumerate(model_labels[video][i]['labels']):
                        if label2["category"] != obj:
                            continue
                        if j in matched:
                            continue
                        bbox2 = label2['box2d']
                        iou = get_iou(bbox1, bbox2)
                        if iou > 0.8:
                            temp = True
                            lb = {'name': true_labels[video][i]['name'], 'bbox':label['box2d']}
                            if "attributes" in label:
                                for key in label["attributes"]:
                                    lb[key] = label["attributes"][key]
                            for key in label:
                                if key != "attributes" and key !="box2d":
                                    lb[key] = label[key]
                            
                            lb['model_bbox'] = label2['box2d']
                            flabels['tp'].append(lb)
                            matched.append(j)
                            break
                    if not temp:
                        lb = {'name': true_labels[video][i]['name'], 'bbox':label['box2d']}
                        if "attributes" in label:
                            for key in label["attributes"]:
                                lb[key] = label["attributes"][key]
                        for key in label:
                            if key != "attributes" and key !="box2d":
                                lb[key] = label[key]
                            
                        flabels['fn'].append(lb)
                for j, label2 in enumerate(model_labels[video][i]['labels']):
                    if j not in matched and label["category"] == obj:
                        lb = {'name': model_labels[video][i]['name'], 'bbox':label2['box2d'], 'category': label["category"]}
                        flabels['fp'].append(lb)
            labels[video].append(flabels)
    return labels


def match_object_virat(true_labels, model_labels, iou = 0.8):
    """
    divide labels into: true positive, false positive, false negative
    """
    labels = {}
    for video in true_labels:
        labels[video] = [] 
        keys = set(true_labels[video].keys())
        keys = keys.union(set(model_labels[video].keys()))
        max_key = 0
        for key in keys:
            if key > max_key:
                max_key = key
        for i in range(max_key):
            flabels = {'tp': [], 'fn': [], 'fp': []}
            if i not in true_labels[video] and i not in model_labels[video]:
                pass
            elif i in true_labels[video] and i not in model_labels[video]:
                for label in true_labels[video][i]:
                    lb = {'name': video, 'bbox':{"x1":label[0] , "x2": label[2], "y1": label[1], "y2": label[3]}}
                    flabels['fn'].append(lb)
            elif i in model_labels[video] and i not in true_labels[video]:
                for label in true_labels[video][i]:
                    lb = {'name': video, 'bbox':{"x1":label[0] , "x2": label[2], "y1": label[1], "y2": label[3]}}
                    flabels['fp'].append(lb)
            else:
                matched = []
                for label in true_labels[video][i]:
                    bbox1 = {"x1":label[0] , "x2": label[2], "y1": label[1], "y2": label[3]}
                    temp = False
                    lb = {'name': video, 'bbox':bbox1}
                    for j, label2 in enumerate(model_labels[video][i]):
                        if j in matched:
                            continue
                        bbox2 = {"x1":label2[0] , "x2": label2[2], "y1": label2[1], "y2": label2[3]}
                        iou = get_iou(bbox1, bbox2)
                        if iou > 0.8:
                            temp = True
                            lb['model_bbox'] = label2['box2d']
                            flabels['tp'].append(lb)
                            matched.append(j)
                            break
                    if not temp:
                        flabels['fn'].append(lb)
                for j, label2 in enumerate(model_labels[video][i]):
                    if j not in matched:
                        bbox2 = {"x1":label2[0] , "x2": label2[2], "y1": label2[1], "y2": label2[3]}
                        lb = {'name': video, 'bbox':bbox2}
                        flabels['fp'].append(lb)
            labels[video].append(flabels)
    return labels