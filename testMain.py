import sendImg
import cv2
cap=cv2.VideoCapture('video/v10_fix.mp4')

ret,frame=cap.read()

sendImg.send_img(frame, 1, 1, "서울역")

print("성공")