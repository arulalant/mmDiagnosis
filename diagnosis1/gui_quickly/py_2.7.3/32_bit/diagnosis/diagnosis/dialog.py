import gtk

class DialogBox():
    
    def __init__(self, builder):
        self.dialog = builder.get_object('dialogBox')
        self.dialogLabel = builder.get_object('dialog_label')
        #self.diagnosis = builder.get_object('diagnosis_window')
    
    def title(self, txt):
        self.dialog.set_title(txt)
    
    def run(self, txt):
        self.dialogLabel.set_text(txt)
        #self.diagnosis.set_sensitive(False)
        return self.dialog.run()
        
    def hide(self):        
        self.dialog.hide()
        #self.diagnosis.set_sensitive(True)
        
    def destroy(self):
        self.dialog.destroy()
        #self.diagnosis.set_sensitive(True)
 
