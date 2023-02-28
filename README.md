<p align="center">
<img src="https://img.icons8.com/ios-glyphs/512/general-ocr.png" 
        alt="Picture" 
        width="300" 
        height="200" 
        style="display: block; margin: 0 auto" />
</p>

# OCR Part of the YACC project, made by PONNOU Wilfried and Sary Ballou
## <div align="center">➊ To run OCR make sure to downlad detection weights:</div>
[Download detection model weights](https://drive.google.com/file/d/1Dyw5hAkQwpBJsnJRdbFyc3o1PIM1jk3M/view?usp=sharing)
, rename it as db_resnet50_latest.pt if it is not already the case and put it in this folder
## <div align="center">➋ Install dependencies by running the following command:</div>
```
$pip install -r requirements.txt
```
#### If you face dependencies issues try to use virtual python environment.
## <div align="center">➌ After that, to perform OCR on YuGiOh Cards, run the following command:</div>
```
$python main.py <path to your image file>
```
#### we provide a test image, you could run the following command to test it:
```
$python main.py test.jpg
```
## <div align="center">➍ You can explore the notebooks folder to understand how we've scrapped data and made our ~5000 YugiOh card images dataset, and how we've made our custom card detector:</div>
```
https://www.cards-capital.com/ © all rights reserved for the card images
```