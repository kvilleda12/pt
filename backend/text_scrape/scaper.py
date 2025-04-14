from pypdf import PdfReader
import pymupdf 


#need to create a database before startign 
# to extract all the text 
pdf = "Mobility-Morsole.pdf"
doc = pymupdf.open(pdf)
out = open("{pdf}.txt", 'wb')
for page in doc: 
    text = page.get_text().encode('utf8')
    out.write(text)
    out.write(bytes((12,)))
out.close() 

#to extract all the images from teh same file 

for page_index in range(len(doc)): # iterate over pdf pages
    page = doc[page_index] # get the page
    image_list = page.get_images()

    # print the number of images found on the page
    if image_list:
        print(f"Found {len(image_list)} images on page {page_index}")
    else:
        print("No images found on page", page_index)

    for image_index, img in enumerate(image_list, start=1): # enumerate the image list
        xref = img[0] # get the XREF of the image
        pix = pymupdf.Pixmap(doc, xref) # create a Pixmap

        if pix.n - pix.alpha > 3: # CMYK: convert to RGB first
            pix = pymupdf.Pixmap(pymupdf.csRGB, pix)

        pix.save("page_%s-image_%s.png" % (page_index, image_index)) # save the image as png
        pix = None