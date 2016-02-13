import gtk
import os
import subprocess


class search_movie:
    # this function is used just for printing messages.
    def callback(self, widget, data=None):
        print("%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active()]))

        # dont know if this will be used.

    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False

    def delete_root_selector(self, widget, data=None):
        gtk.main_quit()
        return False

    def disable_all_other_check_buttons(self, widget):
        if self.cbuttonall.get_active():
            self.cbuttonmp4.set_sensitive(False)
            self.cbuttonmkv.set_sensitive(False)
            self.cbuttonpdf.set_sensitive(False)
            self.cbuttonavi.set_sensitive(False)
        else:
            self.cbuttonmp4.set_sensitive(True)
            self.cbuttonmkv.set_sensitive(True)
            self.cbuttonpdf.set_sensitive(True)
            self.cbuttonavi.set_sensitive(True)

    def show_password_not_set_error(self, widget):
        pass

    def tb_clicked(self, widget):

        try:

            if widget.get_active():
                self.root_path.set_sensitive(True)
                self.bsearch.set_sensitive(False)

            else:
                # get the home dir of user
                p = subprocess.Popen("echo $USER", stdout=subprocess.PIPE, shell=True)
                (uname, err) = p.communicate()

                default_dir = "/home/" + uname.rstrip() + "/"
                # if path textbox is empty
                if not self.root_path.get_text():
                    self.root_path.set_text(default_dir)
                    # if path entered is not valid.
                else:
                    # check if the path exists.
                    if not os.path.exists(self.root_path.get_text()):
                        self.root_path.set_text(default_dir)
                        # check permissions to this dir.
                        #                elif not os.access(self.root_path.get_text(),os.W_OK):
                        #                    self.root_path.set_text(default_dir)

                self.root_path.set_sensitive(False)
                self.bsearch.set_sensitive(True)
                # This function is called when the search button is pressed.
                # sense all relevent data in this function and pass them as parameters to
                # the search script.
        except subprocess.CalledProcessError as e:
            print e.output

    def search_this_text(self, widget, data):
        try:
            if self.pwd_entry.get_text() and self.textbox.get_text():
                # actual search text
                search_txt = self.textbox.get_text()
                # whether to ignore case or not
                if self.check_case.get_active():
                    check_case = "true"
                else:
                    check_case = "false"
                # The root dir of the search.
                root = self.root_path.get_text()

                # whether all formats tab is checked.
                if self.cbuttonall.get_active():
                    all_formats = "true"
                else:
                    all_formats = "false"
                # mp4
                if self.cbuttonmp4.get_active():
                    mp4 = "true"
                else:
                    mp4 = "false"
                # pdf
                if self.cbuttonpdf.get_active():
                    pdf = "true"
                else:
                    pdf = "false"
                # avi
                if self.cbuttonavi.get_active():
                    avi = "true"
                else:
                    avi = "false"
                # mkv
                if self.cbuttonmkv.get_active():
                    mkv = "true"
                else:
                    mkv = "false"

                pwd = self.pwd_entry.get_text()

                # calling the script.                              $1        $2        $3      $4        $5   $6   $7   $8   $9
                proc = subprocess.Popen(
                    ["./sudo-search-video-gtk-version.sh", search_txt, check_case, root, all_formats, mp4, pdf, avi,
                     mkv, pwd],
                    stdout=subprocess.PIPE)

                tmp = proc.stdout.read()
                buf = self.textview.get_buffer()
                tmp = "Following files were found on the disk, " \
                      "having\n \"%s\" in their names ---> " % (search_txt) + tmp
                buf.set_text(tmp)
                # once the search result is displayed, activate choice textbox for entry
                self.choice.set_sensitive(True)
                self.bplay.set_sensitive(True)

            else:
                pwd_not_set_dailog = gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR,
                                                       buttons=gtk.BUTTONS_CLOSE, message_format=None)
                pwd_not_set_dailog.set_markup(
                    "Please make sure that:\n\n1) Search box is not empty\n\n\tAND\n\n2) You've set correct password for the SUDO command")
                #           message.b




                pwd_not_set_dailog.run()
                pwd_not_set_dailog.destroy()



        except Exception as e:
            if e.errno == 2:
                # show a pop up message here instead of printing in console
                message = gtk.MessageDialog(parent=None, flags=0,
                                            type=gtk.MESSAGE_ERROR,
                                            buttons=gtk.BUTTONS_CLOSE,
                                            message_format=None)
                message.set_markup(
                    "Did you accidentally delete or move any files which came with this bundle? \nIf you did, re-extract this software from the original tar file.\nThen, try again.")
                #           message.b
                message.run()
                message.destroy()

    def show_about(self, widget):
        about = gtk.AboutDialog()
        about.set_name('FileFinder')
        about.set_version('version 1.0')
        about.set_website("https://github.com/tanmay-kulkarni/FileFinder")
        gpl = 'This program is free software:\nyou can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.\nThis program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.\nSee the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with this program.\nIf not,see <http://www.gnu.org/licenses/>.'

        about.set_license(gpl)
        about.set_wrap_license(True)
        # about.set_authors('Tanmay Kulkarni')


        about.set_comments(
            "This simple tool searches and plays files from your computer. The files may be located anywhere on the disk. Currently only commonly used video and .pdf formats are supported.\n=============================\n Created by\n=============\nTanmay Kulkarni [using employer's computer & electricity ;) ]\n========================================\nThe single executable bundle is created using Pyinstaller. Thanks to which, this software can run on any linux machine which supports Bash. Even those who don't have python installed. \n Should you find any bugs, drop me an email at:\n-----------------------------------------------\nucanreachtvk@gmail.com\n-----------------------------------------------\n Or better still, remove them yourself. The code is in the tarball of this software or can be found at:")
        about.run()
        about.destroy()

    # this method is to be called when the play button is pressed.
    def open_file(self, widget, data):
        # first pick up the number in textbox.
        number = self.choice.get_text()
        # do error catching here. If the choice entered is absurd, etc.


        # commands
        video_command = self.command_video.get_text()
        pdf_command = self.command_pdf.get_text()

        # proc = subprocess.Popen('ls', stdout=subprocess.PIPE)
        #                                       $1      $2              $3
        proc = subprocess.Popen(["./play.sh", number, video_command, pdf_command], stdout=subprocess.PIPE)

        tmp = proc.stdout.read()
        buf = self.textview.get_buffer()
        buf.set_text(tmp)
        # after the result is displayed, activate the choice textbox.
        self.choice.set_sensitive(True)

    def show_how_to_use(self, widget):
        msg = "\t\t\t\nInstructions:\n<1>.\n\tSet root directory for search\n\n<2>.\n\tThe default commands to open .pdf and video applications are shown near bottom left corner. If these are different on your computer, change them accordingly. \nNOTE: Enter terminal commands here and not names of the applications.\nAlso, it is strongly advised that you use OKULAR for .pdf and VLC for video files. This software has not been tested for other applications, as it works nicely with these two.\n\n<3>.\n\tEnter some characters from the file name.\n\n<4>.\n\tPress \"search\".\n\n<5>.\n\tThe result will be displayed in the central area.\n\n<6>.\n\tEnter your choice in the textbox given.\n\n<7>.\n\tHit \"Play this!\". If all options are correct on the window, your file will open in no time!\n\nTIP:\nIf you don't see results as expected, make sure you've set the root for the search right. \n"

        how_to_use_dialog = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, gtk.BUTTONS_OK,
                                              msg)
        how_to_use_dialog.run()
        how_to_use_dialog.set_title("how to use?")

        how_to_use_dialog.destroy()

    def change_video_file_command(self, widget):
        if self.tbvideo.get_active():
            self.bsearch.set_sensitive(False)
            self.bplay.set_sensitive(False)
            self.tb.set_sensitive(False)
            self.tbpdf.set_sensitive(False)
            self.command_video.set_sensitive(True)



        else:
            self.bsearch.set_sensitive(True)
            self.bplay.set_sensitive(True)
            self.tb.set_sensitive(True)
            self.command_pdf.set_sensitive(False)
            self.command_video.set_sensitive(False)
            self.tbpdf.set_sensitive(True)
            # when toggled off, check if the command is valid.

    def change_pdf_file_command(self, widget):
        if self.tbpdf.get_active():
            self.bsearch.set_sensitive(False)
            self.bplay.set_sensitive(False)
            self.tb.set_sensitive(False)
            self.tbvideo.set_sensitive(False)
            self.command_video.set_sensitive(False)
            self.command_pdf.set_sensitive(True)


        else:
            self.bsearch.set_sensitive(True)
            self.bplay.set_sensitive(True)
            self.tb.set_sensitive(True)
            self.tbvideo.set_sensitive(True)
            self.command_video.set_sensitive(False)
            self.command_pdf.set_sensitive(False)
            # when toggled off, check if the command is valid.

    def save_or_delete_password(self, widget):
        if self.rem_pwd.get_active():
            # create file here if not exists and write to it.
            # if password is not null
            if self.pwd_entry.get_text():
                with open("./sudo.pwd", "w+") as f:
                    f.write(self.pwd_entry.get_text())
            else:
                self.rem_pwd.set_active(False)

        # when button unchecked.
        else:
            # delete that file from disk so next time it's not loaded.
            if os.path.isfile("./sudo.pwd"):
                os.remove("./sudo.pwd")

    # constructor of GUI
    def __init__(self):

        # The main window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("FileFinder 1.o")
        self.window.set_icon_from_file("./s.png")
        self.window.connect("delete_event", self.delete_event)
        self.window.set_border_width(2)
        self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.window.set_resizable(False)

        #        color = gtk.gdk.color_parse('#0f0')
        #        self.window.modify_bg(gtk.STATE_NORMAL, color)


        #        self.window.set_frame_dimensions(10, 10, 10, 10)
        #        self.window.allow_grow(False)
        #        self.window.set_default_size(300,200)
        self.window.set_size_request(800, 410)

        # this HBox, is added to the window.
        hbox0 = gtk.HBox(False, 2)
        # these VBoxes are packed in the HBox from left to right.
        vbox0 = gtk.VBox(False, 2)
        vbox1 = gtk.VBox(False, 2)
        vbox2 = gtk.VBox(False, 2)

        # a vertical seperator at the very beginning
        sep = gtk.VSeparator()
        hbox0.pack_start(sep, True, True, 1)
        sep.show()


        # pack vbox0
        hbox0.pack_start(vbox0, False, True, 5)
        # check button to ignore case
        self.check_case = gtk.CheckButton("Ignore Case")
        # set it to ignore case by default
        self.check_case.set_active(True)
        vbox0.pack_start(self.check_case, True, True, 2)
        self.check_case.show()

        sep = gtk.HSeparator()
        vbox0.pack_start(sep, False, False, 1)
        sep.show()

        # label to show file formats
        label = gtk.Label("----- File Format -----")
        label.show()
        vbox0.pack_start(label, True, True, 2)

        # check button for all
        # when check button is selected, toggle all other buttons off.
        self.cbuttonall = gtk.CheckButton("Any of the below")
        self.cbuttonall.set_active(True)
        vbox0.pack_start(self.cbuttonall, True, True, 2)
        self.cbuttonall.connect("toggled", self.disable_all_other_check_buttons)
        #    cbutton.set_sensitive(False)
        #        self.cbuttonall.set_active(True)
        self.cbuttonall.show()

        # a seperator
        sep = gtk.HSeparator()
        vbox0.pack_start(sep, False, False, 0)
        sep.show()

        # check button for mkv
        self.cbuttonmkv = gtk.CheckButton(".mkv")
        vbox0.pack_start(self.cbuttonmkv, True, True, 2)
        self.cbuttonmkv.set_sensitive(False)
        self.cbuttonmkv.show()
        # check button for mp4
        self.cbuttonmp4 = gtk.CheckButton(".mp4")
        vbox0.pack_start(self.cbuttonmp4, True, True, 2)
        self.cbuttonmp4.set_sensitive(False)
        self.cbuttonmp4.show()
        # check button for pdf
        self.cbuttonpdf = gtk.CheckButton(".pdf")
        vbox0.pack_start(self.cbuttonpdf, True, True, 2)
        self.cbuttonpdf.set_sensitive(False)
        self.cbuttonpdf.show()
        # check button for avi
        self.cbuttonavi = gtk.CheckButton(".avi")
        vbox0.pack_start(self.cbuttonavi, True, True, 2)
        self.cbuttonavi.set_sensitive(False)
        self.cbuttonavi.show()

        sep = gtk.HSeparator()
        vbox0.pack_start(sep, False, False, 0)
        sep.show()

        # terminal command for vlc files.
        label = gtk.Label("Set what terminal command is used for which type of file(toggle buttons):")
        label.set_justify(gtk.JUSTIFY_FILL)
        label.set_use_underline(True)
        label.set_line_wrap(True)
        label.set_size_request(145, -1)
        vbox0.pack_start(label, False, False)
        label.show()

        # toggle video command
        self.tbvideo = gtk.ToggleButton("Video Files")
        self.tbvideo.connect("toggled", self.change_video_file_command)
        vbox0.pack_start(self.tbvideo, False, True, 1)
        self.tbvideo.show()

        # text box for video files command
        self.command_video = gtk.Entry()
        self.command_video.set_text("/usr/bin/vlc")
        self.command_video.set_sensitive(False)
        vbox0.pack_start(self.command_video, True, True, 2)
        self.command_video.show()

        # toggle video command
        self.tbpdf = gtk.ToggleButton("PDF Files")
        self.tbpdf.connect("toggled", self.change_pdf_file_command)
        vbox0.pack_start(self.tbpdf, False, True, 1)
        self.tbpdf.show()

        # text box for pdf files command
        self.command_pdf = gtk.Entry()
        self.command_pdf.set_text("/usr/bin/okular")
        self.command_pdf.set_sensitive(False)
        vbox0.pack_start(self.command_pdf, True, True, 10)
        self.command_pdf.show()

        # a vertical seperator
        sep = gtk.VSeparator()
        hbox0.pack_start(sep, True, True, 2)
        sep.show()

        # vbox1 is packed.
        hbox0.pack_start(vbox1, True, True, 2)

        # a vertical seperator
        sep = gtk.VSeparator()
        hbox0.pack_start(sep, True, True, 2)
        sep.show()

        # vbox2 is packed
        hbox0.pack_start(vbox2, False, True, 2)

        # another vertical seperator
        sep = gtk.VSeparator()
        hbox0.pack_start(sep, False, False, 2)
        sep.show()

        # a Horizontal seperator
        sep = gtk.HSeparator()
        vbox1.pack_start(sep, False, False, 2)
        sep.show()
        # a label
        label = gtk.Label("ENTER NAME OF THE FILE")
        vbox1.pack_start(label, False, False, 2)
        label.show()
        # Hseperator
        sep = gtk.HSeparator()
        vbox1.pack_start(sep, False, False, 2)
        sep.show()
        # a textox for entry
        self.textbox = gtk.Entry()
        #        self.textbox.set_text("linux")
        self.textbox.set_alignment(0.5)
        vbox1.pack_start(self.textbox, False, True, 2)
        self.textbox.show()
        # Hseperator
        sep = gtk.HSeparator()
        vbox1.pack_start(sep, False, False, 2)
        sep.show()

        # this is a complex task (at least it seems so as of now.)
        # for every file type selected, display a list of applications that can
        # open that file format.
        # The user's selection is to be saved in a config file on the disk.
        # While playing the file, the config file should be referred,
        # and play that file in the registered format.

        # textbox for root path specification
        self.root_path = gtk.Entry()
        self.root_path.set_text("/")
        self.root_path.set_alignment(0.5)
        # off by default. Can be modified by toggling the button.
        self.root_path.set_sensitive(False)

        # set it insensitive when focus is lost
        #        self.root_path.connect("")
        self.root_path.show()

        frm_root_path = gtk.Frame("Current search path:")
        frm_root_path.add(self.root_path)

        # pswd for SUDO command.
        pwd_label = gtk.Label("password for SUDO")
        vbox2.pack_start(pwd_label, False, False, 1)
        pwd_label.show()

        box_pwd = gtk.VBox(False, 0)

        # entry for sudo password
        self.pwd_entry = gtk.Entry()
        box_pwd.pack_start(self.pwd_entry, False, False, 1)
        self.pwd_entry.set_visibility(False)
        self.pwd_entry.set_alignment(0.5)

        # read pass from the password file.
        if (os.path.isfile("./sudo.pwd")):
            with open("./sudo.pwd", "r") as f:
                self.pwd_entry.set_text(f.read())

        self.pwd_entry.show()

        self.rem_pwd = gtk.CheckButton("Remember password")
        box_pwd.pack_start(self.rem_pwd, False, False, 1)
        self.rem_pwd.connect("toggled", self.save_or_delete_password)
        self.rem_pwd.set_active(True)
        self.rem_pwd.show()

        box_pwd.show()
        vbox2.pack_start(box_pwd, False, False, 1)

        sep = gtk.HSeparator()
        vbox2.pack_start(sep, False, False, 1)
        sep.show()

        # label for toggle button
        label = gtk.Label("Toggle to change root of search")
        label.set_line_wrap(True)
        label.set_size_request(145, -1)
        label.set_justify(gtk.JUSTIFY_FILL)
        vbox2.pack_start(label, False, True, 2)
        label.show()

        # toggle button for changing search path
        self.tb = gtk.ToggleButton(label="change root")
        vbox2.pack_start(self.tb, False, False, 2)
        # on click, call function to activate the txtbox and
        # on exit, lock txtbox again. If blank, set default "/home/"

        self.tb.connect("toggled", self.tb_clicked)
        self.tb.show()

        vbox2.pack_start(frm_root_path, False, False, 2)
        frm_root_path.show()

        # The search button
        self.bsearch = gtk.Button("Search")
        vbox2.pack_start(self.bsearch, False, False, 2)
        self.bsearch.connect("clicked", self.search_this_text, self.textbox.get_text())
        self.bsearch.show()

        # Label for "enter your choice"
        label = gtk.Label("Enter your choice below.")
        vbox2.pack_start(label, False, False, 2)
        label.show()

        # textbox for entering choice. Disable until result is displayed.

        self.choice = gtk.Entry()
        vbox2.pack_start(self.choice, False, False, 2)
        # default choice is 1
        self.choice.set_text("1")
        self.choice.set_alignment(0.5)
        self.choice.set_sensitive(False)
        self.choice.show()

        # The play button
        # The button disabled by default.
        # It will be activated when the result is displayed,
        # and the user enters a number in the choice textbox.

        self.bplay = gtk.Button("play this!")
        vbox2.pack_start(self.bplay, False, False, 2)
        self.bplay.connect("clicked", self.open_file, self.textbox.get_text())

        self.bplay.set_sensitive(False)

        self.bplay.show()

        # textview for displaying results

        self.textview = gtk.TextView()
        #        self.textview.set_wrap_mode(gtk.WRAP_WORD)
        self.textview.set_wrap_mode(gtk.WRAP_CHAR)
        self.textview.set_justification(gtk.JUSTIFY_LEFT)

        #        self.textview.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse('gray'))
        #        self.textview.modify_text(gtk.STATE_NORMAL, gtk.gdk.color_parse('white'))

        # buffer contains a text to be displayed in the TextView.
        buff = self.textview.get_buffer()

        self.textview.set_wrap_mode(gtk.WRAP_WORD)

        tv_text = "\n\n\n\n\nThe results will be displayed here,\n" \
                  "after you press search. \n" \
                  "Please be patient. \n" \
                  "The first search after boot, \ngenerally requires more time."

        self.textview.set_wrap_mode(gtk.WRAP_CHAR)

        buff.set_text(tv_text)
        self.textview.set_border_width(10)

        # Scrolled Window to hold textView.

        self.sw = gtk.ScrolledWindow()
        # policy for horizontal and vertical scroll respectively.
        self.sw.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        # adds tv to scrolledWindow.
        self.sw.add_with_viewport(self.textview)

        vbox1.pack_start(self.sw, True, True, 2)
        self.sw.show()
        self.textview.show()

        sep = gtk.HSeparator()
        vbox1.pack_start(sep, False, False, 2)
        sep.show()

        self.window.add(hbox0)

        self.how_to_use = gtk.Button("How to use?")
        self.how_to_use.connect("clicked", self.show_how_to_use)
        vbox2.pack_start(self.how_to_use, False, False, 1)
        self.how_to_use.show()

        self.about_button = gtk.Button("About This Software")
        self.about_button.connect("clicked", self.show_about)
        vbox2.pack_start(self.about_button, False, False, 1)
        self.about_button.show()


        hbox0.show()
        vbox0.show()

        vbox1.show()
        vbox2.show()
        self.window.show()


def main():
    gtk.main()
    return 0


if __name__ == "__main__":
    search_movie()
    main()
