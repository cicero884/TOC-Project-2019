from transitions.extensions import GraphMachine

from utils import send_text_message


class TocMachine(GraphMachine):
    keys=[False,False,False,False,False]
    active_monster=False
    monster_pre_pos=4
    monster_new_pos=4
    house=[
            {
                'objects':['box'],
                'doors':['door_A','door_B','door_C']
            },
            {
                'objects':['locker A1','locker A2','locker A3','locker A4'],
                'doors':['door_A']
            },
            {
                'objects':['dead body'],
                'doors':['door_B','door_D']
                },
            {
                'objects':[],
                'doors':['door_C','door_E']
            },
            {
                'objects':['monster'],
                'doors':['door_D','door_exit']
            }
        ]

    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self,**machine_configs)

    def door_A(self, event):
        print('@door_A')
        if event.get("message"):
            text = event['message']['text']
            if text == 'enter door_A':
                if self.keys[0]:
                    return True
                else:
                    sender_id = event['sender']['id']
                    send_text_message(sender_id,'The door is locked!')

        return False

    def door_B(self, event):
        if event.get("message"):
            text = event['message']['text']
            if text == 'enter door_B':
                if self.keys[1]:
                    return True
                else:
                    sender_id = event['sender']['id']
                    send_text_message(sender_id,'The door is locked!')
        return False

    def door_C(self, event):
        if event.get("message"):
            text = event['message']['text']
            if text == 'enter door_C':
                if self.keys[2]:
                    return True
                else:
                    sender_id = event['sender']['id']
                    send_text_message(sender_id,'The door is locked!')
        return False

    def door_D(self, event):
        if event.get("message"):
            text = event['message']['text']
            if text == 'enter door_D':
                if self.keys[3]:
                    return True
                else:
                    sender_id = event['sender']['id']
                    send_text_message(sender_id,'The door is locked!')
        return False

    def door_E(self, event):
        if event.get("message"):
            text = event['message']['text']
            if text == 'enter door_E':
                if self.keys[4]:
                    return True
                else:
                    sender_id = event['sender']['id']
                    send_text_message(sender_id,'The door is locked!')
        return False
    def door_exit(self,event):
        if event.get("message"):
            text = event['message']['text']
            return text == 'enter door_exit' 
        return False

    def reset(self, event):
        if event.get("message"):
            text = event['message']['text']
            if text == 'reset' or self.state=='outside' or int(self.state[4])==self.monster_pre_pos:
                #global house
                #global keys
                #global active_monster
                #global monster_pos
                self.house=[
                        {
                            'objects':['box'],
                            'doors':['door_A','door_B','door_C']
                            },
                        {
                            'objects':['locker A1','locker A2','locker A3','locker A4'],
                            'doors':['door_A']
                            },
                        {
                            'objects':['dead body'],
                            'doors':['door_B','door_D']
                            },
                        {
                            'objects':[],
                            'doors':['door_C','door_E']
                            },
                        {
                            'objects':['monster'],
                            'doors':['door_D']
                            }
                        ]
                self.keys=[False,False,False,False,False]
                self.active_monster=False
                self.monster_pre_pos=4
                self.monster_new_pos=4
                sender_id = event['sender']['id']
                return True
        return False


    def room_description(self,event,pos):
        sender_id = event['sender']['id']
        if pos!='outside' :
            room=int(pos[4])
            send_text_message(sender_id,'You are in the '+self.state)
            send_text_message(sender_id,'There are '+(', '.join(self.house[room]['objects']) if len(self.house[room]['objects']) else "nothing")+" in it,")
            send_text_message(sender_id,'and there are '+', '.join(self.house[room]['doors'])+' in the room')
        else:
            send_text_message(sender_id,'The outside is fake!,you found...')
            self.command(event)
    
    def help(self,sender_id):
        send_text_message(sender_id,'Your actions:\nreset,help, observe, enter [door], search [object]')

    def search(self,event):
        if(self.state=='outside'):
            return
        sender_id = event['sender']['id']
        text = event['message']['text']
        #global keys
        for Object in self.house[int(self.state[4])]['objects']:
            if (text.find(Object)>=0):
                if Object=='box':
                    self.keys[0]=True
                    send_text_message(sender_id,'You found key A,you can open door_A now!')
                if Object=='locker A1':
                    self.keys[1]=True
                    send_text_message(sender_id,'You found key B,you can open door_B now!')
                if Object=='locker A2':
                    send_text_message(sender_id,'Nothing in the locker')
                if Object=='locker A3':
                    send_text_message(sender_id,'Nothing in the locker')
                if Object=='locker A4':
                    self.keys[3]=True
                    send_text_message(sender_id,'You found key D,you can open door_D now!')
                if Object=='dead body':
                    self.keys[2]=True
                    self.keys[4]=True
                    send_text_message(sender_id,'You found key C and key E!')
                if Object=='monster':
                    send_text_monster(sender_id,'The monster is trying to eat you!')

    def monster_move(self,sender_id):
        if(self.state=='outside'):
            return
        send_text_message(sender_id,'The monster is chasing you!')
        #print(self.house[self.monster_pos]['objects'])
        self.house[self.monster_pre_pos]['objects'].remove('monster')
        self.house[self.monster_new_pos]['objects'].append('monster')
        self.monster_pre_pos=self.monster_new_pos

    def monster_attack(self,event):
        if(self.state=='outside'):
            return
        for Object in self.house[int(self.state[4])]['objects']:
            if Object=='monster':
                self.gameover(event,1)

    def gameover(self,event,status):
        sender_id = event['sender']['id']
        if status==0:
            send_text_message(sender_id,'You finally escape the house!')
        elif status==1:
            send_text_message(sender_id,'You are eaten by monster...')
            self.command(event)

    def on_enter_room0(self,event):
        print("@room0")
        sender_id = event['sender']['id']
        send_text_message(sender_id,'You walked into room0.')

    def on_enter_room1(self,event):
        print("@room1")
        sender_id = event['sender']['id']
        send_text_message(sender_id,'You walked into room1.There are some locker there.')

    def on_enter_room2(self,event):
        print("@room2")
        sender_id = event['sender']['id']
        send_text_message(sender_id,'You walked into room2.The smell from the dead body is terrible.')

    def on_enter_room3(self,event):
        print("@room3")
        sender_id = event['sender']['id']
        send_text_message(sender_id,'You walked into room3.')

    def on_enter_room4(self,event):
        print("@room4")
        #global active_monster
        sender_id = event['sender']['id']
        if self.active_monster==False:
            self.active_monster=True
            send_text_message(sender_id,'You saw a monster,so you run back to room2')
            self.monster_new_pos=4
            self.enter(event)
        else:
            send_text_message(sender_id,'You walked into room4.')

    def on_enter_outside(self,event):
        print("@out")
        sender_id = event['sender']['id']
        send_text_message(sender_id,'You walked outside.')
        self.gameover(event,0)

