from PIL import Image
for i in range(14, 15):
    im = Image.open('map1_' + str(i) + '.png')
    im_rotate = im.rotate(-23, expand=True)
    im_rotate.save('map1_' + str(i) + 'r.png')
