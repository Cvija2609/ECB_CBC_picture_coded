from PIL import Image
import os.path
import sys
from Crypto.Cipher import AES

padding = b'\x00'
padding2 = b'\x0e'
ECB = "ecb"
CBC = "cbc"


def file_exists(file):
    if os.path.isfile(file):
        return True
    return False


datoteka = input("Enter the path to the file that is picture: ")

if file_exists(datoteka):
    if datoteka.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
        key = input("Enter the cipher key: ").encode()
        mode = input("Enter the AES cipher mode (cbc ili ecb): ")

        if mode != CBC and mode != ECB:
            print("Wrong mode, ECB or CBC available", file = sys.stderr)
            exit(5)

        keylen = len(key)

        if keylen > 32:
            print("Key length is too big", file=sys.stderr)
            exit(1)
        elif 16 <= keylen <= 32:
            bit = 2 ** 5
        elif 0 <= keylen < 16:
            bit = 2 ** 4

        punjenje = bit - keylen % bit

        for i in range(0, punjenje):
            key += padding

        p = datoteka.split("/")
        put = ""

        for f in p[0:-1]:
            put += f + "/"

        im = Image.open(datoteka)

        width, height = im.size

        pix = im.load()

        bitmap = list()

        for i in range(0, width):
            for j in range(0, height):
                d = list()
                for c in pix[i, j]:
                    e = c.to_bytes(2, byteorder='big')
                    for k in range(0, 14):
                        e += padding2
                    d.append(e)
                bitmap.append(tuple(d))

        bmlen = len(bitmap)
        bitmap_coded = list()

        for tup in bitmap:
            if mode == ECB:
                obj = AES.new(key, AES.MODE_ECB)
            else:
                obj = AES.new(key, AES.MODE_CBC)
            mr = tup[0]
            mg = tup[1]
            mb = tup[2]

            cr = obj.encrypt(mr)
            cg = obj.encrypt(mg)
            cb = obj.encrypt(mb)

            bitmap_coded.append((cr, cg, cb))

        bmc = list()
        for tup in bitmap_coded:
            red = int.from_bytes(tup[0], "big") % 255
            green = int.from_bytes(tup[1], "big") % 255
            blue = int.from_bytes(tup[2], "big") % 255
            bmc.append((red, green, blue))

        for j in range(0, width):
            for k in range(0, height):
                pix[j, k] = bmc[j * height + k]      # j*3 + k => ternarni sustav

        slika = p[-1].split(".")

        im.save(put + slika[0] + "_coded" + "_" + mode + "." + slika[1])

    else:
        print("File is not a picture", file=sys.stderr)
        exit(2)
else:
    print("File does not exist", file=sys.stderr)
    exit(3)