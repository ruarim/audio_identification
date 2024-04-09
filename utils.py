# helper function to get id frrom genre and song number
def get_id(file):
    split = file.name.split('.')
    id = split[0] + split[1][:5]
    return id