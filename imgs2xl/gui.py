#!/usr/bin/env python
# coding: utf-8
import os
import sys
import subprocess
import tkinter as tk
import imgs2xl
from tkinter import ttk
from tkinter import filedialog
from threading import Thread
from contextlib import contextmanager


class Application(tk.Frame):
    TAGNAMES = [
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

        master.minsize(400, 200)
        master.title("gimgs2xl")

        frame = ttk.Frame(master, padding=10)
        frame.pack()

        self.create_widgets(frame)

    def create_widgets(self, parent):
        self.imgspath_var = tk.StringVar()
        self.xlsxpath_var = tk.StringVar()
        self.thumbssize_var = tk.IntVar(value=320)
        self.othertags_var = tk.StringVar()
        self.recursive_var = tk.BooleanVar()

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
        tagslist_label = tk.Label(parent, text="Tags:")
        tagslist_label.grid(row=row, column=0, sticky=tk.NE)
        self.tags_list = tk.Listbox(
            parent,
            listvariable=tk.StringVar(value=Application.TAGNAMES),
            selectmode="multiple",
            width=0,
        )
        self.tags_list.grid(row=row, column=1, sticky=tk.NE + tk.NW + tk.S)
        scrollbar = tk.Scrollbar(
            parent, orient=tk.VERTICAL, command=self.tags_list.yview
        )
        self.tags_list["yscrollcommand"] = scrollbar.set
        scrollbar.grid(row=row, column=2, sticky=(tk.NW + tk.S))

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
            geo = self.master.geometry().replace('x', '+').split('+')
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

    def execute_imgs2xl(self):
        with self.on_busy_task():
            tags = []
            selected = self.tags_list.curselection()
            for index in selected:
                tags.append(Application.TAGNAMES[index])

            tags += self.othertags_var.get().split(",")

            imgs2xl.run(
                imgspath=self.imgspath_var.get(),
                xlsxpath=self.xlsxpath_var.get(),
                thumbssize=self.thumbssize_var.get(),
                tags=tags,
                recursive=self.recursive_var.get(),
                callback=self.progress_callback,
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
