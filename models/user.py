import profile


class User():
    def __init__(self, id, first_name, last_name, email, bio, username, password, created_on, active, profile_image_url=""):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.bio = bio
        self.username = username
        self.password = password
        self.created_on = created_on
        self.active = active
        self.profile_image_url = profile_image_url