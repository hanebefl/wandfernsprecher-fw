# User interface classes for LCD160CR
# MIT License; Copyright (c) 2017 Jeffrey N. Magee
# MIT License; Copyright (c) 2025 hanebefl (https://github.com/hanebefl)

from time import ticks_ms
#from lcd160cr import LCD160CR
from logging import debug, info, warning, error


#BLACK = LCD160CR.rgb(0,0,0)
#GREY  = LCD160CR.rgb(128,128,128)
#WHITE = LCD160CR.rgb(255,255,255)
#GREEN = LCD160CR.rgb(0,255,0)
#BLUE = LCD160CR.rgb(0,0,255)
#RED   = LCD160CR.rgb(255,0,0)
#FG = WHITE
#BG = BLACK
#
#FONTHEIGHT = [5, 8, 8, 14]
#FONTWIDTH  = [4, 6, 6, 9]



# class Button:

#     def __init__(self, screen, x, y, w, h, fg, bg, label, font = 3, bold = 1):
#          self.lcd = screen.lcd
#          screen.actionable(self)
#          self.x = x
#          self.y = y
#          self.w = w
#          self.h = h
#          self.fg =fg
#          self.bg =bg
#          self.label = label
#          self.font = font
#          self.bold = bold
#          self.action = None
#          self.state = False

#     def callback(self, fn):
#         self.action =fn

#     def draw(self, pressed=False):
#         self.lcd.set_font(self.font,0,self.bold,0)
#         self.lcd.set_pos(self.x+ self.w//2 - (len(self.label)*FONTWIDTH[self.font])//2,
#                          self.y + self.h//2 -FONTHEIGHT[self.font]//2)
#         if not pressed:
#             self.lcd.set_pen(self.bg, self.bg)
#             self.lcd.set_text_color(self.fg, self.bg)
#         else:
#             self.lcd.set_pen(self.fg, self.fg)
#             self.lcd.set_text_color(self.bg, self.fg)
#         self.lcd.rect(self.x, self.y, self.w, self.h)
#         self.lcd.write(self.label)

#     def check(self,touched, x,y):
#         if touched and x > self.x and x < self.x + self.w and y > self.y and y < self.y + self.h:
#             if not self.state:
#                 self.state = True
#                 self.draw(True)
#         else:
#             if self.state:
#                 self.state = False
#                 self.draw(False)
#                 if self.action:
#                     self.action()


#     def set_background(self,color):
#         self.bg = color
#         self.draw()


# class Label:

#     def __init__(self, screen, x, y, w, h, fg, bg, label, font = 3, bold = 1, centred = True):
#          self.lcd = screen.lcd
#          screen.drawable(self)
#          self.x = x
#          self.y = y
#          self.w = w
#          self.h = h
#          self.fg =fg
#          self.bg =bg
#          self.width = w // FONTWIDTH[font]
#          self.label = label[:self.width]
#          self.font = font
#          self.bold = bold
#          self.centred = centred

#     def draw(self):
#         self.lcd.set_font(self.font,0,self.bold,0)
#         if self.centred:
#             xpos = self.x+ self.w//2 - (len(self.label)*FONTWIDTH[self.font])//2
#         else:
#             xpos = self.x
#         self.lcd.set_pos(xpos, self.y + self.h//2 -FONTHEIGHT[self.font]//2)
#         self.lcd.set_pen(self.fg, self.bg)
#         self.lcd.set_text_color(self.fg, self.bg)
#         self.lcd.rect_interior(self.x, self.y, self.w, self.h)
#         self.lcd.write(self.label)

#     def set_background(self,color):
#         self.bg = color

#     def set_text(self,txt):
#         self.label = txt[:self.width]
#         self.draw()


# class Textbox:

#     def __init__(self, screen, x, y, w, h, fg, bg, label, font = 3, bold = 1):
#         self.lcd = screen.lcd
#         screen.drawable(self)
#         self.x = x
#         self.y = y
#         self.w = w
#         self.h = h
#         self.fg =fg
#         self.bg =bg
#         self.font = font
#         self.width = w // FONTWIDTH[font]
#         self.lines = h // FONTHEIGHT[font]
#         self.label = label[:self.width]
#         self.bold = bold

#     def draw(self):
#         self.lcd.set_font(self.font,0,self.bold,0)
#         self.lcd.set_pen(self.fg, self.bg)
#         self.lcd.set_text_color(self.fg, self.bg)
#         self.lcd.rect_interior(self.x, self.y, self.w, self.h)
#         curline = 0; pos = 0
#         wlines = self.label.split('\n')
#         for ln in range(len(wlines)):
#             words = wlines[ln].split(' ')
#             for wn in range(len(words)):
#                 if pos + len(words[wn]) > self.width:
#                     pos = 0; curline = curline +1
#                     if curline >= self.lines:
#                         return
#                     while len(words[wn]) > self.width:
#                         self.lcd.set_pos(self.x, self.y+curline*8)
#                         self.lcd.write(words[wn][:self.width])
#                         words[wn] = words[wn][self.width:]
#                         curline = curline +1
#                         if curline >= self.lines:
#                             return
#                 self.lcd.set_pos(self.x + pos*FONTWIDTH[self.font], self.y+curline*FONTHEIGHT[self.font])
#                 self.lcd.write(words[wn]+' ')
#                 pos = pos + len(words[wn])+1
#             pos = 0; curline = curline +1
#             if curline >= self.lines:
#                 return

#     def set_text(self,txt):
#         self.label = txt
#         self.draw()

# class Image:

#     def __init__(self, screen, x, y, w, h, jpegimage):
#          self.lcd = screen.lcd
#          self.bg = screen.bg
#          screen.drawable(self)
#          self.x = x
#          self.y = y
#          self.w = w
#          self.h = h
#          self.jpegimage = jpegimage

#     def draw(self):
#         self.lcd.set_pos(self.x, self.y)
#         if self.jpegimage:
#             self.lcd.jpeg(self.jpegimage)
#         else:
#             self.lcd.set_pen(self.bg, self.bg)
#             self.lcd.rect(self.x, self.y, self.w, self.h)

#     def set_image(self,im):
#         self.jpegimage = im
#         self.draw()


# class SignalLevel:

#     def __init__(self, screen,level = 0):
#         screen.drawable(self)
#         self.level = level
#         self.lcd = screen.lcd
#         self.draw()

#     def set_level(self, level):
#         if level<0 or level>5:
#             return
#         if not level == self.level:
#             self.level = level
#             self.draw()

#     def draw(self):
#         for i in range(5):
#             if i+1 <= self.level:
#                 self.lcd.set_pen(WHITE, WHITE)
#             else:
#                 self.lcd.set_pen(WHITE, BLACK)
#             self.lcd.rect(i*7,0,5,5)


# class BatteryLevel:

#     def __init__(self,screen, level = 0):
#         screen.drawable(self)
#         self.level = level
#         self.lcd = screen.lcd
#         self.draw()

#     def set_level(self, level):
#         if level<0 or level>100:
#             return
#         if not level == self.level:
#             self.level = level
#             self.draw()

#     def draw(self):
#         self.lcd.set_pen(WHITE, WHITE)
#         self.lcd.rect(122,3,2,3)
#         self.lcd.set_pen(WHITE, BLACK)
#         self.lcd.rect(100,0,22,9)
#         if self.level>=5:
#             if self.level>40:
#                 self.lcd.set_pen(GREEN, GREEN)
#             else:
#                 self.lcd.set_pen(RED, RED)
#             self.lcd.rect(101,1,self.level//5,7)


# class Keys():

#     def __init__(self,screen,y):
#         screen.actionable(self)
#         self.lcd = screen.lcd
#         self.y = y
#         self.shiftlevel = 0  # 0 = lowercase, 1= uppercase, 2 = numeric
#         self.selectedkey = None
#         self.action = None
#         self.row = [['qwertyuiop','QWERTYUIOP','1234567890'],
#                     ['asdfghjkl;','ASDFGHJKL:','@#£&*()\'"_'],
#                     ['`zxcvbnm,.','~ZXCVBNM!?','%-+=/;:<>^']]

#     def set_shiftlevel(self,level):
#         if self.shiftlevel == level:
#             self.shiftlevel = 0
#         else:
#             self.shiftlevel = level
#         self.draw()

#     def callback(self, fn):
#         self.action =fn

#     def draw(self):
#         self.lcd.set_font(3)
#         for r in range(3):
#             for i in range(10):
#                 self.lcd.set_text_color(WHITE, GREY)
#                 self.lcd.set_pos(i*13,self.y+r*17)
#                 key = self.row[r][self.shiftlevel][i]
#                 if not key == self.selectedkey:
#                     self.lcd.set_text_color(WHITE, GREY)
#                 else:
#                     self.lcd.set_text_color(BLACK, WHITE)
#                 self.lcd.write(key)

#     def check(self,touched, x,y):
#         if touched and  y > self.y and y < self.y + 51:
#             rowindex = (y-self.y)//17
#             keyindex = x//13
#             if rowindex>=0 and rowindex<3 and keyindex<10:
#                 key = self.row[rowindex][self.shiftlevel][keyindex]
#                 if not key == self.selectedkey:
#                     self.selectedkey = key
#                     self.draw()
#         else:
#             if self.selectedkey:
#                 key = self.selectedkey
#                 self.selectedkey = None
#                 self.draw()
#                 if self.action:
#                     self.action(key)


# class SetLevel():

#     def __init__(self,screen, y, name, minval,maxval,val,incr=5):
#         self.val = val
#         self.minval = minval
#         self.maxval = maxval
#         self.incr = incr
#         self.name = Label(screen,0,y,50,20,FG,BG,name,2,0)
#         self.dec = Button(screen,60,y,20,20,FG,RED,'-')
#         self.value = Label(screen,80,y,28,20,FG,BG,str(val),3,0)
#         self.inc = Button(screen,108,y,20,20,FG,GREEN,'+')
#         self.inc.callback(lambda : self._increment())
#         self.dec.callback(lambda : self._decrement())
#         self.action = None

#     def callback(self, fn):
#         self.action =fn

#     def _increment(self):
#         self.val = self.val + self.incr
#         if self.val > self.maxval:
#             self.val = self.maxval
#         self.value.set_text(str(self.val))
#         if self.action:
#             self.action(self.val)

#     def _decrement(self):
#         self.val = self.val - self.incr
#         if self.val < self.minval:
#             self.val = self.minval
#         self.value.set_text(str(self.val))
#         if self.action:
#             self.action(self.val)


class Screen():

    def __init__(self, label=None):
        # self.lcd = lcd
        # self.drawlist = []
        self.label = label
        self.checklist = []
        # self.fg = fg
        # self.bg = bg
        pass

    def draw(self):
        # self.lcd.set_pen(self.fg, self.bg)
        # self.lcd.erase()
        # for d in self.drawlist:
        #     d.draw()
        pass

    def check(self, dial, gs, es):
        for c in self.checklist:
            c.check(dial, gs, es)
        pass

    def actionable(self, obj):
        # self.drawlist.append(obj)
        self.checklist.append(obj)
        pass

    def drawable(self, obj):
        # self.drawlist.append(obj)
        pass

    def __str__(self):
        return self.label


class DialScreen(Screen):

    def __init__(self, label=''):
        super().__init__(label)
        # self.win = Label(self,0,3,128,20,FG,BG,label)
        # keypad = [
        #     Button(self,48,100,30,20,FG,GREY,'0'),
        #     Button(self,8,25,30,20,FG,GREY,'1'),
        #     Button(self,48,25,30,20,FG,GREY,'2'),
        #     Button(self,88,25,30,20,FG,GREY,'3'),
        #     Button(self,8,50,30,20,FG,GREY,'4'),
        #     Button(self,48,50,30,20,FG,GREY,'5'),
        #     Button(self,88,50,30,20,FG,GREY,'6'),
        #     Button(self,8,75,30,20,FG,GREY,'7'),
        #     Button(self,48,75,30,20,FG,GREY,'8'),
        #     Button(self,88,75,30,20,FG,GREY,'9'),
        #     Button(self,8,100,30,20,FG,GREY,'*'),
        #     Button(self,88,100,30,20,FG,GREY,'#')
        # ]
        self.callstring=''
        self.dial_timeout = None
        self.dial = None
        self.gs_switch = None
        self.stop_tones_cb = None
        # for i in range(10):
        #     keypad[i].callback(lambda x='{0}'.format(i): self.keyaction(x,True))
        # keypad[10].callback(lambda x='*': self.keyaction(x,True))
        # keypad[11].callback(lambda x='#': self.keyaction(x,True))
        # self.call = Button(self,8,125,30,30,FG,GREEN,'CAL')
        # self.clr = Button(self,88,125,30,30,FG,BLUE,'DEL')
        # self.cancel = Button(self,48,125,30,30,FG,RED,'CNL')
        # self.clr.callback(lambda x=' ': self.keyaction(x,False))
        # TODO: add sonething for callbacks

        self.action = self.Action(self)

        #    pass
        # self.actionable(fn)
    
    class Action:
        def __init__(self, screen:DialScreen):
            self.gs_switch = None
            self.get_dial_timeout = screen.get_dial_timeout
            self.set_dial_timeout = screen.set_dial_timeout
            self.dial = None
            self.keyaction = screen.keyaction
            self.get_number = screen.get_number
            self.stop_tones = None
            self.start_call_cb = None
            self.cancel_call_cb = None
            self.stop_tones_cb = None
            self.es_switch = None
            self.es_pressed = None
            self.es_pressed_since = None
            self.shutdown_cb = None
            screen.actionable(self)
        def callback_call(self, fn):
            self.start_call_cb = fn
        def callback_cancel(self, fn):
            self.cancel_call_cb = fn
        def set_dial_obj(self, dial):
            self.dial = dial
        def set_gs_switch_fn(self, obj):
            self.gs_switch = obj
        def set_es_switch_fn(self, obj):
            self.es_switch = obj
        def set_stop_tones_cb(self, fn):
            self.stop_tones = fn
        def set_shutdown_cb(self, fn):
            self.shutdown_cb = fn
        def check(self, dial:bool, gs:bool, es:bool):
            #debug(f"check dialS {dial},{gs},{es}")
            if gs:
                debug(f"dialS gs")
                if self.gs_switch is not None:
                    debug(f"dialS gs: {self.gs_switch()}")
                    if self.gs_switch(): # GS placed down
                        if self.cancel_call_cb:
                            self.cancel_call_cb()
            if self.get_dial_timeout() != None:
                if ticks_ms() - self.get_dial_timeout() > 0:
                    self.set_dial_timeout(None)
                    if self.start_call_cb:
                        self.start_call_cb()
            if dial:
                if self.dial:
                    number = self.dial.getNum()
                    if number is not None:
                        self.keyaction(str(number), True)
                        self.set_dial_timeout(ticks_ms() + 3000)
                        debug(self.get_number())
                        if len(self.get_number().strip()) <= 1:
                            self.stop_tones()
            if es or self.es_pressed:
                if self.es_switch is not None:
                    if not self.es_switch():
                        if self.es_pressed_since is not None:
                            t = ticks_ms() - self.es_pressed_since
                        if not self.es_pressed:
                            self.es_pressed = True
                            self.es_pressed_since = ticks_ms()
                        elif t > 3000:
                            self.shutdown_cb()
                        else:
                            debug(f"es pressed: {t}")
                    elif self.es_pressed:
                        self.es_pressed = False
                        self.es_pressed_since = None


    def set_dial_timeout(self, timeout:int):
        self.dial_timeout = timeout

    def get_dial_timeout(self):
        return self.dial_timeout
    
    def set_gs_switch(self, gs_switch):
        self.gs_switch = gs_switch
        self.action.set_gs_switch_fn(gs_switch)
    
    def set_es_switch(self, fn):
        self.es_switch = fn
        self.action.set_es_switch_fn(fn)
    
    def set_dial(self, dial):
        self.dial = dial
        self.action.set_dial_obj(dial)
    
    def stop_tones(self, stop_tones_fn):
        self.stop_tones_cb = stop_tones_fn
        self.action.set_stop_tones_cb(stop_tones_fn)
    
    def set_shutdown_cb(self, fn):
        self.action.set_shutdown_cb(fn)

    def keyaction(self, s:str, add:bool):
        if add:
            if len(self.callstring)<13:
                self.callstring = self.callstring + s
        else:
            self.callstring = self.callstring[:len(self.callstring)-1]
        #self.win.set_text(self.callstring)

    def callback_call(self,fn):
        self.action.callback_call(fn)

    def callback_cancel(self,fn):
        self.action.callback_cancel(fn)

    def get_number(self):
        return self.callstring

    def set_number(self,x:str):
        self.callstring = x
        # self.win.set_text(self.callstring)

############################
# CallScreen():     active call
# CallScreen(True): incoming call
class CallScreen(Screen):

    def __init__(self, label = '', ans=False):
        super().__init__(label)
        self.ans = ans
        self.dial = None
        self.gs_switch = None
        self.answer_cb = None
        self.hangup_cb = None
        self.dtmf_cb = None
        # self.status = Label(self,0,10,128,20,FG,BG,label)
        # self.number = Label(self,0,50,128,20,FG,BG,'')
        # self.cancel = Button(self,29,85,70,30,FG,RED,'CANCEL')
        # self.answer = None
        # if ans:
        #     self.answer = Button(self,29,125,70,30,FG,GREEN,'ANSWER')
        # TODO: - [ ] add class and action to start end call with GS
        # TODO: - [ ] add class and action to send DTMF tones from rotary dial
        self.action = self.Action(self)
    class Action:
        def __init__(self, screen:CallScreen):
            self.ans = screen.ans
            self.gs_switch = None
            self.hangup_cb = None
            self.answer_cb = None
            self.dial = None
            self.dtmf_cb = None
            screen.actionable(self)
        def set_gs_switch_obj(self, obj):
            self.gs_switch = obj
        def set_hangup_cb(self, fn):
            self.hangup_cb = fn
        def set_answer_cb(self, fn):
            self.answer_cb = fn
        def set_dial_obj(self, obj):
            self.dial = obj
        def set_dtmf_cb(self, fn):
            self.dtmf_cb = fn
        def check(self, dial:bool, gs:bool, es:bool):
            if self.ans:
                #debug(f"check incoS {dial},{gs},{es}")
                if gs:
                    if not self.gs_switch():  # GS lifted up
                        if self.answer_cb:
                            self.answer_cb()    # swtiches to CallS
                    else:                       # GS placed down
                        if self.hangup_cb:
                            self.hangup_cb()    # switches to HomeS
                if es:
                    # TODO: maybe mute ringing?
                    pass
            else:
                #debug(f"check callS {dial},{gs},{es}")
                if gs:
                    if self.gs_switch(): # GS placed down
                        if self.hangup_cb:
                            self.hangup_cb()
                if dial:
                    if self.dial:
                        num = self.dial.getNum()
                        if self.dtmf_cb and num is not None:
                            self.dtmf_cb(str(num))

    # def set_status(self, s):
    #     self.status.set_text(s)

    # def set_number(self, s):
    #     self.number.set_text(s)



    # def callback_answer(self,fn):
    #     if self.answer:
    #         self.answer.callback(fn)
    def set_dial(self, dial):
        self.dial = dial
        self.action.set_dial_obj(dial)
    
    def set_gs_switch(self, gs_switch):
        self.gs_switch = gs_switch
        self.action.set_gs_switch_obj(gs_switch)
    
    def callback_answer(self, fn):
        self.answer_cb = fn
        self.action.set_answer_cb(fn)
    
    def callback_hangup(self, fn):
        self.hangup_cb = fn
        self.action.set_hangup_cb(fn)
    
    def dtmf(self, fn):
        self.dtmf_cb = fn
        self.action.set_dtmf_cb(fn)


class HomeScreen(Screen):

    def __init__(self, label=''):
        super().__init__(label)
        self.gs_switch = None
        self.stop_tones_cb = None

        self.set_call_cb = None
        # self.signal = SignalLevel(self,0)
        # self.battery= BatteryLevel(self,0)
        # self.network = Label(self,40,0,50,10,FG,BG,'',1)
        # self.name = Label(self,0,20,128,16,FG,BG,label)
        # self.time = Label(self,0,40,128,10,FG,BG,'')
        # self.date = Label(self,40,55,50,10,FG,BG,'',1)
        # self.smsid  = Label(self,40,70,50,10,FG,BG,'',1)
        # self.call = Button(self,0,85,30,30,FG,BLUE,'CAL')
        # self.sms = Button(self,48,85,30,30,FG,BLUE,'SMS')
        # self.app = Button(self,95,85,30,30,FG,BLUE,'APP')
        # self.book  = Button(self,0,125,30,30,FG,BLUE,'PB')
        # self.message = Button(self,48,125,30,30,FG,BLUE,'Msg')
        # self.settings  = Button(self,95,125,30,30,FG,BLUE,'Set')
        # TODO: - [ ] GS lifted -> play dial tone
        # TODO: - [ ] GS put down -> stop tones
        self.action = self.Action(self)

    class Action:
        def __init__(self, screen:HomeScreen):
            self.gs_switch = None
            self.set_call_cb = None
            self.stop_tone_cb = None
            screen.actionable(self)
        
        def check(self, dial:bool, gs:bool, es:bool):
            #debug(f"check homeS {dial},{gs},{es}")
            # dial: nothing to do
            # gs: liftoff: goto setcall
            if gs:
                debug("gs")
                if self.gs_switch is not None:
                    debug(f"gs_switch {self.gs_switch()}")
                    if self.gs_switch():
                        self.stop_tone_cb()
                        pass
                    else: # gs lifted off
                        if self.set_call_cb:
                            debug("set_call_cb()")
                            self.set_call_cb()
            # es: nothing to do.
            pass

        def set_gs_switch(self, gs_switch):
            self.gs_switch = gs_switch
        def set_callback_call(self,fn):
            self.set_call_cb = fn
        def set_stop_tone_cb(self, fn):
            self.stop_tone_cb = fn
    
    def callback_call(self,fn):
        self.set_call_cb = fn
        self.action.set_callback_call(fn)
        pass

    def set_gs_switch(self,gs_switch):
        debug(f"homeS {gs_switch()}")
        self.gs_switch = gs_switch
        self.action.set_gs_switch(gs_switch)
    
    def callback_stop_tones(self,fn):
        self.stop_tones_cb = fn
        self.action.set_stop_tone_cb(fn)

    # def callback_sms(self,fn):
    #     # self.sms.callback(fn)
    #     pass

    # def callback_app(self,fn):
    #     # self.app.callback(fn)
    #     pass

    # def callback_book(self,fn):
    #     # self.book.callback(fn)
    #     pass

    # def callback_message(self,fn):
    #     # self.message.callback(fn)
    #     pass

    # def callback_settings(self,fn):
    #     # self.settings.callback(fn)
    #     pass

    # def set_date_time(self,label):
    #     # if label:
    #     #    dt = label.split(',')
    #     #    d  = dt[0].split('/')
    #     #    t = dt[1].split(':')
    #     #    self.date.set_text(d[2]+'/'+d[1]+'/'+d[0])
    #     #    self.time.set_text(t[0]+':'+t[1])
    #     pass

    # def set_signal_level(self,val):
    #     pass
    #     #self.signal.set_level(val)

    # def set_battery_level(self,val):
    #     # self.battery.set_level(val)
    #     pass

    # def set_network(self,label):
    #     # self.network.set_text(label)
    #     pass

    # def set_smsid(self,id):
    #     # self.message.set_background(GREEN)
    #     # self.smsid.set_background(GREEN)
    #     # self.smsid.set_text('MSG {}'.format(id))
    #     pass

    # def clear_sms(self):
    #     # self.message.set_background(BLUE)
    #     # self.smsid.set_background(BG)
    #     # self.smsid.set_text('')
    #     pass

    # def clear_smsid(self):
    #     #self.message.set_background(BG)
    #     #self.smsid.set_background(BG)
    #     #self.smsid.set_text('')
    #     pass


# class PhoneBookScreen(Screen):

#     def __init__(self, label, phonebook):
#         super().__init__()
#         self.name =  Label(self,0,0,128,20,FG,BG,label)
#         self.cal  =  Button(self,8,125,30,30,FG,GREY,'C')
#         self.msg  =  Button(self,48,125,30,30,FG,GREEN,'M')
#         self.back  = Button(self,88,125,30,30,FG,BLUE,'Bk')
#         self.cal.callback(self.set_calling)
#         self.msg.callback(self.set_messaging)
#         self.CallorMsg = False # default to sms
#         self.buttons = {}
#         ystart = 20
#         for name in phonebook.keys():
#             self.buttons[name] =  Button(self,0,ystart,128,16,FG,GREY,name,2,0)
#             ystart = ystart + 15

#     def callmode(self):
#         return self.CallorMsg

#     def set_calling(self):
#         if not self.CallorMsg:
#             self.CallorMsg = True
#             self.cal.set_background(GREEN)
#             self.msg.set_background(GREY)

#     def set_messaging(self):
#         if  self.CallorMsg:
#             self.CallorMsg = False
#             self.cal.set_background(GREY)
#             self.msg.set_background(GREEN)

#     def callback_back(self,fn):
#         self.back.callback(fn)

#     def callback(self,fn):
#         for n,b in self.buttons.items():
#             b.callback(lambda x=n:fn(x))


# class SettingsScreen(Screen):

#     def __init__(self, label):
#         super().__init__()
#         self.name = Label(self,0,0,128,20,FG,BG,label)
#         self.back  = Button(self,98,125,30,30,FG,BLUE,'Bk')
#         self.checkcredit = Button(self,0,125,30,30,FG,BLUE,'CR')
#         self.memfree     = Label(self,32,141,64,14,FG,GREY,'',1,0)
#         self.credit_txt  = Label(self,32,125,64,14,FG,GREY,'',1,0)
#         self.brightness = SetLevel(self,30,"Bright",5,31,31,incr=5)
#         self.volume     = SetLevel(self,60,"Volume",0,99,33,incr=10)

#     def callback_bright(self,fn):
#         self.brightness.callback(fn)

#     def callback_volume(self,fn):
#         self.volume.callback(fn)

#     def callback_back(self,fn):
#         self.back.callback(fn)

#     def callback_checkcredit(self,fn):
#         self.checkcredit.callback(fn)

#     def set_credit(self,c):
#         self.credit_txt.set_text(c)

#     def set_memfree(self,c):
#         self.memfree.set_text(c)

# class MessageScreen(Screen):

#     def __init__(self, label):
#         super().__init__()
#         self.name = Label(self,0,0,128,16,FG,BG,label,3,0)
#         self.source = Label(self,10,20,100,8,FG,GREY,'',1,0)
#         self.time = Label(self,0,30,60,8,FG,GREY,'',1,0)
#         self.date = Label(self,64,30,60,8,FG,GREY,'',1,0)
#         self.text = Textbox(self,0,40,128,80,FG,BG,'',1,0)
#         self.delete = Button(self,0,125,20,30,FG,RED,'D')
#         self.plus  = Button(self,26,125,20,30,FG,BLUE,'+')
#         self.minus = Button(self,52,125,20,30,FG,BLUE,'-')
#         self.reply = Button(self,78,125,20,30,FG,BLUE,'R')
#         self.back  = Button(self,104,125,26,30,FG,BLUE,'Bk')
#         self.id = 1

#     def callback_plus(self,fn):
#         self.plus.callback(fn)

#     def callback_minus(self,fn):
#         self.minus.callback(fn)

#     def callback_delete(self,fn):
#         self.delete.callback(fn)

#     def callback_reply(self,fn):
#         self.reply.callback(fn)

#     def callback_back(self,fn):
#         self.back.callback(fn)

#     def set_id(self,id):
#         self.id = id
#         self.name.set_text('Message {}'.format(id))

#     def get_id(self):
#         return self.id

#     def set_message(self,msg):
#         if msg:
#             self.source.set_text(msg[0])
#             d = msg[1].split('/')
#             self.date.set_text(d[2]+'/'+d[1]+'/'+d[0])
#             time = msg[2].split('+')
#             self.time.set_text(time[0])
#             self.text.set_text(msg[3])
#         else:
#             self.source.set_text('DELETED')
#             self.date.set_text('')
#             self.time.set_text('')
#             self.text.set_text('')


# class SendsmsScreen(Screen):

#     def __init__(self, label):
#         self.msgtext =''
#         super().__init__()
#         self.send  = Button(self,0,0,30,16,FG,BLUE,'Send',1,0)
#         self.clear = Button(self,60,0,30,16,FG,BLUE,'Clr',1,0)
#         self.cancel  = Button(self,94,0,30,16,FG,BLUE,'Home',1,0)
#         self.destination = Label(self,24,20,80,8,FG,GREY,label,1,0)
#         self.text = Textbox(self,0,32,128,56,FG,BG,'',1,0)
#         self.keys = Keys(self,88)
#         self.abc  = Button(self,0,140,20,16,FG,GREY,'ABC',1,0)
#         self.numbers = Button(self,22,140,20,16,FG,GREY,'123',1,0)
#         self.spacebar = Button(self,44,140,40,16,FG,GREY,'SPACE',1,0)
#         self.delete = Button(self,86,140,20,16,FG,GREY,'del',1,0)
#         self.enter = Button(self,108,140,20,16,FG,GREY,'ret',1,0)
#         self.abc.callback(lambda x=1: self.keys.set_shiftlevel(x))
#         self.numbers.callback(lambda x=2: self.keys.set_shiftlevel(x))
#         self.keys.callback(self.addchar)
#         self.spacebar.callback(lambda x=' ':self.addchar(x))
#         self.enter.callback(lambda x='\n':self.addchar(x))
#         self.delete.callback(self.delchar)
#         self.clear.callback(self.clearall)

#     def callback_cancel(self,fn):
#         self.cancel.callback(fn)

#     def callback_send(self,fn):
#         self.send.callback(fn)

#     def set_destination(self,n):
#         self.destination.set_text(n)

#     def get_msgtext(self):
#         return self.msgtext

#     def addchar(self,ch):
#         self.msgtext += ch
#         self.text.set_text(self.msgtext)

#     def delchar(self):
#         self.msgtext = self.msgtext[:-1]
#         self.text.set_text(self.msgtext)

#     def clearall(self):
#         self.msgtext = ''
#         self.text.set_text(self.msgtext)


