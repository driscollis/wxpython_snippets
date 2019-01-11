import eyed3
import glob
import wx

class EditDialog(wx.Dialog):
    
    def __init__(self, mp3):
        title = 'Editing "{title}"'.format(title=mp3.tag.title)
        super().__init__(parent=None, title=title)

class Mp3Panel(wx.Panel):
    
    def __init__(self, parent):
        super().__init__(parent)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.row_obj_dict = {}
        
        self.list_ctrl = wx.ListCtrl(self, size=(-1,100),
                                     style=wx.LC_REPORT
                                     |wx.BORDER_SUNKEN
                                     )
        self.list_ctrl.InsertColumn(0, 'Artist', width=140)
        self.list_ctrl.InsertColumn(1, 'Album', width=140)
        self.list_ctrl.InsertColumn(2, 'Title', width=200)
        self.list_ctrl.InsertColumn(3, 'Year', width=200)
        main_sizer.Add(self.list_ctrl, 0, wx.ALL|wx.EXPAND, 5)
        
        edit_button = wx.Button(self, label='Edit')
        edit_button.Bind(wx.EVT_BUTTON, self.on_edit)
        main_sizer.Add(edit_button, 0, wx.ALL|wx.CENTER, 5)
        
        self.SetSizer(main_sizer)
        
    def on_edit(self, event):
        selection = self.list_ctrl.GetFocusedItem()
        if selection >= 0:
            mp3 = self.row_obj_dict[selection]
            dlg = EditDialog(mp3)
            dlg.ShowModal()
            dlg.Destroy()
        
    def update_mp3_listing(self, folder_path):
        self.list_ctrl.ClearAll()
        
        self.list_ctrl.InsertColumn(0, 'Artist', width=140)
        self.list_ctrl.InsertColumn(1, 'Album', width=140)
        self.list_ctrl.InsertColumn(2, 'Title', width=200)
        self.list_ctrl.InsertColumn(3, 'Year', width=200)
        
        mp3s = glob.glob(folder_path + '/*.mp3')
        mp3_objects = []
        index = 0
        for mp3 in mp3s:
            mp3_object = eyed3.load(mp3)
            self.list_ctrl.InsertItem(
                index, mp3_object.tag.artist)
            self.list_ctrl.SetItem(index, 1, mp3_object.tag.album)
            self.list_ctrl.SetItem(index, 2, mp3_object.tag.title)
            mp3_objects.append(mp3_object)
            self.row_obj_dict[index] = mp3_object
            index += 1
        
        
class Mp3Frame(wx.Frame):
    
    def __init__(self):
        super().__init__(parent=None, title='Mp3 Tag Editor')
        self.panel = Mp3Panel(self)
        self.create_menu()
        self.Show()
        
    def create_menu(self):
        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        open_folder_menu_item = file_menu.Append(
            wx.NewId(), 'Open Folder', 'Open a folder with MP3s'
        )
        menu_bar.Append(file_menu, '&File')
        self.Bind(wx.EVT_MENU, self.on_open_folder, 
                  open_folder_menu_item)
        self.SetMenuBar(menu_bar)
        
    def on_open_folder(self, event):
        dlg = wx.DirDialog(self, "Choose a directory:",
                           style=wx.DD_DEFAULT_STYLE,
                           )
        if dlg.ShowModal() == wx.ID_OK:
            self.panel.update_mp3_listing(dlg.GetPath())
        dlg.Destroy()
        
if __name__ == '__main__':
    app = wx.App(False)
    frame = Mp3Frame()
    app.MainLoop()
