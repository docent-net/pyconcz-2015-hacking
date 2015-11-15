#!/usr/bin/python

import requests

def upload_palette(username, password, c1, c2, c3, c4, c5):
    sess = requests.Session()

    form_data = {
        "e": username,
        "p": password
    }
    # login: python_scraper
    # pwd: secure_password

    res = sess.post("https://coolors.co/ajax/login", data=form_data)

    res_json = res.json()

    assert res_json["result"] == 0, 'logging in failed'

    form_data = {
        "c1": c1,
        "c2": c2,
        "c3": c3,
        "c4": c4,
        "c5": c5,
        "name": "test_docent2",
        "tags": "",
        "key": "Coolors_Simple_KEY",
    }

    res = sess.post("https://coolors.co/ajax/add_user_palette", data=form_data)
    #assert res.status_code == 200
    assert len(res.text), "cannot save the palette!"

if __name__ == "__main__":
    import sys
    sys.argv.pop(0) # remove script name
    upload_palette(*sys.argv)
    print ("OK")