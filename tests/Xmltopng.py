import scene as mi 
mi.set_variant('scalar_rgb')
import matplotlib.pyplot as plt

scene = mi.load_file("RICHxml.xml")

image = mi.render(scene)
plt.figure(figsize = (20,20))
plt.axis('off')
plt.imshow(image ** (1.0 / 2.2))
plt.savefig('test.png')
