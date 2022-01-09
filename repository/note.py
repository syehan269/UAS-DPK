class Note:
    def __init__(self) -> None:
        self.__task = [
            {
                'id': 1,
                'title': 'Lorem 1',
                'date': '09-12-2021',
                'content': """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."""
            },
            {
                'id': 2,
                'title': 'Lorem 2',
                'date': '10-12-2021',
                'content': """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."""
            },
            {
                'id': 3,
                'title': 'Lorem 3',
                'date': '11-12-2021',
                'content': """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."""
            },
            {
                'id': 4,
                'title': 'Lorem 4',
                'date': '13-12-2021',
                'content': """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. """
            }
        ]

    """get all the notes"""

    def get_data(self) -> dict:
        self.sort_data('DESC')

        return self.__task

    """ get note using ID"""

    def get_data_by_id(self, id) -> dict:
        for item in self.__task:
            if item['id'] == int(id):
                return item

    """insert new note"""

    def insert_data(self, payload) -> dict:
        self.__task.append(payload)
        return self.get_data()

    """sort notes by date"""

    def sort_data(self, direction='ASC') -> dict:
        self.__task.sort(
            key=lambda i: i['date'], reverse=True if direction == 'ASC' else False)

    """update note"""

    def update_data(self, id, payload) -> list:
        id = int(id)

        for index, item in enumerate(self.__task):
            if item['id'] == id:
                task = self.__task[index]

                task['title'] = payload['title']
                task['content'] = payload['content']

                return self.__task[index]

        return False

    """delete note using ID"""

    def delete_data(self, id) -> bool:
        id = int(id)

        for index, item in enumerate(self.__task):
            if item['id'] == id:
                del self.__task[index]
                return True

        return False
