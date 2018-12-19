from transitions.extensions import GraphMachine

from utils import send_text_message


class TocMachine(GraphMachine):
    Backpack=[]
    house=[
            {
                'objects':[],
                'doors':['door_A','door_B','door_C']
            },
            {
                'objects':[],
                'doors':['door_A']
            },
            {
                'objects':[],
                'doors':['door_B','door_D','door_E']
                },
            {
                'objects':[],
                'doors':['door_C','door_E']
            },
            {
                'objects':[],
                'doors':['door_D']
            }
        ]

    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self,**machine_configs)

    def door_A(self, event):
        print('@door_A')
        if event.get("message"):
            text = event['message']['text']
            return text == 'enter door_A'
        return False

    def door_B(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text == 'enter door_B'
        return False

    def door_C(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text == 'enter door_C'
        return False

    def door_D(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text == 'enter door_D'
        return False

    def door_E(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text == 'enter door_E'
        return False

    def reset(self, event):
        if event.get("message"):
            text = event['message']['text']
            if text == 'reset':
                global house
                house=[
                        {#0
                            'objects':[],
                            'doors':['door_A','door_B','door_C']
                        },
                        {#1
                            'objects':[],
                            'doors':['door_A']
                        },
                        {#2
                            'objects':[],
                            'doors':['door_B','door_D','door_E']
                        },
                        {#3
                            'objects':[],
                            'doors':['door_C','door_E']
                        },
                        {#4
                            'objects':[],
                            'doors':['door_D']
                        }
                        ]
                sender_id = event['sender']['id']
                send_text_message(sender_id,'reset game')
                return True
        return False


    def room_description(self,sender_id,room):
        send_text_message(sender_id,'You are in the '+self.state)
        send_text_message(sender_id,'There are '+(', '.join(self.house[room]['objects']) if len(self.house[room]['objects']) else "nothing")+" in it,")
        send_text_message(sender_id,'and there are '+', '.join(self.house[room]['doors'])+' in the room')
    
    def help(self,sender_id):
        send_text_message(sender_id,'Your actions:\nreset,help,enter [door],open [object],pickup [object]')

    def on_enter_room0(self,event):
        print("@room0")
        sender_id = event['sender']['id']
        send_text_message(sender_id,'You walked into room0.')
        self.room_description(sender_id,int(self.state[4]))

    def on_enter_room1(self,event):
        print("@room1")
        sender_id = event['sender']['id']
        send_text_message(sender_id,'You walked into room1.')
        self.room_description(sender_id,int(self.state[4]))

    def on_enter_room2(self,event):
        print("@room2")
        sender_id = event['sender']['id']
        send_text_message(sender_id,'You walked into room2.')
        self.room_description(sender_id,int(self.state[4]))

    def on_enter_room3(self,event):
        print("@room3")
        sender_id = event['sender']['id']
        send_text_message(sender_id,'You walked into room3.')
        self.room_description(sender_id,int(self.state[4]))

    def on_enter_room4(self,event):
        print("@room4")
        sender_id = event['sender']['id']
        send_text_message(sender_id,'You walked into room4.')
        self.room_description(sender_id,int(self.state[4]))

