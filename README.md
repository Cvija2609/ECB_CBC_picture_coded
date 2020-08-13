# ECB_CBC_picture_coded
This repository consists of a program written in Python. This program codes a picture using AES_CBC mode or AES_ECB mode.
Furthermore it shows lack of difusion that AES_ECB mode has.

How to use this program:
1) Enter the path to the file that is picture (available formats: '.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')
2) Enter the cipher key that will code your picture (keylen should be between 0 and 32 bits)
3) Enter the mode of AES (CBC and ECB are only available)

Then wait for few seconds (or minutes depending on picture size) and picture_name_coded.format should appear in the same path
(directory) that is given in 1).
