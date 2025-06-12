import os
from dotenv import load_dotenv
import requests

API_VERSION = '5.131'
load_dotenv()

def fetch_vk_data(method, params, token):
    """Базовый метод для выполнения запросов к VK API"""
    base_url = f"https://api.vk.com/method/{method}"
    params.update({
        'access_token': token,
        'v': API_VERSION
    })
    try:
        response = requests.get(base_url, params=params)
        return response.json()
    except requests.exceptions.RequestException:
        return None


def get_user_id(user_input, token):
    """Получаем ID пользователя по входным данным"""
    if user_input.isdigit():
        return user_input

    username = user_input.split('/')[-1].split('?')[0]  # Удаляем возможные параметры URL
    data = fetch_vk_data('users.get', {'user_ids': username}, token)

    return str(data['response'][0]['id']) if data and data.get('response') else None


def get_friends_list(user_id, token):
    """Получаем список друзей пользователя"""
    data = fetch_vk_data('friends.get', {
        'user_id': user_id,
        'fields': 'first_name,last_name'
    }, token)

    return data['response']['items'] if data and data.get('response') else []


def get_groups_list(user_id, token):
    """Получаем список групп пользователя"""
    data = fetch_vk_data('groups.get', {
        'user_id': user_id,
        'extended': 1
    }, token)

    return data['response']['items'] if data and data.get('response') else []


def display_user_info(user_id, token):
    """Отображаем информацию о друзьях и группах пользователя"""

    friends = get_friends_list(user_id, token)
    if friends:
        print("\nСписок друзей пользователя:")
        for friend in friends:
            print(f"{friend['first_name']} {friend['last_name']}")
    else:
        print("\nНе удалось получить список друзей")

    # Разделитель
    print("\n" + "-" * 25)


    groups = get_groups_list(user_id, token)
    if groups:
        print("\nСписок групп пользователя:")
        for group in groups:
            print(group['name'])
    else:
        print("\nНе удалось получить список групп")


def main():

    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")


    user_input = input(
        "Введите ID пользователя или ссылку (например, https://vk.com/pribylov2000 или 578768998): ").strip()


    user_id = get_user_id(user_input, ACCESS_TOKEN)
    if not user_id:
        print("Профиль закрыт или пользователь не найден")
        return


    display_user_info(user_id, ACCESS_TOKEN)


if __name__ == "__main__":
    main()
