import cv2 as cv
import face_recognition as fr
import os
import numpy as np
import PIL as pil
from PIL import Image
import pickle


print("1 -> Enter new data")
print("2 -> See system testing")
print("3 -> Exit")
choice=(int)(input("Choose option: "))
os.system('cls')
while(1):
    if(choice==1):
        with open("encoding.dat",'rb') as encoding_file:
            dict=pickle.load(encoding_file)
            encoding_file.close()
        print("1 -> Upload photo from the computer")
        print("2 -> Live capture")
        choice1=(int)(input("Choose option: "))
        os.system('cls')
        if(choice1==1):
            imgname=input("Enter the name of the image: ")
            name=input("Enter name of the person: ")
            os.system('cls')
            img=pil.Image.open(imgname+".jpg")
            img.save(".\\image\\"+name+".jpg")
            person_image=fr.load_image_file(".\\image\\"+name+".jpg")
            dict.update({name:fr.face_encodings(person_image)[0]})
            with open("encoding.dat",'wb') as encoding_file:
                pickle.dump(dict,encoding_file)
                encoding_file.close()
            print("Image set Successfully")
        else:
            name=input("Enter name of the person: ")
            print("Opening Camera...")
            camera=cv.VideoCapture(0)
            while True:
                ret, image=camera.read()
                if not ret:
                    print("Failed to capture photo")
                    print("Closing Camera...")
                    break
                cv.imshow("Image - Press Space to capture Photo",image)
                k=cv.waitKey(1)
                if k%256==27:
                    print("Closing Camera...")
                    break
                elif k%256==32:
                    cv.imwrite(".\\image\\"+name+".jpg",image)
                    person_image=fr.load_image_file(".\\image\\"+name+".jpg")
                    dict.update({name:fr.face_encodings(person_image)[0]})
                    with open("encoding.dat",'wb') as encoding_file:
                        pickle.dump(dict,encoding_file)
                        encoding_file.close()
                    print("Photo captured Successfully")
            del(camera)
        cv.destroyAllWindows()

    elif(choice==2):
        print("Opening Camera...")
        with open("encoding.dat",'rb') as encoding_file:
            dict=pickle.load(encoding_file)
            encoding_file.close()
        known_face_names=list(dict.keys())
        known_face_encoding=list(dict.values())
        video_capture=cv.VideoCapture(0)

        while True:
            ret, frame=video_capture.read()

            face_location=fr.face_locations(frame)
            face_encoding=fr.face_encodings(frame,face_location)

            for(top,right,bottom,left),face_encoding in zip(face_location,face_encoding):
                matches=fr.compare_faces(known_face_encoding,face_encoding)
                name="Unknown"
                if True in matches:
                    first_match_index=matches.index(True)
                    name=known_face_names[first_match_index]
                    cv.rectangle(frame,(left,top),(right,bottom),(0,255,0),2)
                    cv.putText(frame,name,(left,top-10),cv.FONT_HERSHEY_SIMPLEX,0.9,(0,255,0),2)
                else:
                    cv.rectangle(frame,(left,top),(right,bottom),(0,0,255),2)
                    cv.putText(frame,name,(left,top-10),cv.FONT_HERSHEY_SIMPLEX,0.9,(0,0,255),2)

            cv.imshow("Press ESC to close camera",frame)
            k=cv.waitKey(1) 

            if k%256==27:
                print("Closing Camera...")
                break

        video_capture.release()
        cv.destroyAllWindows()

    elif(choice==3):
        break;
    
    os.system('cls')
    print("1 -> Enter new data")
    print("2 -> See system testing")
    print("3 -> Exit")
    choice=(int)(input("Choose option: "))
    os.system('cls')