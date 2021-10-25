import numpy as np
import torch
import pandas as pd
import cv2
import tqdm
import torchvision
import matplotlib
import seaborn
from PIL import Image

class checkGate:
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='models/best.pt')
    # model.conf =
    df=0
    countGate=0
    countBox=0
    gate=[]
    blackBox=[]
    def sort_df(self, frame):
        results=self.model(frame[..., ::-1])
        results.print()
        df = pd.DataFrame(results.pandas().xyxy[0])
        df = df.sort_values('xmin')
        df = df.sort_values('class')
        df = df.reset_index(drop=True)
        self.df=df
        return self.draw_gate(frame)
        # return self.count_gate()
    def draw_gate(self,frame):
        for i in range(len(self.df)):
            x1 = int(self.df['xmin'][i])
            x2 = int(self.df['xmax'][i])
            y1 = int(self.df['ymin'][i])
            y2 = int(self.df['ymax'][i])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 1)
        self.count_gate()

        return self.check_gate(frame)

    def count_gate(self):
        self.countGate = int(self.df['class'].value_counts()[0:1].array[0])  # 게이트 갯수
        self.countBox = int(self.df['class'].value_counts()[1:2].array[0])  # 검은박스표지판 갯수

    def check_gate(self,frame):
        good = 0
        for i in range(self.countGate):
            for j in range(self.countBox):
                if (self.df.loc[j + self.countGate, 'xmin'] > self.df.loc[i, 'xmin'] and self.df.loc[j + self.countGate, 'xmin'] < self.df.loc[
                    i, 'xmax']):
                    good += 1
                    if i==0:  # 다음 게이트가 있다면 실행
                        self.gate.append([0,(self.df.loc[i , 'xmin'] + self.df.loc[i, 'xmax']) / 2])  # 게이트 영역 좌표 리스트
                    else:
                        self.gate.append([(self.df.loc[i - 1, 'xmin'] + self.df.loc[i - 1, 'xmax']) / 2,(self.df.loc[i, 'xmin'] + self.df.loc[i, 'xmax']) / 2])  # 마지막 게이트에서 사진 끝까지 표시
        if good == self.countBox:
            return self.check_blockBox(frame)

    def check_blockBox(self,frame):
        for i in range(self.countBox):
            x2= int(self.df['xmax'][self.countGate + i])  # 오른 끝점
            x1 = int(self.df['xmin'][self.countGate + i])  # 왼 끝점
            y2 = int(self.df['ymax'][self.countGate + i])  # 아래 끝점
            y1 = int(self.df['ymin'][self.countGate + i])  # 위 끝점
            y = int((y2 - y1) // 3 * 2.2 + y1)  # 특별 승차자 박스 위 좌표
            cv2.rectangle(frame, (x1, y), (x2, y2), (0, 255, 0), 2)
            self.blackBox.append([x1, y, x2, y2])
        return frame
