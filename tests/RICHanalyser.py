import pyg4ometry
r = pyg4ometry.gdml.Reader("RICH1.gdml")
info = pyg4ometry.geant4.AnalyseGeometryComplexity(r.getRegistry().getWorldVolume())
info.printSummary()
