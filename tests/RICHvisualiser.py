import pyg4ometry
r = pyg4ometry.gdml.Reader("RICH1.gdml")
l = r.getRegistry().getWorldVolume()
v = pyg4ometry.visualisation.VtkViewer()
v.addLogicalVolume(l)
v.view()

