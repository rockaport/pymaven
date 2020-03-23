from enum import Enum


class Scope(Enum):
    compile = 'compile'
    provided = 'provided'
    runtime = 'runtime'
    system = 'system'
    test = 'test'
