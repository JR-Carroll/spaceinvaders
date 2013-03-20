import wx
import random

MAX_INVADERS = 10
INVADERS_COLORS = ["yellow_invader",
                   "green_invader",
                   "blue_invader",
                   "red_invader"]


class SpaceFrame(wx.Frame):
    def __init__(self):
        """
        The generic subclassed Frame/"space" window.  All of the invaders fall
        into this frame.  All animation happens here as the parent window
        as well.
        """
        wx.Frame.__init__(self, None, wx.ID_ANY, "Space Invaders", pos=(0, 0))
        self.SetFocus()
        self.Bind(wx.EVT_MOTION, self.mouseMovement)
        self.Bind(wx.EVT_CHAR_HOOK, self.keyboardMovement)
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour('black')
        self.SetBackgroundColour('black')
        self.monitorSize = wx.GetDisplaySize()
        for invader in range(0, MAX_INVADERS, 1):
            randX = random.randint(0, self.monitorSize[0])
            self.showInvader(coords=(randX, 0),
                             invader=random.choice(INVADERS_COLORS),
                             scale=(random.randint(2, 10)/100.0))

    def mouseMovement(self, event, *args):
        print self.FindFocus()

    def keyboardMovement(self, event, *args):
        self.Destroy()

    def showInvader(self, coords=(0, 0), invader="green_invader", scale=.05):
        """
        Displays an invader on the screen
        """
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.dropInvader, self.timer)
        self.timer.Start(1000)
        self.invader = wx.Bitmap("{0}.png".format(invader))
        self.invader = wx.ImageFromBitmap(self.invader)
        self.invader = self.invader.Scale((self.invader.GetWidth()*scale),
                                          (self.invader.GetHeight()*scale),
                                          wx.IMAGE_QUALITY_HIGH)
        self.result = wx.BitmapFromImage(self.invader)
        self.control = wx.StaticBitmap(self, -1, self.result)
        self.control.SetPosition(coords)
        self.panel.Show(True)

    def moveInvader(self, coords):
        self.control.SetPosition(coords)

    def dropInvader(self, *args):
        # print "this hit"
        self.control.SetPosition((100, 600))

if __name__ == "__main__":
    application = wx.PySimpleApp()
    window = SpaceFrame()
    window.ShowFullScreen(True, style=wx.FULLSCREEN_ALL)
    application.MainLoop()
