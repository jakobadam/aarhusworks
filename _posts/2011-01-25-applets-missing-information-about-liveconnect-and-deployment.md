---
layout: post
title: "Applets: missing information about liveconnect and deployment"
author: Jakob Aarøe Dam
---
## LiveConnect – The glue between Java and JavaScript

Did you know Java-to-JavaScript interaction is possible? This is known
as LiveConnect. LiveConnect makes it possible to use Java for things
not otherwise possible in browser environments, while still keeping
display logic in the web page in HTML/JavaScript.

<link rel="stylesheet" href="//google-code-prettify.googlecode.com/svn/trunk/src/prettify.css">
<style type="text/css">
td,th{
    border:1px solid #BEDCE7;
    background-color:#EAF2F5;
    padding: 10px 10px 10px 10px;

}
.test{
    list-style: none;
    overflow: hidden;
}
.test li{
    width: 240px;
    margin: 5px;
}
.true:before{
    content:'✓';
}
.true{
    background-repeat:no-repeat;
    background-color: #DFD;
    padding-left:25px;
    background-position:0 50%;
}
.false{
    background-color: #FDD;
    background-repeat:no-repeat;
    padding-left:25px;

}
.test .true, .test .false{
    background-position:0 50%;
}
.testtable .true, .testtable .false{
    background-position:50% 50%;
}

.icon{
background-position:0 50%;
background-repeat:no-repeat;
display:block;
float:left;
height:40px;
line-height:40px;
padding-left:50px;
}

pre.prettyprint{
border:none;
}
</style>

<p>LiveConnect is in most cases straightforward. Two examples:</p>

<pre class="prettyprint">document.getElementById('applet').uploadFile();</pre>

<p>Above the JavaScript code calls the java <code>uploadFile</code>
  method.</p>

<pre class="prettyprint">import netscape.javascript.JSObject;
public class Applet{
  public void init(){
  JSObject.getWindow(this).eval("alert('applet:init')");
  // alternative way
  // (JSOBject)(JSObject.getWindow(this).getMember('alert')).call('applet:init');
  }
}</pre>

Above the Applet upon initialization calls JavaScript
<code>alert</code>. <code>JSObject</code> is located in
<code>$JAVA_HOME/jre/lib/plugin.jar</code> on Linux/Windows, which
must be included on the classpath when compiling.
  
### The least common denominator for Cross-browser LiveConnect support

LiveConnect has been around for ages (since Netscape Navigator 3.0 and
IE4); however, some browsers do still not fully support LiveConnect!
The table underneath gives an overview of LiveConnect support in major
browsers and OSes. The table is based on a LiveConnect feature
test. The test is available at <a
href="http://jdams.org/live-connect-test">jdams.org</a> where you can
test your own browser. In the table (J) means Java-to-JavaScript, and
(JS) means JavaScript-to-Java.
  
<table class="testtable">
<tbody>
<tr>
<th><br /></th>
<th colspan="3">Linux</th>
<th colspan="3">Mac</th>
<th colspan="4">Windows</th>
</tr>
<tr>
<th>Test&nbsp;/&nbsp;
        Browser</th>
<td class="linux">Chrome</td>
<td class="linux">Firefox 3.6</td>
<td class="linux">Opera 9.8</td>
<td class="mac">Chrome</td>
<td class="mac">Firefox 3.6</td>
<td class="mac">Safari 5</td>
<td class="win">Chrome</td>
<td class="win">Firefox 3.6</td>
<td class="win">IE 6</td>
<td class="win">Safari 5</td>
</tr>
<tr>
<td>Mayscript param not required</td>
<td class="linux chrome true"><br /></td>
<td class="linux firefox true"><br /></td>
<td class="linux opera true"><br /></td>
<td class="mac chrome true"><br /></td>
<td class="mac firefox false"><br /></td>
<td class="mac safari true"><br /></td>
<td class="win chrome true"><br /></td>
<td class="win firefox true"><br /></td>
<td class="win ie6 true"><br /></td>
<td class="win safari true"><br /></td>
</tr>
<tr>
<td>JSObject != null</td>
<td class="linux chrome true"><br /></td>
<td class="linux firefox true"><br /></td>
<td class="linux opera true"><br /></td>
<td class="mac chrome true"><br /></td>
<td class="mac firefox true"><br /></td>
<td class="mac safari true"><br /></td>
<td class="win chrome true"><br /></td>
<td class="win firefox true"><br /></td>
<td class="win ie6 true"><br /></td>
<td class="win safari true"><br /></td>
</tr>
<tr>
<td>(J) <code>getMember</code></td>
<td class="linux chrome true"><br /></td>
<td class="linux firefox true"><br /></td>
<td class="linux opera true"><br /></td>
<td class="mac chrome true"><br /></td>
<td class="mac firefox true"><br /></td>
<td class="mac safari true"><br /></td>
<td class="win chrome true"><br /></td>
<td class="win firefox true"><br /></td>
<td class="win ie6 true"><br /></td>
<td class="win safari true"><br /></td>
</tr>
<tr>
<td>(J) <code>setMember</code></td>
<td class="linux chrome true"><br /></td>
<td class="linux firefox true"><br /></td>
<td class="linux opera true"><br /></td>
<td class="mac chrome true"><br /></td>
<td class="mac firefox true"><br /></td>
<td class="mac safari true"><br /></td>
<td class="win chrome true"><br /></td>
<td class="win firefox true"><br /></td>
<td class="win ie6 true"><br /></td>
<td class="win safari true"><br /></td>
</tr>
<tr>
<td>(J) <code>getMember</code> nested object call fct on it</td>
<td class="linux chrome true"><br /></td>
<td class="linux firefox true"><br /></td>
<td class="linux opera true"><br /></td>
<td class="mac chrome true"><br /></td>
<td class="mac firefox true"><br /></td>
<td class="mac safari true"><br /></td>
<td class="win chrome true"><br /></td>
<td class="win firefox true"><br /></td>
<td class="win ie6 true"><br /></td>
<td class="win safari true"><br /></td>
</tr>
<tr>
<td>(J) <code>call</code> null args</td>
<td class="linux chrome true"><br /></td>
<td class="linux firefox true"><br /></td>
<td class="linux opera true"><br /></td>
<td class="mac chrome true"><br /></td>
<td class="mac firefox false"><br /></td>
<td class="mac safari true"><br /></td>
<td class="win chrome true"><br /></td>
<td class="win firefox true"><br /></td>
<td class="win ie6 true"><br /></td>
<td class="win safari true"><br /></td>
</tr>
<tr>
<td>(J) <code>call</code> empty args</td>
<td class="linux chrome true"><br /></td>
<td class="linux firefox true"><br /></td>
<td class="linux opera true"><br /></td>
<td class="mac chrome true"><br /></td>
<td class="mac firefox false"><br /></td>
<td class="mac safari true"><br /></td>
<td class="win chrome true"><br /></td>
<td class="win firefox true"><br /></td>
<td class="win ie6 true"><br /></td>
<td class="win safari true"><br /></td>
</tr>
<tr>
<td>(J) <code>call</code> prim. arg</td>
<td class="linux chrome true"><br /></td>
<td class="linux firefox true"><br /></td>
<td class="linux opera true"><br /></td>
<td class="mac chrome true"><br /></td>
<td class="mac firefox true"><br /></td>
<td class="mac safari true"><br /></td>
<td class="win chrome true"><br /></td>
<td class="win firefox true"><br /></td>
<td class="win ie6 true"><br /></td>
<td class="win safari true"><br /></td>
</tr>
<tr>
<td>(J) <code>call</code> java object arg</td>
<td class="linux chrome true"><br /></td>
<td class="linux firefox true"><br /></td>
<td class="linux opera true"><br /></td>
<td class="mac chrome true"><br /></td>
<td class="mac firefox true"><br /></td>
<td class="mac safari false"><br /></td>
<td class="win chrome true"><br /></td>
<td class="win firefox true"><br /></td>
<td class="win ie6 true"><br /></td>
<td class="win safari true"><br /></td>
</tr>
<tr>
<td>(J) <code>call</code> with prim. return value</td>
<td class="linux chrome true"><br /></td>
<td class="linux firefox true"><br /></td>
<td class="linux opera true"><br /></td>
<td class="mac chrome true"><br /></td>
<td class="mac firefox true"><br /></td>
<td class="mac safari true"><br /></td>
<td class="win chrome true"><br /></td>
<td class="win firefox true"><br /></td>
<td class="win ie6 true"><br /></td>
<td class="win safari true"><br /></td>
</tr>
<tr>
<td>(J) <code>call</code> with obj. return value</td>
<td class="linux chrome true"><br /></td>
<td class="linux firefox true"><br /></td>
<td class="linux opera false"><br /></td>
<td class="mac chrome true"><br /></td>
<td class="mac firefox true"><br /></td>
<td class="mac safari true"><br /></td>
<td class="win chrome true"><br /></td>
<td class="win firefox true"><br /></td>
<td class="win ie6 true"><br /></td>
<td class="win safari true"><br /></td>
</tr>
<tr>
<td>(J) call with <code>eval</code></td>
<td class="linux chrome true"><br /></td>
<td class="linux firefox true"><br /></td>
<td class="linux opera true"><br /></td>
<td class="mac chrome true"><br /></td>
<td class="mac firefox true"><br /></td>
<td class="mac safari true"><br /></td>
<td class="win chrome true"><br /></td>
<td class="win firefox true"><br /></td>
<td class="win ie6 true"><br /></td>
<td class="win safari true"><br /></td>
</tr>
<tr>
<td>(J) call with <code>eval</code> return value</td>
<td class="linux chrome true"><br /></td>
<td class="linux firefox true"><br /></td>
<td class="linux opera true"><br /></td>
<td class="mac chrome true"><br /></td>
<td class="mac firefox true"><br /></td>
<td class="mac safari true"><br /></td>
<td class="win chrome true"><br /></td>
<td class="win firefox true"><br /></td>
<td class="win ie6 true"><br /></td>
<td class="win safari true"><br /></td>
</tr>
<tr>
<td>(JS) get prim. java member</td>
<td class="linux chrome true"><br /></td>
<td class="linux firefox true"><br /></td>
<td class="linux opera true"><br /></td>
<td class="mac chrome true"><br /></td>
<td class="mac firefox true"><br /></td>
<td class="mac safari true"><br /></td>
<td class="win chrome true"><br /></td>
<td class="win firefox true"><br /></td>
<td class="win ie6 true"><br /></td>
<td class="win safari true"><br /></td>
</tr>
<tr>
<td>(JS) Java Strings are converted to JavaScript strings</td>
<td class="linux chrome true"><br /></td>
<td class="linux firefox true"><br /></td>
<td class="linux opera true"><br /></td>
<td class="mac chrome true"><br /></td>
<td class="mac firefox true"><br /></td>
<td class="mac safari false"><br /></td>
<td class="win chrome true"><br /></td>
<td class="win firefox true"><br /></td>
<td class="win ie6 true"><br /></td>
<td class="win safari true"><br /></td>
</tr>
<tr>
<td>(JS) get object java member</td>
<td class="linux chrome true"><br /></td>
<td class="linux firefox true"><br /></td>
<td class="linux opera true"><br /></td>
<td class="mac chrome true"><br /></td>
<td class="mac firefox false"><br /></td>
<td class="mac safari false"><br /></td>
<td class="win chrome true"><br /></td>
<td class="win firefox true"><br /></td>
<td class="win ie6 true"><br /></td>
<td class="win safari false"><br /></td>
</tr>
</tbody>
</table>

The tests show that applets using LiveConnect must avoid parsing
  complex objects back and forth and using <code>call</code>. If
  complex objects are needed they should be converted to a JSON string
  or similar before returning them to JavaScript from Java or vice
  versa. Luckily, the <code>call</code> method is superfluous
  since <code>eval</code> is available and working.
  
### Plugin2: Maybe someday it gets easier

Java Plugin 2 (introduced in <a
href="http://www.oracle.com/technetwork/java/javase/plugin2-142482.html">1.6_10</a>)
solves many of the issues above. Only problem: Plugin2 is not
available on the Mac! Until then or until all browser vendors fix the
bugs, we have to stick with the lowest common denominator working
feature set.

### Signed applets

Applets, like all other client-code in browsers, is running under
restrictions of the browser security model (<a
href="http://code.google.com/p/browsersec/wiki/Part2">Browser Security
Handbook, part 2</a>). For example, applets can't access the file
system, or make requests to cross-domains. That is, unless the applet
is signed.

LiveConnect, however, degrades the security status of signed applet to
unsigned. This is because unsigned code (JavaScript) interacts with
signed code (Java). Fortunately, it is possible to elevate the
privileges again:

<pre><code class="prettyprint">
try {
    AccessController.doPrivileged(new PrivilegedExceptionAction() {
        public Object run() throws Exception {
            // do stuff
            return null;
        }
    });
} catch (PrivilegedActionException e) {
    Exception ex = e.getException();
    // ...
}
</code></pre>

## Deploying Applets 

<em>Goto <a href="./live-connect-test">live-connect-test</a> for
different deployment examples</em></p>

There are numerous different applet deployment tags: the
<code>applet</code> tag; the Mozilla-only <code>embed</code> tag; or
the <code>object</code> tag. The <code>applet</code> tag was
deprecated in HTML4.01 (<a
href="http://www.w3.org/TR/html401/struct/objects.html#h-13.4">spec</a>)
in favor for the generic object inclusion tag <code>object</code>.

Oracle claims that Applets deployed with <code>object</code> is not
widely supported (<a
href="http://download.oracle.com/javase/7/docs/technotes/guides/plugin/developer_guide/using_tags.html">Java
plug-in developer guide</a>). This is, however, not the case for
modern browsers. The only tag needed to deploy applets is
<code>object</code>!

Three parameters are essential for the object tag:

* <code>archive</code>: space separated list of jar files;
* <code>code</code>: fully qualified name of the aplet class; and
* <code>codebase</code>: base URI for archive and code.

In addition, three attributes are essential:

* <code>type</code> (required): must be the mimetype of applets, i.d., <code>application/x-java-applet</code>
* <code>width</code> and <code>height</code>: specifies the display size of the applet.

With these things in mind, there are two deployment options for deploying applets with static HTML:

<pre class="prettyprint">&lt;!-- with class files located individually under the applet directory. --&gt;
&lt;object type="application/x-java-applet"&gt;
  &lt;param name="codebase"  value="/applet" /&gt;
  &lt;param name="code"      value="AppletTest" /&gt;
  &lt;param name="mayscript" value="true" /&gt;
&lt;/applet&gt;</pre>

<pre class="prettyprint">&lt;!-- with class files jarred. --&gt;
&lt;object type="application/x-java-applet" &gt;
  &lt;param name="code"      value="AppletTest" /&gt;
  &lt;param name="archive"   value="/applet.jar" /&gt;
  &lt;param name="mayscript" value="true" /&gt;
&lt;/object&gt;</pre>

Dependencies to third-party libraries are specified either in the <code>archive</code> parameter or in the manifest of the JARed applet, e.g.,

<pre>Manifest-Version: 1.0
Class-Path: lib.jar lib2.jar</pre>

Third-party JARs are resolved relative to the URI of the JAR
referencing them. In this case that means all JAR files (lib.jar and
lib2.jar) must be located in the same directory as the applet jar.

<em>Deployment caveats</em>

<ul>
    <li>The <code>mayscript</code> parameter must be present in
  Firefox Mac since LiveConnect otherwise is disabled.
    </li>
    <li>On Firefox Mac LiveConnect is initialized when your make the
  first reference to any applet, e.g.,
  by <code>document.getElementById('appid')</code>. An unfortunate side effect
  of that is the following: If the applet is included in the page via
  plain HTML, references to JSObject in the applet are initially <code>null</code>!
  The easy fix is to always inject the applet into the DOM via a
  script.</li>
    <li>In Chrome if the size of the applet is set to zero (<code>width="0" height="0"</code>)
    the applet is not loaded (<a href="http://code.google.com/p/chromium/issues/detail?id=51392">bug</a>).</li>
    <li>Chrome issues an superfluous erroneous request for the Java
    class specified via the <code>code</code> parameter (<a href="http://code.google.com/p/chromium/issues/detail?id=71525">bug</a>).</li></ul>
Taking the caveats into consideration makes the cross-browser LiveConnect and HTML valid approach to deploy applets the following:

<pre>  <code class="prettyprint">
&lt;script&gt;
  document.getElementById('someid').innerHTML += [
  '&lt;object type="application/x-java-applet" width="1" height="1"&gt;',
    '&lt;param name="code" value="AppletTest"&gt;&lt;/param&gt;',
    '&lt;param name="archive" value="/applet.jar"&gt;&lt;/param&gt;',
    '&lt;param name="id" value="1"&gt;&lt;/param&gt;',
  '&lt;/object&gt;'].join('\n');
&lt;/script&gt;</code></pre>
  
During development I recommend bypassing all the caching mechanisms by adding a time stamp to the jar URL. The deployment code then becomes:

<pre><code class="prettyprint">&lt;script&gt;
  document.getElementById('someid').innerHTML += [
  '&lt;object type="application/x-java-applet" width="1" height="1"&gt;',
    '&lt;param name="code" value="AppletTest"&gt;&lt;/param&gt;',
    '&lt;param name="archive" value="/applet.jar?v=' + new Date().getTime() + '"&gt;&lt;/param&gt;',
    '&lt;param name="id" value="1"&gt;&lt;/param&gt;',
  '&lt;/object&gt;'].join('\n');
&lt;/script&gt;</code></pre>
  
Note: Deployment is also possible with a script from oracle: <a href="//www.java.com/js/deployJava.txt"><code>deployJava.js</code></a>. Two things are suboptimal with <code>deployJava.js</code>

<ul>
      <li>it uses <code>document.write</code> to write applet tags to
  the DOM. That makes it impossible to lazy load the applet; and,
      </li>
      <li>it injects the applet into the DOM with the
      deprecated <code>applet</code> tag.</li></ul>

<script src="//google-code-prettify.googlecode.com/svn/trunk/src/prettify.js"></script>
<script>
document.onload = prettyPrint();
</script>
