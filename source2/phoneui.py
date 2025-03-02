# MIT License; Copyright (c) 2017 Jeffrey N. Magee
# MIT License; Copyright (c) 2025 hanebefl (https://github.com/hanebefl)

"""
Combines User Interface with SIM800L module.
"""

import sim800l
import gc
from time import sleep_ms
from machine import Pin, SLEEP, DEEPSLEEP, Timer, deepsleep, idle
from pinout import pinout
from dial import Dial

from  ui import DialScreen, CallScreen, HomeScreen

from logging import debug, info, warning, error

#import esp32

# lcd = lcd160cr.LCD160CR('Y')
# lcd.set_orient(lcd160cr.PORTRAIT)

dialS = DialScreen(label='dialS')
callS = CallScreen(label='callS')
incomingS = CallScreen(ans=True, label='incomingS')
homeS = HomeScreen(label='homeS')

phone = sim800l.SIM800L(1)

current = homeS
count = 300
# period = 0
# bright_level = 31
volume_level = 33
# new_sms = False


def do_gs_switch(t):
    global wokenby
    wokenby = 1

def w(t):
    global wokenby
    wokenby = 2

# wakebutton = pyb.ExtInt('X12', pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, do_wakebutton)
# phonering = pyb.ExtInt('X5', pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, do_phonering)
gs_switch = Pin(pinout["GS"], mode=Pin.IN, pull=Pin.PULL_UP)
wb_irq     = gs_switch.irq(do_gs_switch, Pin.IRQ_FALLING, wake=SLEEP|DEEPSLEEP)
#esp32.wake_on_gpio(pin=gs_switch, level=esp32.WAKE_ANY_LOW)
gs_switch_hist = gs_switch.value()
gs_switch_value = None
def get_gs_value() -> int:
    global gs_switch_value
    return gs_switch_value

phonering  = Pin(pinout["ES1"], mode=Pin.IN, pull=Pin.PULL_UP)
ring_irq   = phonering.irq(do_phonering, Pin.IRQ_FALLING, wake=SLEEP|DEEPSLEEP)
#esp32.wake_on_gpio(pin=phonering, level=esp32.WAKEUP_ANY_LOW)

es_button = Pin(pinout["ES2"], mode=Pin.IN, pull=Pin.PULL_UP)
es_button_hist = es_button.value()
es_button_value = None
def get_es_value() -> int:
    global es_button_value
    return es_button_value

dial = Dial(pinout["NSA"], pinout["NSI"])

hv_en = Pin(pinout["HV_EN"], Pin.OUT)
hv_en.off()
bell_a = Pin(pinout["BELL_A"], Pin.OUT)
bell_a.off()
bell_b = Pin(pinout["BELL_B"], Pin.OUT)
bell_b.off()

def toggle_bell(timer):
    if bell_a.value():
        bell_a.off()
        bell_b.on()
    else:
        bell_b.off()
        bell_a.on()

bell_timer = Timer(0)
bell_timer2 = Timer(-1)

def ring_bells():
    debug("RING")
    if not hv_en.value():
        hv_en.on()
        sleep_ms(20)
        bell_timer.init(freq=20*2, mode=Timer.PERIODIC, callback=toggle_bell)
        bell_timer2.init(period=1500, mode=Timer.ONE_SHOT, callback=mute_bells)

def mute_bells(timer):
    debug("RING_OFF")
    if hv_en.value():
        bell_timer.deinit()
        hv_en.off()

def switch_to(screen):
    global current #, period
    info(str(screen))
    current = screen
    current.draw()
    # if current == homeS:
    #     period = 145

def docall():
    switch_to(callS)
    #callS.set_number(dialS.get_number())
    phone.call(dialS.get_number())

# msg_destination = ''

# def dosms():
#     global msg_destination
#     switch_to(sendsms)
#     msg_destination = dial.get_number()
#     sendsms.set_destination(msg_destination)

# def dosendsms():
#     sendsms.set_destination('  SENDING')
#     result = phone.send_sms(msg_destination, sendsms.get_msgtext())
#     sendsms.set_destination(result)

def set_call():
    dialS.callback_call(docall)
    dial.clear()
    if phone.online():
        phone.play_dial_tone()
    else:
        phone.play_tone(2)
    switch_to(dialS)

# def set_sms():
#     dial.callback_call(dosms)
#     switch_to(dial)


def incomingcall():
    switch_to(incomingS)
    ring_bells()
    clear_phone_sleep_mode()

#def phonebookcall(name):
#    global msg_destination
#    if book.callmode():
#        switch_to(callS)
#        callS.set_number(name)
#        phone.call(phonebook[name])
#    else:
#        switch_to(sendsms)
#        msg_destination = phonebook[name]
#        sendsms.set_destination(name)

def incomingclip():
    # global inverted_pb, national_pb
    # if current == incomingS:
    #     nn = phone.get_clip()
    #     if nn in inverted_pb:
    #         nn = inverted_pb[nn]
    #     elif nn in national_pb:
    #         nn = national_pb[nn]
    #     incomingS.set_number(nn)
    pass

def no_carrier():
    mute_bells(None)
    switch_to(homeS)
    if not get_gs_value():
        phone.play_tone(1)
    clear_phone_sleep_mode()

def docancel():
    dialS.set_number(' ')
    dialS.set_dial_timeout(None)
    #dial.clear()
    phone.stop_tones()
    switch_to(homeS)

def cancelcall():
    dialS.set_number(' ')
    #dial.clear()
    switch_to(homeS)
    phone.hangup()
    phone.stop_tones()

def answercall():
    mute_bells(None)
    switch_to(callS)
    phone.answer()

def play_dtmf(num: str):
    phone.dtmf(num)

# def set_brightness(level):
#     global bright_level
#     bright_level = level
#     lcd.set_brightness(bright_level)

def set_volume(level):
    global volume_level
    volume_level = level
    phone.set_volume(volume_level)

def stop_phone_tones():
    phone.hangup()
    phone.stop_tones()
# def incoming_sms():
#     global new_sms
#     switch_to(home)
#     clear_phone_sleep_mode()
#     id = phone.get_msgid()
#     home.set_smsid(id)
#     new_sms = True
#     phone.sms_alert()

# def display_msg(id):
#     global msg_destination, inverted_pb
#     current_msg = phone.read_sms(id)
#     if current_msg:
#         msg_destination = current_msg[0]
#         if msg_destination in inverted_pb:
#             current_msg[0] = inverted_pb[msg_destination]
#         messages.set_message(current_msg)
#     else:
#         msg_destination = ''
#         messages.set_message(None)
#     messages.set_id(id)

# def do_messages():
#     global new_sms
#     home.clear_sms()
#     switch_to(messages)
#     if new_sms:
#         id = phone.get_msgid()
#         new_sms =False
#     else:
#         id = messages.get_id()
#     display_msg(id)

# def do_msg_plus():
#     id = messages.get_id();
#     if id<65:
#         id = id+1
#         display_msg(id)

# def do_msg_minus():
#     id = messages.get_id();
#     if id>1:
#         id = id-1
#         display_msg(id)

# def do_msg_reply():
#     global msg_destination
#     if not msg_destination == '':
#         switch_to(sendsms)
#         sendsms.set_destination(msg_destination)

# def do_msg_delete():
#     id = messages.get_id()
#     phone.delete_sms(id)
#     display_msg(id)


# hasnetname = False
# def update():
#     global period
#     global hasnetname
#     # homeS.set_date_time(phone.date_time())
#     # homeS.set_signal_level(phone.signal_strength())
#     # homeS.set_battery_level(phone.battery_charge())
#     # if not hasnetname:
#     #     ns = phone.network_name()
#     #     if not ns == '':
#     #         homeS.set_network(ns)
#     #         hasnetname = True

# def check_credit():
#     phone.check_credit()
#     settings.set_credit('Checking..')

# def set_credit():
#     switch_to(settings)
#     settings.set_credit(phone.get_credit())

# def dosettings():
#     switch_to(settings)
#     settings.set_memfree(str(gc.mem_free()))

wokenby = 0

def clear_phone_sleep_mode():
    global wokenby
    if wokenby == 2:
        phone.wakechars()
        phone.sleep(0)
        wokenby = 0


def shutdown():
    phone.play_tone(4)
    phone.shutdown()
    deepsleep()



dialS.callback_cancel(docancel)
# dialS.callback_call(docall) done while switching
dialS.set_gs_switch(get_gs_value)
dialS.set_dial(dial)
dialS.stop_tones(stop_phone_tones)
dialS.set_shutdown_cb(shutdown)
dialS.set_es_switch(get_es_value)
callS.callback_hangup(cancelcall)
callS.set_gs_switch(get_gs_value)
callS.set_dial(dial)
callS.dtmf(play_dtmf)
homeS.callback_call(set_call)
homeS.set_gs_switch(get_gs_value)
homeS.callback_stop_tones(stop_phone_tones)
# homeS.callback_sms(set_sms)
#homeS.callback_app(lambda x=applications: switch_to(x))
#homeS.callback_book(lambda x=book: switch_to(x))
#homeS.callback_message(do_messages)
#homeS.callback_settings(dosettings)
phone.callback_incoming(incomingcall)
phone.callback_no_carrier(no_carrier)
phone.callback_clip(incomingclip)
# phone.callback_msg(incoming_sms)
#phone.callback_credit_action(set_credit)
incomingS.callback_answer(answercall)
incomingS.callback_hangup(cancelcall)
incomingS.set_gs_switch(get_gs_value)

current.draw()
#phone.set_pin("2538")
sleep_ms(1000) # wait for phone to be ready
while not phone.ready():
    sleep_ms(250)
sleep_ms(1000)
phone.setup()
phone.set_volume(volume_level)

while not phone.enter_pin("2538"):
    sleep_ms(250)

info(str(current))
while True:
    phone.check_incoming()
    try:
        # TODO: - [ ] get interface inputs:
        # TODO:   - [ ] Dial input
        d = dial.run()
        # TODO:   - [ ] Headset input
        gs_switch_value = gs_switch.value()
        gs = gs_switch_value != gs_switch_hist
        gs_switch_hist = gs_switch_value
        # TODO:   - [ ] Button input
        es_button_value = es_button.value()
        es = es_button_value != es_button_hist
        es_button_hist = es_button_value

        #t,x,y = lcd.get_touch()

        current.check(d, gs, es)
        #current.check(t,x,y)
        # if period == 0:
        #     if current==homeS:
        #         update()
        # period =  (period + 1) % 150
        if d or gs or es:
            count = 300 # delay for sleep mode
        else:
            count = count - 1
            if count<=0 and not current == incomingS and not current == callS:
                #sleep
                #lcd.set_power(0)
                phone.sleep(2)
                # if not usb.isconnected():
                #     #pyb.stop()     # wait for button or incoming call
                #     pass
                #else:
                wokenby = 0
                while wokenby == 0:
                    idle()
                #wakeup
                count = 300
                # period = 145
                if wokenby ==1:
                    phone.wakechars()
                    phone.sleep(0)
                    current.draw()
                    wokenby==0
    except OSError:
        print('Error')
        t = False
    sleep_ms(100)


 