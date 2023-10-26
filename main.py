import pyg4ometry
from xml.dom.minidom import parse
from bs4 import BeautifulSoup
import pandas as pd
import re

class objectGroup:
    registeredMaterials = {}
    
    def __init__(self, material, element):
        self.material = material
        self.elements = [element]
        
        objectGroup.registeredMaterials[material] = self
        
        self.dependencies = set()
        self.defines = set()
        self.materials = set()
        self.solids = set()
        self.structures = set()
        
    def append(self, element):
        self.elements.append(element)
        
    def evaluate_dependencies(self):
        if self.material == "RichRich1Nitrogen" or self.material == "RichR1RadiatorGas" or self.material == "RichAir":
            return
        print("---------------------------------------------------------\nDOING group: ",self.material, self, "")
        for element in self.elements:
            self.find_dependencies_recursive(element) 
        print("---------------------------------------------------------\n")
        
        self.write_gdml()
        
    def find_dependencies_recursive(self, element):
        #self.dependencies.add(element)
        self.add_dependency(element)

        refs = element.find_all(ref=True, recursive=True)
        print(refs)
        
        
        #refs = element.find_all(re.compile("ref"))
        if not refs or self.dependencies.union(set(element)) == self.dependencies:
            return
        else:
            for each in refs:
                next = soup.find(attrs={"name": each['ref']})
                self.find_dependencies_recursive(next)
    
    def add_dependency(self,element):
        self.dependencies.add(element)
        nextparent = element.parent
        current = element
        while nextparent.name != "gdml" or None:
            current = nextparent
            nextparent = current.parent
        
        if current == None or nextparent == None:
            print("Im confused")
        else:
            if current.name == "define":
                self.defines.add(element)
            elif current.name == "materials":
                self.materials.add(element)
            elif current.name == "solids":
                self.solids.add(element)
            elif current.name == "structure":
                self.structures.add(element)
            else:
                print("im confused")
           
            
            
        #check if no parent
    def write_gdml(self):
        filename = self.material + ".gdml"
        f = open(filename, "w")
        f.write("<?xml version=\"1.0\"?>\n")
        f.write("<gdml xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:noNamespaceSchemaLocation=\"http://service-spi.web.cern.ch/service-spi/app/releases/GDML/schema/gdml.xsd\">\n")
        f.write("<define>\n")
        for define in self.defines:
            f.write(define.prettify())
        f.write("</define>\n")
        f.write("<materials>\n")
        for material in self.materials:
            f.write(material.prettify())
        f.write("</materials>\n")
        f.write("<solids>\n")
        for solid in self.solids:
            f.write(solid.prettify())
        f.write("</solids>\n")
        f.write("<structure>\n")
        for structure in self.structures:
            f.write(structure.prettify())
        f.write("</structure>\n")
        f.write("<setup name=\"default\" version=\"1.0\">\n<world ref=\"world_volume\"/>\n</setup>")
        f.write("</gdml>")
        #need to add worldvolume to all of them for the setup
        f.close()
    
#RICH1 = parse("RICH1.gdml")
#structures = RICH1.getElementsByTagName("volume")

with open("RICH1.gdml") as RICH1:
    soup = BeautifulSoup(RICH1, "xml")
    #refs = soup.find_all(re.compile("ref"))
    #print(refs)
    structures = soup.find_all("volume")
    #print(structures)
    structure = soup.find(attrs={"name": "world_volume"})
    # for structure in structures:
    #     if structure['name'] == 'world_volume':
    #         continue
        
    material = structure.find("materialref")['ref']
    
    if material in objectGroup.registeredMaterials:
        objectGroup.registeredMaterials[material].append(structure)
    else:
        objectGroup(material, structure)
    
    groups = list(objectGroup.registeredMaterials.values())
    
    
    #the world volume causes issues
    # if world_volume != None:
    #     for each in groups:
    #         if each.material != "Air":
    #             each.append(world_volume)
    # else:
    #     print("There is no world!!")
    
    groups = list(objectGroup.registeredMaterials.values())
    for each in groups:
        each.evaluate_dependencies()
    # for each in groups:
    #     #print(key)
    #     each.evaluate_dependencies()
        
#print(structures)

#groupings = []

#for structure in structures:
    #material = (structure.getElementsByTagName("materialref"))[0].getAttribute("ref")
    #if material in objectGroup.registeredMaterials:
        #objectGroup.registeredMaterials[material].append(structure)
    #else:
        #groupings.append(objectGroup(material, structure))

#for group in groupings:

# r = pyg4ometry.gdml.Reader("RichRich1MirrorCarbonFibre.gdml")
# l = r.getRegistry().getWorldVolume()
# v = pyg4ometry.visualisation.VtkViewer()
# v.addLogicalVolume(l)
# v.exportOBJScene("RichRich1MirrorCarbonFibre")

#what is bordersurface and evaluate the physvol ref
#how to deal with assemblies?
