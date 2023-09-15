---
layout: post
title: "Building a RESTful Ajax App With Dojo and Python Werkzeug: The back-end"
author: Jakob Aarøe Dam
---

<em>This post is the second post in a series of three that demonstrate
how to create a small RESTful Ajax application leveraging the Dojo
Toolkit and Python Werkzeug. This post describes the implementation of a
RESTful back-end.</em>

<p>We're not the first building a RESTful web
service. <a href="http://a-series-of-tubes.appspot.com/">Tubes</a> is
a useful small library on top of Python Werkzeug that helps create
such services with a minimal amount of coding effort.</p>

Down to business. Our back-end consist of two files:
<ul>
  <li>views.py: holding the
  task <a href="http://docs.djangoproject.com/en/dev/topics/http/views/">views</a>
  of the application; and</li>
  <li>models.py: holding a task model.</li>
</ul>

The task model is depicted underneath.

```python
@tubes.JsonClass()
class Task(object):
    
    def __init__(self, name=None, startdate=None, starttime=None, enddate=None, endtime=None):
        self.name = name
        self.startdate = startdate
        self.starttime = starttime
        self.enddate = enddate
        self.endtime = endtime
```

Tubes includes a number of decorators that ease development. Our task
model is decorated with the <code>JsonClass</code>. That class adds
usefull methods that ease JSON-to-Python conversion. A quick example
of how to create and convert a task model to a JSON string.

```python
>>> Task(name="a task").to_json_str()
'{"start": null, "end": null, "name": "a task"}'
```

To convert the task model into RESTful resources we expose the model
via URIs and the methods of HTTP. In tubes again with decorators this
is really easy.

```python
import tubes
from models import Task

handler = tubes.Handler()

# For this tutorial we have an in-memory database, which is just a
# common Python dictionary.  
TASKS = {}
next_task_id = 0

@handler.post('^/tasks/?$', accepts=tubes.JSON, transform_body=Task.from_json)
def new_task(handler, task):
    global next_task_id
    task.id = next_task_id
    TASKS[task.id] = task
    next_task_id = next_task_id + 1
    headers = {'Location': handler.url + str(task.id)}
    return tubes.Response(task.to_json_str(), status=201, mimetype=tubes.JSON, headers=headers)

@handler.get('^/tasks/?')
def get_tasks(handler):
    return Task.to_json_list(TASKS.values())

@handler.get('^/tasks/(.+)/?')
def get_task(handler, id):
    if id in TASKS:
        return TASKS[id]
    return tubes.Response("task not found", 404)

@handler.put('^/tasks/(.+)/?$', accepts=tubes.JSON, transform_body=Task.from_json)
def update_task(handler, task, id):
    task.id = id
    TASKS[id] = task
    return TASKS[id]

@handler.delete('^/tasks/(.+)/?', transform_body=Task.from_json)
def remove_task(handler, id):
    if id in TASKS:
        del TASKS[id]
    else:
        return tubes.Response("task not found", 404)

if __name__ == '__main__':
    tubes.run(handler)
```

And that's it! We have now exposed the tasks model as RESTful
resources. Running <code>views.py</code> starts a development server;
and we can interact with the tasks resource.

```bash
$ python views.py
* Running on http://0.0.0.0:8000/
...
```

In the following curl is used to issue HTTP requests. Note that uninteresting 
headers are left out. 

List all resources:

```bash
curl localhost:8000/tasks/
[]
```

Create a new resource:

```bash
curl -i -H "Content-Type: application/json" -X POST -d '{"name":"a task"}' localhost:8000/tasks/
HTTP/1.0 201 CREATED
Location: http://localhost:8000/tasks/0
Content-Type: application/json
{"startdate": null, "enddate": null, "name": "a task", "starttime": null, "endtime": null, "id": 0}
```

Edit it:

```bash
 curl -i -H "Content-Type: application/json" -X PUT -d '{"name":"the task"}' localhost:8000/tasks/0
HTTP/1.0 200 OK
Content-Type: application/json
```

And delete it:

```bash
curl -X DELETE localhost:8000/tasks/0
null
```

<h3>Creating a Dojo front-end</h3> 

Dojo includes thourough support for interacting with RESTful
webservices. The only thing we have do to is point dojo to our exposed
resources and we can now do RESTful interaction with that resource
through dojo.

```javascript
dojo.require("dojox.data.JsonRestStore");
tasks = dojox.data.JsonRestStore({target: "/tasks/", idAttribute: "id"});

var t = tasks.newItem({name:"a task"});
tasks.save();

t.__id; // "/tasks/1" <- from the location header in the XHR request.
t.name = "the task";
tasks.changing(t);
tasks.save();

// fetch all tasks and write each task to log.
tasks.fetch({onItem: function(){console.log(arguments)}});

// fetch by identity
tasks.fetchItemByIdentity({identity:"1"});
```

Dojo includes many different layout widgets. The cool thing with
theese widgets is that they support the different dojo datastore. That
means we can seamless wire our RESTful resource together with the
widgets.

