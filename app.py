import shlex


import streamlit as st



st.title("Stack Overflow Auto-Search Tool")

st.text(
    'Instruction:' + '\n''1. Select a Code File' + '\n''2. Click the Search Button' + '\n''3. You will get all the err solutions for the selected code file')

from subprocess import Popen, PIPE
import requests
import webbrowser

uploaded_file = st.file_uploader('File upload')


def getData(cmd):
   
    args = shlex.split(cmd)
    proc = Popen(args, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    return out, err

def make_request(err):
    print("Searching for " + err)
    response = requests.get(
        "https://api.stackexchange.com" + "/2.2/search?order=desc&sort=activity&tagged=python&intitle={}&site=stackoverflow".format(err))
    return response.json()


def get_urls(json_dict):
    url_list = []
    count = 0
    for i in json_dict["items"]:
        if i["is_answered"]:
            url_list.append(i["link"])
        count += 1
        if count == 3 or count == len(i):
            break
    for i in url_list:
        webbrowser.open(i)


def autoSearch():
    if __name__ == "__main__":
     out, err = getData("python {}".format(uploaded_file))
     out, err = getData("python test.py")
     err = err.decode("utf-8").strip().split("\r\n")[-1]
     print("err => ", err)
     print(getData("python {}".format(uploaded_file)))
    if (err):
        err_list = err.split(":")
        json1 = make_request(err_list[0])
        json2 = make_request(err_list[1])
        json3 = make_request(err)
        get_urls(json1)
        get_urls(json2)
        get_urls(json3)
    else:
        print("No error is found")

st.button("Search", on_click=autoSearch)