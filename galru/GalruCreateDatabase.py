from galru.DatabaseBuilder import DatabaseBuilder


class GalruCreateDatabase:
    def __init__(self, options):
        self.input_files = options.input_files
        self.output_directory = options.output_directory
        self.verbose = options.verbose
        self.threads = options.threads
        self.debug = options.debug
        self.allow_missing_st = options.allow_missing_st

    def run(self):
        database_builder = DatabaseBuilder(
            self.input_files,
            self.output_directory,
            self.verbose,
            self.threads,
            self.allow_missing_st,
            self.debug
        )

        database_builder.run()
