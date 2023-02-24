import app_detrec
import app_rec
import cropper
import cropper_rec
import sys

# A changer avec l'image en input de l'utilisateur a partir de l'interface web
images=sys.argv[1]

detandrec,reconly=app_detrec.detrec(images),app_rec.rec(images)

print("Detection and recognition: ",detandrec,"\nRecognition only: ",reconly)

