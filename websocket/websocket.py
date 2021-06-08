async def websocket_application(scope, receive, send):
    while True:
        event = await receive()

        if event['type'] == 'websocket.connect':
            await send({
                'type': 'websocket.accept',
            })

        if event['type'] == 'websocket.disconnect':
            break

        if event['type'] == 'websocket.receive':
            users_messages = {}
            data = str(event['text'])
            # Делим сообщение по двоеточию
            data_split = data.split(':')
            # Если введён id пользователя которому шлём сообщение
            user_from = data_split[0]
            if data_split[1]:
                user_to = data_split[1]
                # Записываем сообщение в словарь и отправляем в файлик
                users_messages.update({user_from: user_to})
                with open('../data.txt', 'a') as File:
                    File.write(str(users_messages) + ';')
            # Ищем в файлике сообщения для текущего пользователя
            with open('../data.txt', 'r') as File:
                buffer = File.read()
                messages = buffer.split(';')
                for message in messages:
                    try:
                        # Примитивное форматирование сообщений с отслежкой возможных ошибок
                        u_from, u_to = message.replace('}', '').replace('{', '').split(':')
                    except ValueError:
                        pass
                    # Если находим сообщение предназначенное текущему пользователю - отправляем
                    if str(user_from) in u_to:
                        message_to_send = u_from
                        await send({
                            'type': 'websocket.send',
                            'text': f'YOU HAVE A NEW MESSAGE FROM: {message_to_send}'
                        })
                    buffer.replace(message, '')
            # Перезаписываем буффер, удаляя отправленные сообщения
            with open('../data.txt', 'w') as File:
                File.write(buffer)

            await send({
                'type': 'websocket.send',
                'text': f"Your message:'{data}'"
            })

