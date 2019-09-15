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

    file_name = "scripts/"

    def name(self) :
        return 'action_track_stop'

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        skill = tracker.get_slot('skill')
        print("Stopping tracking action to learn to :", skill)

        skill = skill.replace(" ", "_")
        self.file_name = self.file_name + skill + ".sh"

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
        
        message = "Next time you ask me to '" + skill.replace("_", " ") + "' I know what to do. Keep coding!"

        dispatcher.utter_message(message)

        return []