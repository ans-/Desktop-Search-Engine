import wx, wx.html
from searchquery import *
from makeindex import *
import os

answer = ''
corrector = ''
suggestvalue = ''


class HtmlWindow(wx.html.HtmlWindow):
    def __init__(self, parent, id, size=(400,600)):
        wx.html.HtmlWindow.__init__(self, parent, id, size=size)
        if "gtk2" in wx.PlatformInfo:
            self.SetStandardFonts()

    def OnLinkClicked(self, link):
        wx.LaunchDefaultBrowser(link.GetHref())

class SearchBox(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "search answer",
            style = wx.CAPTION | wx.CLOSE_BOX | wx.SYSTEM_MENU | wx.THICK_FRAME | wx.RESIZE_BORDER | wx.TAB_TRAVERSAL)
        hwin = HtmlWindow(self, -1)
        global answer
        hwin.SetPage(answer)
        irep = hwin.GetInternalRepresentation()
        hwin.SetSize((irep.GetWidth()+25, irep.GetHeight()+10))
        self.SetClientSize(hwin.GetSize())
        self.CentreOnParent(wx.BOTH)
        self.SetFocus()

class myframe(wx.Frame):

    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, "My Simple GUI App.")
        self.Move((300,100))
        self.panel = wx.Panel(self, style=wx.TAB_TRAVERSAL | wx.CLIP_CHILDREN | wx.FULL_REPAINT_ON_RESIZE)

        self.text = wx.TextCtrl(self.panel, -1, pos = (10,10), size=(300,-1))
        self.text1 = wx.TextCtrl(self.panel, -1, pos=(10,40), size = (100, -1))
        self.text1.Enable(False)
        self.buttonsearch = wx.Button(self.panel, label = 'search', pos=(310, 10), size=(55, -1))

        self.radio4 = wx.RadioButton(self.panel, -1, "TF-IDF", pos=(10, 110), style=wx.RB_GROUP)
        self.radio5 = wx.RadioButton(self.panel, -1, "BM25F", pos=(110, 110))
        self.radio6 = wx.RadioButton(self.panel, -1, "Frequency", pos=(210, 110))


        self.radio7 = wx.RadioButton(self.panel, -1, "OR", pos=(10, 140), style=wx.RB_GROUP)
        self.radio8 = wx.RadioButton(self.panel, -1, "AND", pos=(110,140))


        self.checkbox1 = wx.CheckBox(self.panel, -1, "pdf", pos=(10,80))
        self.checkbox2 = wx.CheckBox(self.panel, -1, "doc", pos=(60,80))
        self.checkbox3 = wx.CheckBox(self.panel, -1, "txt", pos=(110,80))
        self.checkbox4 = wx.CheckBox(self.panel, -1, "other", pos=(160,80))


        self.radio9 = wx.RadioButton(self.panel, -1, "Nothing", pos = (10,170), style=wx.RB_GROUP)
        self.radio10 = wx.RadioButton(self.panel, -1, "MajorClust", pos = (110, 170))



        self.text_dir = wx.TextCtrl(self.panel, -1, pos= (10, 240), size = (300,-1))
        self.buttonindex = wx.Button(self.panel, label = "index", pos=(310,240), size = (55,-1))
        self.radio1 = wx.RadioButton(self.panel, -1, "Standard", pos=(10, 270), style=wx.RB_GROUP)
        self.radio2 = wx.RadioButton(self.panel, -1, "Stemming", pos=(110, 270))
        self.radio3 = wx.RadioButton(self.panel, -1, "4-gram", pos=(210, 270))

        self.static_box = wx.StaticText(self.panel, -1, "Create file index, please enter your dir name:", pos = (10, 210))
        self.static_line = wx.StaticLine(self.panel, pos=(0,200),size=(400,5),style=wx.LI_HORIZONTAL)
        self.static_line1 = wx.StaticLine(self.panel, pos=(0,70),size=(400,5),style=wx.LI_HORIZONTAL)

        self.static_text1 = wx.StaticText(self.panel,-1, label=':suggest',pos=(310,43))
        self.static_text2 = wx.StaticText(self.panel,-1, label=':scores',pos=(310,110))
        self.static_text3 = wx.StaticText(self.panel,-1, label=':and/or?',pos=(310,140))
        self.static_text4 = wx.StaticText(self.panel,-1, label=':file type',pos=(310,80))
        self.static_text5 = wx.StaticText(self.panel, -1, label=':index type',pos=(310,270))
        self.static_text6 = wx.StaticText(self.panel, -1, label=':clustering', pos=(310,170))
        self.static_text7 = wx.StaticText(self.panel, -1, label='Did you mean :', pos=(10, 45))

        self.buttonhide = wx.Button(self.panel, pos=(370,10), size=(20,-1))
        self.isShown = False
        self.buttonhide.SetLabel(u'+')

        self.suggestbotton = wx.Button(self.panel, -1, pos = (110,40), size=(150,-1),style=wx.NO_BORDER)


        ###
        self.text1.Hide()
        self.text_dir.Hide()
        self.radio4.Hide()
        self.radio5.Hide()
        self.radio6.Hide()
        self.radio7.Hide()
        self.radio8.Hide()
        self.checkbox1.Hide()
        self.checkbox2.Hide()
        self.checkbox3.Hide()
        self.checkbox4.Hide()
        self.buttonindex.Hide()
        self.radio1.Hide()
        self.radio2.Hide()
        self.radio3.Hide()
        self.radio9.Hide()
        self.radio10.Hide()
        self.suggestbotton.Hide()

        self.static_text1.Hide()
        self.static_text2.Hide()
        self.static_text3.Hide()
        self.static_text4.Hide()
        self.static_box.Hide()
        self.static_text5.Hide()
        self.static_text6.Hide()
        self.static_text7.Hide()
        self.static_line.Hide()
        self.static_line1.Hide()
        self.SetClientSize((400,50))
        ###
        self.Bind(wx.EVT_BUTTON, self.search, self.buttonsearch)
        self.Bind(wx.EVT_BUTTON, self.index, self.buttonindex)
        self.Bind(wx.EVT_BUTTON, self.touch, self.buttonhide)

    def touch(self, event):
        if self.isShown:
            self.buttonhide.SetLabel(u'+')
            self.text1.Hide()
            self.text_dir.Hide()
            self.radio4.Hide()
            self.radio5.Hide()
            self.radio6.Hide()
            self.radio7.Hide()
            self.radio8.Hide()
            self.checkbox1.Hide()
            self.checkbox2.Hide()
            self.checkbox3.Hide()
            self.checkbox4.Hide()
            self.buttonindex.Hide()
            self.radio1.Hide()
            self.radio2.Hide()
            self.radio3.Hide()
            self.radio9.Hide()
            self.radio10.Hide()
            self.suggestbotton.Hide()
            self.static_text1.Hide()
            self.static_text2.Hide()
            self.static_text3.Hide()
            self.static_text4.Hide()
            self.static_text7.Hide()
            self.static_box.Hide()
            self.static_text5.Hide()
            self.static_text6.Hide()
            self.static_line.Hide()
            self.static_line1.Hide()
            self.isShown = False
            self.SetClientSize((400,50))
        else:
            self.text1.Hide()
            self.text_dir.Show()
            self.radio4.Show()
            self.radio5.Show()
            self.radio6.Show()
            self.radio7.Show()
            self.radio8.Show()
            self.checkbox1.Show()
            self.checkbox2.Show()
            self.checkbox3.Show()
            self.checkbox4.Show()
            self.buttonindex.Show()
            self.radio1.Show()
            self.radio2.Show()
            self.radio3.Show()
            self.radio9.Show()
            self.radio10.Show()
            self.suggestbotton.Show()
            self.static_text1.Show()
            self.static_text2.Show()
            self.static_text3.Show()
            self.static_text4.Show()
            self.static_box.Show()
            self.static_text5.Show()
            self.static_text6.Show()
            self.static_text7.Show()
            self.static_line.Show()
            self.static_line1.Show()
            self.buttonhide.SetLabel(u'*')
            dirname = os.environ['HOME']
            self.text_dir.SetValue(dirname + '/Desktop')
            self.isShown = True
            self.SetClientSize((400,305))

    def search(self, event):
        l = self.text.GetValue()
        self.text1.Clear()
        self.do_search(l)


    def searchsuggest(self, event):
        l = self.text1.GetValue()
        self.text1.Clear()
        self.do_search(l)

    def do_search(self, l):
        global answer,corrector, suggestvalue
        answer = ''
        corrector = ''
        suggestvalue = ''
        if self.radio6.GetValue():
            score_method = 'Frequency'
        elif self.radio5.GetValue():
            score_method = 'BM25F'
        else:
            score_method = 'TF_IDF'

        if self.radio8.GetValue():
            and_or = 'AND'
        else:
            and_or = 'OR'

        if self.radio9.GetValue():
            clustering_not = 'no'
        else:
            clustering_not = 'majorclust'

        filetypelist = []
        if self.checkbox1.GetValue():
            filetypelist.append('pdf')
        if self.checkbox2.GetValue():
            filetypelist.append('doc')
        if self.checkbox3.GetValue():
            filetypelist.append('txt')
        if self.checkbox4.GetValue():
            filetypelist.append('@_@')
        if not check_all_stop_words(l):
            box = wx.MessageDialog(None, 'STOP WORDS! NO information! please re-type!', 'stop words', wx.OK)
            if box.ShowModal() == wx.ID_OK:
                box.Destroy()
            self.text.Clear()
        else:
            a, b = searchfile(l, score_method, and_or, filetypelist, clustering_not)
            answer += a
            corrector += b
            if len(corrector) > 0:
                self.text1.write('Did you mean: ')
                self.suggestbotton.SetLabel(corrector)
                suggestvalue = corrector
                if len(suggestvalue) > 0:
                    self.text1.SetValue(corrector)
                    self.Bind(wx.EVT_BUTTON, self.searchsuggest, self.suggestbotton)
            dlg = SearchBox()
            dlg.Show()
 
    def index(self, event):
        l = self.text_dir.GetValue()
        if self.radio3.GetValue():
            analyser = '4-gram'
        elif self.radio2.GetValue():
            analyser = 'Stemming'
        else:
            analyser = 'Standard'
        xxx = make_index(l, analyser)
        if xxx:
            box1 = wx.MessageDialog(None, 'Finish making index!', 'finish', wx.OK)
            if box1.ShowModal() == wx.ID_OK:
                box1.Destroy()
        if not xxx:
            box2 = wx.MessageDialog(None, 'The dir does not exist!', 'wrong', wx.OK)
            if box2.ShowModal() == wx.ID_OK:
                box2.Destroy()

if __name__=='__main__':
    app = wx.PySimpleApp()
    frame = myframe(None, -1)
    frame.Show()
    app.MainLoop()
