# -*- coding: utf-8 -*-
# Copyright 2012 Brett Ponsler
# This file is part of pysiriproxy.
#
# pysiriproxy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pysiriproxy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pysiriproxy.  If not, see <http://www.gnu.org/licenses/>.
'''The testPlugin module contains the definition of the Test-Plugin.

This plugin gives examples of controlling Siri's responses to the user
in various ways, such as: responding with text, asking a question, and
waiting for the user to give a specific answer.

'''
from pysiriproxy.objects import Buttons, ObjectFactory
from pysiriproxy.plugins import BasePlugin, From_Server, From_iPhone, \
    SpeechPacket, StartRequest, matches, regex, ResponseList

from pyamp.logging import Colors

import requests

def execute(cmd):
    cmd = unicode(cmd, 'utf-8')
    if cmd in COMMANDS:
        params = dict(cmd0=COMMANDS[cmd], cmd1='aspMainZone_WebUpdateStatus/')
        requests.get('http://192.168.0.128/MainZone/index.put.asp', params=params)
        return True
    return False

COMMANDS = {
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


class Plugin(BasePlugin):
    '''This plugin contains examples of creating object filters, and
    speech rules in order to control Siri's responses to the user.

    '''
    # Define the name and log color for this plugin
    name = "HKK-Plugin"
    logColor = Colors.Foreground.Cyan

    ##### Define all of the filters for this plugin. #####

    @From_Server
    def filterServer(self, obj, direction):
        '''Example of a directional filter for objects from Apple's
        web server.
        
        * obj -- The received object
        * direction -- The direction of the received data

        '''
        return obj

    @SpeechPacket
    def filterSpeech(self, obj, direction):
        '''Example of a class filter for a speech packet.
        
        * obj -- The received object
        * direction -- The direction of the received data

        '''
        return obj

    ##### Define all of the speech rules for this plugin. #####

    @regex("Verstärker ein.*")
    def AmplifierOn(self, text):
        """ Test """
        execute('verstärker ein')
        self.say("Verstärker wurde eingeschaltet")
        self.completeRequest()

    @regex("Verstärker aus.*")
    def AmplifierAus(self, text):
        """ Test """
        execute('verstärker aus')
        self.say("Verstärker wurde ausgeschaltet")
        self.completeRequest()

    @matches("radio station eins")
    @matches("radio sr zwei")
    @regex("saarl.* zwei")
    def sr2(self, text):
        """ Test """
        execute('sr2')
        self.say("Viel Spaß mit Roland Kunz")
        self.completeRequest()

    @matches("radio station zwei")
    @matches("radio swr zwei")
    @regex("süd.* zwei")
    def swr2(self, text):
        """ Test """
        execute('swr2')
        self.say("Schwabenklassik eingeschaltet")
        self.completeRequest()

    @matches("radio station drei")
    @matches("radio swr drei")
    @regex("süd.* drei")
    def swr3(self, text):
        """ Test """
        execute('swr3')
        self.say("Willst Du den Radau wirklich hören?")
        self.completeRequest()

    @matches("verstärker")
    def AmplifierOnOff(self, text):
        responses = ['ein', 'aus']
        question = 'Soll ich den Verstärker ein- oder ausschalten?'
        unknown = 'Wie bitte?'

        response = yield ResponseList(responses, question, unknown)
        if response == 'ein':
            self.say("Verstärker eingeschaltet")
            execute('verstärker ein')
        elif response == 'aus':
            self.say("Verstärker ausgeschaltet")
            execute('verstärker aus')
        self.completeRequest()

    @matches("radio")
    def confirmTest(self, text):
        responses = ["roland kunz", "klassik aus stuttgart", "pop musik"]
        question = "Welche Station willst du hören?"
        unknown = "Wie bitte?"

        response = yield ResponseList(responses, question, unknown)
        print response
        if response == 'roland kunz':
            execute('sr2')
            self.say("Du hörst SR 2")
        elif response == 'klassik aus stuttgart':
            execute('swr2')
            self.say("Du hörst SWR 2")
        elif response == 'pop musik':
            execute('swr3')
            self.say("Du hörst SWR 3")

        self.completeRequest()
