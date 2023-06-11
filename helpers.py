def read_file(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    return content

def create_dict_from_data(data):
    lines = data.split("\n")
    dictionary = {}
    for line in lines:
        if ":" in line:
            key, value = line.split(":")
            key = key.strip()
            value = value.strip()
            dictionary[key] = value
    return dictionary