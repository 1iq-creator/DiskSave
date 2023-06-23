import requests
import sys

with open('tokens.txt', encoding='utf-8') as file_object:
    token_VK = file_object.readline().strip('token_VK = ')
    disk_token = ""

class VK:
    def __init__(self, vk_id, quantity_photo):
        self.vk_id = input("Введите id: ")
        self.quantity_photo = input("Введите необходимое количество фотографий: ")

    def get_photo(self):
        response = requests.get('https://api.vk.com/method/photos.get',
                        params={
                            'v': 5.131,
                            'access_token': token_VK,
                            'owner_id': self.vk_id,
                            'album_id': 'profile',
                            'extended': '1',
                            'count': self.quantity_photo
                        })
        if response.status_code == 200:
            res = response.json()
            return response.json()
        sys.exit(f"Ошибка , код: {response.status_code}")

    def photo_info(self):
        vk_list = self.get_photo()
        res_vk = list()
        vk_list_sort = vk_list['response']['items']
        for i in vk_list_sort:
            for j in i["sizes"]:
                if j["type"] == "w":
                    res_vk.append({"size": j["type"], "ulr": j["url"], "likes": sum(i["likes"].values())})
        return res_vk

class UserYandex:
    def __init__(self, token, folder_path):
        self.token = token
        self.folder_path = folder_path
        self.url = "https://cloud-api.yandex.net/v1/disk/resources"
        self.headers = {
            "Authorization": f"OAuth {self.token}",
            "Content-Type": "application/json"
        }

    def create_folder(self):  # метод создаёт папку на диске по указанному пути
        params = {'path': self.folder_path}
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        if requests.get(url, headers=self.headers, params=params).status_code != 200:
            requests.put(url, headers=self.headers, params=params)
            print(f'\nПапка {self.folder_path} успешно создана в корневом каталоге Яндекс диска\n')
        else:
            print(f'\nПапка {self.folder_path} уже существует. Файлы с одинаковыми именами не будут скопированы\n')
        return self.folder_path

    def upload_files(self):
        vk = VK(token_VK, user_id)
        res_photos = vk.photo_info()
        url_upload = self.url + "/upload"
        for i in res_photos:
            name = i["likes"]
            params = {
                "path": f'{self.folder_path}/{name}',
                "url": i["ulr"]
            }
            requests.post(url_upload, headers=self.headers, params=params)
        return "Все фотографии успешно загрузились в папку"

user_id = ''
ya = UserYandex(disk_token, "фотографии_вк")
ya.create_folder()
ya.upload_files()
