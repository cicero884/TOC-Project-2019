from transitions.extensions import GraphMachine

from utils import send_text_message


class TocMachine(GraphMachine):
    Backpack=[]
    roomA_object=[]
    roomB_object=[]
    roomC_object=[]
    roomD_object=[]
    roomE_object=[]

    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model=self,
            **machine_configs
        )

    def is_going_to_state1(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == 'go to state1'
        return False
    
    def is_going_to_state2(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == 'go to state2'
        return False

    def room_discription(sender_id,objects,doors):
        send_text_message(sender_id, 'There are '+', '.join(roomA_object) if len(roomA_object) else "nothing"+"in it");

    def on_enter_roomA(self,event):
        print("@roomA")
        sender_id = event['sender']['id']
        send_text_message(sender_id,'I walk into room A.')
        room_discription(sender_id,roomA)
        
        
    def on_enter_state1(self, event):
        print("I'm entering state1")
        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, "I'm entering state1")
        self.go_back()

    def on_exit_state1(self):
        print('Leaving state1')

    def on_enter_state2(self, event):
        print("I'm entering state2")

        sender_id = event['sender']['id']
        send_text_message(sender_id, "I'm entering state2")
        self.go_back()

    def on_exit_state2(self):
        print('Leaving state2')
