import gtk
import os
from xml.etree.ElementTree import parse, Element, SubElement
from diagnosis.ElementTree_pretty import prettify, indent

# Once user installed this 'diagnosis' package into the system, then the xml 
# path should be '/usr/share/diagnosis/xml' to write/read. Otherwise, we have 
# write/read xml from the previous directory path called '../data/xml'.

xmlDataDir = '/usr/share/diagnosis/xml'
if not os.path.isdir(xmlDataDir):
    __binDir__ = os.path.dirname(__file__)
    xmlDataDir = os.path.abspath(os.path.join(__binDir__, '../data/xml/'))
__currentXmlFile__ = 'register.xml'
currentRegisterXml = os.path.join(xmlDataDir, __currentXmlFile__)
__previousXmlFile__ = 'previous_' + __currentXmlFile__
previousRegisterXml = os.path.join(xmlDataDir, __previousXmlFile__)

__setupXmlFile__ = 'setup.xml'
setupXml = os.path.join(xmlDataDir, __setupXmlFile__)
    
_seperator_ = ' : '


class Tree():
    
    def __init__(self, treename=None, builder=None):        
        if treename and builder:				
            treestore = self.getTreeStore(treename)
            self.treestore = builder.get_object(treestore)
            
        # to trace the available file type while edit/copy model by the user.
        # initialize empty dictionary. update the in this dict, what ever 
        # we adding like 'Analysis' and 'forecast hours'. 
        self._filetype_collection = {}
        self.__ensembleno = 0
        
    def __getitem__(self, name):
        return self.getTreeStore(name)
        
    def getTreeStore(self, treename):  
    
        trees = {'models': 'model_treestore',
                 'observations': 'obs_treestore',
                 'climatologies': 'clim_treestore',          
                 'model_temp': 'model_temporaray_treestore',
                 'model_file': 'model_files_treestore',
                 'model_fcst': 'model_fcst_hours_treestore'}
        
        return trees.get(treename, None)       
        
            
    def loopElements(self, elements):        
        for topEl in elements:
            # loop through all the elements
            for rootEl in topEl:
                self.loopRootElement(rootEl)
            
    def loopRootElement(self, root, addtype='append', row=None):                

        uid = root.get('id')
        tmp = list(root)
        # get the institution, name & version from the xml tree elements.
        # if text attribute returned None then the empty string ('') should be 
        # assigned to that variable. 
        institution = tmp[0].text or ''
        name = tmp[1].text or ''
        version = tmp[2].text or ''       
        
        # generate the parent txt from the name & version
        parentTxt = 'Name' + _seperator_ + name + ' Version' + _seperator_ + version 
 
        # add or insert name & version to the tree as parent
        if addtype == 'append':
            parent = self.treestore.append(None, [parentTxt])
        elif addtype == 'insert':
            parent = self.treestore.insert(None, row, [parentTxt])
      
        # add the institution child element to the above parent iter
        institutionTxt = "Source of data" + _seperator_ + institution
        self.treestore.append(parent, [institutionTxt])        
                        
        # add the uid child element to the parent
        uidTxt = 'Uid' + _seperator_ + uid
        self.treestore.append(parent, [uidTxt])
        
        # finally add the remaining elements to the parent iter                 
        for subEl in root:
            if not list(subEl):
                # single element.                 
                if subEl.tag not in ['name', 'version', 'institution']:
                    # add the child elements other than name, version & institution
                    childTxt = subEl.tag.capitalize() + _seperator_
                    # add '' if text attrib returns None                     
                    childTxt += subEl.text or ''
                    # add the child iter to the parent iter 
                    chid = self.treestore.append(parent, [childTxt])
            else:   
                # the subEl element contains inner elements too.
                self._loop_model_elements(subEl, parent)
                        
    def _loop_model_elements(self, element, parent=None):       
        
        tag = element.tag
        
        if tag == 'ensemble':
            ensembleId = element.get('id')
            ensembleElement = list(element)            
            # get the name value            
            name = ensembleElement.pop(0).text or ''            
            # get the no element
            no = ensembleElement.pop(0) 
            number = no.text
            # initialize the ensemble no into the collections
            self.__ensembleno = int(number)
            self._filetype_collection[self.__ensembleno] = []
            # make the ensemble parent txt 
            ensTxt = 'Ensemble Name' + _seperator_ + name + ' '
            ensTxt += no.tag.capitalize() + _seperator_ + number            
            # add the ensemble txt to the parent(argument parent) 
            ensParent = self.treestore.append(parent, [ensTxt])
            # add the ensemble uid to ensemble parent 
            ensid = 'Ensemble ID' + _seperator_ + ensembleId
            self.treestore.append(ensParent, [ensid])
            # add the description to the ensemble parent 
            desTxt = 'Description' + _seperator_
            # get the ensemble description or empty '' empty string if None 
            desTxt += ensembleElement.pop(0).text or ''            
            self.treestore.append(ensParent, [desTxt])
            
            for ensel in ensembleElement:
                # ensemble forecast available
                if ensel.tag == 'forecast':
                    self.__loop_forecast_elements(ensel, ensParent)
                elif ensel.tag == 'analysis':
                    anlTxt = ensel.tag.capitalize() + _seperator_
                    ensel = list(ensel)
                    if ensel:
                        anlTxt += ensel[0].text
                    self.treestore.append(ensParent, [anlTxt]) 
                    self._filetype_collection[self.__ensembleno].append('Analysis')
        
        elif tag == 'analysis':
            anlTxt = tag.capitalize() + _seperator_
            element = list(element)
            if element:
                anlTxt += element[0].text
            self.treestore.append(parent, [anlTxt]) 
            # initialize the 0 th collections. i.e. this is model forecast.
            self.__ensembleno = 0
            if self.__ensembleno not in self._filetype_collection:
                self._filetype_collection[self.__ensembleno] = []
            self._filetype_collection[self.__ensembleno].append('Analysis')
                        
        elif tag == 'forecast':
            # initialize the 0 th collections. i.e. this is model forecast.
            self.__ensembleno = 0
            if self.__ensembleno not in self._filetype_collection:
                self._filetype_collection[self.__ensembleno] = []
            # model forecast available
            self.__loop_forecast_elements(element, parent)        
            
                                    
    def __loop_forecast_elements(self, fcstelement, parent=None):
            
        # make the fcst parent text & add to the argument parent
        fcstTxt = fcstelement.tag.capitalize()
        fcstParent = self.treestore.append(parent, [fcstTxt])
        for hrfile in fcstelement:
            hour = hrfile.get('hour')
            self._filetype_collection[self.__ensembleno].append(hour)
            hrTxt = hour + _seperator_ + hrfile.text            
            # add the forecast hour file into the fcst parent 
            self.treestore.append(fcstParent, [hrTxt])      
                
                
    def clear(self):
        self.treestore.clear()
        
        
class XmlReader():
    
    def __init__(self, builder):
     
        if not os.path.isfile(setupXml):
            self.initSetup(setupXml)
        if not os.path.isfile(currentRegisterXml):
            self.initRegister(currentRegisterXml)
        self.currentXmlDom = parse(currentRegisterXml)
        if not os.path.isfile(previousRegisterXml):
            self._fromXmlDom2File(self.currentXmlDom, previousRegisterXml)          
        self.previousXmlDom = parse(previousRegisterXml)
        self.builder = builder 
               
    def initRegister(self, fpath):
        f = open(fpath, 'w')
        
        root = Element('registration')
        SubElement(root, 'models')
        SubElement(root, 'climatologies')
        SubElement(root, 'observations')
        
        f.write(prettify(root))
        f.close()
        
        
    def initSetup(self, fpath):
        
        f = open(fpath, 'w')
        
        root = Element('setup')
        cdat = SubElement(root, 'cdat')
        SubElement(cdat, 'path')
        
        # add the default institutions
        institutions = SubElement(root, 'institutions')
        ins1 = SubElement(institutions, 'institution')
        ins1.text = ""
        ins2 = SubElement(institutions, 'institution')
        ins2.text = "NCMRWF"
        ins3 = SubElement(institutions, 'institution')
        ins3.text = "CMA"
        ins4 = SubElement(institutions, 'institution')
        ins4.text = "CMC"
        
        # add the default climatology time resolutions
        climatology = SubElement(root, 'climatology')
        timeResolution = SubElement(climatology, 'time-resolution')
        time1 = SubElement(timeResolution, 'time')
        time1.text = ""
        time2 = SubElement(timeResolution, 'time')
        time2.text = "daily"
        time3 = SubElement(timeResolution, 'time')
        time3.text = "monthly"
        
        f.write(prettify(root))
        f.close()
        
    def _fromXmlDom2File(self, dom, tofile):        
        indent(dom.getroot(), 0)
        dom.write(tofile, "utf-8")
        
    def savePrevious(self, action='copy'):
        if action == 'copy':
            xmldom = self.currentXmlDom
        elif action == 'nocopy':
            xmldom = self.previousXmlDom      
            # make free memory
            del self.previousXmlDom
        indent(xmldom.getroot(), 0)
        xmldom.write(previousRegisterXml, "utf-8")
        self.previousXmlDom = parse(previousRegisterXml)
        
    def save(self):
        indent(self.currentXmlDom.getroot(), 0)
        self.currentXmlDom.write(currentRegisterXml, "utf-8")
        
    def swape(self):       
        self.previousXmlDom, self.currentXmlDom = self.currentXmlDom, self.previousXmlDom
        self.savePrevious(action = 'nocopy')
        self.save()
        self.refresh()
        
    def refresh(self):
        self.run('models')
        self.run('observations')
        self.run('climatologies')
        
    def run(self, name):
        treeObj = Tree(name, self.builder)
        root = self.currentXmlDom.getroot()                
        elements = root.getiterator(name)  
        # Clear the treestore object. i.e. remove all the contents from this treestore   
        treeObj.clear()  
        # Add the new contents to the treestore object.      
        treeObj.loopElements(elements) 
    
       
        
        
