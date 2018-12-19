from bottle import route, run, request, abort, static_file
import os
from fsm import TocMachine

VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
PORT = os.environ['PORT']

machine = TocMachine(
    states=[
        'room0',
        'room1',
        'room2',
        'room3',
        'room4',
        'outside'
    ],
    transitions=[
        {
            'trigger': 'enter',
            'source': 'room0',
            'dest': 'room1',
            'conditions': 'door_A'
        },
        {
            'trigger': 'enter',
            'source': 'room1',
            'dest': 'room0',
            'conditions': 'door_A'
        },
        {
            'trigger': 'enter',
            'source': 'room0',
            'dest': 'room2',
            'conditions': 'door_B'
        },
        {
            'trigger': 'enter',
            'source': 'room2',
            'dest': 'room0',
            'conditions': 'door_B'
        },
        {
            'trigger': 'enter',
            'source': 'room0',
            'dest': 'room3',
            'conditions': 'door_C'
        },
        {
            'trigger': 'enter',
            'source': 'room3',
            'dest': 'room0',
            'conditions': 'door_C'
        },
        {
            'trigger': 'enter',
            'source': 'room2',
            'dest': 'room4',
            'conditions': 'door_D'
        },
        {
            'trigger': 'enter',
            'source': 'room4',
            'dest': 'room2',
            'conditions': 'door_D'
        },
        {
            'trigger': 'enter',
            'source': 'room3',
            'dest': 'room2',
            'conditions': 'door_E'
        },
        {
            'trigger': 'enter',
            'source': 'room4',
            'dest': 'outside',
            'conditions': 'door_exit'
        },
        {
            'trigger': 'command',
            'source': [
                'room0',
                'room1',
                'room2',
                'room3',
                'room4',
                'outside'
            ],
            'dest': 'room0',
            'conditions':'reset'
        }
    ],
    initial='room0',
    auto_transitions=False,
    show_conditions=True,
)


@route("/webhook", method="GET")
def setup_webhook():
    mode = request.GET.get("hub.mode")
    token = request.GET.get("hub.verify_token")
    challenge = request.GET.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("WEBHOOK_VERIFIED")
        return challenge

    else:
        abort(403)


@route("/webhook", method="POST")
def webhook_handler():
    body = request.json
    print('\nFSM STATE: ' + machine.state)
    #print('REQUEST BODY: ')
    #print(body)

    if body['object'] == "page":
        event = body['entry'][0]['messaging'][0]
        print(event)
        if 'message' in event:
            sender_id = event['sender']['id']
            text=event['message']['text']
            
            if (text=='reset'):
                machine.command(event)

            elif text=='help':
                machine.help(sender_id)

            else:
                if(machine.state!='outside'):
                    machine.monster_new_pos=int(machine.state[4])
                if (text.find('enter')>=0):
                    machine.enter(event)

                elif (text.find('search')>=0):
                    machine.search(event)

                elif (text=='observe'):
                    machine.room_description(event,machine.state)

                machine.monster_attack(event)
                if machine.active_monster:
                    machine.monster_move(sender_id)
                machine.monster_attack(event)

        #print(event)
        return 'OK'


@route('/show-fsm', methods=['GET'])
def show_fsm():
    machine.get_graph().draw('fsm.png', prog='dot', format='png')
    return static_file('fsm.png', root='./', mimetype='image/png')


if __name__ == "__main__":
    run(host="localhost", port=5000, debug=True, reloader=True)
