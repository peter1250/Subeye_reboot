import cv2
class UseCard:
    blackBoxs=[]
    def __init__(self,blackBoxs):
        self.blackBoxs=blackBoxs


    def Find_Kid(self,img,i):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_blue = (10, 150, 150)
        upper_blue = (30, 255, 255)
        lower_old = (300, 150, 150)
        upper_old = (320, 255, 255)

        x=self.blackBoxs[i][0]
        y=self.blackBoxs[i][1]
        w=self.blackBoxs[i][2]-self.blackBoxs[i][0]
        h=self.blackBoxs[i][3]-self.blackBoxs[i][1]
        roi = hsv[y:y+h, x:x+w] #[y:y+h, x:x+w]

        img_mask = cv2.inRange(roi, lower_blue, upper_blue)
        img_mask_old = cv2.inRange(roi, lower_old, upper_old)

        pixels = cv2.countNonZero(img_mask)
        pixels_old =cv2.countNonZero(img_mask_old)

        cv2.imshow("mask", roi)
        if pixels > 100:
            #print(i,"번 게이트 검출")
            return 1

        elif pixels_old > 100:
             return 2
        else:
            #print(i, "번 게이트 불검출")
            return 0
