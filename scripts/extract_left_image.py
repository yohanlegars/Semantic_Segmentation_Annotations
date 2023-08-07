import sys
import pyzed.sl as sl
import numpy as np
import cv2
from pathlib import Path
import os

# example command to extract every 50 images from svo:
"""
python3 extract_left_image.py \
/path/to/filename.svo\
/path/to/images_output_dir\
50
"""


def progress_bar(percent_done, bar_length=50):
    done_length = int(bar_length * percent_done / 100)
    bar = '=' * done_length + '-' * (bar_length - done_length)
    sys.stdout.write('[%s] %f%s\r' % (bar, percent_done, '%'))
    sys.stdout.flush()

def main():

    svo_input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    step_size = sys.argv[3] 

    init_params = sl.InitParameters()
    init_params.set_from_svo_file(str(svo_input_path))
    init_params.svo_real_time_mode = False
    init_params.coordinate_units = sl.UNIT.MILLIMETER


    zed = sl.Camera()

    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        sys.stdout.write(repr(err))
        zed.close()
        exit()

    left_image = sl.Mat()

    rt_param = sl.RuntimeParameters()

    sys.stdout.write("Converting SVO... Use Ctrl-C to interrupt conversion.\n")

    nb_frames = zed.get_svo_number_of_frames()
    
    svo_file = os.path.basename(sys.argv[1])
    svo_name = svo_file.split("_")[1]


    while True:
        if zed.grab(rt_param) == sl.ERROR_CODE.SUCCESS:
                svo_position = zed.get_svo_position()
                 
                if svo_position % int(step_size) == 0 or svo_position == 0:

                # Retrieve SVO images
                    zed.retrieve_image(left_image, sl.VIEW.LEFT)

                    image_timestamp = zed.get_timestamp(sl.TIME_REFERENCE.IMAGE).get_nanoseconds()
                    image_filename = os.path.join(output_path,"ZED_%s.png" % (svo_name + '_'+ str(image_timestamp)) )
                   
                    cv2.imwrite(str(image_filename), left_image.get_data())
                
                    progress_bar((svo_position+1) / nb_frames*100, 30)

        else:
             break
    

    sys.stdout.write("Extraction Done")

if __name__ == "__main__":
     main()

