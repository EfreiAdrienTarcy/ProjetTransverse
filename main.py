import sys, os
sys.path.append(os.path.join(os.getcwd(),'ocr'))

from ocr import app_detrec, app_rec, ocr_main, cropper
#from API import api_main
from mkmsdk.mkm import Mkm
from mkmsdk.api_map import _API_MAP

images=sys.argv[1]

detandrec,reconly=app_detrec.detrec(images),app_rec.rec(images)

ocr_result = ocr_main.result()

mkm_sandbox = Mkm(_API_MAP["2.0"]["api"], _API_MAP["2.0"]["api_sandbox_root"])

for image in ocr_result:
    print(image[0])
    print(type(image[0]))
    try:
        find = mkm_sandbox.market_place.find_product(params={"search":image[0],"idGame":3,"idLanguage":1})
        product_id = find.json().pop('product')[0].pop('idProduct')

        product = mkm_sandbox.market_place.product(product=product_id)

        tmp = product.json().pop('product')
        tmp_price_guide = tmp.pop('priceGuide')

        print('idProduct')
        print(tmp.get('idProduct'))

        print('\nenName')
        print(tmp.get('enName'))

        print('\nfrName')
        print(tmp.get('localization')[1].get('name'))

        print('\nimageURL')
        print(tmp.get('image'))

        print('\nprice_average')
        print(tmp_price_guide.get('AVG'))

        print('\nsellprice')
        print(tmp_price_guide.get('SELL'))

        print('\nselltrend')
        print(tmp_price_guide.get('TREND'))
    except:
        print('failure')