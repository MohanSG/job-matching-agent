import yaml

def parse_yaml():
    with open("profile.yaml") as stream:
        try:
            data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    return data
