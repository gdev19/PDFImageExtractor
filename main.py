# https://github.com/py-pdf/sample-files/blob/main/023-cmyk-image/cmyk-image.pdf
from pypdf import PdfReader

reader = PdfReader("cmyk-image.pdf")

page = reader.pages[0]

for count, image_file_object in enumerate(page.images):
    with open(str(count) + image_file_object.name, "wb") as fp:
        fp.write(image_file_object.data)
        

