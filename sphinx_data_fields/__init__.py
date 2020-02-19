# "noqa" setting stops flake8 from flagging unused imports in __init__
from ._version import __version__  # noqa
from ._setup import setup
from ._example_object import ExampleDataclass


(setup, ExampleDataclass)
