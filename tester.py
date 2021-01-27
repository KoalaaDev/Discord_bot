import yaml
def SettingsOption():
    try:
        with open("Setting.yml","r") as f:
            Setting = yaml.load(f, Loader = yaml.FullLoader)
            username = Setting['ACCOUNT']['USERNAME']
            password = Setting['ACCOUNT']['PASSWORD']
    except FileNotFoundError:
        username = input("Username: ")
        password = input("Password: ")
        settingsfile = {
            "ACCOUNT":{
                "USERNAME": username,
                "PASSWORD": password
            }
        }
        with open("Setting.yml","w") as f:
            yaml.dump(settingsfile, f, default_flow_style=False)
            print("Saved settings")
SettingsOption()
