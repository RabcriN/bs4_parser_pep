from enum import Enum


class ParserOutput(Enum):

    PRETTY = 'pretty'
    FILE = 'file'

    @classmethod
    def choices(cls):
        return tuple([item.value for item in cls])


class ParserMode(Enum):

    whats_new = 'whats-new'
    latest_versions = 'latest-versions'
    download = 'download'
    pep = 'pep'

    @classmethod
    def modes(cls):
        return [item.value for item in cls]
