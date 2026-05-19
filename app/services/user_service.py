users = {}
next_id = 1


def get_all_users():
    return list(users.values())


def get_user_by_id(user_id):
    return users.get(user_id)


def create_user(name):
    global next_id
    for user in users.values():
        if user["name"] == name:
            return None
    user = {"id": next_id, "name": name}
    users[next_id] = user
    next_id += 1
    return user


def update_user(user_id, name):
    if user_id not in users:
        return None
    for uid, user in users.items():
        if user["name"] == name and uid != user_id:
            return None
    users[user_id]["name"] = name
    return users[user_id]


def delete_user(user_id):
    if user_id not in users:
        return None
    return users.pop(user_id)


def search_users_by_name(query):
    if not query:
        return list(users.values())
    query_lower = query.lower()
    return [u for u in users.values() if query_lower in u["name"].lower()]


def reset_users():
    global next_id
    users.clear()
    next_id = 1
