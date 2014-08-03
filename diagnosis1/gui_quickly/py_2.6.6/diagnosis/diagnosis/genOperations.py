from diagnosis.ModelPage import ModelOperations
from diagnosis.ObservationPage import ObsOperations
from diagnosis.ClimatologyPage import ClimOperations

class GeneralOperations(ModelOperations, ObsOperations, ClimOperations):
    
    def __init__(self):
        
        model = ModelOperations.__init__(self, self.builder, self.xmlTree).model
        obs = ObsOperations.__init__(self, self.builder, self.xmlTree).obs
        clim = ClimOperations.__init__(self, self.builder, self.xmlTree).clim
        
        # create a dictionary where the key is the name of the main
        # widget of the notebook tab and the value is the name 
        # of the function that should be called for that specific tab
        self.addItem = {'Model': model.add,
                        'Climatology': clim.add,
                        'Observation': obs.add}
                        
        self.editItem = {'Model': model.edit,
                        'Climatology': clim.edit,
                        'Observation': obs.edit}
        
        self.copyItem = {'Model': model.copy,
                         'Climatology': clim.copy,
                         'Observation': obs.copy}
                        
        self.removeItem = {'Model': model.remove,
                           'Climatology': clim.remove,
                           'Observation': obs.remove}

        self.editButton = self.builder.get_object('edit')
        self.copyButton = self.builder.get_object('copy')    
        self.removeButton = self.builder.get_object('remove')
        self.undoButton =  self.builder.get_object('undo')
        self.undoArrowButton = self.builder.get_object('undo_arrow')
        self.redoButton =  self.builder.get_object('redo')
        self.redoArrowButton = self.builder.get_object('redo_arrow')
        
        self.model_tree_selection = model.modelTreeView.get_selection()
        self.model_tree_selection.connect("changed", self.onSelectionChanged)

        self.obs_tree_selection = obs.obsTreeView.get_selection()
        self.obs_tree_selection.connect("changed", self.onSelectionChanged)

        self.clim_tree_selection = clim.climTreeView.get_selection()
        self.clim_tree_selection.connect("changed", self.onSelectionChanged)
        
        self.model_temp_tree_selection = model.temporaryTreeView.get_selection()
        self.model_temp_tree_selection.connect("changed", 
                                        self.onTemporaryTreeSelectionChanged)
        self._temp_status = False
                
    def onSelectionChanged(self, tree_selection):
        
        if tree_selection.get_selected_rows()[1]:
            # Enable all the buttons
            self._set_ECR_Buttons()
            tabName = self.getCurrentTabName()
            if tabName in 'Model':
                self.model_temp_tree_selection.unselect_all() 
        
    def onTemporaryTreeSelectionChanged(self, tree_selection):

        if tree_selection.get_selected_rows()[1]:           
            # Enable the remove button only
            self._set_ECR_Buttons(edit = False, copy = False, remove = True)  
            self._temp_status = True 
            self.model_tree_selection.unselect_all()         
        else:
            self._temp_status = False
            
    def getCurrentTabName(self):
        # tabChild points to the main widget in the current tab
        tabChild = self.notebook.get_nth_page(self.notebook.get_current_page())
        # tabName is the name of tabChild
        return self.notebook.get_tab_label_text(tabChild).strip()
        
        
    def on_add_clicked(self, widget, data=None):
        tabName = self.getCurrentTabName()        
        # now you can use tabName to reference the dictionary and call
        # the appropriate function        
        self.addItem[tabName]()
        # unselect all selections
        self._unselect_all_trees_selection()                

    def on_edit_clicked(self, widget, data=None):
        tabName = self.getCurrentTabName()  
        self.editItem[tabName]()
        # Disable the edit, copy, remove buttons
        self._disable_ECR_Buttons()
        # unselect all selections
        self._unselect_all_trees_selection()
        
    def on_copy_clicked(self, widget, data=None):
        tabName = self.getCurrentTabName()             
        self.copyItem[tabName]()
        # Disable the edit, copy, remove buttons
        self._disable_ECR_Buttons()
        # unselect all selections
        self._unselect_all_trees_selection()
        
    def on_remove_clicked(self, widget, data=None):
        tabName = self.getCurrentTabName()
        if tabName in 'Model':
            # calling models           
            self.removeItem[tabName](self._temp_status)
        else:
            # calling for observations, climatologies...
            self.removeItem[tabName]()
        # Disable the edit, copy, remove buttons
        self._disable_ECR_Buttons()
        # unselect all selections
        self._unselect_all_trees_selection()
    
    def on_mainNotebook_switch_page(self, page, page_num, data=None):
        # Disable the edit, copy, remove buttons
        self._disable_ECR_Buttons()  
        # unselect all selections      
        self._unselect_all_trees_selection()
        
    def _unselect_all_trees_selection(self):
        # Unselect all the pages tree values
        self.model_tree_selection.unselect_all()
        self.obs_tree_selection.unselect_all()  
        self.clim_tree_selection.unselect_all() 
        self.model_temp_tree_selection.unselect_all() 
        
    def _disable_ECR_Buttons(self):
        # Disable the buttons
        self.editButton.set_sensitive(False)
        self.copyButton.set_sensitive(False)
        self.removeButton.set_sensitive(False)
    
    def _set_ECR_Buttons(self, edit=True, copy=True, remove=True):
        # set the buttons sensitive property by args
        self.editButton.set_sensitive(edit)
        self.copyButton.set_sensitive(copy)
        self.removeButton.set_sensitive(remove)
           
    def __undo_redo_sensitive(self, undo=False, redo=False):
        # Enable/Disable the undo buttons
        self.undoButton.set_sensitive(undo)
        self.undoArrowButton.set_sensitive(undo)
        # Enable/Disable the redo buttons
        self.redoButton.set_sensitive(redo)
        self.redoArrowButton.set_sensitive(redo)

    def on_undo_clicked(self, widget, data=None):
        self.xmlTree.swape()
        self.__undo_redo_sensitive(undo = False, redo = True)
        
        
    def on_undo_arrow_clicked(self, widget, data=None):
        pass

    def on_redo_clicked(self, widget, data=None):
        self.xmlTree.swape()
        self.__undo_redo_sensitive(undo = True, redo = False)
        
    def on_redo_arrow_clicked(self, widget, data=None):
        pass





        
