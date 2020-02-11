from typing import Dict, Text, Any, List, Union, Optional

from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk import Action


##class BookHotel (Action):
##    def name(self):
##        return 'action_book'
##
##    def run(self, dispatcher, tracker, domain):
##
##        sp_data = "The test is successfull"
##    
##        dispatcher.utter_message(sp_data)
##        return []

class PrescriptionForm(FormAction):
    """Example of a custom form action"""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "prescription_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["PERSON","age"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "PERSON": self.from_entity(entity="PERSON", intent=["inform","request_prescription"]),
            "age": [ self.from_entity(entity="age", intent=["inform", "enter_age"]),
                                      self.from_entity(entity="CARDINAL", intent=["enter_age"])
                   ]                   

               }

    def validate(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        slot_values = self.extract_other_slots(dispatcher,tracker,domain)
        slot_to_fill = tracker.get_slot("age","PERSON")
        if slot_to_fill:
            slot_values.update(self.extract_requested_slot(dispatcher,tracker,domain))
        for slot,value in slot_values.items():
            if slot == 'age':
                if int(value) not in range(10,99):
                    dispatcher.utter_template('utter_wrong_age',tracker)
                    slot_values[slot] = None
        return [SlotSet(slot,value) for slot,value in slot_values.items()]
        
	
    
    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""

        # utter submit template
        dispatcher.utter_message(template="utter_submit")
        return []
