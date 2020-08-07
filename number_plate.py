
def main():

    import numpy as np

    import cv2

    import imutils

    import sys

    import pytesseract

    import pandas as pd

    import time

    import datetime
    
    import csv

    now=datetime.datetime.now()
    d=str(now.date())
    date=datetime.datetime.strptime(d, "%Y-%m-%d").strftime("%d-%m-%Y")
    t=str(now.time())
    time1=t[:8]


    

    pytesseract.pytesseract.tesseract_cmd= "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


    img = cv2.imread("C:\\Users\\Jayesh\\Desktop\\Number Plate Images\\image1.png")

   

    img = imutils.resize(img, width=500)


    cv2.imshow("Original Image", img)  

    cv2.waitKey(0)



    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    cv2.imshow("Preprocess 1 - Grayscale Conversion", gray_img)     

    cv2.waitKey(0)




   

    gray_img = cv2.bilateralFilter(gray_img, 11, 17, 17)

    cv2.imshow("Preprocess 2 - Bilateral Filter", gray_img)   

    cv2.waitKey(0)



    c_edge = cv2.Canny(gray_img, 170, 200)

    cv2.imshow("Preprocess 3 - Canny Edges", c_edge)    

    cv2.waitKey(0)


 

    cnt, new = cv2.findContours(c_edge, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

   
    cnt = sorted(cnt, key = cv2.contourArea, reverse = True)[:30]

    NumberPlateCount = None


    im2 = img.copy()

    cv2.drawContours(im2, cnt, -1, (0,255,0), 3)

    cv2.imshow("Top 30 Contours", im2)        

    cv2.waitKey(0)


    count = 0

    for c in cnt:

        perimeter = cv2.arcLength(c, True)    
        approx = cv2.approxPolyDP(c, 0.02 * perimeter, True)

        if len(approx) == 4:            
            NumberPlateCount = approx

            break



    masked = np.zeros(gray_img.shape,np.uint8)

    new_image = cv2.drawContours(masked,[NumberPlateCount],0,255,-1)

    new_image = cv2.bitwise_and(img,img,mask=masked)

    cv2.imshow("4 - Final_Image",new_image)    
   
    cv2.waitKey(0)



    configr = ('-l eng --oem 1 --psm 3')


   
    text_no = pytesseract.image_to_string(new_image, config=configr)
    


    Vehicle_number=text_no

    def get_length(file_path):
        with open(file_path) as csvfile:
            reader=csv.reader(csvfile)
            reader_list=list(reader)
            return len(reader_list)
        return 1

    def append_data(file_path,date,time,Vehicle_number):
        fieldnames=['date','time','Vehicle_number'] 
        next_id=get_length(file_path)
        with open(file_path,"a",newline='') as csvfile:
            writer=csv.DictWriter(csvfile,fieldnames=fieldnames)
            writer.writerow({"date":date,"time":time,"Vehicle_number":text_no})       
    append_data("C:\\Users\\Jayesh\\Desktop\\Database",date,time1,Vehicle_number)

   
    print(text_no)

    cv2.waitKey(0)

    
    
    
    
if __name__ == '__main__':

    main()