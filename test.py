
import base64

def read_in_chunks(infile, chunk_size=1024):
    while True:
        chunk = infile.read(chunk_size)
        if chunk:
            yield chunk
        else:
            # The chunk was empty, which means we're at the end
            # of the file
            return

def encode():
    infile = open('saurav.jpg')
    for chunk in read_in_chunks(infile):
        print chunk

def encode2():
	imageFile = open('saurav.jpg')
	base64_string = base64.b64encode(imageFile.read())
	base64_string="abcdefghijklmnopqrstuvwxyz"
	n=4
	for i in xrange(0,len(base64_string),n):
		print base64_string[i:i+n]



def decode():
    pass

def string2image():
	fh = open("imageToSave.png", "wb")
	fh.write(str.decode('base64'))
	fh.close()

if __name__ == '__main__':
	encode2()

