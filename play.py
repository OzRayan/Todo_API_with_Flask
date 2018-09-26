user_data = {
            'username': 'tomika',
            'email': 'sexample@test.com',
            'password': 'password',
            'verify_password': 'password'
        }

prompt = "No {} was provided"

for x in user_data.keys():
    a = user_data.copy()
    del a[x]
    print(prompt.format(x) if '_' not in x else prompt.format(x.replace('_', ' ')))
    print(a.keys())

