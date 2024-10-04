Installation:

```
pip install git+https://github.com/ourresearch/openalex-http
```

Add line to requirements.txt:
```
git+https://github.com/ourresearch/openalex-http
```

Update:

```
pip install -U git+https://github.com/ourresearch/openalex-http
```

Uninstall:

```
pip uninstall openalex-http
```

Example usages:
```
from openalex_http.http_cache import http_get
r = http_get('https://doi.org/10.1103/PhysRevC.109.054910')
print(r.text_big())
```
