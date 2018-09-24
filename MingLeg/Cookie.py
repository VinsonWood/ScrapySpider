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
    cookie = "swpm_session=a0729f55f646f2ee1bf85f628c2e4549; Hm_lvt_c7b9263bd8f9b5b87b3e0e88548b3bea=1537708130,1537749333,1537749536,1537750646; swpm_in_use=swpm_in_use; simple_wp_membership_sec_20cfa294bb93a749d1b63f30c2e794b9=varshonwood%7C1538960567%7C4509ef06f8902c924ca464e8491c7638; wordpress_logged_in_20cfa294bb93a749d1b63f30c2e794b9=varshonwood%7C1538960567%7Ci03brlZaNCZUO3U2U2RE9JBW3cXmHZtuPSgVpKjzeL8%7C2064a19080d8cc18152dfd8e3e76ed2605dcae5b91409255b63dd982396c0c97; Hm_lpvt_c7b9263bd8f9b5b87b3e0e88548b3bea=1537751095"
    trans = transCookie(cookie)
    print(trans.stringToDict())
