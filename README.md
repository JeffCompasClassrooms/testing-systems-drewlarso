# Squirrel Server

============================= test session starts ==============================
collected 22 items

test_squirrel_server.py:

Handle edge cases:
✓ It returns 404 when retrieving at unknown address
✓ It returns 404 when retrieving at base address
✓ It returns 404 when retrieving at non number address
✓ It cant get squirrel after deleting it
✓ It cant update squirrel after deleting it
✓ It cant delete squirrel multiple times
✓ It reuses id after deleting

Handle squirrel index:
✓ It gets empty list
✓ It gets list with one element
✓ It gets list with many elements

Handle squirrels create:
✓ It creates squirrel with valid data
✓ It returns 404 when creating squirrel at invalid address
✓ It can retrieve squirrel after creating it

Handle squirrels delete:
✓ It deletes valid squirrel
✓ It returns 404 when deleting invalid squirrel
✓ It returns 404 when deleting invalid address

Handle squirrels retrieve:
✓ It gets valid squirrel from list of one
✓ It gets valid squirrel from list of many
✓ It returns 404 on invalid squirrel

Handle squirrels update:
✓ It updates valid squirrel with valid data
✓ It returns 404 when updating invalid squirrel
✓ It returns 404 when updating invalid address

============================= 22 passed in 11.41s ==============================

# MyDB

============================= test session starts ==============================
collected 13 items

test_mydb.py:

Constructor:
✓ Db creates file if doesnt exist
✓ Db does nothing if file exists

Load strings:
✓ Db loads data when empty
✓ Db loads data with one string
✓ Db loads data with multiple strings
✓ Db loads data with multiple various types

Save string:
✓ Db saves valid string
✓ Db saves multiple valid strings
✓ Db errors when load strings doesnt return an array
✓ Save string returns nothing

Save strings:
✓ Db saves valid array
✓ Db saves arbitrary data
✓ Save strings returns nothing

============================== 13 passed in 0.03s ==============================
