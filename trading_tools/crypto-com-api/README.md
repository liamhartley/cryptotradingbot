# Crypto-Com API Wrapper

 [![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

In order to start pdf explorer you need:

  - Python 3.6+
  
### Installation


```sh
pip install cryptocomapi
```
 
### Sample Code

```python
from cryptocomapi import CryptoComApi
api = CryptoComApi()
print(api.get_symbols())
```
### Sample Code - API TOKEN

```python
from cryptocomapi import CryptoComApi
api = CryptoComApi(api_key="KEY_SECRET", secret_key="TOKEN_SECRET")
print(api.get_all_orders('bchbtc'))
```

### Sample Code - API TOKEN
#### Sometimes the timezone of the CryptoCom Exchange does not fit your timezone, so a quick hack is to set the offset 
#### The following code shows the initialization of the api with a 8 hour offset

```python
from cryptocomapi import CryptoComApi
api = CryptoComApi(time_offset = 8*60*60, api_key = "KEY_SECRET", secret_key = "TOKEN_SECRET")
print(api.get_open_orders('bchbtc'))
```

### Development

Want to contribute? Great!

Todos:
 - Write Tests
 - Implement Auth Section
 - Implement User Related Calls




License
----

MIT


**Free Software, Hell Yeah!**
