import vk_api


def auth_handler():
    """ При двухфакторной аутентификации вызывается эта функция. """

    # Код двухфакторной аутентификации,
    # который присылается по смс или уведомлением в мобильное приложение
    key = input("Enter authentication code: ")
    # Если: True - сохранить, False - не сохранять.
    remember_device = True

    return key, remember_device


def main(login, password, group_id):
    vk_session = vk_api.VkApi(
        login, password,
        # функция для обработки двухфакторной аутентификации
        auth_handler=auth_handler
    )

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()
    # Используем метод stats.get
    response = vk.stats.get(group_id=group_id, fields="reach", intervals_count=10)
    activities = {}
    ages = {}
    cities = []
    for i in response:
        if 'activity' in i.keys():
            for key, value in i['activity'].items():
                activities[key] = value
        if i['reach'] and list(filter(lambda s: i['reach'][s], i['reach'])):
            reach_info = i['reach']
            for city in reach_info['cities']:
                if city['name'] not in cities:
                    cities.append(city['name'])
            for age in reach_info['age']:
                age_range = age['value']
                age_count = age['count']
                ages[age_range] = age_count
    result = {
        'Activities': activities,
        'Ages': ages,
        'Cities': cities
    }
    return result
