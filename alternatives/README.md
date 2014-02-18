# Alternate ways of using Sentry with Ckan

See also [this thread on the ckan-dev mailing-list](https://lists.okfn.org/pipermail/ckan-dev/2014-February/006863.html).

## Apache + mod_wsgi: add to .wsgi file

Start with an ``apache.wsgi`` file similar [to the example one](https://github.com/ckan/ckan-packaging/blob/master/etc/ckan/default/apache.wsgi):

```python
import os
activate_this = os.path.join('/usr/lib/ckan/default/bin/activate_this.py')
execfile(activate_this, dict(__file__=activate_this))

from paste.deploy import loadapp

config_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'production.ini')
from paste.script.util.logging_config import fileConfig
fileConfig(config_filepath)
application = loadapp('config:%s' % config_filepath)
```

Add something like this at the bottom of the file:

```python
from raven import Client
from raven.middleware import Sentry
client = Client('https://0123456789abcdef00:0123456789abcdef00000@app.getsentry.com/12345',
name='mytestinstance')
application = Sentry(application, client=client)

# this is to make sure 404 are redirected to a page that looks nice,
from pylons.middleware import StatusCodeRedirect
normally done by setting full_stack = True
application  = StatusCodeRedirect(application , [400, 404, 500])
```

And in the ckan configuration file, add this:

```ini
full_stack = false
```

> This will stop the pylons error middlewhere catching these errors and
> therefore all errors will get to sentry.
>
> IMiddlewhere would work but it would not catch all possible errors as
> its too close to the centre of the middlewhere stack.  i.e if
> repoze.who for example went wrong it would not catch it.   The above
> approach means that it catches everything as it is the outermost app.

good point.


## With gunicorn

The ``my_ckan.py`` module contains all the code needed to wrap application
in the Sentry middleware, setup logging and other goodies.

To use it:

```
gunicorn my_ckan:application --debug --log-level debug
```
