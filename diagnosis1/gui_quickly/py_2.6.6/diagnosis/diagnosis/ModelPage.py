import os
import gtk
from xml.etree.ElementTree import Element, SubElement, Comment, tostring, ElementTree
from diagnosis.helpers import get_builder
from diagnosis.cdat_operations import cdfile_check
from diagnosis.ElementTree_pretty import indent
from diagnosis.dialog import DialogBox
from diagnosis.xmltree import Tree  

_seperator_ = ' : '
_fileExtension_ = ['.xml', '.cdml']


class ModelPage():
    __gtype_name__ = "ModelPage"    
    
    def __init__(self, builder, xmltreeobject):        
        self.builder = builder
        self.xmlTreeObj = xmltreeobject
        self.institution = builder.get_object('model_institution')
        self.name = builder.get_object('model_name')
        self.version = builder.get_object('model_version')
        self.experiment = builder.get_object('model_experiment')
        self.ensembleName = builder.get_object('model_ensemble_name')
        self.ensembleNo = builder.get_object('model_ensemble_no')
        self.uid = builder.get_object('model_uid')   
        # descriptions text buffer objects
        self.modelDescription = builder.get_object('model_description_textbuffer')
        self.ensembleDescrtption = builder.get_object('ensemble_description_textbuffer')
        # ensemble description text area
        self.ensembleDescrtptionArea = builder.get_object('ensemble_description_textview')
        # folder/file chooser
        self.modelFolder = builder.get_object('model_folder_chooser') 
        self.modelFolderEntry = builder.get_object('model_folder_entry')
        self.label_status = builder.get_object('model_file_label_status')
        # changing the background color 
        self.uid.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#ECEAE9"))
        self.modelFolderEntry.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#ECEAE9"))
        self.ensembleName.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#ECEAE9"))
        self.ensembleDescrtptionArea.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#ECEAE9"))
        # model final tree 
        self.modelTreeView = builder.get_object('model_treeview')  
        self.modelTreeStore = builder.get_object('model_treestore')
        # forecast hours tree 
        self.fcstHoursTreeView = builder.get_object('model_fcst_hours_treeview')
        self.fcstHourTreeStore = builder.get_object('model_fcst_hours_treestore')
        # available files tree 
        self.filesTreeView = builder.get_object('model_files_treeview')
        self.filesTreeStore = builder.get_object('model_files_treestore')
        # temporary tree 
        self.temporaryTreeView = builder.get_object('model_temporaray_treeview')
        self.temporaryTreeStore = builder.get_object('model_temporaray_treestore')
        # title object
        self.titleLabel = builder.get_object('model_title')                
        # initialize the institution
        self.institutionFn()
        # initialize the experiment      
        self.experimentFn()  
        self.form = builder.get_object('model_form_scrolledwindow')
        self.form.hide()
        self._removeIter = None
        self._removeId = None
        self._match_iter = None
        self._match_path = None
        self.preXmlRoot = None
        self._filetype_collection = {}
        self.associateButton = builder.get_object('model_associate')
        self.fcstHrSelection = self.fcstHoursTreeView.get_selection()
        self.fcstHrSelection.connect("changed", self.associate_on_off)
        self.fileSelection = self.filesTreeView.get_selection()
        self.fileSelection.connect("changed", self.associate_on_off)

    
    def associate_on_off(self, tree_selection):
        
        if self.fcstHrSelection.get_selected_rows()[1] and \
                                self.fileSelection.get_selected_rows()[1]:
            # i.e. if both forecast hours & files shoule be selected by user.
            # then enable the associate button 
            self.associateButton.set_sensitive(True)
        else:
            # otherwise disable the associate button 
            self.associateButton.set_sensitive(False)
            
    def institutionFn(self):
        
        entryCompletion = self.builder.get_object('model_institution_entrycompletion')
        entryCompletion.set_text_column(0)
        self.institution.child.set_completion(entryCompletion)
        # store the all available institutions name 
        allInstititions = self.builder.get_object('institution_liststore')
        _institutions = ['', 'BoM', 'CMA', 'CMC', 'CPTEC', 'ECMWF', 'JMA',  
                            'KMA', 'Meteo France', 'NCEP', 'NCMRWF', 'UKMO']
        
        for i in _institutions:
            allInstititions.append([i])
    
    def experimentFn(self):
        
        entryCompletion = self.builder.get_object('model_experiment_entrycompletion')
        entryCompletion.set_text_column(0)
        self.experiment.child.set_completion(entryCompletion)
        # store the all available institutions name 
        allExperiments = self.builder.get_object('model_experiment_liststore')
        
        for i in ['', 'operational']:
            allExperiments.append([i])

            
    def ensemble_on_off_properties(self):
        
        no = self.ensembleNo.get_value_as_int()
        if not no:
            # light ciment color to make look alike disabled button when 
            # ensemble No is non-zero.
            colorCode = "#ECEAE9"
            # erase the ensemble name & description
            self.ensembleName.set_text('')
            self.ensembleDescrtption.set_text('')
            # make it as non editable
            editable = False            
        else:
            # white color when the ensemble No is zero.
            colorCode = "#FFFFFF"
            # make it as editable
            editable = True
        # setting the background color code for the entry & description
        self.ensembleName.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse(colorCode))
        self.ensembleDescrtptionArea.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse(colorCode))
        # setting editable property
        self.ensembleName.set_editable(editable)
        self.ensembleDescrtptionArea.set_editable(editable)
        return no
    
    def filetype_treestore_init(self):
        self.fcstHourTreeStore.clear()
        self._filetype = [str(i) for i in range(12, 180, 12)]
        self._filetype.insert(0, 'Analysis')        
        for ftype in self._filetype:
            self.fcstHourTreeStore.append(None, [ftype])
    
    def filetype_treestore_update(self, no=0):
        
        if no in self._filetype_collection:
            self.fcstHourTreeStore.clear()
            tmp = self._filetype_collection.get(no)
            for ftype in self._filetype:
                if ftype not in tmp:
                    self.fcstHourTreeStore.append(None, [ftype])
        else:
            if len(self.fcstHourTreeStore) < 15:
                self.filetype_treestore_init()
                

    def _convertTreeStoreToXmlElements(self, model, path, _iter, xmlroot):
        
        """
        This method should be called by some tree store foreach loop funtion.
        Here the user arg is xmlroot (Xml Dom Element).
        
        Purpose : To iterate over the model temporary tree store elements and 
            dynamically add to the passed xmlroot element in the appropriate
            position(i.e attrib, text) of the element node.
            
        """
        
        # split the tree store iter row 
        val = model.get_value(_iter, column = 0).split(_seperator_)
        # get the tag name 
        tag = val[0]
        
        if model.iter_parent(_iter) is None:
            # initialize the obj preXmlRoot variable if _iter doesn't have 
            # parent.
            self.preXmlRoot = xmlroot    
            
        if tag.startswith("Ensemble Name"):
            # add the ensemble element to dom with its name, no as its child             
            ensname = val[1].split()[0]
            ensno = val[-1]
            ensemble = SubElement(xmlroot, 'ensemble')
            name = SubElement(ensemble, 'name')
            name.text = ensname
            no = SubElement(ensemble, 'no')
            no.text = ensno
            self.preXmlRoot = ensemble
            self.ensemble = ensemble
            
        elif tag.startswith('Ensemble ID'):
            # set the ensemble id as attrib
            self.preXmlRoot.attrib["id"] = val[-1] 
        
        elif tag == 'Forecast':
            # add the forecast elements to dom
            fcst = SubElement(self.preXmlRoot, 'forecast')
            self.preXmlRoot = fcst
            
        elif tag.isdigit():
            # add the forecast hours element to dom
            hourfile = SubElement(self.preXmlRoot, 'file', {'hour': tag}) 
            hourfile.text = val[1]
        
        elif tag == 'Analysis': 
            # add the analysis value to dom 
            if model.iter_parent(_iter) is None:
                self.preXmlRoot = xmlroot    
            else:
                self.preXmlRoot = self.ensemble            
            anl = SubElement(self.preXmlRoot, 'analysis')
            anlfile = SubElement(anl, 'file')
            anlfile.text = val[1]

        else:
            # add the description element to dom
            el = SubElement(self.preXmlRoot, tag.lower())
            if len(val) > 1:
                el.text = val[1]
   
    def run(self):
        uidlist = self.uid_update(action = 'return')

        institution, name, version, experiment, ensembleName = uidlist[:5]
        uid = uidlist[-1]
        _uid_ = uid.split('.')
       
 
        if _uid_[-2] == ensembleName:
            # remove ensemble name 
            _uid_.remove(ensembleName)
        if _uid_[-1].isdigit():
            # remove ensemble number
            _uid_.remove(uid[-1])
        # re-make the uid for the model 
        uid = '.'.join(_uid_)

        model = Element('model', {'id': uid})
        
        institutionChild = SubElement(model, 'institution')
        institutionChild.text = institution
        
        nameChild = SubElement(model, 'name')
        nameChild.text = name
        
        versionChild = SubElement(model, 'version')
        versionChild.text = version
        
        experimentChild = SubElement(model, 'experiment')
        experimentChild.text = experiment
        # store the model description
        descriptionChild = SubElement(model, 'description')
        startPosition, endPosition = self.modelDescription.get_bounds()
        modeldescription = self.modelDescription.get_text(startPosition, endPosition)  
        descriptionChild.text =  self._correctTxt(modeldescription)    
         
        modelTop = self.xmlTreeObj.currentXmlDom.getiterator('models')[0]
        
        # save the previous state xml 
        self.xmlTreeObj.savePrevious()  
        
        # convert elements from temporary treestore into xml dom model 
        self.temporaryTreeStore.foreach(self._convertTreeStoreToXmlElements, model)    
        treeObj = Tree('models', self.builder)
                    
        if self.status in ['add', 'copy']:           
            
            # append the entries to the iter model tree store
            treeObj.loopRootElement(model)       
            # append the elements to the xml 
            modelTop.append(model)           
        
        elif self.status == 'edit':
        
            if self._removeIter:
                row = self.modelTreeStore.get_path(self._removeIter)[0]
                # remove the entries from the iter(model tree store)
                self.modelTreeStore.remove(self._removeIter)
                self._removeIter = None
                # insert the entries to the iter model tree store
                treeObj.loopRootElement(model, 'insert', row)                            
                # remove the elements from the xml 
                self._removeEntriesFromXml(modelTop, self._removeId)
                # insert the elements to the xml 
                modelTop.insert(row, model)
                        
        # save the xml 
        self.xmlTreeObj.save()
        
    def do_fillup_ensemble_entries_from_temptree(self, no):
        
        _ens_begin = "Ensemble Name" 
        _ens_end = "No" + _seperator_ + str(no)
        # In foreach function, we can not pass more than one arg.
        # so here we make needed args as dictionary.
        _args_ = {'starts_with': _ens_begin, 
                  'ends_with': _ens_end,
                  'parent': None
                  }
        # iter through out the temporary tree to find match 
        # the ensemble properties                
        self.temporaryTreeStore.foreach(self.__get_match_iter_tree,   
                                                            _args_)
        # get the ensemble iter 
        ensParent = self._match_iter

        if not ensParent:
            # not available in the temporary tree view. So reset the entries
            self.ensembleName.set_text('')
            self.ensembleDescrtption.set_text('')
            return
        # get the stored ensemble name string of the found ensParent
        ensPTxt = self.temporaryTreeStore.get_value(ensParent, column = 0)
        ensName = ensPTxt.split(_ens_end)[0].split(_ens_begin + _seperator_)[1]
        # set ensemble name into the ensemble name entry in the form 
        self.ensembleName.set_text(ensName)
        if self.temporaryTreeStore.iter_has_child(ensParent):
            # get ensemble's description iter  
            ensDesIter = self.temporaryTreeStore.iter_nth_child(ensParent, 1)
            # get the description
            ensDes = self.temporaryTreeStore.get_value(ensDesIter, column = 0)
            ensDes = ensDes.split('Description' + _seperator_)[1]
            # set ensemble description into the ensemble description entry 
            self.ensembleDescrtption.set_text(ensDes)
            
    def do_associate_action(self):
        self.label_status.set_text("Checking the file ...")
        tmpRootParent = None        
        # get the seleted file and remove it from the treestore
        selected_file = self._getValueOfTreeSelection(self.fileSelection,
                                   self.filesTreeStore, action = 'remove')
        # make the selected_file with absolute path 
        selected_file_path = os.path.join(self.modelFolderEntry.get_text(), selected_file)        
        
        # check file through the cdat 
        cdfilestatus = cdfile_check(selected_file_path)
        if cdfilestatus:
            self.label_status.set_text("Checking done. Ready to add '%s' file !" % selected_file)
        else:
            self.label_status.set_text("Wrong File! Can not open '%s' file by cdat.\
                                    \nChoose correct one !" % selected_file)
            return 
        # get the seleted hour (file type) and remove it from the treestore
        selected_ftype = self._getValueOfTreeSelection(self.fcstHrSelection, 
                                self.fcstHourTreeStore, action = 'remove')
        # make selected fcst file string
        fileTxt = selected_ftype + _seperator_ + selected_file_path
      
        ens_no = self.ensembleNo.get_value_as_int()
        if ens_no in self._filetype_collection:
            self._filetype_collection[ens_no].append(selected_ftype)
        else:
            self._filetype_collection[ens_no] = [selected_ftype]
                
        if ens_no:             
            # get the ensemble name 
            ens_name = self._correctTxt(self.ensembleName.get_text())
            # get the ensemble description
            _start, _end = self.ensembleDescrtption.get_bounds()
            _description = self.ensembleDescrtption.get_text(_start, _end)
            _description = self._correctTxt(_description)
            ensDesTxt = "Description" + _seperator_ + _description
            # get the uid 
            uidTxt = "Ensemble ID" + _seperator_ + self.uid.get_text()
            
            if not ens_name:
                # call the dialog to ask the Q. Are you sure you want to 
                # continue without the ensemble name 
                pass 
            
            _ens_begin = "Ensemble Name" 
            _ens_end = " No" + _seperator_ + str(ens_no)
            ensTxt = _ens_begin + _seperator_ + ens_name + _ens_end
            # In foreach function, we can not pass more than one arg.
            # so here we make needed args as dictionary.
            _args_ = {'starts_with': _ens_begin, 
                      'ends_with': _ens_end,
                      'parent': tmpRootParent
                      }
            # iter through out the temporary tree to find match 
            # the ensemble properties                
            self.temporaryTreeStore.foreach(self.__get_match_iter_tree,   
                                                                _args_)
            # get the ensemble iter 
            ensParent = self._match_iter
            if ensParent:                            
                # get the stored ensemble name string of the found ensParent
                _oldEnsName = self.temporaryTreeStore.get_value(ensParent, column = 0)
                if _oldEnsName != ensTxt:
                    # setting the updated ensemble name with full string
                    self.temporaryTreeStore.set_value(ensParent, column = 0,                 
                                                             value = ensTxt)
            else:
                # ensemble parent iter is not available. so create it.
                ensParent = self.temporaryTreeStore.append(tmpRootParent, [ensTxt])
            
            if self.temporaryTreeStore.iter_has_child(ensParent):
                # it has child. update ensemble id, description if needed
                # get ensemble's uid iter 
                ensIdIter = self.temporaryTreeStore.iter_nth_child(ensParent, 0)
                # get uid value 
                ensID = self.temporaryTreeStore.get_value(ensIdIter, column = 0)
                if ensID != uidTxt:
                    # id is not same. so need to update the new id here.
                    # setting the new updated ensemble uid  
                    self.temporaryTreeStore.set_value(ensIdIter, 
                                              column = 0, value = uidTxt)
                
                # get ensemble's description iter  
                ensDesIter = self.temporaryTreeStore.iter_nth_child(ensParent, 1)
                # get the description
                ensDes = self.temporaryTreeStore.get_value(ensDesIter, column = 0)
                if ensDes != ensDesTxt:
                    # description is not same. so need to update it.
                    # setting the new updated ensemble description
                    self.temporaryTreeStore.set_value(ensDesIter, 
                                            column = 0, value = ensDesTxt)
            else:
                # ensemble parent doesn't have child. So need to add its 
                # uid and its description
                # add the ensemble 's uid 
                self.temporaryTreeStore.append(ensParent, [uidTxt])
                # add the ensemble's description
                self.temporaryTreeStore.append(ensParent, [ensDesTxt])                    
                
            # assign this ensemble iter to previous parent variable.
            _previousParent = ensParent
        else:
            # assign this tmp root iter to previous parent variable.
            _previousParent = tmpRootParent                    
        
        if selected_ftype == 'Analysis':
            # append the new selection to the tmp root 
            self.temporaryTreeStore.append(_previousParent, [fileTxt]) 
        
        elif selected_ftype.isdigit():
            # forecast comes here 
            # add forecast hour to the appropriate parent
            _fcst_parent_txt = 'Forecast'
            # In foreach function, we can not pass more than one arg.
            # so here we make needed args as dictionary.
            _args_ = {'match': _fcst_parent_txt, 'parent': _previousParent}
            # loop through temporary tree store to get the appropriate
            # forecast parent iter 
            self.temporaryTreeStore.foreach(self.__get_match_iter_tree, _args_)
            fcstParent = self._match_iter            

            if not fcstParent:
                # forecast parent iter is not available. so create it.
                fcstParent = self.temporaryTreeStore.append(_previousParent, 
                                                          [_fcst_parent_txt])    
           
            # append the forecast hour & its file txt into the forecast
            # parent iter.
            self.temporaryTreeStore.append(fcstParent, [fileTxt])
        
        else:
            # future file type comes here
            pass 
    
        
    def __get_match_iter_tree(self, model, path, _iter, args):
        """ This method should return True if matche found or None.
            If match has found, then that matched iter and its path should be 
            stored in _match_iter and _match_path instant variables.
        """
        # get the argument from the dictionary.i.e like key word arg.
        starts_with = args.get('starts_with')
        ends_with = args.get('ends_with')
        match = args.get('match')
        parent = args.get('parent', None)
        # get the value of the current iter 
        val = model.get_value(_iter, column = 0)

        if starts_with and ends_with:
            # If both starts_with and ends_with matches return True, else False
            condition = val.startswith(starts_with) and val.endswith(ends_with)
        else:
            # If value fully matches return True, else False
            condition = val == match
        
        # re-intialize the instance variables as None
        self._match_iter = None
        self._match_path = None
        if condition:
            # condition is True.            
            if parent is None:
                # Parent, _iter are same and None. So store the current iter, 
                # path into the object instant variables.
                self._match_iter = _iter
                self._match_path = path 
                # stop the foreach loop iteration by returning True
                return True
            else:       
                # passed arg have the parent iter tree.
                # get the current _iter parent
                _iterParent = model.iter_parent(_iter)
                if _iterParent is None:
                    # current _iter's parent is None. So
                    # continue the foreach loop iteration
                    return False
                # get the current _iter parent txt
                _iterParentTxt = model.get_value(_iterParent, column = 0)                   
                # get the argument parent txt       
                argParentTxt = model.get_value(parent, column = 0)       
                # compare the arg parent txt againt the current _iter parent txt
                if argParentTxt == _iterParentTxt:
                    # passed arg parent and current iter's parent values are
                    # same. So store the current iter, path into the object 
                    # instance variables.
                    self._match_iter = _iter
                    self._match_path = path 
                    # stop the foreach loop iteration by returning True
                    return True
        
            

    def _getValueOfTreeSelection(self, tree_selection, tree_store, action='None'):
        """
        return the seleted value in the forecast hour tree / files tree.
        Also if the action arg is 'remove', then the selected item should be 
        removed from the treestore.
        
        """
        # get the seleted path 
        path = tree_selection.get_selected_rows()[1][0]
        # get the seleted iter 
        _iter = tree_store.get_iter(path)
        # get the value of the seleted iter 
        val = tree_store.get_value(_iter, column = 0)
        if action == 'remove':
            # remove the seleted iter 
            tree_store.remove(_iter)
        return val 
            
    def file_operation(self):
        self.label_status.set_text('Checking ...')
        dirPath = self.modelFolder.get_filename()
        # collecting all the files form the chosen directory
        files = os.listdir(dirPath)
        # clear the path directory entry 
        self.modelFolderEntry.set_text('')
        # clear the file tree view/store (clear all the files) 
        self.filesTreeStore.clear()
        if not files:
            # set the status label 
            self.label_status.set_text('No files available. Choose Correct Folder !')            
            return
        # collecting the cdat compatible files (say xml, cdml)
        cdatFiles = [xfile for xfile in files
                        # omitting the sub directories/allowing regular file  
                        if os.path.isfile(os.path.join(dirPath, xfile))
                            # checking all the extensions
                            for ext in _fileExtension_
                                # if file extension matches, then return file  
                                if xfile.endswith(ext)]
        if cdatFiles:
            # set the status label 
            self.label_status.set_text('Collecting Files Done !.')
            # set the directory path into the entry 
            self.modelFolderEntry.set_text(dirPath)
            # adding all the available files into the filesTreeStore. 
            # This should display in the files tree view.
            for xfile in cdatFiles:
                self.filesTreeStore.append(None, [xfile])
             
        else:
            self.label_status.set_text('No xml/cdml files available. Choose Correct Folder !') 
        return 

           
    def clearEntries(self):        
        self.institution.set_active(0)
        self.name.set_text('')
        self.version.set_text('')
        self.experiment.set_active(0)
        self.ensembleName.set_text('')
        self.ensembleNo.set_value(0)
        self.uid.set_text('')        
        self.modelDescription.set_text('')
        self.ensembleDescrtption.set_text('')
        self.modelFolder.set_filename('')
        self.modelFolderEntry.set_text('')
        self.label_status.set_text('')
        self.filesTreeStore.clear()
        self.temporaryTreeStore.clear()
        self.filetype_treestore_init()
        self._filetype_collection = {}
        
    def _setEntries(self, uid):
        
        ### The below find throws error. It may works in python 2.7. Check it 
        ### obs = self.xmlTreeObj.currentXmlDom.find(".//observations/observation[@id='"+ pid + "']")
        allmodels = self.xmlTreeObj.currentXmlDom.getiterator('model') 
        for model in allmodels:   
            if model.get('id') == uid:
                treeObj = Tree('model_temp', self.builder)              
                for el in model:
                    self._setEntry(el.tag, el.text)
                    # add element to the temporary tree store from xml model 
                    treeObj._loop_model_elements(el)     
                    self._filetype_collection = treeObj._filetype_collection         
                return
    
    def _removeEntriesFromXml(self, modelTop, pid):
     
        for model in modelTop:   
            if model.get('id') == pid:
                modelTop.remove(model)                
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
        elif name == 'experiment':
            self.experiment.child.set_text(value)
        elif name == 'description':
            self.modelDescription.set_text(value)
        else:
            return None    
        
    def uid_update(self, action='None'):             
        # get the values from the institution, name, version & more entries
        institution = self.institution.child.get_text()        
        name = self.name.get_text()         
        version = self.version.get_text()  
        experiment = self.experiment.child.get_text()
        ensembleNo = self.ensembleNo.get_value_as_int()
        ensembleName = self.ensembleName.get_text()
        # form the uid elements
        uidlist = [institution, name, version, experiment, ensembleName]
        if ensembleNo:
            # i.e. ensembleNo is non-zero.
            uidlist.append(str(ensembleNo))
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
                text = self._correctTxt(text)
                _corrected.append(text)
            # add the uid 
            _corrected.append(uidTxt)
            # return the values
            return _corrected    
            
    def _correctTxt(self, text):
        text = text.split()
        # remove the begining empty spaces and joining with single 
        # space char if the text contains more than one word/spaces
        return ' '.join(text) if len(text) != 1 else text[0]
            
    def add(self):
        if not self.form.get_visible():
            self.form.show()
        #self.titleLabel.set_text('Register New Model')
        self.status = 'add'
          
    def copy(self, set_uid_endswith=' (Copy) ', action=None):
        
        self.clearEntries()
        
        if not self.form.get_visible():
            self.form.show() 
        self.status = 'copy' 
        #self.titleLabel.set_text('Register New Model')
        treeselection = self.modelTreeView.get_selection()        
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
        # update file type tree store 
        self.filetype_treestore_update()
        
        if action == 'return':    
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
            #self.titleLabel.set_text('Edit Model')
            parentId, treeiter = self.copy(set_uid_endswith = ' (Edit) ',
                                                        action = 'return')
            self.status = 'edit'
            self._removeId = parentId
            # remove the parent iter
            self._removeIter = treeiter

    def removeModel(self):
        self.status = 'remove'  
        # get selected of model tree view
        treeselection = self.modelTreeView.get_selection() 

        treestore, treeiter =  treeselection.get_selected()
        print treeiter
        path = treestore.get_path(treeiter)
        if path:            
            # selected some row by the user            
            row = path[0]
            treeiter = treestore.get_iter(row)
            parentTxt = treestore.get_value(treeiter, 0)

            dialog = DialogBox(self.builder)
            dialog.title("Diagnosis: Model Remove")
            response = dialog.run("Do you want to remove '%s'.\nAre you sure ? " % parentTxt)
            dialog.hide()
            if response == 1:                
                # save the previous state xml 
                self.xmlTreeObj.savePrevious()                
                uid = self.__get_uid__(treestore, path)            
                modelTop = self.xmlTreeObj.currentXmlDom.getiterator('models')[0]
                # remove the elements from the xml 
                self._removeEntriesFromXml(modelTop, uid)                    
                # remove the entries from the model tree store 
                self.modelTreeStore.remove(treeiter)
                # save the xml 
                self.xmlTreeObj.save()
                  
    def removeTemporary(self):
        # get selection of temporary tree view
        treeselection = self.temporaryTreeView.get_selection()
        treestore, treeiter =  treeselection.get_selected()
        path = treestore.get_path(treeiter)
        if path:            
            tmptxt = treestore.get_value(treeiter, 0)
            txt = tmptxt.split(_seperator_)
            if len(txt) == 2:
                txt = txt[0]                    
                if txt == 'Ensemble ID':
                    # selected ensemble id row by the user  to remove.
                    # so remove the whole ensemble items
                    treeiter = treestore.get_iter(path[0])
                    txt = treestore.get_value(treeiter, 0)                    
            else:
                txt = tmptxt
            childCount = treestore.iter_n_children(treeiter)
            dialogTxt = "Do you want to remove '%s' entry from temporary storage" % txt
            if childCount:
                dialogTxt += ',\nincluding its %d child properties.' % childCount
            else:
                dialogTxt += '.\n'
            dialogTxt += ' Are you sure ?'
            dialog = DialogBox(self.builder)
            dialog.title("Diagnosis: Model Remove")
            response = dialog.run(dialogTxt)                             
            dialog.hide()
            if response == 1:                
              
                parent = treestore.iter_parent(treeiter)
                if parent is None:
                    ensembleno = 0
                else:
                    gparent = treestore.iter_parent(parent)
                    if gparent is None:
                        ensembleno = 0
                    else:
                        ensemble = treestore.get_value(gparent, 0)
                        ensembleno = int(ensemble.split(_seperator_)[-1])
                if txt.isdigit():
                    self._filetype_collection[ensembleno].remove(txt)                
                elif txt.startswith('Ensemble'):
                    self._filetype_collection.pop(ensembleno)
                        
                # get the current ensemble no to update the filetype entries
                no = self.ensembleNo.get_value_as_int()
                # update the filetype entries after removed entries from the 
                # temporary storage.
                self.filetype_treestore_update(no)
                # remove the entries from the temporary tree store
                self.temporaryTreeStore.remove(treeiter)
        
    def remove(self, temporary=False):        
               
        if temporary:
            self.removeTemporary()
        else:
            self.removeModel()         
                 
    
class ModelOperations():
    
    def __init__(self, builder, xmltreeobject):
        self.model = ModelPage(builder, xmltreeobject)
        self.modelTreeViewStatus = 'all_collapsed'
        self.tempTreeViewStatus = 'all_collapsed'
        return self
            
    def on_model_associate_clicked(self, widget, data=None):
        self.model.do_associate_action()
        
    def on_model_reset_clicked(self, widget, data=None):
        self.model.clearEntries()
          
    def on_model_done_clicked(self, widget, data=None):                 
        self.model.run()
        self.model.clearEntries()          

    def on_model_folder_chooser_file_set(self, widget, data=None):
        self.model.label_status.set_text('Collecting Files ...')
        self.model.file_operation()
              
    def on_model_institution_changed(self, widget, data=None):
        self.model.uid_update()
            
    def on_model_name_changed(self, widget, data=None):        
        self.model.uid_update()
                
    def on_model_version_changed(self, widget, data=None): 
        self.model.uid_update()
        
    def on_model_experiment_changed(self, widget, data=None):        
        self.model.uid_update()
  
    def on_model_ensemble_no_changed(self, widget, data=None):        
        self.model.uid_update()
        no = self.model.ensemble_on_off_properties()  
        self.model.do_fillup_ensemble_entries_from_temptree(no)  
        self.model.filetype_treestore_update(no)   
  
    def on_model_ensemble_name_changed(self, widget, data=None): 
        self.model.uid_update() 
           
    def on_model_treeviewcolumn_clicked(self, widget, data=None):
        """ Here we making toggle effect """       
        
        if self.modelTreeViewStatus == 'all_collapsed':
            # expand all the tree elements
            self.model.modelTreeView.expand_all()
            self.modelTreeViewStatus = 'all_expanded'        
        elif self.modelTreeViewStatus == 'all_expanded':
            # collapse all the tree elements
            self.model.modelTreeView.collapse_all()
            self.modelTreeViewStatus = 'all_collapsed'
        else:
            pass 
    
    def on_temporary_treeviewcolumn_clicked(self, widget, data=None):
        """ Here we making toggle effect """       
        
        if self.tempTreeViewStatus == 'all_collapsed':
            # expand all the tree elements
            self.model.temporaryTreeView.expand_all()
            self.tempTreeViewStatus = 'all_expanded'        
        elif self.tempTreeViewStatus == 'all_expanded':
            # collapse all the tree elements
            self.model.temporaryTreeView.collapse_all()
            self.tempTreeViewStatus = 'all_collapsed'
        else:
            pass 
        
        
        
        
        
        
          
