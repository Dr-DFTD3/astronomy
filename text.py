
# example textview-basic.py
import pygtk
pygtk.require('2.0')
import gtk

class TextViewExample:
    def toggle_editable(self, checkbutton, textview):
        textview.set_editable(checkbutton.get_active())

    def toggle_cursor_visible(self, checkbutton, textview):
        textview.set_cursor_visible(checkbutton.get_active())
