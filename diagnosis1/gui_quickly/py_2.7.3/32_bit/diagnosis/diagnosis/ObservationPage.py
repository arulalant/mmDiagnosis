import gtk
from xml.etree.ElementTree import Element, SubElement, Comment, tostring, ElementTree
from diagnosis.helpers import get_builder
from diagnosis.cdat_operations import cdfile_check
from diagnosis.ElementTree_pretty import indent
from diagnosis.dialog import DialogBox


_seperator_ = ' : '

class ObservationPage():
    __gtype_name__ = "ObservationPage"    
    
    def __init__(self, builder, xmltreeobject):        
        self.builder = builder
        self.xmlTreeObj = xmltreeobject
        self.institution = builder.get_object('obs_institution')
        self.name = builder.get_object('obs_name')
        self.version = builder.get_object('obs_version')
        self.uid = builder.get_object('obs_uid')   
        self.description = builder.get_object('obs_description_textbuffer')
        self.obsfile = builder.get_object('obs_file_chooser') 
        self.obsFileEntry = builder.get_object('obs_file_entry')
        self.label_status = builder.get_object('obs_file_label_status')
        self.uid.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#ECEAE9"))
        self.obsFileEntry.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#ECEAE9"))
        self.obsTreeView = builder.get_object('obs_treeview')  
        self.obsTreeStore = builder.get_object('obs_treestore')
        self.titleLabel = builder.get_object('obs_title')                
        self.institutionFn()
        self.form = builder.get_object('obs_form_scrolledwindow')
        self.form.hide()
        self._removeIter = None
        self._removeId = None
        
    
    def institutionFn(self):
        
        entryCompletion1 = self.builder.get_object('obs_institution_entrycompletion')
        entryCompletion1.set_text_column(0)
        self.institution.child.set_completion(entryCompletion1)
        
#        allInstititions = self.builder.get_object('institution_liststore')
#        
#        for i in ['', 'NCMRWF', 'CMA', 'CMC']:
#            allInstititions.append([i])
            
            
    def run(self):
        institution, name, version, uid = self.uid_update(action = 'return')
        
        
        observation = Element('observation', {'id': uid})
        
        institutionChild = SubElement(observation, 'institution')
        institutionChild.text = institution
        
        nameChild = SubElement(observation, 'name')
        nameChild.text = name
        
        versionChild = SubElement(observation, 'version')
        versionChild.text = version
        
        descriptionChild = SubElement(observation, 'description')
        startPosition, endPosition = self.description.get_bounds()
        descriptionChild.text = self.description.get_text(startPosition, endPosition)      
        
        File = self.obsFileEntry.get_text()
        fileChild = SubElement(observation, 'file')
        fileChild.text = File

        obsTop = self.xmlTreeObj.currentXmlDom.getiterator('observations')[0]
        
        def _addSubElementsToTree(parent, elements):
            for subEl in elements:
                childTxt = subEl.tag.capitalize() + _seperator_ + subEl.text 
                child = self.obsTreeStore.append(parent, [childTxt])
            
        
        def _addItemToTree(addtype, row=None):
        
            parentTxt = nameChild.tag.capitalize() + _seperator_ + nameChild.text 
            parentTxt += "   " + versionChild.tag.capitalize() + _seperator_ + versionChild.text 
            
            # add name & version to the tree as parent
            if addtype == 'append':
                parent = self.obsTreeStore.append(None, [parentTxt])
            elif addtype == 'insert':
                parent = self.obsTreeStore.insert(None, row, [parentTxt])
            
            # add the institution as child to the above tree parent
            _addSubElementsToTree(parent, [institutionChild])
            uid = "Uid" + _seperator_ + observation.get('id') 
            # add uid to the tree as child 
            self.obsTreeStore.append(parent, [uid])   
            # add the description & file as child to the above tree parent         
            _addSubElementsToTree(parent, [descriptionChild, fileChild])            
            
        
        # save the previous state xml 
        self.xmlTreeObj.savePrevious()  
                    
        if self.status in ['add', 'copy']:
            
            # append the elements to the xml 
            obsTop.append(observation)
            # append the entries to the iter tree store 
            _addItemToTree('append')
            
        
        elif self.status == 'edit':
        
            if self._removeIter:
                row = self.obsTreeStore.get_path(self._removeIter)[0]
                # remove the entries from the iter
                self.obsTreeStore.remove(self._removeIter)
                self._removeIter = None
                # add the entries to the iter tree store 
                _addItemToTree('insert', row)            
                # remove the elements from the xml 
                self._removeEntriesFromXml(obsTop, self._removeId)
                # insert the elements to the xml 
                obsTop.insert(row, observation)
                        
        # save the xml 
        self.xmlTreeObj.save()
        
    
    def file_operation(self):
        self.label_status.set_text('Checking ...')
        filePath = self.obsfile.get_filename()
        cdfilestatus = cdfile_check(filePath)
        if cdfilestatus:
            self.obsFileEntry.set_text(filePath)        
            self.label_status.set_text('Checking done. Ready to add !')           
        else:
            self.label_status.set_text('Wrong File! Can not open by cdat.\nChoose correct file !')
            
    def clearEntries(self):        
        self.institution.set_active(0)
        self.name.set_text('')
        self.version.set_text('')
        self.uid.set_text('')        
        self.description.set_text('')
        self.obsfile.set_filename('')
        self.obsFileEntry.set_text('')
        self.label_status.set_text('')
        
    def _setEntries(self, uid):
        
        ### The below find throws error. It may works in python 2.7. Check it 
        ### obs = self.xmlTreeObj.currentXmlDom.find(".//observations/observation[@id='"+ pid + "']")
        allobs = self.xmlTreeObj.currentXmlDom.getiterator('observation') 
        for obs in allobs:   
            if obs.get('id') == uid:              
                for el in obs:
                    self._setEntry(el.tag, el.text)
                return
    
    def _removeEntriesFromXml(self, obsTop, pid):
     
        for obs in obsTop:   
            if obs.get('id') == pid:
                obsTop.remove(obs)                
                return

                
    def _setEntry(self, name, value):
        
        if not value:
            value = ''
        if name == 'name':
            self.name.set_text(value)
        elif name == 'version':
            self.version.set_text(value)        
        elif name == 'institution':
            self.institution.child.set_text(value)        
        elif name == 'file':
            self.obsfile.set_filename(value)
            self.obsFileEntry.set_text(value)
        elif name == 'description':
            self.description.set_text(value)
        else:
            return None    
        
    def uid_update(self, action='None'):             
        # get the values from the institution, name & version entries
        institution = self.institution.child.get_text()        
        name = self.name.get_text()         
        version = self.version.get_text()  
        # form the list
        uidlist = [institution, name, version]
        # adjust the list text values without any spaces
        uidTxt = [text.replace(' ', '') for text in uidlist if text]
        # join dot in-between the list text values to make it as unique id.
        uidTxt = '.'.join(uidTxt)
        # set the unique id into the uid entry
        self.uid.set_text(uidTxt)
        
        if action == 'return':
            _corrected = []
            # correct the institution, name, version text spaces
            for text in uidlist:               
                text = text.split()
                # remove the begining empty spaces and joining with single 
                # space char if the text contains more than one word
                text = ' '.join(text) if len(text) != 1 else text[0]
                _corrected.append(text)
            # add the uid 
            _corrected.append(uidTxt)
            # return the values
            return _corrected    
            
    def add(self):
        if not self.form.get_visible():
            self.form.show()
        #self.titleLabel.set_text('Register New Observation')
        self.status = 'add'
          
    def copy(self, set_uid_endswith=' (Copy) '):
    
        if not self.form.get_visible():
            self.form.show() 
        self.status = 'copy' 
        #self.titleLabel.set_text('Register New Observation')
        treeselection = self.obsTreeView.get_selection()        
        treestore, parent_treeiter =  treeselection.get_selected()
        path = treestore.get_path(parent_treeiter)
        if not path:
            raise "Select any element to do copy "
        # get the uid from the treestore            
        uid = self.__get_uid__(treestore, path)
        # set the input entries
        self._setEntries(uid)                       
        # add the ' (Copy) ' to the uid entry by default.
        self.uid.set_text(self.uid.get_text() + set_uid_endswith)                           
                       
        if len(path) > 1:
            # user selected child element. So need to get its parent iter
            parent_treeiter = treestore.get_iter(path[0])
            
        # returning the uid and parent tree iter object
        return uid, parent_treeiter           

    def __get_uid__(self, treestore, path):

        row = path[0] if isinstance(path, (list, tuple)) else path
        # get the uid row by selecting (parent row, uid row)
        uid_row = (row, 1)
        # get the uid tree iter object
        uid_treeiter = treestore.get_iter(uid_row)
        # get the uid value as text. The uid text should be 'Uid : bla bla '. 
        # So we split it and to get exact uid. 
        return treestore.get_value(uid_treeiter, 0).split(_seperator_)[1]
         
    
    def edit(self):
            #self.titleLabel.set_text('Edit Observation')
            parentId, treeiter = self.copy(set_uid_endswith = ' (Edit) ')
            self.status = 'edit'
            self._removeId = parentId
            # remove the parent iter
            self._removeIter = treeiter

    def remove(self):
        
        self.status = 'remove'        
        
        treeselection = self.obsTreeView.get_selection()        
        treestore, treeiter =  treeselection.get_selected()
        path = treestore.get_path(treeiter)
        if path:
            # save the previous state xml 
            self.xmlTreeObj.savePrevious()
            # selected some row by the user
            row = path[0]
#            if len(path) > 1:
#                # selected child by the user. So get its parent iter
            treeiter = treestore.get_iter(row)
            parentTxt = treestore.get_value(treeiter, 0)

            dialog = DialogBox(self.builder)
            dialog.title("Diagnosis: Observation Remove")
            response = dialog.run("Do you want to remove '%s'.\nAre you sure ? " % parentTxt)
            dialog.hide()
            if response == 1:
                uid = self.__get_uid__(treestore, path)            
                obsTop = self.xmlTreeObj.currentXmlDom.getiterator('observations')[0]
                # remove the elements from the xml 
                self._removeEntriesFromXml(obsTop, uid)
                # remove the entries from the iter
                self.obsTreeStore.remove(treeiter)
                # save the xml 
                self.xmlTreeObj.save()
    
                 
    
class ObsOperations():
    
    def __init__(self, builder, xmltreeobject):
        self.obs = ObservationPage(builder, xmltreeobject)
        self.treeViewStatus = 'all_collapsed'
        return self
    
    def on_obs_reset_clicked(self, widget, data=None):
        self.obs.clearEntries()
          
    def on_obs_done_clicked(self, widget, data=None):                 
        self.obs.run()
        self.obs.clearEntries()          

    def on_obs_file_chooser_file_set(self, widget, data=None):
        self.obs.label_status.set_text('Checking ...')
        self.obs.file_operation()
              
    def on_obs_institution_changed(self, widget, data=None):
        self.obs.uid_update()
            
    def on_obs_name_changed(self, widget, data=None):        
        self.obs.uid_update()
                
    def on_obs_version_changed(self, widget, data=None): 
        self.obs.uid_update()
        
    def on_obs_treeviewcolumn_clicked(self, widget, data=None):
        """ Here we making toggle effect """       
        
        if self.treeViewStatus == 'all_collapsed':
            # expand all the tree elements
            self.obs.obsTreeView.expand_all()
            self.treeViewStatus = 'all_expanded'
            #self.treeIndicator = builder.get_object('obs_treeviewcolumn')
            #print self.treeIndicator.get_properties()#'arrow', 'up')
            #print dir(self.treeIndicator)
            #print self.treeIndicator.set_sort_indicator.__doc__            
            
        elif self.treeViewStatus == 'all_expanded':
            # collapse all the tree elements
            self.obs.obsTreeView.collapse_all()
            self.treeViewStatus = 'all_collapsed'
        else:
            pass 
        
          
