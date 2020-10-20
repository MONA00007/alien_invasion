pets = {
    'D': {
        'name': 'DD',
        'type': 'dog'
    },
    'M': {
        'name': 'MM',
        'type': 'cat'
    }
}
for pet_name, info in pets.items():
    print(pet_name + ':')
    for key, value in info.items():
        print('name is ' + key)
        print('type is ' + value)
