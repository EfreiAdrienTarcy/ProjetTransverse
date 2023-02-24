<img src="https://img.icons8.com/ios-glyphs/512/general-ocr.png" 
        alt="Picture" 
        width="300" 
        height="200" 
        style="display: block; margin: 0 auto" />
<h1 align="center">OCR Part of the YACC project, made by PONNOU Wilfried and Sary Ballou</h1>
<h2 align="center">➊ To run OCR make sure to downlad detection weights:</h2>
```
https://drive.google.com/file/d/1Dyw5hAkQwpBJsnJRdbFyc3o1PIM1jk3M/view?usp=sharing
#rename it as db_resnet50_latest.pt if it is not already the case
#And put it in this folder
```
<h2 align="center">➋ Install dependencies by running the following command:</h2>
```
$pip install -r requirements.txt
```
#### If you face dependencies issues try to use virtual python environment.
<h2 align="center">➌ After that, to perform OCR on YuGiOh Cards, run the following command:</h2>
```
$python main.py <path to your image file>
```
#### we provide a test image, you could run the following command to test it:
```
$python main.py test.jpg
```
<h2 align="center">➍ You can explore the notebooks folder to understand how we've scrapped data and made our ~5000 YugiOh card images dataset, and how we've made our custom card detector:</h2>
```
https://www.cards-capital.com/ © all rights reserved for the card images
```

