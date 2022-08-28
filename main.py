import hashlib
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import datetime

def get_hash(data):
    return hashlib.sha512(str(data['text']).encode('utf-8')).hexdigest()[:7]

app = FastAPI()


page_auth = """<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat Auth</h1>
      
        <div >
            <input type="text" id="room_id" placeholder="room_id"/>
            <input type="text" id="user_id" placeholder="user_id"/>
            <button onclick = "sendMessage()">Send</button>
        </div>
       
        <script>
        
            function sendMessage() {
                var room_id = document.getElementById("room_id")
                var user_id = document.getElementById("user_id")
                window.location.href =`/room/${room_id.value}/${user_id.value}`
                room_id.value = ''
                user_id.value = ''
            }
        </script>
    </body>
</html>
"""

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            url = window.location.pathname
            var ids = url.split('/')
            console.log(ids)
            client_id = ids[3]
			host = window.location.host
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://${host}/ws${url}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                
                var input = document.getElementById("messageText")

                let data = {'text':input.value,
                            'name':`${client_id}`} 
                let gfg = JSON.stringify(data);
                ws.send(gfg)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""
def instance_attributes(obj):
    """Get a name-to-value dictionary of instance attributes of an arbitrary object."""
    try:
        return vars(obj)
    except TypeError:
        pass

    # object doesn't have __dict__, try with __slots__
    try:
        slots = obj.__slots__
    except AttributeError:
        # doesn't have __dict__ nor __slots__, probably a builtin like str or int
        return {}
    # collect all slots attributes (some might not be present)
    attrs = {}
    for name in slots:
        try:
            attrs[name] = getattr(obj, name)
        except AttributeError:
            continue
    return attrs

class ConnectionManager:
    def __init__(self):
        
        self.rooms = {}
    async def connect(self,room_id:str, websocket: WebSocket):
        await websocket.accept()
        # print(instance_attributes(websocket))
        if self.rooms.get(room_id):
            self.rooms[room_id]['users'].append(websocket)
        else:
            self.rooms[room_id] = {
            'users':[],
            'messages':[]
            }
            self.rooms[room_id]['users'].append(websocket)

    def disconnect(self,room_id:str, websocket: WebSocket):
        count = 0
        for connection in self.rooms[room_id]['users']:
            if connection == websocket:
                self.rooms[room_id]['users'].pop(count)
                break
            count += 1

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self,room_id:str, message: str):
        print(message)
        for connection in self.rooms[room_id]['users']:
            await connection.send_json(message)

    def add_messages(self,room_id:str, message: str, websocket: WebSocket):
        send_date = datetime.datetime.now()
        self.rooms[room_id]['messages'].append({ 
                    'client_id':websocket,
                    'message':message,
                    'send_date': str(send_date)
                    })
        print(self.rooms)

manager = ConnectionManager()


@app.get("/")
async def get():
    return HTMLResponse(page_auth)

@app.get("/room/{room_id}/{client_id}")
async def get_room():
    return HTMLResponse(html)




@app.websocket("/ws/room/{room_id}/{client_id}")
async def websocket_endpoint(websocket: WebSocket,room_id: str, client_id: str):
    await manager.connect(room_id,websocket)
    # print(websocket.scope['path_params'])
    try:
        while True:
            object_data = await websocket.receive_text()
            print(object_data)
            json_object = object_data.encode('utf-8')

            data = json.loads(json_object,encoding='utf-8')
            
            print(data)
            send_date = datetime.datetime.now()

            msg={
                            # 'me': message['me'],
                            # 'id_message':data['name'],
                            'author':  
                                            {
                                                "author_id":str(client_id),
                                                "name":str( data['name']),
                                                "image":f"/addres/users.account/avatar/{str(client_id)}/{get_hash(data)}"
                                            },
                            'text': data['text'],
                            'day':send_date.strftime('%d.%m.%Y'),
                            'time':send_date.strftime('%H:%M'),
                        }
            await manager.broadcast(room_id,msg)
            # await manager.send_personal_message(f"You wrote: {data}", websocket)
            # manager.add_messages(room_id,data,websocket)
    except WebSocketDisconnect:
        manager.disconnect(room_id,websocket)
        await manager.broadcast(room_id,f"Client #{client_id} left the chat")
