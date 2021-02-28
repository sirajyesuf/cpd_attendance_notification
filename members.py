import json

def read():
    with open('members.json','r') as f:
        data = json.load(f)
        return data
def write(payload):
    with open('members.json','w') as f:
        json.dump(payload,f,indent=3)
def store_members(payload):
    write(payload)



def members():
    data = read()
    return data['members']

def update_member(payload):
    data = read()
    for member in data['members']:
        if member['telegram_user_name'] == payload['user_name'] and member['user_id'] == None:
            member['user_id'] = payload['user_id']
            write(data)
            break
        else:
            print("allready done")

def add_member_message(payload):
    data = read()
    for member in data['members']:
        if member['user_id'] == payload['user_id']:
            member['messages'].append(payload['msg'])
            write(data)
            break

# members()
# x()
# members()
