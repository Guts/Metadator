"""
Sample application for playing with Ttk theming.

-- Guilherme Polo, 2008.
"""

import os
import ttk
import pprint
import inspect
import Tkinter
import cPickle
import cStringIO
import ConfigParser
from tkSimpleDialog import Dialog
from tkFileDialog import askopenfilename, asksaveasfilename
from tkMessageBox import showwarning, showerror

IMAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")

def map_widgets():
    """Maps Ttk widgets to their respective layout(s), factory and
    possibly other things."""
    widgets = {}
    wanted_names = ("Button", "Checkbutton", "Combobox", "Entry", "Frame",
        "Label", "Labelframe", "Menubutton", "Notebook", "Panedwindow",
        "Progressbar", "Radiobutton", "Scale", "Scrollbar", "Separator",
        "Sizegrip", "Treeview")

    # some widgets contain Vertical and Horizontal layouts
    vert_horiz = ('Progressbar', 'Scale', 'Scrollbar')
    # several widgets contain a single layout named as Twidgetname
    prefix_t = ('Label', 'Button', 'Checkbutton', 'Radiobutton', 'Menubutton',
        'Entry', 'Combobox', 'Frame', 'Labelframe', 'Separator', 'Sizegrip')

    sample = {'Button': widget_text, 'Checkbutton': widget_text,
        'Label': widget_text, 'Radiobutton': widget_text,
        'Labelframe': widget_text_size, 'Combobox': widget_values,
        'Progressbar': widget_progress, 'Notebook': widget_notebook,
        'Treeview': widget_treeview, 'Scrollbar': widget_expand,
        'Frame': widget_expand, 'Separator': widget_expand,
        'Menubutton': widget_menubtn, 'Panedwindow': widget_paned}

    for name in ttk.__all__:
        if name not in wanted_names:
            continue

        widget_d = {'factory': None, 'layouts': None}

        if name in prefix_t:
            widget_d['layouts'] = ('T%s' % name, )
        elif name in vert_horiz:
            widget_d['layouts'] = ('Horizontal.T%s' % name,
                'Vertical.T%s' % name)
        elif name == 'Notebook':
            widget_d['layouts'] = ('TNotebook', 'TNotebook.Tab')
        elif name == 'Panedwindow':
            widget_d['layouts'] = ('TPanedwindow', 'Horizontal.Sash',
                'Vertical.Sash')
        elif name == 'Treeview':
            widget_d['layouts'] = ('Treeview', 'Treeview.Item',
                'Treeview.Cell', 'Treeview.Heading', 'Treeview.Row')

        if name in sample:
            widget_d['factory'] = sample[name]
        if name == 'Scrollbar':
            widget_d['class'] = 'Vertical.TScrollbar'

        widgets[name] = widget_d

    return widgets

def widget_text(widget, master, text="Sample", **kw):
    """Instantiate widget and set its text option to a custom value."""
    return widget(master, text=text, **kw)

def widget_text_size(widget, master, text="Sample", width=150, **kw):
    """Instantiate widget and set its text option to a custom value and
    set a size for it."""
    return widget(master, text=text, width=width, height=width, **kw)

def widget_values(widget, master, **kw):
    """Instantiate widget with some custom values."""
    return widget(master, values=["Value %d" % i for i in range(5)], **kw)

def widget_progress(widget, master, maximum=10, **kw):
    """Instantiate a progressbar and step it a bit."""
    w = widget(master, maximum=maximum, **kw)
    w.step(4)
    return w

def widget_notebook(widget, master, **kw):
    """Create a sample notebook with 2 tabs."""
    w = widget(master, **kw)
    w.add(ttk.Frame(w, width=150, height=150), text="Tab 1")
    w.add(ttk.Frame(w, width=150, height=150), text="Tab 2")
    return w

def widget_treeview(widget, master, **kw):
    """Create a sample treeview with 2 columns and 2 rows."""
    w = widget(master, columns=[0, 1], **kw)
    w.column('#0', width=70)
    for i in range(2):
        w.column(i, width=40)
        w.heading(i, text=i)
        w.insert('', 'end', text="Row %d" % i, values=[i, i + 1])
    return w

def widget_menubtn(widget, master, **kw):
    """Create a sample menu button with some options."""
    menu = Tkinter.Menu(tearoff=False)
    for i in range(5):
        menu.add_radiobutton(label='Item %d' % i)
    return widget(master, text="Sample", menu=menu, **kw)

def widget_paned(widget, master, **kw):
    """Create a sample Panedwindow with two children."""
    w = widget(master, height=150, **kw)
    w.add(ttk.Label(w, text="Child 1"))
    w.add(ttk.Label(w, text="Child 2"))
    return w

def widget_expand(widget, master, **kw):
    """Instantiate widget and configure it to expand."""
    w = widget(master, **kw)
    try:
        fill = 'x' if 'horizontal' in str(w['orient']) else 'y'
    except Tkinter.TclError:
        fill = 'both'
    w.pack_configure(expand=True, fill=fill)
    return w


class ThemeFile(ConfigParser.ConfigParser):
    def __init__(self, fileobj, style=None, readfrom=False):
        ConfigParser.ConfigParser.__init__(self)
        self._fobj = fileobj
        self._style = style
        if readfrom:
            self.readfp(fileobj)

    def optionxform(self, optionstr):
        """This method overrides the ConfigParser.RawConfigParser's one."""
        caller = inspect.stack()[1] # caller's record
        caller_func_name = caller[3]
        if caller_func_name in ('set', '_read'):
            # don't change option's case for these functions
            return optionstr
        return optionstr.lower()

    def load_configure(self, items):
        self._style_load(items, self._style.configure)

    def load_map(self, items):
        self._style_load(items, self._style.map)

    def load_layout(self, items):
        self._style_load(items, self._style.layout, False)

    def _style_load(self, items, method, dict_unpack=True):
        if not items:
            return

        for layout, data in items:
            # XXX Warning: pickle usage!
            data = cPickle.loads(data)
            layout = "Custom.%s" % layout
            if dict_unpack:
                method(layout, **data)
            else:
                method(layout, data)

    def add_theme_sections(self, theme):
        sections = ('configure', 'map', 'layout')
        for section in sections:
            self.add_section('%s-%s' % (theme, section))

    def save(self):
        self.write(self._fobj)

    def close(self):
        self._fobj.close()


class AutoScroll(object):
    """Configure the scrollbars for a widget."""

    def __init__(self, master):
        vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)

        self.configure(yscrollcommand=self._autoscroll(vsb),
            xscrollcommand=self._autoscroll(hsb))
        self.grid(column=0, row=0, sticky='nsew')
        vsb.grid(column=1, row=0, sticky='ns')
        hsb.grid(column=0, row=1, sticky='ew')

        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)

        # Copy geometry methods of master -- hack! (took from ScrolledText.py)
        methods = Tkinter.Pack.__dict__.keys() + Tkinter.Grid.__dict__.keys()

        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        """Hide and show scrollbar as needed."""
        def wrapped(first, last):
            first, last = float(first), float(last)

            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()

            sbar.set(first, last)

        return wrapped

    def __str__(self):
        return str(self.master)

def _create_container(func):
    """Creates a ttk Frame with a given master, and use this new frame to
    place the scrollbars and the widget."""
    def wrapped(cls, master, **kw):
        container = ttk.Frame(master)
        return func(cls, container, **kw)

    return wrapped


class ScrolledTreeview(AutoScroll, ttk.Treeview):
    """A standard ttk Treeview widget with scrollbars that will
    automatically show/hide as needed."""
    @_create_container
    def __init__(self, master, **kw):
        ttk.Treeview.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)


class ScrolledText(AutoScroll, Tkinter.Text):
    """A standard Tkinter Text widget with scrollbars that will
    automatically show/hide as needed."""
    @_create_container
    def __init__(self, master, **kw):
        Tkinter.Text.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)


class NewOption(Dialog):
    """Ask for an option name and initial value."""

    def __init__(self, master, title="New Option"):
        Dialog.__init__(self, master, title)

    def body(self, master):
        lbl = ttk.Label(master, text="Option name")
        self.o_entry = ttk.Entry(master)

        lbl_val = ttk.Label(master, text="Initial value")
        self.v_entry = ttk.Entry(master)

        lbl.grid(row=0, column=0, padx=6, sticky='e')
        self.o_entry.grid(row=0, column=1, padx=6)
        lbl_val.grid(row=1, column=0, padx=6, pady=6, sticky='e')
        self.v_entry.grid(row=1, column=1, padx=6)

        self.resizable(False, False)

    def buttonbox(self):
        box = ttk.Frame(self)

        w = ttk.Button(box, text="OK", command=self.ok, default='active')
        w.pack(side='right', padx=6, pady=6)
        w = ttk.Button(box, text="Cancel", command=self.cancel)
        w.pack(side='right', padx=6, pady=6)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack(expand=True, fill='x')

    def validate(self):
        """Check if an option name was entered."""
        if self.o_entry.get():
            self.result = (self.o_entry.get(), self.v_entry.get())
            return True

        showwarning("Empty option name",
            "You need to define an option name at least.", parent=self)
        return False


class ImageDialog(NewOption): # reusing buttonbox
    """A dialog that asks for a image name and image path or data and then
    creates a PhotoImage from the data, or, receives data to edit."""
    
    def __init__(self, master, title="New Image", image=None):
        self._editing = True if image else False
        self._image = image
        NewOption.__init__(self, master, title)

    def body(self, master):
        lbl = ttk.Label(master, text="Image name")
        self.img_name = ttk.Entry(master)

        lbl_format = ttk.Label(master, text="Image Format")
        self.img_format = ttk.Entry(master)

        lbl_val = ttk.Label(master, text="Image path")
        self.img_path = ttk.Entry(master)
        browse = ttk.Button(master, text="Find", command=self._find_image)

        lbl_other = ttk.Label(master, text="or")

        lbl_data = ttk.Label(master, text="Image data")
        self.img_data = ScrolledText(master, width=60, height=8)

        lbl.grid(row=0, column=0, padx=6, sticky='e')
        self.img_name.grid(row=0, column=1, padx=6, columnspan=2, sticky='ew')
        lbl_format.grid(row=1, column=0, padx=6, sticky='e', pady=6)
        self.img_format.grid(row=1, column=1, padx=6, columnspan=2,
            sticky='ew', pady=6)
        lbl_val.grid(row=2, column=0, padx=6, sticky='e')
        self.img_path.grid(row=2, column=1, padx=6, sticky='ew')
        browse.grid(row=2, column=2, padx=6, sticky='e')
        lbl_other.grid(row=3, columnspan=3, pady=3)
        lbl_data.grid(row=4, column=0, padx=6, sticky='new')
        self.img_data.grid(row=4, column=1, columnspan=2)

        master.grid_columnconfigure(1, weight=1)

        self.resizable(False, False)

        if self._editing:
            self.img_name.insert(0, self._image.name)
            self.img_name['state'] = 'readonly'
            self.img_format.insert(0, self._image['format'])

            if self._image['file']:
                self.img_path.insert(0, self._image['file'])
            else:
                self.img_data.insert('1.0', self._image['data'])

    def validate(self):
        """Verify that a name was defined and only one between data and
        image path was set."""
        img_name = self.img_name.get()
        img_path = self.img_path.get()
        img_data = self.img_data.get('1.0', 'end').strip()

        if not img_name or (img_path and img_data) or \
            (not img_path and not img_data):
            showwarning("Invalid image specification",
                "You need to specify an image name and then either specify "
                "a image path or the image data, at least.", parent=self)
            return False

        try:
            img_format = self.img_format.get()
            if self._editing:
                # try to create an image with current settings, if it succeeds
                # then it is ok to change the image being edited.
                self._create_image(None, img_path, img_data, img_format)
                self._change_image(img_path, img_data, img_format)
            else:
                self._create_image(img_name, img_path, img_data, img_format)
        except Tkinter.TclError, err:
            showerror("Error creating image", err, parent=self)
            return False
        else:
            return True

    def _create_image(self, img_name, img_path, img_data, img_format):
        """Create a new PhotoImage."""
        kwargs = {'name': img_name}

        if img_format:
            kwargs['format'] = img_format
        if img_data:
            kwargs['data'] = img_data
        else:
            kwargs['file'] = img_path

        self.result = Tkinter.PhotoImage(**kwargs)

    def _change_image(self, img_path, img_data, img_format):
        """Change an existing PhotoImage. This could easily leave the
        image with invalid values, so it is interesting to use
        _create_image and check for some exception before calling this one."""
        if img_format:
            self._image['format'] = img_format
        if img_path:
            pfile, data = img_path, ''
        else:
            pfile, data = '', img_data

        self._image['file'] = pfile
        self._image['data'] = data

    def _find_image(self):
        """Open a file browser and search for the image path."""
        path = askopenfilename(parent=self)
        if path:
            # erase previous content
            self.img_path.delete(0, len(self.img_path.get()))
            # insert new path
            self.img_path.insert(0, path)


class NewElement(NewOption): # reusing buttonbox
    """A dialog for collecting data for a new image element."""

    def __init__(self, master, title="New Element", imglist=None):
        self._imglist = imglist
        NewOption.__init__(self, master, title)

    def body(self, master):
        # element name
        name = ttk.Label(master, text="Element name")
        self.name = ttk.Entry(master)
        # only image type is being supported for now
        etype = ttk.Label(master, text="Element type")
        self.etype = ttk.Entry(master)
        self.etype.insert(0, "image")
        self.etype['state'] = 'readonly'
        defimg = ttk.Label(master, text="Default image")
        self.defimg = ttk.Combobox(master)
        if self._imglist:
            self.defimg['values'] = self._imglist['values']
        # options
        opts = ttk.Label(master, text="Options")
        self.opts = ttk.Entry(master)
        # statespec(s)
        sspec = ttk.Label(master, text="StateSpec(s)")
        self.sspec = ttk.Entry(master)

        # place the widgets
        name.grid(row=0, column=0, sticky='e', padx=6, pady=3)
        self.name.grid(row=0, column=1, pady=3, sticky='ew')
        etype.grid(row=0, column=2, sticky='e', padx=6, pady=3)
        self.etype.grid(row=0, column=3, pady=3)
        defimg.grid(row=1, column=0, sticky='e', padx=6, pady=3)
        self.defimg.grid(row=1, column=1, pady=3, sticky='ew')
        opts.grid(row=1, column=2, sticky='e', padx=6, pady=3)
        self.opts.grid(row=1, column=3, pady=3)
        sspec.grid(row=2, column=0, sticky='e', padx=6, pady=3)
        self.sspec.grid(row=2, column=1, columnspan=3, sticky='ew', pady=3)

        self.resizable(False, False)

    def validate(self):
        """Check if an, apparently, correct element specification has been
        entered."""
        entries = [('elementname', self.name), ('etype', self.etype),
            ('def', self.defimg), ('sspec', self.sspec), ('opts', self.opts)]
        values = {}
        for name, entry in entries:
            values[name] = entry.get()

        if not all((values['elementname'], values['etype'], values['def'])):
            showwarning("Invalid element specification",
                "You need to specify a name, a type and a default image "
                "at least.", parent=self)
            return False

        if values['opts']:
            try:
                # XXX Warning: eval usage!
                values['opts'] = eval(values['opts'])
                if not isinstance(values['opts'], dict):
                    raise TypeError
            except (NameError, SyntaxError), err:
                showerror("Invalid options specification",
                    "Options should be formatted according to a dict.\n\n"
                    "Error: %s" % err,
                    parent=self)
                return False
            except TypeError:
                showerror("Invalid options specification",
                    "Options should be formatted according to a dict.",
                    parent=self)
                return False
        else:
            values['opts'] = {}

        self.result = values
        return True


class MainWindow(object):
    def __init__(self, master, title=None):
        frame = ttk.Frame(master)
        self.master = frame.master
        
        width = 640
        height = width - 50
        self.master.geometry('%dx%d' % (width, height))
        self.master.minsize(width, height)
        self.master.title(title)

        self._filename = None # no custom theme loaded
        self._style = ttk.Style(self.master)
        self._current_widget = {'layout': None, 'widget': None}
        self._images = {} # images created by the user

        self.__create_menu()
        self.__setup_widgets()
        self.__fill_treeview()

    def _change_preview(self, event, invalid=False):
        """New treeview selection (or theme changed), update preview area."""
        treeview = getattr(event, 'widget', event)

        sel = treeview.selection()
        if not sel: # nothing selected
            return
        
        sel = sel[0]
        tv_item = treeview.item(sel)
        widget_name = tv_item['text']
        widget_style = None
        opts = {}

        if self._is_layout(widget_name, sel): # not a widget, but a layout
            self._update_layout_text("Custom.%s" % widget_name)
            if 'Horizontal' in widget_name or 'Vertical' in widget_name:
                opts['orient'] = widget_name.split('.')[0].lower()
                widget_style = "Custom.%s" % widget_name
            widget_name = treeview.item(treeview.parent(sel))['text']
        else:
            self._empty_layout()

        widget = self._widget[widget_name]
        widget_style = widget_style or widget['class']
        curr_widget = self._current_widget

        if not invalid and curr_widget['layout'] == widget_style:
            if not opts or \
               str(curr_widget['widget']['orient']) == opts['orient']:
                # didn't select a new widget/no new options
                return

        # create a sample widget
        if widget.get('factory', None):
            widget_class = getattr(ttk, widget_name)
            sample = widget['factory'](widget_class, self._preview_area, **opts)
        else:
            sample = getattr(ttk, widget_name)(self._preview_area, **opts)

        sample['style'] = widget_style
        if curr_widget['widget'] is not None:
            curr_widget['widget'].pack_forget()
        sample.pack(expand=True)

        curr_widget['layout'] = widget_style
        curr_widget['widget'] = sample
        self._remove_previous_widgets()
        self._update_style_configframe()
        self._update_style_mapframe()

    def _is_layout(self, name, selection):
        """Check if a treeview selection is a layout or a widget."""
        return (name not in self._widget or
            self._widget[name]['tv_item'] != selection)

    def _remove_previous_widgets(self):
        """Remove labels and entries from the style frames."""
        widgets = self._configframe.pack_slaves() + self._mapframe.pack_slaves()

        for widget in widgets:
            if widget.winfo_class() == 'TButton':
                continue
            widget.pack_forget()

    def _update_style_configframe(self):
        """Update the configure frame for the current widget."""
        self._update_style(self._style.configure, self._configframe)

    def _update_style_mapframe(self):
        """Update the map frame for the current widget."""
        self._update_style(self._style.map, self._mapframe)

    def _update_style(self, func, frame):
        """Treeview selection changed, update the displayed style."""
        widget = self._current_widget
        widget_base_layout = widget['widget'].winfo_class()
        custom_layout = widget['layout']
        options = func(widget_base_layout)
        options.update(func(custom_layout))

        # add options to the specified frame
        for opt_name, opt_value in options.items():
            self._add_opt_frame(frame, func, custom_layout, opt_name, opt_value)

    def _add_opt_frame(self, frame, func, layout_name, opt_name, opt_value):
        """Add a new option to a frame."""
        def change_opt(option, text):
            """Try to apply the new value of a option that changed."""
            try:
                # XXX Warning: eval usage!
                func(layout_name, **{option: eval(text)})
            except NameError:
                func(layout_name, **{option: text})
            except (SyntaxError, Tkinter.TclError, TypeError):
                pass
            return True

        lbl = ttk.Label(frame, text=opt_name)
        lbl.pack(side='top', anchor='w')
        entry = ttk.Entry(frame)
        entry.insert(0, opt_value)
        entry.configure(validate='key',
            validatecommand=(self.master.register(change_opt), opt_name, '%P'))
        entry.validate()
        entry.pack(side='top', fill='x', pady=3)

    def _update_layout_text(self, layout_name):
        """Update the layout text for the current widget."""
        output = cStringIO.StringIO()
        pprint.pprint(self._style.layout(layout_name), stream=output)
        layout = output.getvalue()
        output.close()
        self._empty_layout()
        self.layouttext.layout = layout_name
        self.layouttext.insert('1.0', layout) # set new text

    def _empty_layout(self):
        """Clear current text in the layout text widget and unset layout."""
        self.layouttext.delete('1.0', 'end')
        self.layouttext.layout = None

    def _apply_layout(self):
        """Apply the supposed new layout for the current selected widget."""
        layout = self.layouttext.layout
        if not layout: # nothing to do
            return

        text = self.layouttext.get('1.0', 'end')
        if not text.strip(): # no layout
            return
        # XXX Warning: eval usage!
        try:
            self._style.layout(layout, eval(text))
        except (SyntaxError, ValueError, NameError, Tkinter.TclError):
            showerror("Invalid layout", "The specified layout is invalid, "
                "please verify its format.", parent=self.master)

    def _reset_layout(self):
        """Reset the layout for current selected widget."""
        layout = self.layouttext.layout
        if not layout: # nothing to reset
            return

        self._update_layout_text(layout[layout.find('.') + 1:])
        self.layouttext.layout = layout

    def _new_frame_opt(self, frame, func):
        """Open a dialog asking for a new custom option to be added in the
        specified frame and then add it."""
        widget = self._current_widget
        if widget['widget'] is None:
            showwarning("No widget active",
                "Select one widget before trying to add an option.",
                parent=self.master)
            return
        layout_name = widget['layout']

        dlg = NewOption(self.master)
        if dlg.result is not None:
            option, value = dlg.result
            self._add_opt_frame(frame, func, layout_name, option, value)

    def _new_element(self, frame):
        """Open a dialog for getting data for a new style element and then
        create it."""
        dlg = NewElement(self.master, imglist=self._imagelist)
        if dlg.result:
            name = dlg.result['elementname']
            # format args
            if dlg.result['sspec']:
                # XXX Warning: eval usage!
                sspec = eval(dlg.result['sspec'])
                if dlg.result['sspec'].count('(') == 1:
                    # only one statespec defined
                    sspec = (sspec, )
            else:
                sspec = ()
            args = (dlg.result['def'], ) + sspec

            # create element
            try:
                self._style.element_create(name,
                    dlg.result['etype'], *args, **dlg.result['opts'])
            except Tkinter.TclError, err:
                showerror("Element couldn't be created",
                    "The specified element couldn'be created, reason: "
                    "\n%s" % err, parent=self.master)
            else:
                # add it to the list
                self._elems.set(name)
                self._elems['values'] = (self._elems['values'] or ()) + (name, )
                # the new element could have affected the current widget, so
                # we need to update the preview area.
                treeview = self._tv_widgets
                self._change_preview(treeview, invalid=True)

    def _new_image(self):
        """Add a new image to the image combobox. This image can be used
        in any widget layout."""
        dlg = ImageDialog(self.master)
        if dlg.result: # add new image to the images list
            img = dlg.result
            img_name = img.name
            self._images[img_name] = img
            self._imagelist.set(img_name)
            self._imagelist['values'] = (self._imagelist['values'] or ()) + \
                (img_name, )

    def _edit_image(self):
        """Edit current selected image in imagelist."""
        img_name = self._imagelist.get()
        if not img_name:
            return

        ImageDialog(self.master, "Editing Image", self._images[img_name])

    def _remove_image(self):
        """Remove current selected image in imagelist."""
        img_name = self._imagelist.get()
        if not img_name:
            return

        del self._images[img_name]
        values = set(self._imagelist['values']) - set([img_name])
        self._imagelist['values'] = list(values)
        value = values.pop() if values else ''
        self._imagelist.set(value)

    def _change_theme(self, event):
        """New theme selected at themes combobox, change current theme."""
        widget = event.widget
        self._style.theme_use(widget.get())

        treeview = self._tv_widgets
        self._change_preview(treeview, invalid=True)

    def _add_widget(self, name, opts, treeview=None):
        """Add a new widget to self._widget."""
        treeview = treeview or self._tv_widgets
        children = opts.pop('layouts')

        parent = treeview.insert('', 'end', text=name)
        self._widget[name] = {'tv_item': parent,
            'class': "Custom.%s" % children[0]}
        self._widget[name].update(opts)

        for child in children:
            treeview.insert(parent, 'end', text=child)

    def _open_theme(self, event=None):
        """Open and load a theme saved in a file."""
        def get_section_items(themeobj, secname):
            if not themeobj.has_section(secname):
                return None
            return themeobj.items(secname)

        fname = askopenfilename(parent=self.master)
        if not fname:
            return

        try:
            themeobj = ThemeFile(open(fname, 'rb'), self._style, readfrom=True)
        except IOError, err:
            showerror("Theme file couldn't be loaded",
                "Couldn't open requested file.\n\n"
                "Error: %s" % err, parent=self.master)
            return
        except ConfigParser.Error, err:
            showerror("Theme file couldn't be loaded", err, parent=self.master)
            return

        current_theme = self._style.theme_use()

        for theme in self._style.theme_names():
            self._style.theme_use(theme)
            themeobj.load_configure(get_section_items(themeobj,
                '%s-configure' % theme))
            themeobj.load_map(get_section_items(themeobj, '%s-map' % theme))
            themeobj.load_layout(get_section_items(themeobj,
                '%s-layout' % theme))

        # restore theme
        self._style.theme_use(current_theme)
        # refresh widget preview
        treeview = self._tv_widgets
        self._change_preview(treeview, invalid=True)
        # update file in use
        self._filename = fname

        themeobj.close()

    def _save_theme(self, event=None):
        """Save current changes to the current file."""
        if self._filename is None:
            self._filename = self._save_theme_as(event)
        else:
            self.__save_changes(self._filename)

    def _save_theme_as(self, event=None):
        """Save current changes to a file."""
        fname = asksaveasfilename()
        if not fname:
            return
        self.__save_changes(fname)
        return fname

    def __save_changes(self, fname):
        try:
            themeobj = ThemeFile(open(fname, 'wb'))
        except IOError, err:
            showerror("Error on file creation",
                "Theme won't be saved.\n\nError: %s" % err, parent=self.master)
            return

        current_theme = self._style.theme_use()

        # traverse through all themes looking for things that changed
        for theme in self._style.theme_names():
            self._style.theme_use(theme)
            themeobj.add_theme_sections(theme)

            for parent in self._tv_widgets.get_children(''):
                for child in self._tv_widgets.get_children(parent):
                    layout = self._tv_widgets.item(child)['text']
                    custom_layout = "Custom.%s" % layout
                    data = {
                        'configure': (
                            self._style.configure(custom_layout),
                            self._style.configure(layout)),
                        'map': (
                            self._style.map(custom_layout),
                            self._style.map(layout)),
                        'layout': (
                            self._style.layout(custom_layout),
                            self._style.layout(layout))
                    }

                    # save custom data
                    for themeopt, (custom, orig) in data.iteritems():
                        if custom and custom != orig:
                            themeobj.set('%s-%s' % (theme, themeopt),
                                layout, cPickle.dumps(custom, 2))

        themeobj.save()
        themeobj.close()
        # restore previous theme in use
        self._style.theme_use(current_theme)

    def __create_menu(self):
        menu = Tkinter.Menu()
        self.master['menu'] = menu

        file_menu = Tkinter.Menu(menu, tearoff=False)
        file_menu.add_command(label="Open", underline=0, accelerator="Ctrl+o",
            command=self._open_theme)
        file_menu.add_command(label="Save", underline=0, accelerator="Ctrl+s",
            command=self._save_theme)
        file_menu.add_command(label="Save as..", accelerator="Ctrl+Shift+s",
            command=self._save_theme_as)
        file_menu.add_separator()
        file_menu.add_command(label="Quit", underline=1, accelerator="Ctrl+q",
            command=self.master.destroy)

        menu.add_cascade(menu=file_menu, label="File", underline=0)
        self.master.bind('<Control-o>', self._open_theme)
        self.master.bind('<Control-s>', self._save_theme)
        self.master.bind('<Control-Shift-S>', self._save_theme_as)
        self.master.bind('<Control-q>', 'exit')

    def __setup_widgets(self):
        """Create and layout widgets."""
        paned = ttk.Panedwindow()

        # top frame
        top = ttk.Frame(paned)
        top.pack(side='top', fill='both', expand=True)

        # top left frame (widget listing, images)
        left = ttk.Frame(top)
        left.pack(side='left', fill='y')
        # widget listing
        self._tv_widgets = ScrolledTreeview(left, selectmode='browse')
        self._tv_widgets.pack(side='top', fill='y', expand=True)
        self._tv_widgets.heading('#0', text="Widgets")
        self._tv_widgets.bind('<<TreeviewSelect>>', self._change_preview)

        # top right frame (preview, style notebook, images)
        topright = ttk.Frame(top)
        topright.pack(side='top', fill='both', expand=True)

        # preview area
        self._preview_area = ttk.Frame(topright, width=200)
        self._preview_area.pack(side='left', expand=True, fill='both', padx=12)

        # options, images and themes
        frames = ttk.Frame(topright)
        frames.pack(side='right', anchor='n')
        # style notebook and frames
        styleframe = ttk.Labelframe(frames, text="Style", padding=6)
        styleframe.pack(fill='both')
        stylenb = ttk.Notebook(styleframe)
        # style configure
        self._configframe = ttk.Frame(stylenb, padding=6)
        newopt = ttk.Button(self._configframe, text="Add option",
            command=lambda: self._new_frame_opt(self._configframe,
                self._style.configure))
        newopt.pack(side='bottom', anchor='e')
        self._configframe.pack()
        # style map
        self._mapframe = ttk.Frame(stylenb, padding=6)
        newmopt = ttk.Button(self._mapframe, text="Add option",
            command=lambda: self._new_frame_opt(self._mapframe,
                self._style.map))
        newmopt.pack(side='bottom', anchor='e')
        self._mapframe.pack()
        # style elements
        elemframe = ttk.Frame(stylenb, padding=6)
        self._elems = ttk.Combobox(elemframe, state='readonly')
        self._elems.pack(fill='x', pady=6)
        newelem = ttk.Button(elemframe, text="New element",
            command=lambda: self._new_element(elemframe))
        newelem.pack(side='bottom', anchor='e')
        elemframe.pack()
        # themes
        themeframe = ttk.Frame(stylenb, padding=6)
        themeframe.pack(padx=6)
        themes = ttk.Combobox(themeframe, values=self._style.theme_names(),
            state='readonly')
        themes.set("Pick one")
        themes.bind('<<ComboboxSelected>>', self._change_theme)
        themes.pack(fill='x', pady=6)
        # add frames to the style notebook
        stylenb.add(self._configframe, text="Configure")
        stylenb.add(self._mapframe, text="Map")
        stylenb.add(elemframe, text="Elems")
        stylenb.add(themeframe, text="Themes")
        stylenb.pack(fill='both', anchor='n')
        # images frame
        imagesframe = ttk.Labelframe(frames, padding=6)
        imagesframe.pack(fill='x', pady=12)
        iframe = ttk.Frame(imagesframe)
        imagesframe['labelwidget'] = iframe
        self.__img_add = Tkinter.PhotoImage(file=os.path.join(IMAGE_DIR,
            'add.gif'))
        self.__img_edit = Tkinter.PhotoImage(file=os.path.join(IMAGE_DIR,
            'stock_properties.gif'))
        self.__img_del = Tkinter.PhotoImage(file=os.path.join(IMAGE_DIR,
            'remove.gif'))
        ilbl = ttk.Label(iframe, text="Images")
        iadd = ttk.Button(iframe, image=self.__img_add.name,
            style='Toolbutton', command=self._new_image)
        iedit = ttk.Button(iframe, image=self.__img_edit.name,
            style='Toolbutton', command=self._edit_image)
        iremove = ttk.Button(iframe, image=self.__img_del.name,
            style='Toolbutton', command=self._remove_image)
        ilbl.pack(side='left')
        iadd.pack(side='left')
        iedit.pack(side='left')
        iremove.pack(side='left')
        self._imagelist = ttk.Combobox(imagesframe, state='readonly')
        self._imagelist.pack(fill='x')

        # bottom frame (layout)
        bottom = ttk.Frame(paned)
        bottom.pack(side='bottom')
        layoutframe = ttk.Labelframe(bottom, padding=6)
        layoutframe.pack(fill='both', expand=True)
        lframe = ttk.Frame(layoutframe)
        layoutframe['labelwidget'] = lframe
        self.__img_apply = Tkinter.PhotoImage(file=os.path.join(IMAGE_DIR,
            'dialog-apply.gif'))
        self.__img_reset = Tkinter.PhotoImage(file=os.path.join(IMAGE_DIR,
            'back.gif'))
        llbl = ttk.Label(lframe, text="Layout")
        apply_btn = ttk.Button(lframe, image=self.__img_apply.name,
            command=self._apply_layout, style='Toolbutton')
        reset_btn = ttk.Button(lframe, image=self.__img_reset.name,
            command=self._reset_layout, style='Toolbutton')
        llbl.pack(side='left')
        apply_btn.pack(side='left')
        reset_btn.pack(side='left')
        # layouttext
        textframe = ttk.Frame(layoutframe)
        textframe.pack(side='left', fill='both', expand=True)
        self.layouttext = ScrolledText(textframe)
        self.layouttext.layout = None
        self.layouttext.pack(expand=True, fill='both')

        paned.add(top, weight=1)
        paned.add(bottom, weight=0)
        paned.pack(fill='both', expand=True)
        self.__funcid = paned.bind('<Map>', self.__adjust_sash)

    def __adjust_sash(self, event):
        """Adjust the initial sash position between the top frame and the
        bottom frame."""
        height = self.master.geometry().split('x')[1].split('+')[0]
        paned = event.widget
        paned.sashpos(0, int(height) - 180)
        paned.unbind('<Map>', self.__funcid)
        del self.__funcid

    def __fill_treeview(self):
        """Insert available widgets in the treeview."""
        self._widget = {}
        widgets = map_widgets()
        for name, opts in sorted(widgets.items()):
            self._add_widget(name, opts)


def main():
    root = Tkinter.Tk()
    app = MainWindow(root, 'Ttk Theming')
    root.mainloop()

if __name__ == "__main__":
    main()
