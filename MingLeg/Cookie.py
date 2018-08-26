# -*- coding: utf-8 -*-

class transCookie:
    def __init__(self, cookie):
        self.cookie = cookie

    def stringToDict(self):
        itemDict = {}
        items = self.cookie.split(';')
        for item in items:
            key = item.split('=')[0].replace(' ', '')
            value = item.split('=')[1]
            itemDict[key] = value
        return itemDict


if __name__ == "__main__":
    cookie = "wordpress_sec_20cfa294bb93a749d1b63f30c2e794b9=varshonwood%7C1536362156%7Cj94PSkVsVDhCIPCwUd2VJG2u1YQ0QdDPwn0qTf89ciN%7C7c84743f6cff38a80a206f7452705aae658aa96faafe01f41c886279f32b4899; swpm_session=f12c5ca08c94a133c9c2ed4f403e0482; swpm_in_use=swpm_in_use; Hm_lvt_c7b9263bd8f9b5b87b3e0e88548b3bea=1534006826,1535026151,1535026811,1535106977; wordpress_test_cookie=WP+Cookie+check; simple_wp_membership_sec_20cfa294bb93a749d1b63f30c2e794b9=varshonwood%7C1536362156%7Cfb7951e3fede5438782b00f616804cf5; wordpress_logged_in_20cfa294bb93a749d1b63f30c2e794b9=varshonwood%7C1536362156%7Cj94PSkVsVDhCIPCwUd2VJG2u1YQ0QdDPwn0qTf89ciN%7C844def3a4daa678ec604f69f7523b0e1e809e17c2d8a66c23050662746229b03; Hm_lpvt_c7b9263bd8f9b5b87b3e0e88548b3bea=1535152559"
    trans = transCookie(cookie)
    print(trans.stringToDict())
