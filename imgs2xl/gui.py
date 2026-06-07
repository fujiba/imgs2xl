#!/usr/bin/env python
# coding: utf-8
import os
import sys
import subprocess
import imgs2xl
import tkinter as tk
from tkinter import ttk, filedialog
from threading import Thread
from contextlib import contextmanager


class Application(tk.Frame):
    _TAGNAMES = [
        "File:FileName",
        "File:Directory",
        "File:FileSize",
        "File:FileModifyDate",
        "File:FileAccessDate",
        "File:FileType",
        "File:FileTypeExtension",
        "File:MIMEType",
        "File:ImageWidth",
        "File:ImageHeight",
        "EXIF:Make",
        "EXIF:Model",
        "EXIF:XResolution",
        "EXIF:YResolution",
        "EXIF:ResolutionUnit",
        "EXIF:Software",
        "EXIF:ModifyDate",
        "EXIF:Artist",
        "EXIF:Copyright",
        "EXIF:ExposureTime",
        "EXIF:FNumber",
        "EXIF:ExposureProgram",
        "EXIF:ISO",
        "EXIF:SensitivityType",
        "EXIF:StandardOutputSensitivity",
        "EXIF:ExifVersion",
        "EXIF:DateTimeOriginal",
        "EXIF:CreateDate",
        "EXIF:OffsetTime",
        "EXIF:ShutterSpeedValue",
        "EXIF:ApertureValue",
        "EXIF:ExposureCompensation",
        "EXIF:MeteringMode",
        "EXIF:Flash",
        "EXIF:FocalLength",
        "EXIF:FocalLengthIn35mmFormat",
        "EXIF:FocalPlaneXResolution",
        "EXIF:FocalPlaneYResolution",
        "EXIF:FocalPlaneResolutionUnit",
        "EXIF:SensingMethod",
        "EXIF:CustomRendered",
        "EXIF:ExposureMode",
        "EXIF:WhiteBalance",
        "EXIF:SceneCaptureType",
        "EXIF:Contrast",
        "EXIF:Saturation",
        "EXIF:Sharpness",
        "EXIF:SubjectDistanceRange",
        "EXIF:SubSecTimeOriginal",
        "EXIF:SubSecTimeDigitized",
        "EXIF:ColorSpace",
        "EXIF:LensInfo",
        "EXIF:LensModel",
        "IPTC:DateCreated",
        "IPTC:TimeCreated",
        "IPTC:DigitalCreationDate",
        "IPTC:DigitalCreationTime",
        "XMP:Lens",
        "XMP:LensID",
        "XMP:ColorTemperature",
        "XMP:Tint",
        "XMP:Creator",
        "XMP:Rights",
    ]

    def __init__(self, master=None):
        super().__init__(master)

        master.minsize(800, 400)
        master.title("gimgs2xl")

        menu = self.create_menu(master)
        master.config(menu=menu)
        master.rowconfigure(0, weight=1)
        master.columnconfigure(0, weight=1)
        master.grid()

        frame = ttk.Frame(master, padding=10)
        frame.pack()
        self.create_widgets(frame)

    def create_menu(self, parent):
        menubar = tk.Menu(parent)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Load param...", command=self.on_load_param)
        filemenu.add_command(label="Save param...", command=self.on_save_param)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.on_close)

        # helpmenu = tk.Menu(menubar, tearoff=0)
        # helpmenu.add_command(label='Help', command=baz)

        menubar.add_cascade(label="File", menu=filemenu)
        # menubar.add_cascade(label='Help', menu=helpmenu)

        return menubar

    def create_widgets(self, parent):
        self.imgspath_var = tk.StringVar()
        self.xlsxpath_var = tk.StringVar()
        self.thumbssize_var = tk.IntVar(value=320)
        self.othertags_var = tk.StringVar()
        self.recursive_var = tk.BooleanVar()
        self.fullpath_var = tk.BooleanVar()

        row = 0
        imgspath_label = tk.Label(parent, text="Images path:")
        imgspath_label.grid(row=row, column=0, sticky=tk.E)
        self.imgspath_entry = tk.Entry(parent, textvariable=self.imgspath_var, width=24)
        self.imgspath_entry.grid(row=row, column=1, sticky=tk.W)
        self.imgspath_browse = tk.Button(
            parent, text="Browse...", command=self.on_imgspath_browse
        )
        self.imgspath_browse.grid(row=row, column=2)

        row += 1
        self.recursive_chkbox = tk.Checkbutton(
            parent, variable=self.recursive_var, text="Recursive"
        )
        self.recursive_chkbox.grid(row=row, column=1, sticky=tk.W)

        row += 1
        self.fullpath_chkbox = tk.Checkbutton(
            parent, variable=self.fullpath_var, text="Fullpath"
        )
        self.fullpath_chkbox.grid(row=row, column=1, sticky=tk.W)

        row += 1
        xlsxpath_label = tk.Label(parent, text="Excel book path:")
        xlsxpath_label.grid(row=row, column=0, sticky=tk.E)
        self.xlsxpath_entry = tk.Entry(parent, textvariable=self.xlsxpath_var, width=24)
        self.xlsxpath_entry.grid(row=row, column=1, sticky=tk.W)
        self.xlsxpath_browse = tk.Button(
            parent, text="Browse...", command=self.on_xlsxpath_browse
        )
        self.xlsxpath_browse.grid(row=row, column=2)

        row += 1
        thumbssize_label = tk.Label(parent, text="Thumbsnail size:")
        thumbssize_label.grid(row=row, column=0, sticky=tk.E)

        self.thumbssize_entry = tk.Entry(
            parent, textvariable=self.thumbssize_var, width=4, justify=tk.RIGHT
        )
        self.thumbssize_entry.grid(row=row, column=1, sticky=tk.E)

        thumbssizesuffix_label = tk.Label(parent, text="px")
        thumbssizesuffix_label.grid(row=row, column=2, sticky=tk.W)

        row += 1
        tagslist_frame_left = tk.Frame(parent)
        tagslist_frame_left.grid(row=row, column=0, sticky=tk.NE)
        tagslist_label = tk.Label(tagslist_frame_left, text="Available Tags:")
        tagslist_label.pack(side=tk.TOP, anchor=tk.E)
        scan_tags_button = tk.Button(tagslist_frame_left, text="Scan Tags", command=self.update_tags_from_image)
        scan_tags_button.pack(side=tk.TOP, anchor=tk.E, pady=5)
        
        lists_frame = tk.Frame(parent)
        lists_frame.grid(row=row, column=1, columnspan=2, sticky=tk.NE + tk.NW + tk.S + tk.E)
        
        left_frame = tk.Frame(lists_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.available_tags_list = tk.Listbox(
            left_frame,
            listvariable=tk.StringVar(value=Application._TAGNAMES),
            selectmode="multiple",
            width=30,
            exportselection=False
        )
        self.available_tags_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_avail = tk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.available_tags_list.yview)
        self.available_tags_list["yscrollcommand"] = scrollbar_avail.set
        scrollbar_avail.pack(side=tk.LEFT, fill=tk.Y)
        self.available_tags_list.bind("<Double-1>", lambda e: self.add_selected_tags())

        btn_frame = tk.Frame(lists_frame, padx=10)
        btn_frame.pack(side=tk.LEFT, fill=tk.Y)
        btn_add = tk.Button(btn_frame, text="Add ->", command=self.add_selected_tags)
        btn_add.pack(side=tk.TOP, pady=(50, 5))
        btn_remove = tk.Button(btn_frame, text="<- Remove", command=self.remove_selected_tags)
        btn_remove.pack(side=tk.TOP, pady=5)

        right_frame = tk.Frame(lists_frame)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.selected_tags_list = tk.Listbox(
            right_frame,
            selectmode="multiple",
            width=30,
            exportselection=False
        )
        self.selected_tags_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_sel = tk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.selected_tags_list.yview)
        self.selected_tags_list["yscrollcommand"] = scrollbar_sel.set
        scrollbar_sel.pack(side=tk.LEFT, fill=tk.Y)
        self.selected_tags_list.bind("<Double-1>", lambda e: self.remove_selected_tags())

        row += 1
        othertags_label = tk.Label(parent, text="Other tags\n(Comma separated):")
        othertags_label.grid(row=row, column=0, sticky=tk.E)
        self.othertags_entry = tk.Entry(
            parent, textvariable=self.othertags_var, width=40
        )
        self.othertags_entry.grid(row=row, column=1, columnspan=2, sticky=tk.W)

        row += 1
        self.run_button = tk.Button(parent, text="Run!", command=self.on_run)
        self.run_button.grid(row=row, column=0)

        self.close_button = tk.Button(parent, text="Exit", command=self.on_close)
        self.close_button.grid(row=row, column=2)

    def add_selected_tags(self):
        sel_indices = self.available_tags_list.curselection()
        if not sel_indices:
            return
        
        tags_to_add = [self.available_tags_list.get(i) for i in sel_indices]
        current_selected = list(self.selected_tags_list.get(0, tk.END))
        
        for tag in tags_to_add:
            if tag not in current_selected:
                self.selected_tags_list.insert(tk.END, tag)
                
        self.available_tags_list.selection_clear(0, tk.END)

    def remove_selected_tags(self):
        sel_indices = self.selected_tags_list.curselection()
        if not sel_indices:
            return
            
        for i in reversed(sel_indices):
            self.selected_tags_list.delete(i)

    def _find_first_image(self, path, recursive):
        import filetype
        if not recursive:
            try:
                for entry in os.scandir(path):
                    if entry.is_file() and filetype.is_image(entry.path):
                        return entry.path
            except Exception:
                pass
        else:
            try:
                for root, dirs, files in os.walk(path):
                    for file in files:
                        p = os.path.join(root, file)
                        if filetype.is_image(p):
                            return p
            except Exception:
                pass
        return None

    def update_tags_from_image(self, *args):
        path = self.imgspath_var.get()
        if not path or not os.path.isdir(path):
            tk.messagebox.showerror("imgs2xl", "Images path is invalid or empty!", parent=self.master)
            return

        first_image = self._find_first_image(path, self.recursive_var.get())
        if not first_image:
            tk.messagebox.showinfo("imgs2xl", "No images found in the specified path.", parent=self.master)
            return

        from PIL import Image
        import imgs2xl.metadata
        try:
            pilImage = Image.open(first_image)
            metadata = {}
            imgs2xl.metadata.get_file_metadata(first_image, metadata)
            imgs2xl.metadata.get_image_metadata(pilImage, metadata)
            
            new_tags = list(metadata.keys())
            avail_tags = list(self.available_tags_list.get(0, tk.END))
            sel_tags = list(self.selected_tags_list.get(0, tk.END))
            
            for tag in new_tags:
                if tag not in avail_tags and tag not in sel_tags:
                    self.available_tags_list.insert(tk.END, tag)
        except Exception:
            pass

    def on_load_param(self):
        path = filedialog.askopenfilename(
            parent=self.master,
            filetypes=[("JSON", ".json")],
            initialdir=os.path.expanduser("~"),
        )

        if not path:
            return

        try:
            _ = imgs2xl.input_json(path)
            self.imgspath_var.set(_["inputdir"])
            self.xlsxpath_var.set(_["output"])
            self.recursive_var.set(_["recursive"])
            self.fullpath_var.set(_.get("fullpath", False))
            self.thumbssize_var.set(_["size"])
            
            self.selected_tags_list.delete(0, tk.END)
            othertags = []
            avail_tags = list(self.available_tags_list.get(0, tk.END))
            for tag in _["tags"]:
                if tag in avail_tags:
                    self.selected_tags_list.insert(tk.END, tag)
                else:
                    othertags.append(tag)

            if len(othertags) > 0:
                self.othertags_var.set(",".join(othertags))
        except Exception as e:
            tk.messagebox.showerror(
                "imgs2xl", "Failed to load JSON file.", parent=self.master
            )

    def on_save_param(self):
        path = filedialog.asksaveasfilename(
            parent=self.master,
            filetypes=[("JSON", ".json")],
            initialdir=os.path.expanduser("~"),
        )

        if len(path) <= 0:
            return

        imgs2xl.output_json(
            path,
            self.imgspath_var.get(),
            self.xlsxpath_var.get(),
            self.recursive_var.get(),
            self.thumbssize_var.get(),
            self.make_tags_string(),
            self.fullpath_var.get(),
        )

    def on_xlsxpath_browse(self):
        path = filedialog.asksaveasfilename(
            parent=self.master,
            filetypes=[("Excel Book", ".xlsx")],
            initialdir=os.path.expanduser("~"),
        )
        self.xlsxpath_var.set(path)

    def on_imgspath_browse(self):
        path = filedialog.askdirectory(
            parent=self.master, initialdir=os.path.expanduser("~")
        )
        self.imgspath_var.set(path)

    def launch_application(self, filepath):
        filepath = os.path.expanduser(filepath)
        filepath = os.path.expandvars(filepath)

        if sys.platform.startswith("darwin"):
            subprocess.call(("open", filepath))
        elif os.name == "nt":
            os.startfile(filepath)
        elif os.name == "posix":
            subprocess.call(("xdg-open", filepath))

    @contextmanager
    def on_busy_task(self):
        try:
            geo = self.master.geometry().replace("x", "+").split("+")
            pw = int(geo[0])
            ph = int(geo[1])
            px = int(geo[2])
            py = int(geo[3])
            x = int((pw - 300) / 2 + px)
            y = int((ph - 100) / 2 + py)
            self.progress = tk.Toplevel(self.master)
            self.progress.title("Executing...")
            self.progress.geometry(f"300x100+{x}+{y}")
            tk.Label(self.progress, text="Processed file").pack()

            self.progress_var = tk.DoubleVar()
            self.progress_bar = ttk.Progressbar(
                self.progress,
                variable=self.progress_var,
                maximum=1,
                orient=tk.HORIZONTAL,
                length=280,
            )
            self.progress_bar.pack()

            self.progress_filename_var = tk.StringVar()
            self.progress_filename_label = tk.Label(
                self.progress, textvariable=self.progress_filename_var
            )
            self.progress_filename_label.pack()

            self.progress.pack_slaves()
            yield

        finally:
            self.progress.destroy()
            if tk.messagebox.askyesno(
                "imgs2xl", "Do you want to open Excel book file?", parent=self.master
            ):
                self.launch_application(self.xlsxpath_var.get())

    def progress_callback(self, filename, total, n):
        self.progress.update()
        self.progress_var.set(n / total)
        self.progress_filename_var.set(os.path.basename(filename))

    def make_tags_string(self):
        tags = list(self.selected_tags_list.get(0, tk.END))

        if len(self.othertags_var.get()) > 0:
            tags += self.othertags_var.get().split(",")

        return tags

    def execute_imgs2xl(self):
        with self.on_busy_task():
            tags = self.make_tags_string()

            imgs2xl.run(
                imgspath=self.imgspath_var.get(),
                xlsxpath=self.xlsxpath_var.get(),
                thumbssize=self.thumbssize_var.get(),
                tags=tags,
                recursive=self.recursive_var.get(),
                callback=self.progress_callback,
                fullpath=self.fullpath_var.get(),
            )

    def on_run(self):
        if len(self.imgspath_var.get()) <= 0:
            tk.messagebox.showerror(
                "imgs2xl", "Images path is empty!", parent=self.master
            )
            return
        if len(self.xlsxpath_var.get()) <= 0:
            tk.messagebox.showerror(
                "imgs2xl", "Excel book path is empty!", parent=self.master
            )
            return
        thread = Thread(target=self.execute_imgs2xl, daemon=True)
        thread.start()

    def on_close(self):
        if tk.messagebox.askyesno("imgs2xl", "Do you want exit?", parent=self.master):
            quit()


def main():
    root = tk.Tk()

    app = Application(master=root)
    app.mainloop()


if __name__ == "__main__":
    main()
