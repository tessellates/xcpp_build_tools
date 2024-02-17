class MissingFileError(Exception):
    def __init__(self, filename, generation_command):
        self.filename = filename
        self.generation_command = generation_command
        super().__init__(self.generate_message())
        
    def generate_message(self):
        return f"The required file '{self.filename}' is missing. Please run '{self.generation_command}' to generate this a default initialization of this file."
