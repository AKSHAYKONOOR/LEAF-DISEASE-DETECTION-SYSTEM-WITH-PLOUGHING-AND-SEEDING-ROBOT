from imagesearch.localbinarypatterns import LocalBinaryPatterns
from sklearn.svm import LinearSVC
from imutils import paths
import cv2
import os
import time
import pymysql  
from picamera import PiCamera
con=mysql.connector.connect(user='root',host='192.168.43.48',passwd='root',port=3306,db='leaf_disease_db')
cmd=con.cursor()
camera=PiCamera()
desc=LocalBinaryPatterns(24,8)
data=[]
labels=[]
def train_images():
    #loop over the training images
    for imagePath in paths.list_images("images/training"):
        image=cv2.imread(imagePath)
        print(imagePath)
        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        hist=desc.describe(gray)
        labels.append(imagePath.split("/")[-2])
        data.append(hist)
    model=LinearSVC(C=100.0,random_state=42)
    model.fit(data,labels)
def get_object(path='images/testing'):
    for imagePath in paths.list_images(path):
        image=cv2.imread(imagePath)
        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        hist=desc.describe(gray)
        print(hist)
        prediction=model.predict(hist.reshape(1,-1))
        cv2.putText(image,prediction[0],(10,30),cv2.FONT_HERSHEY_SIMPLEX,1.0,(0,0,255),3)
        return prediction[0]
def capture_image():
    camera.start_preview()
    time.sleep(5)
    camera.capture('/home/pi/Leaf Disease/1/images/testing/img.jpg')
    camera.stop_preview()
    time.sleep(1)
    camera.close()
    time.sleep(1)

def main():
    while(True):
        for i in range(1,10):
            try:
                capture_image()
                plant_id=i
                result=get_object()
                cmd.execute("insert into detection_table values(null,'"+str(plant_id)+"','"+str(result)+"')")
                con.commit()
            except Exception as e:
                print('error')
if __name__=="__main__":
    main()

