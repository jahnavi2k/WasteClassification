import os
import cv2
import tensorflow as tf
import numpy as np
from keras.preprocessing import image
import pandas as pd
from PIL import Image
from tensorflow.python.util import compat
from tensorflow.core.protobuf import saved_model_pb2
from google.protobuf import text_format
import pprint
import json
from object_detection.utils import visualization_utils as vis_util
from object_detection.utils import dataset_util, label_map_util
from object_detection.protos import string_int_label_map_pb2


def reconstruct_graph(pb_path):
    if not os.path.isfile(pb_path):
        print("Error: %s not found" % pb_path)

    print("Reconstructing Tensorflow model")
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.compat.v1.GraphDef()
        with tf.io.gfile.GFile(pb_path, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')
    print("Success!")
    return detection_graph

# visualize detection
def image2np(image):
    (w, h) = image.size
    return np.array(image.getdata()).reshape((h, w, 3)).astype(np.uint8)

def image2tensor(image):
    npim = image2np(image)
    return np.expand_dims(npim, axis=0)


def detect(detection_graph, test_image_path, category_index):
    with detection_graph.as_default():
        gpu_options = tf.compat.v1.GPUOptions(per_process_gpu_memory_fraction=0.01)
        with tf.compat.v1.Session(graph=detection_graph,config=tf.compat.v1.ConfigProto(gpu_options=gpu_options)) as sess:
            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
            detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
            detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
            detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
            num_detections = detection_graph.get_tensor_by_name('num_detections:0')

           

            image = Image.open(test_image_path)
            (boxes, scores, classes, num) = sess.run(
                [detection_boxes, detection_scores, detection_classes, num_detections],
                feed_dict={image_tensor: image2tensor(image)}
            )
            # print(boxes, scores, classes, num, category_index)
            npim = image2np(image)
            vis_util.visualize_boxes_and_labels_on_image_array(npim,
                np.squeeze(boxes),
                np.squeeze(classes).astype(np.int32),
                np.squeeze(scores),
                category_index,
                use_normalized_coordinates=True,
                line_thickness=15)
            cv2.imwrite("annotated.jpg", npim)


def predict_result(filename):
    ANNOTATIONS_FILE = os.path.join(os.path.join(os.getcwd(), 'trashAlwaysCan'), 'annotations.json')
    NCLASSES = 60

    with open(ANNOTATIONS_FILE) as json_file:
        data = json.load(json_file)
        
    categories = data['categories']
    label_map = label_map_util.load_labelmap(os.path.join(os.path.join(os.getcwd(), 'trashAlwaysCan'), 'labelmap.pbtxt'))
    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NCLASSES, use_display_name=True)
    category_index = label_map_util.create_category_index(categories)


    detection_graph = reconstruct_graph(os.path.join(os.path.join(os.getcwd(), 'trashAlwaysCan'), "ssd_mobilenet_v2_taco_2018_03_29.pb"))

    detect(detection_graph, os.path.join(os.path.join(os.getcwd(), 'media'), filename), category_index)


# def predict(img_path):
#      labels = {0: 'cardboard', 1: 'glass', 2: 'metal', 3: 'paper', 4: 'plastic', 5: 'trash'}
#      img = image.load_img(img_path, target_size=(300, 300))
#      img = image.img_to_array(img, dtype=np.uint8)
#      img = np.array(img) / 255.0
#     #plt.imshow(img.squeeze())
     
#      model = tf.keras.models.load_model("trained_model.h5")
#      prediction = model.predict(img[np.newaxis, ...])
#      probability = np.max(prediction[0], axis=-1)
#      print("p.shape:", prediction.shape)
#      print("prob", probability)
#      predicted_class = labels[np.argmax(prediction[0], axis=-1)]
#      #os.remove(img_path)
#      print("Classified Label:", predicted_class)
#      return(str(predicted_class)+" \n Probability:"+str(probability))

# print(predict('trash.jpg'))