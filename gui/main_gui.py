from time import gmtime, strftime

# custom functions and classes
from common import *
from time_data import Timer
from catalogs import Messier,NGC,User

import cli
import psolver as ps

try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    # sys.path.append("./gui/")
    # import main_gui as gui
    importStatus = True

except ImportError:
    print "PyGTK3+ module does not exist. Can't launch GUI !"
    print "Please download and install GTK and PyGTK3."
    importStatus = False



UI_INFO = """
<ui>
  <menubar name='MenuBar'>
    <menu action='FileMenu'>
      <menu action='FileNew'>
        <menuitem action='FileNewStandard' />
        <menuitem action='FileNewFoo' />
        <menuitem action='FileNewGoo' />
      </menu>
      <separator />
      <menuitem action='FileQuit' />
    </menu>
    <menu action='EditMenu'>
      <menuitem action='EditCopy' />
      <menuitem action='EditPaste' />
      <menuitem action='EditSave' />
    </menu>
    <menu action='OtherMenu'>
      <menuitem action='Help'/>
      <menuitem action='About'/>
      <separator />
      <menuitem action='Night'/>
    </menu>
  </menubar>
  <toolbar name='ToolBar'>
    <toolitem action='FileNewStandard' />
    <toolitem action='FileQuit' />
  </toolbar>
  <popup name='PopupMenu'>
    <menuitem action='Help' />
    <menuitem action='About' />
  </popup>
</ui>
"""

## TODO:
## finish functions for parsing specific input coordinates
## finish NGC catalog
## add a clear button to clean data
## clean up interface 

# imageLoaded = False
# rawImage = False
# jpgImage = False
# solveFieldOnly = False
# fieldSolved = False
# gotoTarget = False

# inputImageName = ""

# banner =           "__    ____  ____  ____   __   __ _   __   ____  _  _\n" 
# banner = banner + "/ _\  / ___)(_  _)(  _ \ /  \ (  ( \ /  \ (  _ \( \/ )\n"
# banner = banner + "/    \ \___ \  )(   )   /(  O )/    /(  O ) ) __/ )  /\n"
# banner = banner + "\_/\_/ (____/ (__) (__\_) \__/ \_)__) \__/ (__)  (__/\n"

# from pyfiglet import Figlet
# banner2 = Figlet(font='bulbhead')
banner = ""
# banner = """
#   __    ____  ____  ____   __   __ _   __   ____  _  _ 
#  / _\  / ___)(_  _)(  _ \ /  \ (  ( \ /  \ (  _ \( \/ )
# /    \ \___ \  )(   )   /(  O )/    /(  O ) ) __/ )  / 
# \_/\_/ (____/ (__) (__\_) \__/ \_)__) \__/ (__)  (__/ 
# """



parameters = Parameters()

class LabelWindow(Gtk.Window):

    def show_annotated_image(self,message,textdata=None):
        dialog = Gtk.MessageDialog(self, 0, 
            Gtk.MessageType.INFO,Gtk.ButtonsType.OK, 
            "")
    
        image = Gtk.Image ()
        image.set_from_file ("img_resized-ngc.png") #or whatever its variant

        dialog.set_image(image) 
        action_area = dialog.get_content_area()
        lbl2 = Gtk.Label(message)
        action_area.add(lbl2)
        dialog.show_all()
        dialog.run()
        dialog.destroy()

    def check_user_entry(self,entry,textdata):
        print entry.lower()
        if "m" in entry.lower():
            self.post_message("Locating Messier object\n" ,textdata)
            return "found"
        elif "ngc" in entry.lower():
            self.post_message("Locating NGC object\n" ,textdata)
            return "found"
        else:
            self.post_message("Unknown object, try entering the coordinates directly\n",textdata)
            return "none"

    def post_message(self,message,textView):
        textBuff = textView.get_buffer()
        itr = textBuff.get_end_iter()
        textBuff.insert(itr,message)
        spot = textBuff.create_mark("end",itr,False)
        textView.scroll_to_mark(spot,0.05,True,0.0,1.0)

    def on_decEntry_changed(self, entry,textdata=None):
        userEntry = entry.get_text()
        self.post_message("Target DEC(D:M:S):  %s\n" % userEntry,textdata)

    def on_raEntry_changed(self, entry,textdata=None):
        userEntry = entry.get_text()
        # raHMS = parameters.targetRA.split(":")
        self.post_message("Target RA (H:M:S):  %s\n" % userEntry,textdata)

    def on_userEntry_changed(self, entry,textdata=None):
        userEntry = entry.get_text()
        if "m" in userEntry.lower():
            self.messier.load_data()
            self.post_message("Locating Messier object\n" ,textdata)
            objStr = userEntry[:0] + "M" + userEntry[1:]
            self.messier.lookup(objStr)
            raHMS = self.messier.raHMS.split(":")
            decHMS = self.messier.decHMS.split(":")
            self.post_message("Library target:  %s %s\n" % (self.messier.raHMS,self.messier.decHMS),textdata)
            self.targetRA = RightAcsension(float(raHMS[0]),float(raHMS[1]))
            self.targetDEC = Declination(float(decHMS[0]),float(decHMS[1]))
            parameters.targetSet = True
        elif "ngc" in userEntry.lower():
            ngc = True
            objStr = userEntry[:0] + "NGC" + userEntry[3:]
        # obj = self.check_user_entry(userEntry,textdata)
        else:
            self.post_message("Unknown object, try entering the coordinates directly\n",textdata)

        # self.post_message("Library target:  %s %s\n" % (obj,userEntry),textdata)

    def create_ui_manager(self):
        uimanager = Gtk.UIManager()

        # Throws exception if something went wrong
        uimanager.add_ui_from_string(UI_INFO)

        # Add the accelerator group to the toplevel window
        accelgroup = uimanager.get_accel_group()
        self.add_accel_group(accelgroup)
        return uimanager

    def on_menu_file_new_generic(self, widget):
        print("A File|New menu item was selected.")

    def on_menu_file_quit(self, widget):
        Gtk.main_quit()

    def add_edit_menu_actions(self, action_group):
        action_group.add_actions([
            ("EditMenu", None, "Edit"),
            ("EditCopy", Gtk.STOCK_COPY, None, None, None,
             self.on_menu_others),
            ("EditPaste", Gtk.STOCK_PASTE, None, None, None,
             self.on_menu_others),
            ("EditSave", None, "Save As", Gtk.STOCK_SAVE_AS, None,
             self.save_annotated_image)
        ])

    def add_choices_menu_actions(self, action_group):
        action_group.add_action(Gtk.Action("OtherMenu", "Other", None,
            None))

        action_group.add_actions([
            ("OtherMenu", None, "Other"),
            ("Help", None, "Help", "<control><alt>H", None,
             self.help_clicked),
            ("About", None, "About", "<control><alt>A", None,
             self.about_clicked)
        ])

        # action_group.add_radio_actions([
        #     ("Help", None, "Help", None, None, 1),
        #     ("ChoiceTwo", None, "Two", None, None, 2)
        # ], 1, self.on_menu_choices_changed)

        three = Gtk.ToggleAction("Night", "Night mode", None, None)
        three.connect("toggled", self.on_menu_choices_toggled)
        action_group.add_action(three)

    def on_menu_choices_changed(self, widget, current):
        print(current.get_name() + " was selected.")

    def on_menu_choices_toggled(self, widget):
        if widget.get_active():
            print(widget.get_name() + " activated")
        else:
            print(widget.get_name() + " deactivated")

    def save_annotated_image(self, widget):
        print "Saving as"

    def on_menu_others(self, widget):
        print("Menu item " + widget.get_name() + " was selected")

    def add_file_menu_actions(self, action_group):
        action_filemenu = Gtk.Action("FileMenu", "File", None, None)
        action_group.add_action(action_filemenu)

        action_filenewmenu = Gtk.Action("FileNew", None, None, Gtk.STOCK_NEW)
        action_group.add_action(action_filenewmenu)

        action_new = Gtk.Action("FileNewStandard", "_New",
            "Create a new file", Gtk.STOCK_NEW)
        action_new.connect("activate", self.on_menu_file_new_generic)
        action_group.add_action_with_accel(action_new, None)

        action_group.add_actions([
            ("FileNewFoo", None, "New Foo", None, "Create new foo",
             self.on_menu_file_new_generic),
            ("FileNewGoo", None, "_New Goo", None, "Create new goo",
             self.on_menu_file_new_generic),
        ])

        action_filequit = Gtk.Action("FileQuit", None, None, Gtk.STOCK_QUIT)
        action_filequit.connect("activate", self.on_menu_file_quit)
        action_group.add_action(action_filequit)


    def __init__(self):

        self.messier = Messier()
        self.ngc = NGC()
        self.user = User()
        self.timeData = Timer()

        self.count = 1
        Gtk.Window.__init__(self, title="AstronoPy",)
        self.set_border_width(20)
        self.set_default_size(300, 200)

    
        table = Gtk.Table(20, 10, False)
        self.add(table)

        ## Label for the console window
        mlabel = Gtk.Label("")
        mlabel.set_justify(Gtk.Justification.LEFT)

        ## create a scrolled window (SW) to receive status
        ## updates and messages during program usage
        consoleWindow = Gtk.ScrolledWindow()
        consoleWindow.set_policy( Gtk.PolicyType.ALWAYS,  Gtk.PolicyType.ALWAYS)
        
        ## create a text view object to accept
        ## messages to be posted in the SW
        consoleText = Gtk.TextView()
        consoleText.set_wrap_mode(Gtk.WrapMode.WORD)
        consoleText.set_cursor_visible(False)
        consoleText.set_editable(False)

        image = Gtk.Image()
        image.set_from_file ("img_resized.jpg")
        label = Gtk.Label(banner)
        table.attach(label,0,10,1,2)

        # table.attach(image,0,10,0,1)

        ############# MENU BAR #################
        action_group = Gtk.ActionGroup("my_actions")
        self.add_file_menu_actions(action_group)
        self.add_edit_menu_actions(action_group)
        self.add_choices_menu_actions(action_group)
        uimanager = self.create_ui_manager()
        uimanager.insert_action_group(action_group)
        menubar = uimanager.get_widget("/MenuBar")
        table.attach(menubar,0,3,0,1)
        ############# MENU BAR #################

        
        label = Gtk.Label("Target  RA:")
        table.attach(label,0,1,3,4)
        raEntry = Gtk.Entry()
        raEntry.set_size_request(125,0)
        raEntry.connect("activate",self.on_raEntry_changed,consoleText)
        table.attach(raEntry,1,2,3,4)


        label = Gtk.Label("Target DEC:")
        label.set_justify(Gtk.Justification.RIGHT)
        table.attach(label,0,1,5,6)

        decEntry = Gtk.Entry()
        decEntry.set_size_request(125,0)
        decEntry.connect("activate",self.on_decEntry_changed,consoleText)
        table.attach(decEntry,1,2,5,6)


        label = Gtk.Label("Library targets:")
        table.attach(label,0,1,7,8)
        userEntry = Gtk.Entry()
        userEntry.set_size_request(125,0)
        userEntry.connect("activate",self.on_userEntry_changed,consoleText)
        table.attach(userEntry,1,2,7,8)


        ## button to launch file chooser dialog
        loadButton = Gtk.Button("Choose Image file..")
        loadButton.connect( "clicked",self.load_image_clicked,consoleText)
        table.attach(loadButton,0,1,9,10)

        ## button to solve filed only
        solveButton = Gtk.Button.new_with_mnemonic("_Solve Field")
        solveButton.connect("clicked", self.solve_field_clicked,consoleText)
        table.attach(solveButton,1,2,9,10)

        ## button to compute moves to a target
        gotoButton = Gtk.Button.new_with_mnemonic("_Goto Target!")
        gotoButton.connect("clicked", self.goto_target_clicked,consoleText)
        table.attach(gotoButton,2,3,9,10)

        # ## clear button
        # ## button to compute moves to a target
        # gotoButton = Gtk.Button.new_with_mnemonic("Show marked image")
        # gotoButton.connect("clicked", self.show_image_clicked,consoleText)
        # table.attach(gotoButton,0,1,9,11)

        # ## clear button
        # ## button to compute moves to a target
        # gotoButton = Gtk.Button.new_with_mnemonic("Clear data")
        # gotoButton.connect("clicked", self.clear_data_clicked,consoleText)
        # table.attach(gotoButton,1,2,9,11)

        #  ## clear button
        # ## button to compute moves to a target
        # gotoButton = Gtk.Button.new_with_mnemonic("Help")
        # gotoButton.connect("clicked", self.helper,consoleText)
        # table.attach(gotoButton,2,3,9,11)
        
        # load this last, places the console at the bottom
        consoleWindow.add(consoleText)
        consoleWindow.show()
        consoleText.show()
        table.attach(mlabel,0,4,12,13)
        table.attach(consoleWindow,0,4,16,20,Gtk.AttachOptions.FILL,Gtk.AttachOptions.FILL)



    def load_image_clicked(self,button,textdata=None):

        dialog = Gtk.FileChooserDialog("Please select a file",self,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL,Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,Gtk.ResponseType.OK))

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

        filter_CR2 = Gtk.FileFilter()
        filter_CR2.set_name("CR2 files")
        filter_CR2.add_mime_type("CR2/raw")
        dialog.add_filter(filter_CR2)

        filter_jpg = Gtk.FileFilter()
        filter_jpg.set_name("JPG files")
        filter_jpg.add_mime_type("image/jpg")
        filter_jpg.add_mime_type("image/jpeg")
        filter_jpg.add_mime_type("image/JPG")

        dialog.add_filter(filter_jpg)

        response = dialog.run()

        goodFile = True
        if response == Gtk.ResponseType.OK:
            if textdata is not None:
                parameters.inputImageName = dialog.get_filename()
                extension = parameters.inputImageName.lower()[-3:]

                if "jpg" in extension:
                    print "found jpg"
                    parameters.jpgImage = True
                    parameters.imageLoaded = True
                elif "peg" in extension:
                    parameters.jpgImage = True
                    parameters.imageLoaded = True
                elif "cr2" in extension:
                    parameters.rawImage = True
                    parameters.imageLoaded = True
                else:
                    goodFile = False
                    self.post_message("ERROR: " + parameters.inputImageName + " is wrong format. JPG/CR2 only!\n",textdata )

                if goodFile is True:
                    self.post_message("Selected file: " + dialog.get_filename() + "\n",textdata)


        elif response == Gtk.ResponseType.CANCEL:
            if textdata is not None:
                self.post_message("Load image canceled!\n",textdata)
            dialog.destroy()


        if goodFile is True:
            ## if image is already a JPEG, just resize it
            ## if image is RAW, convert to JPEG, then resize
            if parameters.jpgImage is True:
                resize_jpg_image(parameters.inputImageName,"img_resized.jpg")  
            else:
                convert_image(parameters.inputImageName,"img_converted.jpg")
                resize_jpg_image("img_converted.jpg","img_resized.jpg")  
            dialog.destroy()

        

    def goto_target_clicked(self,button,textdata=None):
        ## if plate solving hasnt been done, 
        ## run it now
        if parameters.fieldSolved is False:
            self.solve_field(textdata)
        
        if parameters.targetSet is True:
            raDiff = []
            decDiff = []
            raDiff,decDiff = ps.zero_target(self.imgRA,self.imgDEC,self.targetRA,self.targetDEC)
            raDir,raMove,decDir,decMove = get_moves(raDiff,decDiff)


            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,Gtk.ButtonsType.OK, "+++ Move Scope +++")
            ## print the move direction and magnitude in a popup window
            dialog.format_secondary_markup("<b><big><big>" + raDir + ":</big></big></b>  " + "<b><big><big>" + raMove + "</big></big></b>\n\n" + 
                "<b><big><big>" + decDir + ":</big></big></b>  " + "<b><big><big>" + decMove + "</big></big></b>")

            dialog.run()
            dialog.destroy()
        else:
            self.post_message("ERROR: No target coordinates given, select a library target or enter coordinates manually\n ",textdata)

    def solve_field(self,textdata):
        if parameters.imageLoaded is True:
            self.post_message("Entering the plate solving routine....\n ",textdata)

            imgRAStr,imgDECStr = ps.solve_field("img_resized.jpg")
            ra = imgRAStr.split(":")
            dec = imgDECStr.split(":")

            self.imgRA = RightAcsension(float(ra[0]),float(ra[1]),float(ra[2]))
            self.imgDEC = Declination(float(dec[0]),float(dec[1]),float(dec[2]))

            self.post_message("Success!\n ",textdata)

            message = "+++ Annotated Image +++\n Field center:\nRA:    " + imgRAStr + "\nDEC: " + imgDECStr 

            self.show_annotated_image(message,textdata)
            parameters.fieldSolved = True
        else:
            self.post_message("ERROR: No image loaded, use the \"Choose Image file\" button \n ",textdata)

    def solve_field_clicked(self,button,textdata=None):
        parameters.solveFieldOnly = True
        self.solve_field(textdata)

    ## selectively clear the currently loaded data set
    def clear_data_clicked(self,button,textdata):
        deleted = False
        if parameters.imageLoaded is True:
            parameters.imageLoaded = False
            parameters.jpgImage = False
            parameters.rawImage = False
            parameters.inputImageName = None
            deleted = True
        if parameters.targetSet is True:
            parameters.targetSet = None
            self.targetRA = None
            self.targetDEC = None
            deleted = True
        if parameters.fieldSolved is True:
            parameters.fieldSolved = False
            self.imgRA = None
            self.imgDEC = None
            deleted = True
        if deleted is True:
            self.post_message("Currently loaded data set deleted!\n",textdata) 
        else:
            self.post_message("No currently loaded data set to delete!\n",textdata)

    def help_clicked(self,button,textdata=None):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,Gtk.ButtonsType.OK, "")
        dialog.format_secondary_markup("<b><big><big> AstronoPy Help </big></big></b>\n" 
            + "This program allows one to blindly plate solve an image and produce an\n"
            + "annotated image indicating the stars in the field. In addition, you \n"
            + "can calculate the moves necessary to move to other coordinates or \n"
            + "select from a list of library targets; Messier and NGC\n")

        dialog.run()
        dialog.destroy()

#   __    ____  ____  ____   __   __ _   __   ____  _  _ 
#  / _\  / ___)(_  _)(  _ \ /  \ (  ( \ /  \ (  _ \( \/ )
# /    \ \___ \  )(   )   /(  O )/    /(  O ) ) __/ )  / 
# \_/\_/ (____/ (__) (__\_) \__/ \_)__) \__/ (__)  (__/ 
#    __    ___  ____  ____  _____  _  _  _____  ____  _  _ 
#   /__\  / __)(_  _)(  _ \(  _  )( \( )(  _  )(  _ \( \/ )
#  /(__)\ \__ \  )(   )   / )(_)(  )  (  )(_)(  )___/ \  / 
# (__)(__)(___/ (__) (_)\_)(_____)(_)\_)(_____)(__)   (__) 

    def about_clicked(self,button,textdata=None):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,Gtk.ButtonsType.OK, "")
        dialog.format_secondary_markup("<b><big><big><big> AstronoPy v. 1.0 </big></big></big></b>\n" 
            + "   __    ___  ____  ____  _____  _  _  _____  ____  _  _\n"
            + "  /__ \\  / __)(_  _)(  _ \\(  _  )( \\( )(  _  )(  _ \\( \\/ )\n"
            + " /(__) \\ \\__ \\  )(   )   / )(_)(  )  (  )(_)(  )___/ \\  /  \n"
            + "(__)(__)(___/ (__) (_)\\_)(_____)(_)\\_)(_____)(__)   (__) \n")
        # dialog.format_secondary_markup("<b><big><big><big> AstronoPy v. 1.0 </big></big></big></b>\n" 
        #     + "This program allows one to blindly plate solve an image and produce an\n"
        #     + "annotated image indicating the stars in the field. In addition, you \n"
        #     + "can calculate the moves necessary to move to other coordinates or \n"
        #     + "select from a list of library targets; Messier and NGC\n")

        dialog.run()
        dialog.destroy()

    def show_image_clicked(self,button,textdata=None):
        if parameters.fieldSolved is True:
            message = "+++ Annotated Image +++\n Field center:\nRA:    " + self.imgRA.hms + "\nDEC: " + self.imgDEC.hms
            self.show_annotated_image(message,textdata)
        else:
            self.post_message("ERROR: Internal field data not set, use the \"Choose Image file\" + \"Solve filed\" buttons first\n",textdata)

        





        