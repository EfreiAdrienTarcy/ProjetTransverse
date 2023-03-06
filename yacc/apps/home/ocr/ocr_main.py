from apps.home.ocr import app_detrec
from apps.home.ocr import app_rec
#import cropper
#import cropper_rec
import sys

def result(images):

    detandrec,reconly=app_detrec.detrec(images),app_rec.rec(images)

    best_results=[]
    for i in range(len(detandrec)):
        
        if detandrec[i]:
            if reconly[i]:
                if detandrec[i][1]>reconly[i][1]:
                    value=detandrec[i][0]
                    confidence=detandrec[i][1]
                    best_results.append((value.split('-')[0] + '-' + value.split('-')[1][2:],confidence))
                else:
                    value=reconly[i][0]
                    confidence=reconly[i][1]
                    best_results.append((value.split('-')[0] + '-' + value.split('-')[1][2:],confidence))
            else:
                value=detandrec[i][0]
                confidence=detandrec[i][1]
                best_results.append((value.split('-')[0] + '-' + value.split('-')[1][2:],confidence))
        else:
            try:
                value=reconly[i][0]
                confidence=reconly[i][1]
                best_results.append((value.split('-')[0] + '-' + value.split('-')[1][2:],confidence))
            except:
                print("no detection")
                best_results.append('no card detected')
    return best_results
