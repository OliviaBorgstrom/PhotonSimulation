from bs4 import BeautifulSoup

class flatVolume: #volumes with no references to other volumes
    def __init__(self, logical, physical):
        self.logicalvolume = logical 
        self.physicalvolume = physical
    
    def __repr__(self) -> str:
        return str(self.logicalvolume) + "\n" + str(self.physicalvolume)

class objectGroup:
    registeredMaterials = {}
    
    def __init__(self, material, element):
        self.material = material
        self.elements = [element]
        
        objectGroup.registeredMaterials[material] = self
        
        self.dependencies = set()
        self.defines = []
        self.materials = []
        self.solids = []
        self.physvols = []
        self.logicalvols = []
        
    def append(self, element):
        self.elements.append(element)
        
    def evaluate_dependencies(self, Air):
        print("---------------------------------------------------------\nDOING group: ",self.material, self, "")
        for element in self.elements:
            if not element.logicalvolume in self.logicalvols:
                self.logicalvols.append(element.logicalvolume)
            if not element.physicalvolume in self.physvols:
                self.physvols.append(element.physicalvolume)
            self.find_dependencies_recursive(Air)
            self.find_dependencies_recursive(element.logicalvolume)
            self.find_dependencies_recursive(element.physicalvolume) 
        print("---------------------------------------------------------\n")
        
        self.write_gdml()
        
    def find_dependencies_recursive(self, element):
        refs = element.find_all(ref=True, recursive=True)  
        #refs = element.find_all(re.compile("ref"))
        if refs and not self.dependencies.union(set(element)) == self.dependencies:
            for each in refs:
                if each.name != "volumeref":
                    next = soup.find(attrs={"name": each['ref']})
                    self.find_dependencies_recursive(next)
        
        self.add_dependency(element)
        
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
                if not element in self.defines:
                    self.defines.append(element)
            elif current.name == "materials":
                if not element in self.materials:
                    self.materials.append(element)
            elif current.name == "solids":
                if not element in self.solids:
                    self.solids.append(element)
            elif current.name == "structure":
                pass
                #self.structures.add(element)
            else:
                print("im confused")
    
    def write_gdml(self):
        filename = "generated_files/" + self.material + ".gdml"
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
        f.write("""<box name="world_volume_shape_0x4961250" x="100000" y="100000" z="100000" lunit="cm"/>""")
        for solid in self.solids:
            f.write(solid.prettify())
        f.write("</solids>\n")
        f.write("<structure>\n")
        for logicalvol in self.logicalvols:
            f.write(logicalvol.prettify())
        f.write("<volume name=\"world_volume\"><materialref ref=\"Air\"/><solidref ref=\"world_volume_shape_0x4961250\"/>")
        for physvol in self.physvols:
            f.write(physvol.prettify())
        f.write("</volume>")
        f.write("</structure>\n")
        f.write("<setup name=\"default\" version=\"1.0\">\n<world ref=\"world_volume\"/>\n</setup>")
        f.write("</gdml>")
        #need to add worldvolume to all of them for the setup
        f.close()
        
with open("RICH1.gdml") as RICH1:
    soup = BeautifulSoup(RICH1, "xml")
     
    volumes = soup.find_all("volume", recursive=True)
    flatVolumes = []
    for volume in volumes:
        if volume.find("volumeref"):
            continue
        flatVolumes.append(volume)
    
    for logicalvol in flatVolumes:
        material = logicalvol.find("materialref")['ref']
        physvol = soup.find_all(attrs={"ref": logicalvol['name']}, recursive=True)
        
        for each in physvol:
            #assign material at this point
            obj = flatVolume(logicalvol,each.parent)
            if material in objectGroup.registeredMaterials:
                objectGroup.registeredMaterials[material].append(obj)
            else:
                objectGroup(material, obj)
    
    groups = list(objectGroup.registeredMaterials.values())
    
    Air = soup.find(attrs={"name": "Air"})
    
    for each in groups:
        each.dependencies.add(Air)
        each.materials.append(Air)
        each.evaluate_dependencies(Air)
        
        
        
        
#new idea find all volumes which dont refernce any others, register their materials.
#then find the physvol that refernces that logical volume and link them together
#final idea is put all the phys volumes under the world volume and put that in the setup