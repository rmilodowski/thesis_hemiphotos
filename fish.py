import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt

#file = 'DSCN7695.JPG'  # image file name
file_name = 'ROADS15'
file = './road_hemi_Apr19/hemiphotos_edited/%(hemi_photo)s.jpg' % {'hemi_photo' : file_name}
threshold = 147        # sky brightness threshold (0-255)
nrings = 10            # number of rings for VAI calculation

# read image and split into colours
im = plt.imread(file)
red = im[:,:,0]
grn = im[:,:,1]
blu = im[:,:,2]

# x, y, radius and zenith angle coordinates for the image
ny, nx, c = im.shape
imrad = 0.89*ny/2  # limit radius of image to 180 degrees
y, x = np.ogrid[-ny/2:ny/2,-nx/2:nx/2]
r = np.sqrt(x**2 + y**2) / imrad
theta = ma.masked_where(r > 1, r*np.pi/2)

# threshold and mask the blue image for sky
sky = blu > threshold
sky = ma.masked_where(r > 1, sky)

# show the image and sky map for comparison
plt.subplot(121)
plt.imshow(im)
plt.xticks([])
plt.yticks([])
plt.subplot(122)
plt.imshow(sky,cmap='gray')
plt.xticks([])
plt.yticks([])

view = ma.sum(sky*np.cos(theta)) / ma.sum(np.cos(theta))
print 'sky view fraction', view

dtheta = (np.pi/2) / nrings
VAI = 0
for i in range(nrings):
    theta0 = i*dtheta
    thetar = (i+0.5)*dtheta
    ring = sky[np.logical_and(theta>theta0, theta<=theta0+dtheta)]
    gap = ring.sum() / float(ring.size)
    VAI += 2*np.log(1/gap)*np.cos(thetar)*np.sin(thetar)*dtheta
print 'Vegetation area index ',VAI

plt.show()

#plt.savefig('/home/s1359318/rls_datastore/PhD/RC4/SVF/road_hemi_Apr19/ROAD20_examplefish.png', dpi=300)
