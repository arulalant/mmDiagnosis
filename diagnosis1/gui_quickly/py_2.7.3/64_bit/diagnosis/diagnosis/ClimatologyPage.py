from xml.etree.ElementTree import Element, SubElement, Comment, tostring, ElementTree
import gtk
from diagnosis.cdat_operations import cdfile_check, get_year
from diagnosis.ElementTree_pretty import indent
from diagnosis.dialog import DialogBox


_seperator_ = ' : '

class ClimatologyPage():
    __gtype_name__ = "ClimatologyPage"    
    
    def __init__(self, builder, xmltreeobject):        
        self.builder = builder
        self.xmlTreeObj = xmltreeobject
        self.institution = builder.get_object('clim_institution')
        self.name = builder.get_object('clim_name')
        self.version = builder.get_object('clim_version')
        self.uid = builder.get_object('clim_uid')   
        self.timeResolution = builder.get_object('clim_time_resolution')
        self.description = builder.get_object('clim_description_textbuffer')
        self.climfile = builder.get_object('clim_file_chooser') 
        self.climFileEntry = builder.get_object('clim_file_entry')
        self.label_status = builder.get_object('clim_file_label_status')        
        self.climTreeView = builder.get_object('clim_treeview')  
        self.climTreeStore = builder.get_object('clim_treestore')
        self.titleLabel = builder.get_object('clim_title')                
        self.institutionFn()
        self.timeResolutionFn()
        self.form = builder.get_object('clim_form_scrolledwindow')
        self.form.hide()
        # setting the background color like uneditable
        self.uid.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#ECEAE9"))
        self.climFileEntry.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#ECEAE9"))
        
        self._removeIter = None
        self._removeId = None
        self.yearInClimatologyFile = None
    
    def institutionFn(self):
                
        self.institution = self.builder.get_object('clim_institution')
        entryCompletion2 = self.builder.get_object('clim_institution_entrycompletion')
        entryCompletion2.set_text_column(0)        
        self.institution.child.set_completion(entryCompletion2)
        
#        allInstititions = self.builder.get_object('institution_liststore')
#        
#        for i in ['', 'NCMRWF', 'CMA', 'CMC']:
#            allInstititions.append([i])
            
    def timeResolutionFn(self):
        entryCompletion = self.builder.get_object('time_resolution_entrycompletion')
        entryCompletion.set_text_column(0)        
        self.timeResolution.child.set_completion(entryCompletion)
        allTimeResolution = self.builder.get_object('clim_time_resolution_liststore')
        
        for i in ['', 'daily', 'monthly']:
            allTimeResolution.append([i])

            
    def run(self):
        institution, name, version, time_resolution, uid = self.uid_update(action = 'return')
        
        # create the root element to store the climatology information with id
        climatology = Element('climatology', {'id': uid})
        # set institution
        institutionChild = SubElement(climatology, 'institution')
        institutionChild.text = institution
        # set name 
        nameChild = SubElement(climatology, 'name')
        nameChild.text = name
        # set version
        versionChild = SubElement(climatology, 'version')
        versionChild.text = version
        # set description content 
        descriptionChild = SubElement(climatology, 'description')
        startPosition, endPosition = self.description.get_bounds()
        descriptionChild.text = self.description.get_text(startPosition, endPosition)
        # set time resolution
        timeResolutionChild = SubElement(climatology, 'time-resolution')
        timeResolutionChild.text = time_resolution
        # set climatology file 
        File = self.climFileEntry.get_text()
        fileChild = SubElement(climatology, 'file')
        fileChild.text = File
        # set the year in climatology file 
        yearChild = SubElement(climatology, 'yearInClimatologyFile')
        yearChild.text = self.yearInClimatologyFile
        # reset the year value 
        self.yearInClimatologyFile = None
        
        climTop = self.xmlTreeObj.currentXmlDom.getiterator('climatologies')[0]
        
        def _addSubElementsToTree(parent, elements):
            for subEl in elements:
                childTxt = subEl.tag.capitalize() + _seperator_ + subEl.text 
                child = self.climTreeStore.append(parent, [childTxt])
            
        
        def _addItemToTree(addtype, row=None):
        
            # make the parent text/tree iter (climatology name & version)
            parentTxt = nameChild.tag.capitalize() + _seperator_ + nameChild.text 
            parentTxt += "   " + versionChild.tag.capitalize() + _seperator_ + versionChild.text 
            
            # add name & version to the tree as parent
            if addtype == 'append':
                # append the parent tree iter at the end of the treeview(treestore)
                parent = self.climTreeStore.append(None, [parentTxt])
            elif addtype == 'insert':
                # insert new parent tree iter to the treeview(treestore) at some position
                parent = self.climTreeStore.insert(None, row, [parentTxt])
            
            # add the institution as child to the above tree parent
            _addSubElementsToTree(parent, [institutionChild])
            uid = "Uid" + _seperator_ + climatology.get('id') 
            # add uid to the tree as child 
            self.climTreeStore.append(parent, [uid])   
            # add the description & file as child to the above tree parent         
            _addSubElementsToTree(parent, [descriptionChild, timeResolutionChild, fileChild])            
            
        
        # save the previous state xml 
        self.xmlTreeObj.savePrevious()  
                    
        if self.status in ['add', 'copy']:
            
            # append the elements to the xml 
            climTop.append(climatology)
            # append the entries to the iter tree store 
            _addItemToTree('append')
            
        
        elif self.status == 'edit':
        
            if self._removeIter:                
                row = self.climTreeStore.get_path(self._removeIter)[0]
                # remove the entries from the iter
                self.climTreeStore.remove(self._removeIter)
                # make _removeIter as None
                self._removeIter = None
                # add the entries to the iter tree store 
                _addItemToTree('insert', row)            
                # remove the elements from the xml 
                self._removeEntriesFromXml(climTop, self._removeId)
                # insert the elements to the xml 
                climTop.insert(row, climatology)
                        
        # save the xml 
        self.xmlTreeObj.save()
        
    
    def file_operation(self):
        
        filePath = self.climfile.get_filename()
        cdfilestatus = cdfile_check(filePath)
        if cdfilestatus:
            self.label_status.set_text('Checking done. ')
            self.climFileEntry.set_text(filePath)        
            self.label_status.set_text('Collecting info ...')
            self.yearInClimatologyFile = get_year(filePath)  
            if self.yearInClimatologyFile:
                self.label_status.set_text('Collecting info done. Ready to add !')
            else:
                self.label_status.set_text('Problem !. Cant get the year in the climatology file.\n \
                        Choose correct file !')
        else:
            self.label_status.set_text('Wrong File! Can not open by cdat.\nChoose correct file !')
            
    def clearEntries(self):        
        self.institution.set_active(0)
        self.timeResolution.set_active(0)
        self.name.set_text('')
        self.version.set_text('')
        self.uid.set_text('')        
        self.description.set_text('')
        self.climfile.set_filename('')
        self.climFileEntry.set_text('')
        self.label_status.set_text('')
        
    def _setEntries(self, uid):
        
        ### The below find throws error. It may works in python 2.7. Check it 
        ### obs = self.xmlTreeObj.currentXmlDom.find(".//observations/observation[@id='"+ pid + "']")
        allclims = self.xmlTreeObj.currentXmlDom.getiterator('climatology') 
        for clim in allclims:   
            if clim.get('id') == uid:              
                for el in clim:
                    self._setEntry(el.tag, el.text)
                return
    
    def _removeEntriesFromXml(self, climTop, pid):
     
        for clim in climTop:   
            if clim.get('id') == pid:
                climTop.remove(clim)                
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
        elif name == 'time-resolution':
            self.timeResolution.child.set_text(value)
        elif name == 'file':
            self.climfile.set_filename(value)
            self.climFileEntry.set_text(value)
        elif name == 'description':
            self.description.set_text(value)
        else:
            return None    
        
    def uid_update(self, action='None'):             
        # get the values from the institution, name & version entries
        institution = self.institution.child.get_text()        
        name = self.name.get_text()         
        version = self.version.get_text()  
        time_resolution = self.timeResolution.child.get_text()  
        # form the list
        uidlist = [institution, name, version, time_resolution]
        # adjust the list text values without any spaces
        uidTxt = [text.replace(' ', '') for text in uidlist if text]
        # join dot in-between the list text values to make it as unique id.
        uidTxt = '.'.join(uidTxt)
        # set the unique id into the uid entry
        self.uid.set_text(uidTxt)
        
        if action == 'return':
            _corrected = []            
            # correct the institution, name, version text spaces & time resolution
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
        #self.titleLabel.set_text('Register New Climatology')
        self.status = 'add'
          
    def copy(self, set_uid_endswith=' (Copy) '):
    
        if not self.form.get_visible():
            self.form.show() 
        self.status = 'copy' 
        #self.titleLabel.set_text('Register New Climatology')
        treeselection = self.climTreeView.get_selection()        
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
            #self.titleLabel.set_text('Edit Climatology')
            parentId, treeiter = self.copy(set_uid_endswith = ' (Edit) ')
            self.status = 'edit'
            self._removeId = parentId
            # remove the parent iter
            self._removeIter = treeiter

    def remove(self):
        
        self.status = 'remove'        
        
        treeselection = self.climTreeView.get_selection()        
        treestore, treeiter =  treeselection.get_selected()
        path = treestore.get_path(treeiter)
        if not path:
            raise "Select any element to do remove "
        # save the previous state xml 
        self.xmlTreeObj.savePrevious()
        # selected some row by the user
        row = path[0]
#            if len(path) > 1:
#                # selected child by the user. So get its parent iter
        treeiter = treestore.get_iter(row)
        parentTxt = treestore.get_value(treeiter, 0)

        dialog = DialogBox(self.builder)
        dialog.title("Diagnosis: Climatology Remove")
        response = dialog.run("Do you want to remove '%s'.\nAre you sure ? " % parentTxt)
        dialog.hide()
        if response == 1:
            uid = self.__get_uid__(treestore, path)            
            climTop = self.xmlTreeObj.currentXmlDom.getiterator('climatologies')[0]
            # remove the elements from the xml 
            self._removeEntriesFromXml(climTop, uid)
            # remove the entries from the iter
            self.climTreeStore.remove(treeiter)
            # save the xml 
            self.xmlTreeObj.save()
    
                 
    
class ClimOperations():
    
    def __init__(self, builder, xmltreeobject):
        self.clim = ClimatologyPage(builder, xmltreeobject)
        self.treeViewStatus = 'all_collapsed'
        return self
    
    def on_clim_reset_clicked(self, widget, data=None):
        self.clim.clearEntries()
          
    def on_clim_done_clicked(self, widget, data=None):                 
        self.clim.run()
        self.clim.clearEntries()          

    def on_clim_file_chooser_file_set(self, widget, data=None):
        self.clim.label_status.set_text('Checking ...')
        self.clim.file_operation()
              
    def on_clim_institution_changed(self, widget, data=None):
        self.clim.uid_update()
            
    def on_clim_name_changed(self, widget, data=None):        
        self.clim.uid_update()
                
    def on_clim_version_changed(self, widget, data=None): 
        self.clim.uid_update()
        
    def on_clim_time_resolution_changed(self, widget, data=None):
        self.clim.uid_update()
        
    def on_clim_treeviewcolumn_clicked(self, widget, data=None):
        """ Here we making toggle effect """
        if self.treeViewStatus == 'all_collapsed':
            # expand all the tree elements
            self.clim.climTreeView.expand_all()
            self.treeViewStatus = 'all_expanded'
        elif self.treeViewStatus == 'all_expanded':
            # collapse all the tree elements
            self.clim.climTreeView.collapse_all()
            self.treeViewStatus = 'all_collapsed'
        else:
            pass 
        
          
