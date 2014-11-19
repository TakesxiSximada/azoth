azoth

azoth is sqlalchemy helper library.

Install
========

::

    $ pip install azoth


How to use
===========

alembic::

    $ alembic init alembic

use azoth::

    >>> from azoth.sessions import SessionSetup, DEFAULT_TARGET
    >>> SessionSetup.setup_from_file('alembic.ini', 'alembic', DEFAULT_TARGET)
