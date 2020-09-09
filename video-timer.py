import cv2
import argparse
import numpy as np


def boolean_string(s):
    if s not in {'False', 'True'}:
        raise ValueError('Not a valid boolean string')
    return s == 'True'

# Arguments
parser = argparse.ArgumentParser(description='Add timer to video')
parser.add_argument('--position', type=str, help='Position of the timer (tr,tl,br,bl).')
parser.add_argument('--src_file', type=str, help='Relative path to the video file.')
parser.add_argument('--init_time', type=str, help='Initial time for the timer. (eg 14 or 14.5)')
parser.add_argument('--end_time', type=str, help='Final time for the timer.')
parser.add_argument('--show_minutes', type=boolean_string, help='Show minutes in time.',default=False)

args = parser.parse_args()
# print(args.position)
# print(args.src_file)
# print(args.init_time)
# print(args.end_time)
# print(args.show_minutes)

# Modify given time
init_showing_condition, end_showing_condition = int(float(args.init_time)*60), int(float(args.end_time)*60)


# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name
cap = cv2.VideoCapture(args.src_file)

# Check if camera opened successfully
if (cap.isOpened()== False):
  print("Error opening video stream or file")
 

# Get image size
if cap.isOpened(): 
    # or
    width  = cap.get(3) # float
    height = cap.get(4) # float

    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    # print('frames count:', frame_count)
    # print('width:',width)
    # print('height:',height)
    
# Define file output
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 60, (int(width),int(height)))


# Define time text
font                   = cv2.FONT_HERSHEY_DUPLEX
if args.position == 'tl':
    bottomLeftCornerOfText = (int(width*0.05),int(height*0.10))
elif args.position == 'tr':
    bottomLeftCornerOfText = (int(width*0.65),int(height*0.10))
elif args.position == 'bl':
    bottomLeftCornerOfText = (int(width*0.05),int(height*0.90))
elif args.position == 'br':
    bottomLeftCornerOfText = (int(width*0.65),int(height*0.90))
fontScale              = 1
fontColor              = (255,255,255)
lineType               = 2


running_time = 0
first_time = True
# Read until video is completed
while (cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:
        
        if running_time >= init_showing_condition and running_time <= end_showing_condition:
            if first_time: 
                rel_running_time = 0
                first_time = False
            seconds = str(rel_running_time % 3600 // 60)
            minutes = str(rel_running_time // 3600)
            miliseconds = str((rel_running_time % 3600 % 60)/60).split('.')[-1][:2]
            if not args.show_minutes:
                text_to_print = '{}.{}'.format(seconds,miliseconds)
            else:
                text_to_print = '{}:{}.{}'.format(minutes,seconds,miliseconds)
            # Add time to image
            cv2.putText(frame,text_to_print, 
                bottomLeftCornerOfText, 
                font, 
                fontScale,
                fontColor,
                lineType)
            rel_running_time = rel_running_time+1
            
        elif running_time >= end_showing_condition:
            seconds = str(rel_running_time % 3600 // 60)
            minutes = str(rel_running_time // 3600)
            miliseconds = str((rel_running_time % 3600 % 60)/60).split('.')[-1][:2]
            if not args.show_minutes:
                text_to_print = '{}.{}'.format(seconds,miliseconds)
            else:
                text_to_print = '{}:{}.{}'.format(minutes,seconds,miliseconds)
            # Add time to image
            cv2.putText(frame,text_to_print, 
                bottomLeftCornerOfText, 
                font, 
                fontScale,
                fontColor,
                lineType)
    
        # Display the resulting frame
        #cv2.imshow('Frame', frame)
        out.write(frame)
        # Press Q on keyboard to  exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
        running_time = running_time+1
    # Break the loop
    else:
        break
 
# When everything done, release the video capture object
cap.release()
out.release()

# Closes all the frames
cv2.destroyAllWindows()
