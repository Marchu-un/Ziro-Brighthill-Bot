#Функция для того, чтобы из user id получить его имя
def user_to_name_maper (user_id, users_dict):
    return users_dict[user_id]



if __name__ == "__main__":
    user_id = 12345
    user_name = "Charonchik"
    users_dict = {user_id: user_name}

    print("User name is", user_to_name_maper(user_id, users_dict))
