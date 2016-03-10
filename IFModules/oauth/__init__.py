# -* coding: utf-8 -*-
import VKAPI, time

vk = None

def authorize(user_data):
    global vk
    #user_data = dataMngt.load_user_data()
    vk = VKAPI.VK(user_data)
    res_auth = vk.do_authorize()
    return vk

def proccessing_error(cond, res):
    global one_account
    if cond == 'success': return res
    elif cond == 'error':
        code = res['code']
        msg = res['msg']
        print code, msg
        if code == 5:
            authorize()
            print '\n  Connected to', vk.user_data[1], '\n'
        elif code == 15: pass
        elif code == 220: pass# защита от спама

def vk_usersGet(user_ids, fields, name_case='nom'):
    params = {
        'user_ids': user_ids,
        'fields': fields,
        'name_case': name_case}
    cond, res =  vk.api('users.get', params)
    return proccessing_error(cond, res)

def vk_wallPost(owner_id, message, attachments='', from_group=0):
    params = {
        'owner_id': owner_id,
        'message': message,
        'attachments': attachments,
        'from_group': from_group}
    cond, res =  vk.api('wall.post', params)
    return proccessing_error(cond, res)

def vk_newsfeedSearch(q, count, start_from='', end_time='', extended=0):
    params = {
        'q': q,
        'count': count,
        'start_from': start_from,
        'end_time': end_time,
        'extended': extended}
    cond, res =  vk.api('newsfeed.search', params)
    return proccessing_error(cond, res)

def vk_groupsSearch(q, count, offset=0, city_id=''):
    parametrs = {
        'q': q, 'offset': offset, 'count': count,
        'sort': 2, 'city_id': city_id}
    cond, res = vk.api('groups.search', parametrs)
    return proccessing_error(cond, res)

def vk_groupsGetById(group_id, fields=''):
    parametrs = {'group_id': group_id, 'fields': fields}
    cond, res = vk.api('groups.getById', parametrs)
    return proccessing_error(cond, res)

def vk_groupsGetMembers(group_id, count, offset=0, fields=''):
    parametrs = {
        'group_id': group_id,
        'fields': fields,
        'offset': offset,
        'count': count}
    cond, res = vk.api('groups.getMembers', parametrs)
    return proccessing_error(cond, res)

def vk_messagesSend(user_id, message):
    parametrs = {
        'user_id': user_id,
        'message': message
        }
    cond, res = vk.api('messages.send', parametrs)
    return proccessing_error(cond, res)

def vk_messagesGet(out, count, offset=0):
    parametrs = {
        'out': out,
        'offset': offset,
        'count': count
        }
    cond, res = vk.api('messages.get', parametrs)
    return proccessing_error(cond, res)

def vk_messagesGetById(message_ids):
    parametrs = {
        'message_ids': message_ids
        }
    cond, res = vk.api('messages.getById', parametrs)
    return proccessing_error(cond, res)

def vk_messagesMarkAsRead(message_ids):
    parametrs = {
        'message_ids': message_ids
        }
    cond, res = vk.api('messages.markAsRead', parametrs)
    return proccessing_error(cond, res)

def vk_messagesSetActivity(user_id):
    parametrs = {
        'user_id': user_id,
        'type': 'typing'
        }
    cond, res = vk.api('messages.setActivity', parametrs)
    return proccessing_error(cond, res)
