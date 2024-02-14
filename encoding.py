
import tkinter
import customtkinter
import os
import csv
import dlib
import PIL.Image
import shutil 
from PIL import ImageTk, Image
import pandas
from CTkMessagebox import CTkMessagebox

import numpy as np
from PIL import ImageFile


ImageFile.LOAD_TRUNCATED_IMAGES = True

face_detector = dlib.get_frontal_face_detector()


pose_predictor_68_point = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

pose_predictor_5_point = dlib.shape_predictor('shape_predictor_5_face_landmarks.dat')


cnn_face_detector = dlib.cnn_face_detection_model_v1('mmod_human_face_detector.dat')


face_encoder = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')


def _rect_to_css(rect):
    """
    Convert a dlib 'rect' object to a plain tuple in (top, right, bottom, left) order

    :param rect: a dlib 'rect' object
    :return: a plain tuple representation of the rect in (top, right, bottom, left) order
    """
    return rect.top(), rect.right(), rect.bottom(), rect.left()


def _css_to_rect(css):
    """
    Convert a tuple in (top, right, bottom, left) order to a dlib `rect` object

    :param css:  plain tuple representation of the rect in (top, right, bottom, left) order
    :return: a dlib `rect` object
    """
    return dlib.rectangle(css[3], css[0], css[1], css[2])


def _trim_css_to_bounds(css, image_shape):
    """
    Make sure a tuple in (top, right, bottom, left) order is within the bounds of the image.

    :param css:  plain tuple representation of the rect in (top, right, bottom, left) order
    :param image_shape: numpy shape of the image array
    :return: a trimmed plain tuple representation of the rect in (top, right, bottom, left) order
    """
    return max(css[0], 0), min(css[1], image_shape[1]), min(css[2], image_shape[0]), max(css[3], 0)


def face_distance(face_encodings, face_to_compare):
    """
    Given a list of face encodings, compare them to a known face encoding and get a euclidean distance
    for each comparison face. The distance tells you how similar the faces are.

    :param face_encodings: List of face encodings to compare
    :param face_to_compare: A face encoding to compare against
    :return: A numpy ndarray with the distance for each face in the same order as the 'faces' array
    """
    if len(face_encodings) == 0:
        return np.empty((0))

    return np.linalg.norm(face_encodings - face_to_compare, axis=1)



def load_image_file(file, mode='RGB'):
    """
    Loads an image file (.jpg, .png, etc) into a numpy array

    :param file: image file name or file object to load
    :param mode: format to convert the image to. Only 'RGB' (8-bit RGB, 3 channels) and 'L' (black and white) are supported.
    :return: image contents as numpy array
    """
    im = PIL.Image.open(file)
    if mode:
        im = im.convert(mode)
    return np.array(im)



def _raw_face_locations(img, number_of_times_to_upsample=1, model="hog"):
    """
    Returns an array of bounding boxes of human faces in a image

    :param img: An image (as a numpy array)
    :param number_of_times_to_upsample: How many times to upsample the image looking for faces. Higher numbers find smaller faces.
    :param model: Which face detection model to use. "hog" is less accurate but faster on CPUs. "cnn" is a more accurate
                  deep-learning model which is GPU/CUDA accelerated (if available). The default is "hog".
    :return: A list of dlib 'rect' objects of found face locations
    """
    if model == "cnn":
        return cnn_face_detector(img, number_of_times_to_upsample)
    else:
        return face_detector(img, number_of_times_to_upsample)


def face_locations(img, number_of_times_to_upsample=1, model="hog"):
    """
    Returns an array of bounding boxes of human faces in a image

    :param img: An image (as a numpy array)
    :param number_of_times_to_upsample: How many times to upsample the image looking for faces. Higher numbers find smaller faces.
    :param model: Which face detection model to use. "hog" is less accurate but faster on CPUs. "cnn" is a more accurate
                  deep-learning model which is GPU/CUDA accelerated (if available). The default is "hog".
    :return: A list of tuples of found face locations in css (top, right, bottom, left) order
    """
    if model == "cnn":
        return [_trim_css_to_bounds(_rect_to_css(face.rect), img.shape) for face in _raw_face_locations(img, number_of_times_to_upsample, "cnn")]
    else:
        return [_trim_css_to_bounds(_rect_to_css(face), img.shape) for face in _raw_face_locations(img, number_of_times_to_upsample, model)]



def _raw_face_locations_batched(images, number_of_times_to_upsample=1, batch_size=128):
    """
    Returns an 2d array of dlib rects of human faces in a image using the cnn face detector

    :param images: A list of images (each as a numpy array)
    :param number_of_times_to_upsample: How many times to upsample the image looking for faces. Higher numbers find smaller faces.
    :return: A list of dlib 'rect' objects of found face locations
    """
    return cnn_face_detector(images, number_of_times_to_upsample, batch_size=batch_size)


def batch_face_locations(images, number_of_times_to_upsample=1, batch_size=128):
    """
    Returns an 2d array of bounding boxes of human faces in a image using the cnn face detector
    If you are using a GPU, this can give you much faster results since the GPU
    can process batches of images at once. If you aren't using a GPU, you don't need this function.

    :param images: A list of images (each as a numpy array)
    :param number_of_times_to_upsample: How many times to upsample the image looking for faces. Higher numbers find smaller faces.
    :param batch_size: How many images to include in each GPU processing batch.
    :return: A list of tuples of found face locations in css (top, right, bottom, left) order
    """
    def convert_cnn_detections_to_css(detections):
        return [_trim_css_to_bounds(_rect_to_css(face.rect), images[0].shape) for face in detections]

    raw_detections_batched = _raw_face_locations_batched(images, number_of_times_to_upsample, batch_size)

    return list(map(convert_cnn_detections_to_css, raw_detections_batched))



def _raw_face_landmarks(face_image, face_locations=None, model="large"):
    if face_locations is None:
        face_locations = _raw_face_locations(face_image)
    else:
        face_locations = [_css_to_rect(face_location) for face_location in face_locations]

    pose_predictor = pose_predictor_68_point

    if model == "small":
        pose_predictor = pose_predictor_5_point

    return [pose_predictor(face_image, face_location) for face_location in face_locations]


def face_landmarks(face_image, face_locations=None, model="large"):
    """
    Given an image, returns a dict of face feature locations (eyes, nose, etc) for each face in the image

    :param face_image: image to search
    :param face_locations: Optionally provide a list of face locations to check.
    :param model: Optional - which model to use. "large" (default) or "small" which only returns 5 points but is faster.
    :return: A list of dicts of face feature locations (eyes, nose, etc)
    """
    landmarks = _raw_face_landmarks(face_image, face_locations, model)
    landmarks_as_tuples = [[(p.x, p.y) for p in landmark.parts()] for landmark in landmarks]

    # For a definition of each point index, see https://cdn-images-1.medium.com/max/1600/1*AbEg31EgkbXSQehuNJBlWg.png
    if model == 'large':
        return [{
            "chin": points[0:17],
            "left_eyebrow": points[17:22],
            "right_eyebrow": points[22:27],
            "nose_bridge": points[27:31],
            "nose_tip": points[31:36],
            "left_eye": points[36:42],
            "right_eye": points[42:48],
            "top_lip": points[48:55] + [points[64]] + [points[63]] + [points[62]] + [points[61]] + [points[60]],
            "bottom_lip": points[54:60] + [points[48]] + [points[60]] + [points[67]] + [points[66]] + [points[65]] + [points[64]]
        } for points in landmarks_as_tuples]
    elif model == 'small':
        return [{
            "nose_tip": [points[4]],
            "left_eye": points[2:4],
            "right_eye": points[0:2],
        } for points in landmarks_as_tuples]
    else:
        raise ValueError("Invalid landmarks model type. Supported models are ['small', 'large'].")



def face_encodings(face_image, known_face_locations=None, num_jitters=1, model="small"):
    """
    Given an image, return the 128-dimension face encoding for each face in the image.

    :param face_image: The image that contains one or more faces
    :param known_face_locations: Optional - the bounding boxes of each face if you already know them.
    :param num_jitters: How many times to re-sample the face when calculating encoding. Higher is more accurate, but slower (i.e. 100 is 100x slower)
    :param model: Optional - which model to use. "large" or "small" (default) which only returns 5 points but is faster.
    :return: A list of 128-dimensional face encodings (one for each face in the image)
    """
    raw_landmarks = _raw_face_landmarks(face_image, known_face_locations, model)
    return [np.array(face_encoder.compute_face_descriptor(face_image, raw_landmark_set, num_jitters)) for raw_landmark_set in raw_landmarks]



def compare_faces(known_face_encodings, face_encoding_to_check, tolerance=0.6):
    """
    Compare a list of face encodings against a candidate encoding to see if they match.

    :param known_face_encodings: A list of known face encodings
    :param face_encoding_to_check: A single face encoding to compare against the list
    :param tolerance: How much distance between faces to consider it a match. Lower is more strict. 0.6 is typical best performance.
    :return: A list of True/False values indicating which known_face_encodings match the face encoding to check
    """
    return list(face_distance(known_face_encodings, face_encoding_to_check) <= tolerance)






checkcase=False
def submit():
    
    root.update()
    global id_t
    global name
    global dob
    global position
    global checkcase
    
    

    id_t = id_entry.get()
    
    name = name_entry.get()
    dob = dob_entry.get()
    position = position_entry.get() 
    if(check_index(id_t)):
        CTkMessagebox(title="Warning",icon='warning', message="Error ID already exists! Please enter a new ID")
        checkcase=False
        return
    else:
        checkcase=True
        root.destroy()
        


    

def fill_form():
    global root
    root = customtkinter.CTk()
    root.title("Registration")
    
    root.resizable(False, False)
    
    global id_entry
    global name_entry
    global dob_entry
    global position_entry
    
    img1 = ImageTk.PhotoImage(Image.open("./Resources/screen5.png"))
    l1 = customtkinter.CTkLabel(master=root, image=img1, text=" ")
    l1.pack()


    # Create a label for the title
    

    # Create a label for ID
    id_label = customtkinter.CTkLabel(master=l1, text="ID:", font=("Arial", 14),bg_color="white",text_color="black")
    id_label.place(relx=0.57, rely=0.5, anchor=tkinter.CENTER)

    # Create a label for Name
    name_label = customtkinter.CTkLabel(master=l1, text="Name:", font=("Arial", 14),bg_color="white",text_color="black")
    name_label.place(relx=0.57, rely=0.57, anchor=tkinter.CENTER)

    # Create a label for Date of Birth
    dob_label = customtkinter.CTkLabel(master=l1, text="Date of Birth:", font=("Arial", 14),bg_color="white",text_color="black")
    dob_label.place(relx=0.57, rely=0.64, anchor=tkinter.CENTER)

    # Create a label for Position
    position_label = customtkinter.CTkLabel(master=l1, text="Position:", font=("Arial", 14),bg_color="white",text_color="black")
    position_label.place(relx=0.57, rely=0.71, anchor=tkinter.CENTER)

    # Create a label for ID
    id_entry = customtkinter.CTkEntry(master=l1, font=("Arial", 14),bg_color="white")
    id_entry.place(relx=0.69, rely=0.5, anchor=tkinter.CENTER)

    # Create a label for Name
    name_entry = customtkinter.CTkEntry(master=l1, font=("Arial", 14),bg_color="white")
    name_entry.place(relx=0.69, rely=0.57, anchor=tkinter.CENTER)

    # Create a label for Date of Birth
    dob_entry = customtkinter.CTkEntry(master=l1, font=("Arial", 14),bg_color="white")
    dob_entry.place(relx=0.69, rely=0.64, anchor=tkinter.CENTER)

    # Create a label for Position
    position_entry = customtkinter.CTkEntry(master=l1, font=("Arial", 14),bg_color="white")
    position_entry.place(relx=0.69, rely=0.71, anchor=tkinter.CENTER)

    # Create a button to submit the form
    button = customtkinter.CTkButton(master=l1, text="Submit", font=("Arial", 14), command=submit,bg_color="white")
    button.place(relx=0.67, rely=0.79, anchor=tkinter.CENTER)
    root.mainloop()



def process_folder(folder_path):
    # Load captured photos and find facial encodings
    face_encoders = []
    
    if(os.path.exists(folder_path)):

        for root, dirs, files in os.walk(folder_path):
            for filename in files:
                if filename.endswith(".jpg"):
                    image_path = os.path.join(root, filename)
                    image = load_image_file(image_path)
                    try:
                    # Assuming there's only one face in the image
                        face_encoding = face_encodings(image)[0]
                        face_encoders.append(face_encoding)
                    except IndexError:
                        print(f'No face detected in {image_path}')
                        shutil.rmtree(folder_path) 
                        os.startfile('registration_haar.exe')
        


        return face_encoders

def check_index(index):
    if os.path.exists('./ImageDataset/facial_encodings_combined.csv'):
        df = pandas.read_csv('./ImageDataset/facial_encodings_combined.csv')
        index = int(index)
        print(set(df['ID.']),index)
        
        if index in set(df['ID.']):
            return True
        else:
            return False
    else:
        return False
    
       




def save_encodings_to_csv(face_encodings, csv_file_path):
    fill_form()
    global id_t
    global name
    global dob
    global position
    
    
    if not os.path.exists(csv_file_path):
        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID.", "Face Encoding","Name","DOB","Position"])

            for ID, face_encoding in enumerate(face_encodings, start=1):
                writer.writerow([id_t, face_encoding,name,dob,position])

        print(f'Facial encodings stored to: {csv_file_path}')
    else:
        with open(csv_file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            for ID, face_encoding in enumerate(face_encodings, start=1):
                writer.writerow([id_t, face_encoding,name,dob,position])
                print(f'Facial encodings stored to: {csv_file_path}')
                



if __name__ == "__main__":
    # Specify the folder path where photos are stored
    
    root_folder_path = './ImageDataset'  # Update with the actual path

    # Create a list to store all face encodings
    all_face_encodings = []
    all_folder=[]

    for folder_name in os.listdir(root_folder_path):
        folder_path = os.path.join(root_folder_path, folder_name)
        
        


        if os.path.isdir(folder_path):
            all_folder.append(folder_path)
            print(f'Processing folder: {folder_path}')

            # Run the function to process the folder and get facial encodings
            face_encodings = process_folder(folder_path)

            if face_encodings:
                # Extend the list with the current folder's encodings
                all_face_encodings.extend(face_encodings)

        


    # Specify the CSV file path for the combined encodings
    combined_csv_file_path = os.path.join(root_folder_path, "facial_encodings_combined.csv")

    # Run the function to save combined facial encodings to CSV
    
    save_encodings_to_csv(all_face_encodings, combined_csv_file_path)
    print(all_folder)
    
    for i in all_folder:
        if os.path.exists(i):
            shutil.rmtree(i)
        

    
