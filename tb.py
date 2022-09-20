#!/usr/bin/python2.7

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class ComboBoxWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="ComboBox Example")

        self.set_border_width(10)

        name_store = Gtk.ListStore(int, str)
        name_store.append([1, "Billy Bob"])
        name_store.append([11, "Billy Bob Junior"])
        name_store.append([12, "Sue Bob"])
        name_store.append([2, "Joey Jojo"])
        name_store.append([3, "Rob McRoberts"])
        name_store.append([31, "Xavier McRoberts"])


        table = Gtk.Table(5, 3, True)
        self.add(table)

        # span whole app
        name_combo = Gtk.ComboBox.new_with_model_and_entry(name_store)
        name_combo.connect("changed", self.on_name_combo_changed)
        name_combo.set_entry_text_column(1)
        table.attach(name_combo,0,3,0,1)

        country_store = Gtk.ListStore(str)
        countries = ["Austria", "Brazil", "Belgium", "France", "Germany",
            "Switzerland", "United Kingdom", "United States of America",
            "Uruguay"]
        for country in countries:
            country_store.append([country])

        country_combo = Gtk.ComboBox.new_with_model(country_store)
        country_combo.connect("changed", self.on_country_combo_changed)
        renderer_text = Gtk.CellRendererText()
        country_combo.pack_start(renderer_text, True)
        country_combo.add_attribute(renderer_text, "text", 0)
        table.attach( country_combo,0,1,1,2)

        country_combo = Gtk.ComboBox.new_with_model(country_store)
        country_combo.connect("changed", self.on_country_combo_changed)
        renderer_text = Gtk.CellRendererText()
        country_combo.pack_start(renderer_text, True)
        country_combo.add_attribute(renderer_text, "text", 0)
        table.attach( country_combo,1,2,1,2)

        country_combo = Gtk.ComboBox.new_with_model(country_store)
        country_combo.connect("changed", self.on_country_combo_changed)
        renderer_text = Gtk.CellRendererText()
        country_combo.pack_start(renderer_text, True)
        country_combo.add_attribute(renderer_text, "text", 0)
        table.attach( country_combo,2,3,1,2)


        # country_combo = Gtk.ComboBox.new_with_model(country_store)
        # country_combo.connect("changed", self.on_country_combo_changed)
        # renderer_text = Gtk.CellRendererText()
        # country_combo.pack_start(renderer_text, True)
        # country_combo.add_attribute(renderer_text, "text", 0)
        # table.attach( country_combo,0,1,1,2)

        # vbox.set
        # print(spc)

        
        # vbox1.pack_start(name_combo, False, False, 20)

        # country_store = Gtk.ListStore(str)
        # countries = ["Austria", "Brazil", "Belgium", "France", "Germany",
        #     "Switzerland", "United Kingdom", "United States of America",
        #     "Uruguay"]
        # for country in countries:
        #     country_store.append([country])

        
        # vbox1.pack_start(country_combo, False, False, True)

        # hbox.pack_start(country_combo,False,False,True)

        # currencies = ["Euro", "US Dollars", "British Pound", "Japanese Yen",
        #     "Russian Ruble", "Mexican peso", "Swiss franc"]
        # currency_combo = Gtk.ComboBoxText()
        # currency_combo.set_entry_text_column(0)
        # currency_combo.connect("changed", self.on_currency_combo_changed)
        # for currency in currencies:
        #     currency_combo.append_text(currency)

        # vbox1.pack_start(currency_combo, False, False, 0)
        # hbox.pack_start(currency_combo,False,False,True)

        # vbox1.pack_start(hbox,False,False,True)

        # self.add(vbox1)
        # self.add(hbox)

    def on_name_combo_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter != None:
            model = combo.get_model()
            row_id, name = model[tree_iter][:2]
            print("Selected: ID=%d, name=%s" % (row_id, name))
        else:
            entry = combo.get_child()
            print("Entered: %s" % entry.get_text())

    def on_country_combo_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter != None:
            model = combo.get_model()
            country = model[tree_iter][0]
            print("Selected: country=%s" % country)

    def on_currency_combo_changed(self, combo):
        text = combo.get_active_text()
        if text != None:
            print("Selected: currency=%s" % text)

win = ComboBoxWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
