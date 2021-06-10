import numpy as np
import tensorflow.compat.v1 as tf
import matplotlib.pyplot as plt
import cv2
import time
import requests as r

class DetectorAPI:
    def __init__(self, path_to_ckpt):
        self.path_to_ckpt = path_to_ckpt

        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(self.path_to_ckpt, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

        self.default_graph = self.detection_graph.as_default()
        self.sess = tf.Session(graph=self.detection_graph)
        self.image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
        self.detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
        self.detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
        self.detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
        self.num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')

    def processFrame(self, image):
        image_np_expanded = np.expand_dims(image, axis=0)
        start_time = time.time()
        (boxes, scores, classes, num) = self.sess.run(
            [self.detection_boxes, self.detection_scores, self.detection_classes, self.num_detections],
            feed_dict={self.image_tensor: image_np_expanded})
        end_time = time.time()

    #    print("Elapsed Time:", end_time-start_time)

        im_height, im_width,_ = image.shape
        boxes_list = [None for i in range(boxes.shape[1])]
        for i in range(boxes.shape[1]):
            boxes_list[i] = (int(boxes[0,i,0] * im_height),
                        int(boxes[0,i,1]*im_width),
                        int(boxes[0,i,2] * im_height),
                        int(boxes[0,i,3]*im_width))

        return boxes_list, scores[0].tolist(), [int(x) for x in classes[0].tolist()], int(num[0])

    def close(self):
        self.sess.close()
        self.default_graph.close()

def loadpic(src):
    img = r.get(src)
    img_file = open('loaded.jpg', 'wb')
    img_file.write(img.content)
    img_file.close()
    return cv2.imread('loaded.jpg')

####################################
model_path = 'frozen_inference_graph.pb'
odapi = DetectorAPI(path_to_ckpt=model_path)
#####################################

def human_count(src):
    threshold = 0.7
    img = loadpic(src)
    img = cv2.resize(img, (640, 480))
    boxes, scores, classes, num = odapi.processFrame(img)
    human_count = 0
    for i in range(len(boxes)):
        if classes[i] == 1 and scores[i] > threshold:
            human_count += 1
    return human_count

def get_people_number(cameras):
    mean_value = 0
    count = 0
    camera_number = cameras #вот тут поменял
    for i in camera_number:
        try:
            mean_value+= human_count('http://www.cactus.tv:8080/cam%d/preview.jpg'%i)
            count+=1
        except Exception as e:
            continue
    return mean_value



if __name__ == "__main__":
