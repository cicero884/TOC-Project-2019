from bottle import route, run, request, abort, static_file

from fsm import TocMachine

VERIFY_TOKEN = "Your Webhook Verify Token"
machine = TocMachine(
    states=[
        'roomA',
        'roomB',
        'roomC',
        'roomD',
        'roomE',
    ],
    transitions=[
        {
            'trigger': 'enter',
            'source': 'roomA',
            'dest': 'roomB',
            'conditions': 'open_door_i'
        },
        {
            'trigger': 'enter',
            'source': 'roomA',
            'dest': 'roomC',
            'conditions': 'open_door_j'
        },
        {
            'trigger': 'enter',
            'source': 'roomA',
            'dest': 'roomD',
            'conditions': 'open_door_k'
        },
        {
            'trigger': 'enter',
            'source': 'roomC',
            'dest': 'roomE',
            'conditions': 'open_door_l'
        },
        {
            'trigger': 'enter',
            'source': 'roomD',
            'dest': 'roomC',
            'conditions': 'open_door_m'
        },
        {
            'trigger': 'enter',
            'source': 'roomC',
            'dest': 'roomD',
            'conditions': 'open_door_m'
        },
        {
            'trigger': 'reset',
            'source': [
                'roomA',
                'roomB',
                'roomC',
                'roomD',
                'roomE',
            ],
            'dest': 'user',
            'conditions':'reset'
        }
    ],
    initial='roomA',
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
        text=event[message][text]
        if text.find('enter'):
            machine.enter(event)

        if text.find('open'):
            machine.open(event)
        print(event)
        return 'OK'


@route('/show-fsm', methods=['GET'])
def show_fsm():
    machine.get_graph().draw('fsm.png', prog='dot', format='png')
    return static_file('fsm.png', root='./', mimetype='image/png')


if __name__ == "__main__":
    run(host="localhost", port=5000, debug=True, reloader=True)
