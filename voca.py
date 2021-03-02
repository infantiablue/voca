# for more information on how to install requests
# http://docs.python-requests.org/en/master/user/install/#install
import requests
import json

# TODO: replace with your own app_id and app_key
app_id = 'fd0f1799'
app_key = 'b07f95f839de63b54d400c2f023658d3'

language = 'en-gb'
# word_id = 'Ace'
fields = 'definitions'
strictMatch = 'false'


def look_up(word):
    url = 'https://od-api.oxforddictionaries.com:443/api/v2/entries/' + language + \
        '/' + word.lower() + '?fields=' + fields + '&strictMatch=' + strictMatch

    r = requests.get(url, headers={'app_id': app_id, 'app_key': app_key})

    # print("code {}\n".format(r.status_code))
    # print("text \n" + r.text)
    # print("json \n" + json.dumps(r.json()))
    res = r.json()
    # senses = res['results'][0]['lexicalEntries'][0]['entries'][0]['senses']
    # lexicalCategory = res['results'][0]['lexicalEntries'][0]['lexicalCategory']
    # for i in senses:
    #     print(i['definitions'])

    # print(lexicalCategory)
    word = []

    if 'results' in res:
        for r in res['results']:
            res = []
            for l in r['lexicalEntries']:
                t = {}
                print(f'({l["lexicalCategory"]["text"]})')
                t['lexical'] = l["lexicalCategory"]["text"].lower()
                t['senses'] = []
                for e in l['entries']:
                    for s in e['senses']:
                        for d in s['definitions']:
                            t['senses'].append(d)
                            # print(d)
                res.append(t)
                # print()
            # print('---')
            word.append(res)
        return(word)
    else:
        return False


if __name__ == '__main__':
    d = look_up('done')
    if(d):
        for r in d:
            for l in r:
                print(l['lexical'])
                for s in l['senses']:
                    print(s)
                print()
            print('--')
    else:
        print('not found')
