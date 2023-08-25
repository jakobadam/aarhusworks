---
layout: post
title: "Building a RESTful Ajax App With Dojo and Python Werkzeug: The front-end"
author: Jakob Aarøe Dam
---

<em>This post is the third post in a series that demonstrate how to
create a small RESTful Ajax application leveraging the Dojo Toolkit
and Python Werkzeug. This post describes the implementation of a ajax
front-end using <a href="http://http://dojotoolkit.org/">the dojo
toolkit</a>.</em>

<p>In <a href="">part two</a> of this series we implemented a RESTful backend. In
this post we'll utilize that back-end and produce a usable UI
with <a href="http://http://dojotoolkit.org/">the dojo
toolkit</a>. The application is available
at <a href="http://letsplantheevent.appspot.com/">letsplantheevent</a>.</p>

<p>Dojo is a comprehensive versatile JavaScript toolkit which offers
about anything you can think of when it comes to JavaScript web
development. The example application takes advantage of the following
components in the toolkit:
<ul>
  <li>the <a href="http://dojocampus.org/explorer/#Dijit">comprehensive widget system</a>;</li>
  <li><a href="http://docs.dojocampus.org/dojo/data">the uniform data
  access layers</a> for a wide range of formats;</li>
  <li>the <a href="http://dojocampus.org/content/2008/06/03/understanding-dojodeclare-dojorequire-and-dojoprovide/">package
  system for JavaScript</a>; and</li>
  <li>DOM manipulation facilities.</li>
</ul>
</p>

<h2>RESTing with Dojo</h2> 
<p>Dojo includes thorough support for interacting with web
services. Especially, when it comes to RESTful JSON web services, it
requires a minimal amount of client-side code to interact with these,
because of the predefined application protocol governed by REST.</p>

<p>In dojo, we interact with a RESTful resources through
the <code>JsonRestStore</code>. In the last post, we implemented the
concept of tasks as RESTful resources. A transcript of a session with
a JavaScript interpreter interacting with those resources can look as
follows:</p>

``` javascript
dojo.require("dojox.data.JsonRestStore"); 
tasks = dojox.data.JsonRestStore({target: "/tasks/"});

// create new task, and save with POST
var t = tasks.newItem({name:"a task"});
tasks.save();

// NOTE: save is async. so you need wait here for the save to finished (or use a deferred)
t.__id; // "/tasks/1" <- from the location header in the XHR request.

// edit task and PUT it back.
t.name = "the task";
tasks.changing(t);
tasks.save();

// GET all tasks
tasks.fetch();

// GET item with specific id
tasks.fetchItemByIdentity({identity:t.__id});

// DELETE item
tasks.deleteItem(t);
```

You can tryout the example by pointing your browser
to <a href="http://letsplantheevent.appspot.com/">letsplantheevent</a>,
and paste code into your JavaScript console.

<h2>Transforming data into information with Dojo</h2>

<p>Dojo includes many different layout widgets. The cool thing with
these widgets are that they support the different dojo datastores
which all have the same uniform interface. That uniform interface
makes it possible to seamlessly wire together data and widgets.</p>

<p>For the example, we use
the <a href="http://dojocampus.org/explorer/#Dojox_Grid_Basic">data
grid</a>, which enables users to explore and edit data quickly. The
grid looks as follows, and is defined programmatically by:
</p>

``` javascript
tasks_grid = new dojox.grid.DataGrid({
  name: "tasks",
  structure: tasks_grid_structure, 
  store:tasks}, 'tasks_grid');

tasks_grid.startup();
```

In the code, the 'tasks_grid' refers to the DOM node where the grid is
injected - a standard dijit widget pattern. The structure property
defines the layout of the grid, manifested in an array of views. In
views, we take advantage of an
<a href="http://docs.dojocampus.org/dojox/grid/DataGrid">undocumented</a>
field: <code>type</code>. <code>type</code> refers to the widget that
presents the value.
<code>constraint</code> is a field used by
our <a href="https://github.com/jakobadam/letsplantheevent/blob/master/static/js/lpte/formatters.js">formatter</a>.

```javascript
  var tasks_grid_structure = [
    { 
      field: 'name',
      editable: true
    },
    {
      field: 'startdate',
      width: '70px',
      editable: true,
      type: dojox.grid.cells.DateTextBox,
      constraint: {formatLength: 'long', selector: "date"},
      formatter: lpte.formatters.datetimeFormatter
    },
    {
      field: 'starttime',
      width: '70px',
      editable: true,
      type: dojox.grid.cells.TimeTextBox,
      constraint: {timePattern: "HH:mm", selector: "time"},
      formatter: lpte.formatters.datetimeFormatter
    },
    // omitted end(time|date) for brevity
    {
      name: 'Actions',
      formatter: function(val, rowIdx, cell){
        var item = this.grid.getItem(rowIdx);
        if(!item.id){
          return "";
        }
        return "tasks.deleteById('" + item.id + "');";
      }
    }
  ];

  tasks_grid = new dojox.grid.DataGrid({
    name: "tasks",
    structure: tasks_grid_structure, 
    store:tasks}, 'tasks_grid');

  tasks_grid.startup();
```

The actions column shows a delete button when tasks have an id. On
press the button calls the function <code>tasks.deleteById</code>,
which is a function mixed into the tasks store.  

```javascript
dojo.require('dojox.data.JsonRestStore');

$.tasks = new dojox.data.JsonRestStore({
  target:"/tasks/", 
  deleteById: function(id){
    this.fetchItemByIdentity({identity: id, onItem: function(item){
      tasks.deleteItem(item);
      tasks.save();
    }});
  }
});
```
