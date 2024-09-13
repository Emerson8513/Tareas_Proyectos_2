import qrcode
img = qrcode.make("14:45")
f = open("output.png", "wb")
img.save(f)
f.close()