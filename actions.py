# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message("Hello World!")
#
#         return []

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from pynput import keyboard

from os import path
import os
import stat
import subprocess

script = ""

def on_press(key):
    global script
    try:
        print('alphanumeric key {0} pressed'.format(key.char))
        #with open(file_name, "a+") as file:
        script += key.char
        #file.close()
    except AttributeError:
        print('special key {0} pressed'.format(key))
        if key == keyboard.Key.space:
            #with open(file_name, "a+") as file:
            script += " "
            #file.close()

        if key == keyboard.Key.enter:
            #with open(file_name, "a+") as file:
            script += "\n"
            #file.close()

        if key == keyboard.Key.esc:
            script += "\b"

def on_release(key):
    print('{0} released'.format(key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release
)

class ActionTrackStart(Action) :

    def name(self) :
        return 'action_track_start'

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        skill = tracker.get_slot('skill')
        print("Inititated tracking action to learn to :", skill)

        if listener.running == False :
            listener.start()        

        return []

class ActionTrackStop(Action) :

    file_name = ""

    def name(self) :
        return 'action_track_stop'

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        skill = tracker.get_slot('skill')
        print("Stopping tracking action to learn to :", skill)

        skill = skill.replace(" ", "_")
        self.file_name = "scripts/" + skill + ".sh"

        if listener.running == True :
            listener.stop()
        
        global script

        # to ignore the "done"
        script = script[:-5]
        print("Generate the script: ", script)

        # write the learnt skill into a script for future use
        with open(self.file_name, "a+") as file:
            file.write(script)
        file.close()

        st = os.stat(self.file_name)
        os.chmod(self.file_name, st.st_mode | stat.S_IEXEC)
        
        message = "Next time you ask me to 'peform " + skill.replace("_", " ") + "' I know what to do. Keep coding!"

        dispatcher.utter_message(message)

        return []

class ActionTrigger(Action):

    def name(self) -> Text:
        return "action_trigger"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        skill = tracker.get_slot('skill')
        skill_file = skill.replace(" ", "_") + ".sh"

        if path.exists("scripts/" + skill_file) :
            print("exists")
            message = "Got it! Preparing to " + skill
            dispatcher.utter_message(message)
            if os.system("sh scripts/" + skill_file) == 0 :
                status = "Executed!"
            else :
                status = "I think there was a problem in executing the skill you taught me. Please teach me the skill again!"
            dispatcher.utter_message(status)
        else :
            print("not exists")
            message = "Sorry! I haven't acquired that skill yet! Please teach me first"
            dispatcher.utter_message(message)
            
        return []