import json


def get_value_from_raw_log(
    raw_log: str,
    key: str,
):
    if not raw_log:
        return ''

    raw_log = json.loads(raw_log)
    for l in raw_log:
        for e in l['events']:
            for a in e['attributes']:
                if f'{e["type"]}.{a["key"]}' == key:
                    return str(a['value'])
    return ''

def get_value_from_events(
    events: str,
    key: str,
):
    if not events:
        return ''

    for e in events:
        for a in e['attributes']:
            if f'{e["type"]}.{a["key"]}' == key:
                return str(a['value'])
    return ''
