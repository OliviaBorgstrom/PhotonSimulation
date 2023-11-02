import mitsuba as mi
import matplotlib.pyplot as plt

mi.set_variant("scalar_rgb")
scene_description = {
    'type': 'scene',
    
    'integrator': { 
        'type': 'path', 
        'max_depth': 4,
        'hide_emitters': False,
    },

    'sensor': { 
        'type': 'perspective',
        'fov': 40,
        'to_world': mi.ScalarTransform4f.look_at(origin=[200, 1800, 700],
                                                 target=[200, 2200, 1400],
                                                 up=[0, 0, 1]),
        'sampler': {
            'type': 'independent',
            'sample_count': 1,
        },
        'film': {
            'type': 'hdrfilm',
            'width': 1024,
            'height': 1024,
            'file_format': 'openexr',
            'pixel_format': 'rgb',
            'component_format': 'uint32',
            'filter' : {
                'type': 'tent',
            },
        },
    },

    'MirrorBSDF' : {
        'type' : 'conductor',
        'material' : 'none',
    },

    'test' : {
        'type' : 'diffuse',
        'reflectance': {
            'type' : 'rgb',
            'value': [1, 1, 1],
        },
    },

    'structure' : {
        'type' : 'obj',
        'filename' : 'generated_files/RichRichSoftIron.gdml.obj',
        'to_world': mi.ScalarTransform4f.look_at(origin=[200, 500, -0.5],
                                                 target=[200, 1600, -0.5],
                                                 up=[0, 0, 1]),
        'bsdf_id' : {
            'type' : 'ref',
            'id' : 'test',
        },
    },
}


scene = mi.load_dict(scene_description)
image = mi.render(scene, spp=256)


plt.axis("off")
plt.imshow(image ** (1.0 / 2.2)); # approximate sRGB tonemapping

mi.util.write_bitmap("my_first_render.png", image)