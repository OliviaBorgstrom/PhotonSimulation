import pyg4ometry
gdmls = ["PipeAl2219F.gdml", "PipeBeTV56.gdml", "RichMuMetal.gdml", "RichRich1DiaphramMaterial.gdml", "RichRich1G10.gdml", "RichRich1GasWindowQuartz.gdml", "RichRich1Mirror2SupportMaterial.gdml", "RichRich1MirrorCarbonFibre.gdml", "RichRich1MirrorGlassSimex.gdml", "RichRich1Nitrogen.gdml", "RichRich1PMI.gdml", "RichRichPMTAnodeMaterial.gdml", "RichRichPMTEnvelopeMaterial.gdml", "RichRichPMTPhCathodeMaterial.gdml", "RichRichPMTQuartzMaterial.gdml", "RichRichSoftIron.gdml", "Vacuum.gdml"]
for gdml in gdmls:
    print("doing: ", gdml)
    r = pyg4ometry.gdml.Reader(gdml)
    l = r.getRegistry().getWorldVolume()
    v = pyg4ometry.visualisation.VtkViewer()
    v.addLogicalVolume(l)
    v.exportOBJScene(gdml)