import cv2 as cv
import os
import re
import numpy as np
from pynput import keyboard
from pynput.keyboard import Key

###########################################################
###########################################################
################## Path Initialization ####################
path = "Path/to/sequence"
sequence = input("Please enter the sequence you want to process; 1, 2, 3, ...: ")
mask_path = path + "sequence" + sequence + "/sequence" + sequence + "_annotations/SegmentationClass"
image_path = path + "sequence" + sequence + "/images/"
processed_mask_path = path + "sequence" + sequence + "/masks"

################## Global variables #############################

drawing = False
processing = True
keep_processing = False
change = True
ix, iy = -1, -1
tmp = 0
max_value = 255
max_value_H = 360//2
low_H = 91
low_S = 0
low_V = 136
high_H = 109
high_S = max_value
high_V = max_value
window_capture_name = 'Raw Image'
low_H_name = 'Low H'
low_S_name = 'Low S'
low_V_name = 'Low V'
high_H_name = 'High H'
high_S_name = 'High S'
high_V_name = 'High V'

def on_low_H_thresh_trackbar(val):
    global low_H
    global high_H
    low_H = val
    low_H = min(high_H-1, low_H)
    cv.setTrackbarPos(low_H_name, window_detection_name, low_H)
def on_high_H_thresh_trackbar(val):
    global low_H
    global high_H
    high_H = val
    high_H = max(high_H, low_H+1)
    cv.setTrackbarPos(high_H_name, window_detection_name, high_H)
def on_low_S_thresh_trackbar(val):
    global low_S
    global high_S
    low_S = val
    low_S = min(high_S-1, low_S)
    cv.setTrackbarPos(low_S_name, window_detection_name, low_S)
def on_high_S_thresh_trackbar(val):
    global low_S
    global high_S
    high_S = val
    high_S = max(high_S, low_S+1)
    cv.setTrackbarPos(high_S_name, window_detection_name, high_S)
def on_low_V_thresh_trackbar(val):
    global low_V
    global high_V
    low_V = val
    low_V = min(high_V-1, low_V)
    cv.setTrackbarPos(low_V_name, window_detection_name, low_V)
def on_high_V_thresh_trackbar(val):
    global low_V
    global high_V
    high_V = val
    high_V = max(high_V, low_V+1)
    cv.setTrackbarPos(high_V_name, window_detection_name, high_V)

def remove_isolated_pix(event, x, y, flags, param):
     
    global drawing, ix, iy, refPt, mask, window

    if event == cv.EVENT_LBUTTONDOWN:   
        drawing  = True
        ix, iy = x, y
        refPt = [(ix,iy)]
 
    elif event == cv.EVENT_MOUSEMOVE: #and flags == cv.EVENT_FLAG_LBUTTON: 
        if drawing == True:
           
            draw = frame_threshold_rs.copy()

            cv.rectangle(draw, (ix, iy), (x, y), 255)
            cv.imshow(window_detection_name, draw)
 
    elif event == cv.EVENT_LBUTTONUP:
        refPt.append((x,y))
        drawing = False

            
        if refPt[0][0] < refPt[1][0]:

            window = frame_threshold_rs[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
            mask = window != 0
            window[mask] = 0
    
        elif refPt[0][0] > refPt[1][0]:

            window = frame_threshold_rs[refPt[0][1]:refPt[1][1], refPt[1][0]:refPt[0][0]]         
            mask = window != 0
            window[mask] = 0
        
        cv.imshow(window_detection_name, frame_threshold_rs)

    elif event == cv.EVENT_MOUSEWHEEL:

        window[mask]  = 255
        cv.imshow(window_detection_name, frame_threshold_rs)

        

def remove_void(event, x, y, flags, param):

    global color, ix, iy, window
    global refPt, drawing, mask


    if event == cv.EVENT_MBUTTONDBLCLK:                  
          color = clone[y, x, :]
          print("the color is: ", color)
        
    
    if event == cv.EVENT_LBUTTONDOWN:   
        drawing  = True
        ix, iy = x, y
        refPt = [(ix,iy)]
 
    elif event == cv.EVENT_MOUSEMOVE: #and flags == cv.EVENT_FLAG_LBUTTON: 
        if drawing == True:
           
            draw = clone.copy()

            cv.rectangle(draw, (ix, iy), (x, y), (0, 255, 0), 3)
            cv.imshow("Processed_Mask", draw)
            
            
    elif event == cv.EVENT_LBUTTONUP:
        refPt.append((x,y))
        drawing = False

        if refPt[0][0] < refPt[1][0]:
            window = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]         
        else:
            window = clone[refPt[0][1]:refPt[1][1], refPt[1][0]:refPt[0][0]]         
        
        mask = np.ones((window.shape[0], window.shape[1]), dtype=bool)
       
        for i, bgr in enumerate(colors_bgr):
            color_mask = (window == bgr).all(axis=2)
            mask &= ~color_mask

        window[mask] = color 
        cv.imshow("Processed_Mask", clone)
    
    elif event == cv.EVENT_MOUSEWHEEL:
        
        window[mask] = [0,0,0] 
        cv.imshow("Processed_Mask", clone)


def change_label(event, x, y, flags, param):

    global color1, color2, refPt, window, mask, drawing, change, ix, iy

    if event == cv.EVENT_MBUTTONDBLCLK:
        if change == True:
            color1 = clone[y,x,:]
            print("color to be added is: ", color1)
            change = False
            print("change is: ", change)
        else:    
            color2 = clone[y,x,:]
            print("color to be replaced is: ", color2)
            change = True
    
    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        refPt = [(ix, iy)]
    
    elif event == cv.EVENT_MOUSEMOVE:
        if drawing == True:
            draw = clone.copy()

            cv.rectangle(draw, (ix, iy), (x, y), (0,255,0), 3)
            cv.imshow("Processed_Mask", draw)
    
    elif event == cv.EVENT_LBUTTONUP:
        refPt.append((x,y))
        drawing = False

        if refPt[0][0] < refPt[1][0]:
            window = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
        else:
            window = clone[refPt[0][1]:refPt[1][1], refPt[1][0]:refPt[0][0]]

        mask = np.zeros((window.shape[0], window.shape[1]), dtype = bool)

        mask = (window == color2).all(axis=2)
        window[mask] = color1
        cv.imshow("Processed_Mask", clone)
    
    elif event == cv.EVENT_MOUSEWHEEL:
        window[mask] = color2
        cv.imshow("Processed_Mask", clone)


    

    

################### label map color extraction ###############################################
labelpath = path + "/sequence" + sequence + "/sequence" + sequence + "_annotations/labelmap.txt"

with open(labelpath, 'r') as file:
     text = file.read()

pattern = r'\d+'
color_matches = re.findall(pattern, text)
colors = [list(map(int, color_matches[i:i+3])) for i in range(0, len(color_matches), 3)]
colors_filtered = [color for color in colors if color != [0,0,0]] 
colors_bgr = [[color[2], color[1], color[0]] for color in colors_filtered]
###############################################################################################

####################### Main Loop #############################################################

loop = True
index = int(input("Where do you want to start?: "))
os.chdir(image_path)
images_list = [filename for filename in os.listdir(image_path)]
images_list = sorted(images_list)

while loop:
              

        if keep_processing == False:
            while True:
                os.chdir(image_path)
                frame = cv.imread(images_list[index])
                frame = cv.resize(frame, (960, 540))
                cv.imshow(window_capture_name, frame)
                
                key0 = cv.waitKey(0)
                
                if key0 == ord('l'):
                    if index == len(images_list) -1:
                        index = 0
                        cv.destroyAllWindows()
                        continue
                    else:
                        index +=1
                        cv.destroyAllWindows()
                        continue
                
                elif key0 == ord('a'):
                    if index == 0:
                        index = len(images_list) - 1
                        cv.destroyAllWindows()
                        continue

                    else:
                        index -= 1
                        cv.destroyAllWindows()
                        continue
                
                elif key0 == ord('c'):

                    keep_processing = True
                    break


                elif key0 == ord('q'):
                    loop = False
                    break 

                else:
                    break


            if loop == False:
                cv.destroyAllWindows()
                continue          
                
            label = input("What class you want to process; sky, grass, tree or manual: ")
            window_detection_name = label
            cv.destroyAllWindows()
        if label != "manual":
            if label == "sky":
                
                low_H = 91
                low_S = 0
                low_V = 136
                high_H = 109
                high_S = 255
                high_V = 255
            
            else:
                low_H = 0
                low_S = 104
                low_V = 0
                high_H = 56
                high_S = 221
                high_V = 255
                
            frame_HSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
            cv.namedWindow(window_capture_name)
            cv.namedWindow(window_detection_name)
            cv.createTrackbar(low_H_name, window_detection_name , low_H, max_value_H, on_low_H_thresh_trackbar)
            cv.createTrackbar(high_H_name, window_detection_name , high_H, max_value_H, on_high_H_thresh_trackbar)
            cv.createTrackbar(low_S_name, window_detection_name , low_S, max_value, on_low_S_thresh_trackbar)
            cv.createTrackbar(high_S_name, window_detection_name , high_S, max_value, on_high_S_thresh_trackbar)
            cv.createTrackbar(low_V_name, window_detection_name , low_V, max_value, on_low_V_thresh_trackbar)
            cv.createTrackbar(high_V_name, window_detection_name , high_V, max_value, on_high_V_thresh_trackbar)


            while True:

                frame_threshold = cv.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))

                frame_threshold_rs = cv.resize(frame_threshold, (960, 540))
                
                cv.imshow(window_capture_name, frame)
                cv.imshow(window_detection_name, frame_threshold_rs)

                key1 = cv.waitKey(0)
                
                if key1 == ord("s"):
                    processing = True
                    break
                elif key1 == ord("q"):
                    processing = False
                    break
                else:
                    continue

            if processing == True:
                while True:

                    cv.setMouseCallback(window_detection_name, remove_isolated_pix)                                    

                    key2 = cv.waitKey(0)
                    if key2 == ord('s'):
                            tmp = frame_threshold_rs
                            cv.destroyWindow(window_detection_name)
                            break

                if keep_processing == False:
                    os.chdir(mask_path)
                    masks_list = [filename for filename in os.listdir(mask_path)]
                    masks_list = sorted(masks_list)
                    mask_list = masks_list[index]

                elif keep_processing == True:
                    file = images_list[index]
                    os.chdir(processed_mask_path)
                    mask_list = [filename for filename in os.listdir(processed_mask_path) if filename == file][0]
                    print(mask_list)
                    
                    
                img = cv.imread(mask_list)
                clone = img.copy()
                clone = cv.resize(clone, (960,540))

                if processing == True:
                    if label == "sky":
                        sky = np.all(clone == [255, 0, 0], axis=2)
                        clone[sky] = [0,0,0]
                        clone[tmp != 0] = [255,0,0]

                    elif label == "grass":
                        grass = np.all(clone == [0,102,0], axis=2)
                        clone[grass] = [0,0,0]
                        clone[tmp!=0] = [0,102,0]

                    elif label == "tree":
                        tree = np.all(clone == [0, 255, 0], axis=2)
                        clone[tree] = [0,0,0]
                        clone[tmp!=0] = [0,255,0]


                img = cv.resize(img, (960, 540))
                cv.namedWindow("Original_Mask")
                cv.namedWindow("Processed_Mask")
                cv.setMouseCallback("Processed_Mask", remove_void)  
                cv.imshow("Original_Mask", img)
                cv.imshow("Processed_Mask", clone)

        
        elif label == "manual":

            file = images_list[index]
            os.chdir(processed_mask_path)
            mask_list = [filename for filename in os.listdir(processed_mask_path) if filename == file][0]

            img = cv.imread(mask_list)
            clone = img.copy()
            clone = cv.resize(clone, (960, 540))
           
            cv.namedWindow("Processed_Mask")
            cv.setMouseCallback("Processed_Mask", change_label)
            cv.imshow("Processed_Mask", clone)

        while True:
            
            key3 = cv.waitKey(0)
            if key3 == ord('l'):
                if index == len(images_list) - 1:
                        index = 0
                        cv.destroyAllWindows()
                        keep_processing = False
                        break
                else:
                        index +=1
                        cv.destroyAllWindows()
                        keep_processing = False
                        break
                    
            elif key3 == ord('a'):
                if index == 0:
                    index = len(images_list) - 1
                    cv.destroyAllWindows()
                    keep_processing = False
                    break
                else:
                    index -= 1
                    cv.destroyAllWindows()
                    keep_processing = False
                    break
            
            elif key3 == ord('s'):
                mask = clone
                mask = cv.resize(mask, (img.shape[1], img.shape[0]))
                saved_path = "path/to/output/" + sequence + "/masks/" + mask_list
                cv.imwrite(saved_path, mask) 
                print("The image " + mask_list + " has been saved in " +  "vautlab/RB_CAR/sequence" + sequence + "/masks/")

            elif key3 == ord('c'):
                 cv.destroyAllWindows()
                 label = input("What class you want to process now? sky, grass, tree or manual: ") 
                 window_detection_name = label
                 keep_processing = True
                 break
            
                    
            elif key3 == ord("q"):
                loop = False
                break

            

        










