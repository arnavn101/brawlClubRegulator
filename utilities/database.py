import dataset
import os


class SQL_Server():

    def __init__(self):
        self.init_database()

    def init_database(self):
        self.db = dataset.connect('sqlite:///' + os.path.join("storage_files", "pythonsqlite.db"))

    def delete_database(self):
        os.remove(os.path.join("storage_files", "pythonsqlite.db"))

    def save_database(self):
        self.db.commit()

    def insert_user(self, discord_id, player_tag):
        discord_id = str(discord_id)
        (self.db[discord_id]).insert(dict(player_tag=player_tag))

    def insert_user_warning(self, discord_id):
        discord_id = str(discord_id)
        (self.db[discord_id]).insert(dict(player_warning=1, warn="yes"))

    def append_user_warning(self, discord_id):
        discord_id = str(discord_id)
        new_warning = self.return_userWarning(discord_id) + 1
        (self.db[discord_id]).update(dict(warn="yes", player_warning=new_warning), ['warn'])

    def information_present(self, discord_id):
        discord_id = str(discord_id)
        if not self.view_information_user(discord_id):
            return False
        return True

    def returnTagUser(self, brawlStars_tag):
        list_users = self.return_allUsers()
        for user in list_users:
            if brawlStars_tag.upper() == self.view_information_user(user):
                return user
        return False

    def view_information_user(self, discord_id):
        try:
            for information in self.db[discord_id]:
                if information['player_tag'] is not None:
                    return information['player_tag']
            return False
        except Exception:
            return False

    def return_userWarning(self, discord_id):
        discord_id = str(discord_id)
        try:
            for information in self.db[discord_id]:
                if information['player_warning'] is not None:
                    return int(information['player_warning'])
            return 0
        except Exception:
            return 0

    def remove_user(self, discord_id):
        discord_id = str(discord_id)
        return self.db[discord_id].delete()

    def return_allPlayers(self):
        list_players = []
        for user in self.return_allUsers():
            if self.view_information_user(user):
                list_players.append((self.view_information_user(user)).upper())
            list_players.append((self.view_information_user(user)))
        return list_players

    def return_allUsers(self):
        return self.db.tables
