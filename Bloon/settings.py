class SettingsLoader:
    def __init__(self, working_directory):
        """
        Bloon Settings Loader.
        Designated for file 'settings.txt'
        :param working_directory:
        """
        with open(working_directory + "/settings.txt", "r+") as f:
            self.raw = f.read()
        self.values = {}

        for line in self.raw.split("\n"):
            if line == "" or line.startswith(";;"):
                pass
            else:
                self.values |= {line.split("=")[0]: line.split("=")[1]}

    def get(self, k):
        return self.values.get(k)
