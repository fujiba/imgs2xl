#!/usr/bin/env python
# coding: utf-8
import os
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

        imgspath_label = tk.Label(parent, text="Images path:")
        imgspath_label.grid(row=0, column=0, sticky=tk.E)
        self.imgspath_entry = tk.Entry(parent, textvariable=self.imgspath_var, width=24)
        self.imgspath_entry.grid(row=0, column=1)
        self.imgspath_browse = tk.Button(
            parent, text="Browse...", command=self.on_imgspath_browse
        )
        self.imgspath_browse.grid(row=0, column=2)

        xlsxpath_label = tk.Label(parent, text="Excel book path:")
        xlsxpath_label.grid(row=1, column=0, sticky=tk.E)
        self.xlsxpath_entry = tk.Entry(parent, textvariable=self.xlsxpath_var, width=24)
        self.xlsxpath_entry.grid(row=1, column=1)
        self.xlsxpath_browse = tk.Button(
            parent, text="Browse...", command=self.on_xlsxpath_browse
        )
        self.xlsxpath_browse.grid(row=1, column=2)

        thumbssize_label = tk.Label(parent, text="Thumbsnail size:")
        thumbssize_label.grid(row=2, column=0, sticky=tk.E)

        self.thumbssize_entry = tk.Entry(
            parent, textvariable=self.thumbssize_var, width=4, justify=tk.RIGHT
        )
        self.thumbssize_entry.grid(row=2, column=1, sticky=tk.E)

        thumbssizesuffix_label = tk.Label(parent, text="px")
        thumbssizesuffix_label.grid(row=2, column=2, sticky=tk.W)

        tagslist_label = tk.Label(parent, text="Tags:")
        tagslist_label.grid(row=3, column=0, sticky=tk.NE)
        self.tags_list = tk.Listbox(
            parent,
            listvariable=tk.StringVar(value=Application.TAGNAMES),
            selectmode="multiple",
            width=0,
        )
        self.tags_list.grid(row=3, column=1, sticky=tk.NE + tk.NW + tk.S)
        scrollbar = tk.Scrollbar(
            parent, orient=tk.VERTICAL, command=self.tags_list.yview
        )
        self.tags_list["yscrollcommand"] = scrollbar.set
        scrollbar.grid(row=3, column=2, sticky=(tk.NW + tk.S))

        othertags_label = tk.Label(parent, text="Other tags\n(Comma separated):")
        othertags_label.grid(row=4, column=0, sticky=tk.E)
        self.othertags_entry = tk.Entry(
            parent, textvariable=self.othertags_var, width=40
        )
        self.othertags_entry.grid(row=4, column=1, columnspan=2)

        self.run_button = tk.Button(parent, text="Run!", command=self.on_run)
        self.run_button.grid(row=6, column=0)

        self.close_button = tk.Button(parent, text="Exit", command=self.on_close)
        self.close_button.grid(row=6, column=2)

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

    @contextmanager
    def on_busy_task(self):
        try:
            self.progress = tk.Toplevel(self.master)
            self.progress.title("Executing...")
            self.progress.geometry("300x100")
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

            imgs2xl.imgs2xl(
                imgspath=self.imgspath_var.get(),
                xlsxpath=self.xlsxpath_var.get(),
                thumbssize=self.thumbssize_var.get(),
                tags=tags,
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
