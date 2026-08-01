import os
from pathlib import Path
import json
from typing import List

FILE_CWD = Path(__file__).resolve().parent
SOURCE_CWD = FILE_CWD / "source"


def get_source_file() -> str:
    files = os.listdir(SOURCE_CWD)
    if len(files) == 0:
        raise ValueError("No source file given")
    elif len(files) > 1:
        print("More than one source file given, using first")
    print(files[0])
    return files[0]


def cut_str_after(data: str, key: str) -> str:
    start_index = data.index(key) + len(key)
    data = data[start_index:-1]
    return data


def extract_next_event(data: str) -> dict:
    result = {}
    event = {}
    data = cut_str_after(data, "isbfilter")
    #from
    data = cut_str_after(data, '<td class="nofloat">')
    event["from"] = data[0:10]
    #until
    data = cut_str_after(data, '<td class="nofloat">')
    event["until"] = data[0:10]
    #url
    data = cut_str_after(data, 'formaction="')
    end_index = data.index('"')
    event["url"] = data[0:end_index]
    #name
    data = cut_str_after(data, '"post">')
    end_index = data.index('</button>')
    event["name"] = data[0:end_index]
    #plz
    data = cut_str_after(data, '<td class="nofloat">')
    end_index = data.index('</td>')
    event["plz"] = data[0:end_index]
    #place
    data = cut_str_after(data, '<td class="nofloat">')
    end_index = data.index('</td>')
    event["place"] = data[0:end_index]

    data = cut_str_after(data, '</tr>')
    result["data"] = data
    result["event"] = event
    return result


def extract_data(file_name: str) -> List:
    events = []
    with open(SOURCE_CWD / file_name, encoding='utf-8') as file:
        file_data = file.read()
        while(file_data.find("isbfilter") >= 0):
            event_result = extract_next_event(file_data)
            events.append(event_result["event"])
            print(event_result["event"])
            file_data = event_result["data"]
    print(f"Entries: {len(events)}")
    return events


def save_data(events_list: List) -> None:
    with open(FILE_CWD / "data.json", "w", encoding='utf-8') as f:
        json.dump(events_list, f, indent=2)


def main() -> None:
    file_name = get_source_file()
    if "mittelalterkalender.info" not in file_name:
        raise ValueError("Currently only 'mittelalterkalender.info' is accepted as source")
    events_list = extract_data(file_name)
    save_data(events_list)


if __name__ == "__main__":
    main()