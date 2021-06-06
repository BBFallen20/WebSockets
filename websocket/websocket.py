def check_user_in_file(user:str):
    with open('../data.txt', 'r') as File:
        data = File.read().split(';')
        for d in data:
            data_user, data_value = d.split(':')
            if user in data_user:
                return int(data_value)


data = 1
checked = False


async def websocket_application(scope, receive, send):
    while True:
        event = await receive()

        if event['type'] == 'websocket.connect':
            await send({
                'type': 'websocket.accept'
            })

        if event['type'] == 'websocket.disconnect':
            break

        if event['type'] == 'websocket.receive':
            global data
            global checked
            memory_data = None
            received_data = event['text']
            counter, user = received_data.split('/')
            print(checked)
            if not checked:
                memory_data = check_user_in_file(user)
                checked = True
            if memory_data:
                data = memory_data
            else:
                data = int(counter) + 1
            with open('../data.txt', 'w') as File:
                File.write(f'{user}:{counter};')
            await send({
                'type': 'websocket.send',
                'text': str(data)
            })

