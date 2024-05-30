def get_username(link):
    if "@" in link:
        username = link.split("@")[-1]
    elif "t.me/" in link:
        username = link.split("t.me/")[-1]
    else:
        return link
    return username