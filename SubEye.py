import guessAge,cv2
import checkGate,useCard,sendImg,asyncio

station = input("역명을 입력해주세요 : ")
cctvNum = int(input("CCTV 번호를 입력해주세요 : "))
cap=cv2.VideoCapture('video/v10_fix.mp4')

overlapping=[]
meAge=[]
roi=[]
ret,frame=cap.read()

cGate=checkGate.checkGate()
frame=cGate.sort_df(frame)
useCard=useCard.UseCard(cGate.blackBox)
for i in range(cGate.countBox):
    overlapping.append([0,0])
    meAge.append([0,0])


while (cap.isOpened()):
    ret,frame=cap.read()
    if ret:


        for i in range(cGate.countBox):
            frame=cv2.rectangle(frame, (cGate.blackBox[i][0], cGate.blackBox[i][1]), (cGate.blackBox[i][2], cGate.blackBox[i][3]), (0, 255, 0), 2)
            frame = cv2.rectangle(frame, (int(cGate.gate[i][0]), 0), (int(cGate.gate[i][1]), cGate.blackBox[i][3]),(0, 0, 255), 1)

        for i in range(cGate.countBox):
            cardNum=useCard.Find_Kid(frame,i)
            if cardNum==overlapping[i][0]:
                pass
            else:
                overlapping[i][0]=cardNum
                print(i+1,"번 게이트 화면 색 변경됨", overlapping)
                if cardNum>0:
                    overlapping[i][1]=10
                    print("표 사용 카운트 증가")

            if overlapping[i][0] >0 and overlapping[i][1] >=0: #특수표를 사용하고 스택이 0이상이면 실행
                overlapping[i][1] -=1 #표 사용 스택 깎이
                a=0 #나이값 임시 변수
                x = cGate.gate[i][0]
                w = cGate.gate[i][1] - cGate.gate[i][0]
                roi= (frame[0:1000, int(x):int(x + w)])  # [y:y+h, x:x+w]
                frame,a=guessAge.guess_age(frame) #화면 받아오기

                if a>0:
                    meAge[i][0]+=a
                    meAge[i][1]+=1
                if overlapping[i][1] == -1 and (meAge[i][0]/meAge[i][1])>12:
                    print(i+1,"번 게이트",meAge[i][0]/meAge[i][1],"나이로 추정,",overlapping[i][0],"번 카드 사용 불법 승차로 확인 ")
                    print("전송")
                    sendImg.send_img(roi, i + 1, cctvNum, station,overlapping[i][0])

                elif overlapping[i][1] == -1 and (meAge[i][0]/meAge[i][1])<65:
                    print(i+1,"번 게이트",meAge[i][0]/meAge[i][1],"나이로 추정,",overlapping[i][0],"번 카드 사용 불법 승차로 확인 ")
                    print("전송")
                    sendImg.send_img(roi, i + 1, cctvNum, station,overlapping[i][0])

        cv2.namedWindow("gate", flags=cv2.WINDOW_NORMAL)
        cv2.resizeWindow("gate", 700, 1200)
        cv2.imshow("gate", frame)
        if cv2.waitKey(1) & 0xFF ==ord('q'):
            break
    else:
        break
cap.release()
