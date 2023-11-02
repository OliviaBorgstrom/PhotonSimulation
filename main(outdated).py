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
        self.add_dependency(element)

        refs = element.find_all(ref=True, recursive=True)
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
        f.close()

class structure:
    registeredStructures = []
    registeredMaterials = []
    
    def __init__(self, xml):
        self.xml = xml
        self.material = None
        self.needsSplitting = False
        self.splitStrictures = {}
        structure.registeredStructures.append(self)
    
    def findMaterial(self):
        self._findMaterial_recursive(self.xml)
        if self.needsSplitting:
            self._splitStructure_recursive(self.xml)
    
    def _findMaterial_recursive(self, element):
        refs = element.find_all(ref=True, recursive=True)
        
        if not refs:
            #?????
            return
        else:
            for each in refs:
                if each.name == 'materialref' and not self.material:
                    self.material = each
                    return
                elif each.name == 'materialref' and self.material:
                    self.needsSplitting = True
                    return
                elif each.name == 'volumeref':
                    next = soup.find(attrs={"name": each['ref']})
                    self._findMaterial_recursive(next)
                    #multiple materials need to split
                #next = soup.find(attrs={"name": each['ref']})
                #self.find_dependencies_recursive(next)
            #material not found case?
            
    
    def _splitStructure_recursive(self,element):
        volumerefs = element.find_all("volumeref", recursive=True)
        # refs = element.find_all(ref=True, recursive=True)
        # for each in refs:
        #     if each.name == 'volumeref':
        #         next = soup.find(attrs={"name": each['ref']})
        #         self._splitStructure_recursive(next)
        
        #found a base material

        

with open("RICH1.gdml") as RICH1:
    soup = BeautifulSoup(RICH1, "xml")
    structures = soup.find("structure").findChildren(recursive=False)

    for s in structures:
        obj = structure(s)
        obj.findMaterial()
    '''
    structureobjs = []
    for structure in structures:
        structures.append(new structure)
        structure.findMaterial
        if structure has more than one material:
            extrastructures = structure.split()
            structures.append(extrastructures)
    
    for each structureobj:
        group them
        then perform the rest
    '''
