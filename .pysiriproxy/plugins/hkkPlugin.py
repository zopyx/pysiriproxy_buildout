# -*- coding: utf-8 -*-

from pysiriproxy.objects import Buttons, ObjectFactory
from pysiriproxy.plugins import BasePlugin, From_Server, From_iPhone, \
    SpeechPacket, StartRequest, matches, regex, ResponseList

from pyamp.logging import Colors

import requests


class Plugin(BasePlugin):
    """ HKK 33 Siri plugin """

    name = "HKK-Plugin"
    logColor = Colors.Foreground.Cyan

    commands = {
        u'verstärker ein': 'PutVolumeMute/off',
        u'verstärker aus': 'PutVolumeMute/on',
        u'sr2': 'PutZone_InputFunction/FAVORITE1',
        u'swr2': 'PutZone_InputFunction/FAVORITE2',
        u'swr3': 'PutZone_InputFunction/FAVORITE3',
        u'lautstärke 2' : 'PutMasterVolumeSet/-55.0',
        u'lautstärke 3' : 'PutMasterVolumeSet/-50.0',
        u'lautstärke 4' : 'PutMasterVolumeSet/-45.0',
        u'lautstärke 5' : 'PutMasterVolumeSet/-40.0',
        u'lautstärke 6' : 'PutMasterVolumeSet/-35.0',
        u'lautstärke 7' : 'PutMasterVolumeSet/-30.0',
    }

    def execute(self, cmd):
        cmd = unicode(cmd, 'utf-8')
        if cmd in self.commands:
            params = dict(cmd0=self.commands[cmd], cmd1='aspMainZone_WebUpdateStatus/')
            requests.get('http://192.168.0.128/MainZone/index.put.asp', params=params)
            return True
        return False

    @matches('Verstärker')
    @regex("Verstärker .*")
    def Amplifier(self, text):
        """ Amplifier on/off """
    
        if 'ein' in text:
            self.say("Verstärker wurde eingeschaltet")
            self.execute('verstärker ein')
        elif 'aus' in text:
            self.say("Verstärker wurde ausgeschaltet")
            self.execute('verstärker aus')
        else:
            responses = ['ein', 'einschalten', 'aus', 'ausschalten']
            question = 'Soll ich den Verstärker ein- oder ausschalten?'
            unknown = 'Wie bitte?'

            response = yield ResponseList(responses, question, unknown)
            if response == 'ein' or response == 'einschalten':
                self.say("Verstärker eingeschaltet")
                self.execute('verstärker ein')
            elif response == 'aus' or response == 'ausschalten':
                self.say("Verstärker ausgeschaltet")
                self.execute('verstärker aus')

        self.completeRequest()

    # Callback for buttons

    def radio_sr2(self, obj):
        self.say("Du hörst SR 2")
        self.execute('sr2')
        self.completeRequest()

    def radio_swr2(self, obj):
        self.say("Du hörst SWR 2")
        self.execute('swr2')
        self.completeRequest()

    def radio_swr3(self, obj):
        self.say("Du hörst SWR 2")
        self.execute('swr3')
        self.completeRequest()

    customCommandMap = {
        "SR2": "radio_sr2",
        "SWR2": "radio_swr2",
        "SWR3": "radio_swr3"
        }

    __buttonList = [
        ("SR 2", "SR2"),
        ("SWR 2", "SWR2"),
        ("SWR 3", "SWR3")
        ]

    @matches('radio')
    def radio(self, text):

        def createCustomButtons():
            '''Create a list of buttons that perform custom commands.'''
            buttons = []

            # Create buttons to execute custom commands for each of the
            # buttons in the list of buttons
            for buttonText, command in self.__buttonList:
                button = ObjectFactory.button(Buttons.Custom, 
                                              buttonText,
                                              command)
                buttons.append(button)
            return buttons

        buttons = createCustomButtons()
        utterance = ObjectFactory.utterance("Welche Station willst du hören?")
        self.makeView([utterance] + buttons)
        self.completeRequest()
