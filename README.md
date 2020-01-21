# Verisign NameStudio API

This is a very barebones Python API for interacting with Verisign's [NameStudio](https://www.namestudioapi.com) API.

At the moment the only endpoint implemented here is the `bulk-check` call to check domain availability.

### Basic Use

```python
>>> from namestudio import NameStudioAPI
>>> ns = NameStudioAPI(api_key="****")
>>> ns.bulk_check(['whalesalad.com', 'google.com'])
([{'name': 'whalesalad.com', 'availability': 'registered'}, {'name': 'google.com', 'availability': 'registered'}], <Response [200]>)

```

A tuple of `(results, response)` is returned where the `response` is the raw [Requests](https://requests.readthedocs.io/en/master/) response object.

You can use unpacking or destructuring to get just what you want:

```python
>>> results, response = ns.bulk_check(['whalesalad.com', 'google.com'])
>>> import pprint
>>> pprint.pprint(results)
[{'availability': 'registered', 'name': 'whalesalad.com'},
 {'availability': 'registered', 'name': 'google.com'}
```


### TODO

This was ripped out of an existing project to get re-used in a sibling project. It was not designed from the ground up for open source release, so ther are quite a few things missing.

- Tests
- Additional API methods
- An improved design for exception handling
