import sys, os
sys.path.append(os.path.join(os.getcwd(),'ocr'))


from ocr import app_detrec, app_rec, ocr_main, cropper
from API import api_main
from mkmsdk.mkm import Mkm
from mkmsdk.api_map import _API_MAP

images=sys.argv[1]

detandrec,reconly=app_detrec.detrec(images),app_rec.rec(images)

ocr_result = ocr_main.result(images)

mkm_sandbox = Mkm(_API_MAP["2.0"]["api"], _API_MAP["2.0"]["api_sandbox_root"])

for image in ocr_result:
    print(image[0])
    try:
        api_main.card_search(image[0])
    except:

        print('failure for image code' + image[0])
