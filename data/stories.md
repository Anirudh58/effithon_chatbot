## happy path
* greet
  - utter_greet
* mood_great
  - utter_happy

## sad path 1
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* affirm
  - utter_happy

## sad path 2
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* deny
  - utter_goodbye

## say goodbye
* goodbye
  - utter_goodbye

## tracking path start
* track
  - utter_track
  - action_track_start

## tracking path end
* over
  - utter_over
  - action_track_stop

## interactive_story_1
* greet
    - utter_greet
* mood_great
    - utter_happy
* track{"skill": "run logs"}
    - slot{"skill": "run logs"}
    - utter_track
    - action_track_start
* over
    - utter_over
    - action_track_stop
* track{"skill": "play app"}
    - slot{"skill": "play app"}
    - utter_track
    - action_track_start
* over
    - utter_over
    - action_track_stop


## interactive_story_1
* track{"skill": "run watch logs"}
    - slot{"skill": "run watch logs"}
    - utter_track
    - action_track_start
* over
    - utter_over
    - action_track_stop
* track{"skill": "configure server"}
    - slot{"skill": "configure server"}
    - utter_track
    - action_track_start
* over
    - utter_over
    - action_track_stop
