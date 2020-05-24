# Template

- Basic usage
- Basic template
- Syntax
  - output
  - comment
  - block
  - extends
  - for
  - if
  - include
  - using
- Form extend
  - form basic
  - button
  - checkbox
  - color
  - date
  - datetime
  - email
  - file
  - hidden
  - label
  - month
  - number
  - password
  - radio
  - range
  - search
  - submit
  - tel
  - text
  - textarea
  - time
  - url
  - week

## Basic usage
```
  t = Template("<html><%= val %></html>")
  print(t.render(val="XXX"))
```

`Loader` is a class that loads and caches template from a directory

```
  t = FileLoader(html_dir, debug=True).load('test.html')
  print(t.render(val="XXX"))
```
> will not cache if debug else cache


## Basic template

Syntax for the templates

```
<# base.html #>

<html>
  <head>
    <title><% block title %>Default title<% end %></title>
  </head>
  <body>
    <ul>
      <% for student in students %>
        <% block student %><% end %>
      <% end %>
    </ul>
  </body>
</html>
```

```
<# bold.html #>

<% extends "base.html" %>

<% block title %>A bolder title<% end %>

<% block student %>
  <li><%= student.name %></li>
    <% if student.age < 10 %>
      <%= 'less than 10 age' %>
    <% elif student.age == 10 %>
      <%= 'equals 10 age' %>
    <% else %>
      <%= 'great than 10 age' %>
    <% end %>
  <% end %>
<% end %>
```

## Syntax

### output
`<%= ... %>`

### comment
`<# ... #>`

### block
`<% block *name* %>...<% end %>`

### extends
`<% extends *filename* %>`

`block` and `extends` usually appear together:

```
  <!-- base.html -->
  <title>
    <% block title %>Default title<% end %>
  </title>

  <!-- mypage.html -->
  <% extends "base.html" %>
  <% block title %>My page title<% end %>
```

### for
```
  <% for *var* in *expr* %>
    ...
  <% end %>
```
Same as the python `for` statement.  `<% break %>` and `<% continue %>` may be used inside the loop.

### if
```
  <% if *condition* %>
    ...
  <% elif *condition* %>
    ...
  <% else %>
    ...
  <% end %>
```
Same as the python `if` statement    

### include
```
  <% include *filename* %>
```
Include another template file.  The included file can see all the local variables


### using
```
  <%= using *object* do *val* %>
    <%= val.xxx %>
  <% end %>
```
using a object which implement begin_render() and end_render() as val.

steps:

1. set `val` = `object`
2. val.begin_render()
3. val.xxx
4. val.end_render()

## form extend

### form basic
```
  <%= using form("/user/new", method="POST", multipart=True, remote=False) do f %>
    ...
  <% end %>
  
  # =>
    
  <form action="/user/new" method="GET" accept-charset="UTF8">
    ...
  </form>    
  
```

```  
  <%= using form("/user/new", _id="user_new_id", method="GET", multipart=True, remote=False) do f %>
    ...
  <% end %>

  # =>

  <form id="user_new_id" action="/user/new" method="GET" accept-charset="UTF8">
    ...
  </form>

```

```
  <%= using form("/user/new", method="POST", multipart=True, remote=False, html={"data-index": 10}) do f %>
    ...
  <% end %>
 
  # =>

  <form action="/user/new" method="POST" accept-charset="UTF8" enctype="multipart/form-data" data-index="10">
    ...
  </form>
```

### button
```
  <%= using form("/user/new") do f %>
    <%= f.button() %>
    <%= f.button('Reset', tp='reset') %>
    <%= f.button('Button', tp='button') %>
    <%= f.button('Reset', tp='reset', disabled=True) %>
    <%= f.button('Save', html={'data-confirm': 'Are you sure?'}) %>
    <%= f.button('Checkout', html={"data-disable-with": "Please wait..."}) %>
  <% end %>
```

The HTML generated:

```
  <form action="/user/new" method="GET" accept-charset="UTF8">
    <button name="button" type="submit">Button</button>
    <button name="button" type="reset">Reset</button>
    <button name="button" type="button">Button</button>
    <button name="button" type="reset" disabled="disabled">Reset</button>
    <button name="button" type="submit" data-confirm="Are you sure?">Save</button>
    <button name="button" type="submit" data-disable-with="Please wait...">Checkout</button>
  </form>
```

### checkbox
```
  <%= using form("/user/new") do f %>
    <%= f.checkbox('accept') %>
    <%= f.checkbox('rock', 'rock music') %>
    <%= f.checkbox('receive_email', 'yes', checked=True) %>
    <%= f.checkbox('tos', 'yes', checked=False, html={"class": 'accept_tos'}) %>
    <%= f.checkbox('eula', 'accepted', checked=False, disabled=True) %>
  <% end %>
```

The HTML generated:

```
  <form action="/user/new" method="GET" accept-charset="UTF8">
    <input id="accept" name="accept" type="checkbox" value="1" />
    <input id="rock" name="rock" type="checkbox" value="rock music" />
    <input id="receive_email" name="receive_email" type="checkbox" value="yes" checked="checked" />
    <input id="tos" name="tos" type="checkbox" value="yes" class="accept_tos" />
    <input id="eula" name="eula" type="checkbox" value="accepted" disabled="disabled" />
  </form>
```

### color
```
  <%= using form("/user/new") do f %>
    <%= f.color('name') %>
    <%= f.color('color', '#DEF726') %>
    <%= f.color('color', class_='special_input') %>
    <%= f.color('color', '#DEF726', disabled=True, class_='special_input') %>
  <% end %>
```

The HTML generated:

```
  <form action="/user/new" method="GET" accept-charset="UTF8">
    <input id="name" name="name" type="color" />
    <input id="color" name="color" type="color" value="#DEF726" />
    <input id="color" name="color" type="color" class="special_input" />
    <input id="color" name="color" type="color" value="#DEF726" disabled="disabled" 
  </form>
```

### date
```
  <%= using form("/user/new") do f %>
    <%= f.date('name') %>
    <%= f.date('date', '2020-01-01') %>
    <%= f.date('date', class_='special_input') %>
    <%= f.date('date', '2020-01-01', disabled=True, class_='special_input') %>
  <% end %>
```

The HTML generated:

```
  <form action="/user/new" method="GET" accept-charset="UTF8">
    <input id="name" name="name" type="date" />
    <input id="date" name="date" type="date" value="2020-01-01" />
    <input id="date" name="date" type="date" class="special_input" />
    <input id="date" name="date" type="date" value="2020-01-01" disabled="disabled" />
  </form>
```

### datetime
```
  <%= using form("/user/new") do f %>
    <%= f.datetime("user_born_on") %>
    <%= f.datetime("user_born_on", date(year=2020, month=1, day=1)) %>
    <%= f.datetime("user_born_on", datetime(year=2020, month=1, day=2, hour=10, minute=20, second=30)) %>
    <%= f.datetime("user_born_on", _min=date(year=2020, month=1, day=2)) %>
  <% end %>
```

The HTML:

```
  <form action="/user/new" method="GET" accept-charset="UTF8">
    <input id="user_born_on" name="user_born_on" type="datetime-local" />
    <input id="user_born_on" name="user_born_on" type="datetime-local" value="2020-01-01T00:00:00" />
    <input id="user_born_on" name="user_born_on" type="datetime-local" value="2020-01-02T10:20:30" />
    <input id="user_born_on" name="user_born_on" type="datetime-local" min="2020-01-02T00:00:00" />
  </form>
```

### email
```
  <%= using form("/user/new") do f %>
    <%= f.email('name') %>
    <%= f.email('email', 'xxx@yyy.com') %>
    <%= f.email('email', class_='special_input') %>
    <%= f.email('email', 'xxx@yyy.com', disabled=True, class_='special_input') %>
  <% end %>
```

The HTML:

```
  <form action="/user/new" method="GET" accept-charset="UTF8">
    <input id="name" name="name" type="email" />
    <input id="email" name="email" type="email" value="xxx@yyy.com" />
    <input id="email" name="email" type="email" class="special_input" />
    <input id="email" name="email" type="email" value="xxx@yyy.com" disabled="disabled" 
  </form>
```

### file
```
  <%= using form("/user/new") do f %>
    <%= f.file('attachment') %>
    <%= f.file('avatar', class_='profile_input') %>
    <%= f.file('picture', disabled=True) %>
    <%= f.file('resume', value='~/resume.doc') %>
    <%= f.file('user_pic', accept='image/png,image/gif,image/jpeg') %>
    <%= f.file('file', accept='text/html', class_='upload', value='index.html') %>
  <% end %>
```

The HTML:

```
  <form action="/user/new" method="GET" accept-charset="UTF8">
    <input id="attachment" name="attachment" type="file" />
    <input id="avatar" name="avatar" type="file" class="profile_input" />
    <input id="picture" name="picture" type="file" disabled="disabled" />
    <input id="resume" name="resume" type="file" value="~/resume.doc" />
    <input id="user_pic" name="user_pic" type="file" accept="image/png,image/gif,image/jpeg" />
    <input id="file" name="file" type="file" value="index.html" class="upload" accept="text/html" />
  </form>
```

### hidden
```
  <%= using form("/user/new") do f %>
    <%= f.hidden('tags_list') %>
    <%= f.hidden('token', 'VUBJKB23UIVI1UU1VOBVI@') %>
    <%= f.hidden('collected_input', html={"onchange": "alert('Input collected!')" }) %>
  <% end %>
```

The HTML:

```
  <form action="/user/new" method="GET" accept-charset="UTF8">
    <input id="tags_list" name="tags_list" type="hidden" />
    <input id="token" name="token" type="hidden" value="VUBJKB23UIVI1UU1VOBVI@" />
    <input id="collected_input" name="collected_input" type="hidden" onchange="alert('Input 
  </form>
```

### label
```
  <%= using form("/user/new") do f %>
    <%= f.label('name') %>
    <%= f.label('name', 'Your Name') %>
    <%= f.label('name', class_='small_label') %>
  <% end %>
```

The HTML:

```
  <form action="/user/new" method="GET" accept-charset="UTF8">
    <label for="name">Name</label>
    <label for="name">Your Name</label>
    <label for="name" class="small_label">Name</label>
  </form>
```

### month
```
  <%= using form("/user/new") do f %>
    <%= f.month("user_born_on") %>
    <%= f.month("user_born_on", "11") %>
    <%= f.month("user_born_on", _min="01") %>
  <% end %>
```

The HTML:

```
  <form action="/user/new" method="GET" accept-charset="UTF8">
    <input id="user_born_on" name="user_born_on" type="month" />
    <input id="user_born_on" name="user_born_on" type="month" value="11" />
    <input id="user_born_on" name="user_born_on" type="month" min="01" />
  </form>
```

### number
```
  <%= using form("/user/new") do f %>
    <%= f.number('quantity') %>
    <%= f.number('quantity', '1') %>
    <%= f.number('quantity', class_='special_input') %>
    <%= f.number('quantity', _min=1) %>
    <%= f.number('quantity', _max=9) %>
    <%= f.number('quantity', _min=1, _max=9) %>
    <%= f.number('quantity', _min=1, _max=9, step=2) %>
    <%= f.number('quantity', '1', class_='special_input', disabled=True) %>
  <% end %>
```

The HTML:

```
  <form action="/user/new" method="GET" accept-charset="UTF8">
    <input id="quantity" name="quantity" type="number" />
    <input id="quantity" name="quantity" type="number" value="1" />
    <input id="quantity" name="quantity" type="number" class="special_input" />
    <input id="quantity" name="quantity" type="number" min="1" />
    <input id="quantity" name="quantity" type="number" max="9" />
    <input id="quantity" name="quantity" type="number" min="1" max="9" />
    <input id="quantity" name="quantity" type="number" min="1" max="9" step="2" />
    <input id="quantity" name="quantity" type="number" value="1" disabled="disabled" class="special_input" />
  </form>
```

### password
```
  <%= using form("/user/new") do f %>
    <%= f.password('pass') %>
    <%= f.password('secret', 'Your secret here') %>
    <%= f.password('masked', class_='masked_input_field') %>
    <%= f.password('token', '', size=15) %>
    <%= f.password('key', maxlength=16) %>
    <%= f.password('confirm_pass', disabled=True) %>
    <%= f.password('pin', '1234', maxlength=4, size=6, class_="pin_input") %>
  <% end %>
```

The HTML:

```
  <form action="/user/new" method="GET" accept-charset="UTF8">
    <input id="pass" name="pass" type="password" />
    <input id="secret" name="secret" type="password" value="Your secret here" />
    <input id="masked" name="masked" type="password" class="masked_input_field" />
    <input id="token" name="token" type="password" value="" size="15" />
    <input id="key" name="key" type="password" maxlength="16" />
    <input id="confirm_pass" name="confirm_pass" type="password" disabled="disabled" />
    <input id="pin" name="pin" type="password" value="1234" size="6" maxlength="4" 
  </form>
```

### radio
```
  <%= using form("/user/new") do f %>
    <%= f.radio('favorite_color', 'maroon') %>
    <%= f.radio('receive_updates', 'no', checked=True) %>
    <%= f.radio('time_slot', "3:00 p.m.", checked=False, disabled=True) %>
    <%= f.radio('color', "green", checked=True, class_="color_input") %>
  <% end %>
```

The HTML:

```
  <form action="/user/new" method="GET" accept-charset="UTF8">
    <input id="favorite_color_maroon" name="favorite_color" type="radio" value="maroon" />
    <input id="receive_updates_no" name="receive_updates" type="radio" value="no" 
    <input id="time_slot_3:00_p.m." name="time_slot" type="radio" value="3:00 p.m." disabled="disabled" />
    <input id="color_green" name="color" type="radio" value="green" class="color_input" checked="checked" />
  </form>
```

### range
```
  <%= using form("/user/new") do f %>
    <%= f.range('quantity') %>
    <%= f.range('quantity', '1') %>
    <%= f.range('quantity', class_='special_input') %>
    <%= f.range('quantity', _in=[1, 9]) %>
    <%= f.range('quantity', _in=[1, 9], step=2) %>
    <%= f.range('quantity', '1', class_='special_input', disabled=True) %>
  <% end %>
```

The HTML:

```
  <form action="/user/new" method="GET" accept-charset="UTF8">
    <input id="quantity" name="quantity" type="range" />
    <input id="quantity" name="quantity" type="range" value="1" />
    <input id="quantity" name="quantity" type="range" class="special_input" />
    <input id="quantity" name="quantity" type="range" min="1" max="9" />
    <input id="quantity" name="quantity" type="range" min="1" max="9" step="2" />
    <input id="quantity" name="quantity" type="range" value="1" disabled="disabled" class="special_input" />
  </form>
```

### search
```
  <%= using form("/user/new") do f %>
    <%= f.search('name') %>
    <%= f.search('search', 'Enter your search query here') %>
    <%= f.search('search', None, class_='special_input') %>
    <%= f.search('search', 'Enter your search query here', class_='special_input', disabled=True) %>
  <% end %>
```

The HTML:

```
  <form action="/user/new" method="GET" accept-charset="UTF8">
    <input id="name" name="name" type="search" />
    <input id="search" name="search" type="search" value="Enter your search query here" />
    <input id="search" name="search" type="search" class="special_input" />
    <input id="search" name="search" type="search" value="Enter your search query here" disabled="disabled" class="special_input" />

  </form>
```

### submit
```
  <%= using form("/user/new") do f %>
    <%= f.submit() %>
    <%= f.submit("Edit this article") %>
    <%= f.submit( "Save edits", disabled=True) %>
    <%= f.submit("Edit", class_="edit_button") %>
    <%= f.submit( "Save", html={ 'data-confirm': "Are you sure?" }) %>
    <%= f.submit( "Complete sale", html={ 'data-disable-with': "Submitting..." }) %>
  <% end %>
```

The HTML:

```
  <form action="/user/new" method="GET" accept-charset="UTF8">
    <input name="commit" type="submit" value="Save changes" data-disable-with="Save changes" />
    <input name="commit" type="submit" value="Edit this article" data-disable-with="Edit this article" />
    <input name="commit" type="submit" value="Save edits" disabled="disabled" data-disable-with="Save edits" />
    <input name="commit" type="submit" value="Edit" class="edit_button" data-disable-with="Edit" />
    <input name="commit" type="submit" value="Save" data-confirm="Are you sure?" data-disable-with="Save" />
    <input name="commit" type="submit" value="Complete sale" data-disable-with="Submitting..." />
  </form>
```

### tel
```
  <%= using form("/user/new") do f %>
    <%= f.tel('name') %>
    <%= f.tel('tel', '0123456789') %>
    <%= f.tel('tel', class_='special_input') %>
    <%= f.tel('tel', '0123456789', class_='special_input', disabled=True) %>
  <% end %>
```

The HTML:

```
  <form action="/user/new" method="GET" accept-charset="UTF8">
    <input id="name" name="name" type="tel" />
    <input id="tel" name="tel" type="tel" value="0123456789" />
    <input id="tel" name="tel" type="tel" class="special_input" />
    <input id="tel" name="tel" type="tel" value="0123456789" disabled="disabled" class="special_input" />
  </form>
```

### text
```
  <%= using form("/user/new") do f %>
    <%= f.text('name') %>
    <%= f.text('query', 'Enter your search query here') %>
    <%= f.text('search', placeholder='Enter search term...') %>
    <%= f.text('request', class_='special_input') %>
    <%= f.text('address', '', size=75) %>
    <%= f.text('zip', maxlength=5) %>
    <%= f.text('payment_amount', '$0.00', disabled=True) %>
    <%= f.text('ip', '0.0.0.0', maxlength=15, size=20, class_="ip-input") %>
  <% end %>
```

The HTML:

```
  <form action="/user/new" method="GET" accept-charset="UTF8">
    <input id="name" name="name" type="text" />
    <input id="query" name="query" type="text" value="Enter your search query here" />
    <input id="search" name="search" type="text" placeholder="Enter search term..." />
    <input id="request" name="request" type="text" class="special_input" />
    <input id="address" name="address" type="text" value="" size="75" />
    <input id="zip" name="zip" type="text" maxlength="5" />
    <input id="payment_amount" name="payment_amount" type="text" value="$0.00" disabled="disabled" />
    <input id="ip" name="ip" type="text" value="0.0.0.0" size="20" maxlength="15" class="ip-input" />
  </form>
```

### textarea
```
  <%= using form("/user/new") do f %>
    <%= f.textarea('post') %>
    <%= f.textarea('bio', 'This is my biography.') %>
    <%= f.textarea('body', rows=10, cols=25) %>
    <%= f.textarea('description', "Description goes here.", disabled=True) %>
    <%= f.textarea('comment', class_='comment_input') %>
  <% end %>
```

The HTML:

```
  <form action="/user/new" method="GET" accept-charset="UTF8">
    <textarea id="post" name="post"></textarea>
    <textarea id="bio" name="bio">This is my biography.</textarea>
    <textarea id="body" name="body" rows="10" cols="25"></textarea>
    <textarea id="description" name="description" disabled="disabled">Description goes here.</textarea>
    <textarea id="comment" name="comment" class="comment_input"></textarea>
  </form>
```


### time
```
  <%= using form("/user/new") do f %>
    <%= f.time('created_at') %>
    <%= f.time('created_at', '1') %>
    <%= f.time('created_at', class_='special_input') %>
    <%= f.time('created_at', _min=1) %>
    <%= f.time('created_at', _max=9) %>
    <%= f.time('created_at', _min=1, _max=9) %>
    <%= f.time('created_at', _min=1, _max=9, step=2) %>
    <%= f.time('created_at', '1', class_='special_input', disabled=True) %>
  <% end %>
```

The HTML:

```
  <form action="/user/new" method="GET" accept-charset="UTF8">
    <input id="created_at" name="created_at" type="time" />
    <input id="created_at" name="created_at" type="time" value="1" />
    <input id="created_at" name="created_at" type="time" class="special_input" />
    <input id="created_at" name="created_at" type="time" min="1" />
    <input id="created_at" name="created_at" type="time" max="9" />
    <input id="created_at" name="created_at" type="time" min="1" max="9" />
    <input id="created_at" name="created_at" type="time" min="1" max="9" step="2" />
    <input id="created_at" name="created_at" type="time" value="1" disabled="disabled" class="special_input" />
  </form>   
```

### url
```
  <%= using form("/user/new") do f %>
    <%= f.url('name') %>
    <%= f.url('url', 'http://www.baidu.com') %>
    <%= f.url('url', class_='special_input') %>
    <%= f.url('url', 'http://www.baidu.com', class_='special_input', disabled=True) %>
  <% end %>
```

The HTML:

```
  <form action="/user/new" method="GET" accept-charset="UTF8">
    <input id="name" name="name" type="url" />
    <input id="url" name="url" type="url" value="http://www.baidu.com" />
    <input id="url" name="url" type="url" class="special_input" />
    <input id="url" name="url" type="url" value="http://www.baidu.com" disabled="disabled" class="special_input" />
  </form>
```


### week
```
  <%= using form("/user/new") do f %>
    <%= f.week("user_born_week") %>
    <%= f.week("user_born_week", "06") %>
    <%= f.week("user_born_week", _min="01") %>
  <% end %>

  <form action="/user/new" method="GET" accept-charset="UTF8">
    <input id="user_born_week" name="user_born_week" type="week" />
    <input id="user_born_week" name="user_born_week" type="week" value="06" />
    <input id="user_born_week" name="user_born_week" type="week" min="01" />
  </form>
```


> note:
> 
> form init can accept a argument named `model`. if do that, all form fields can set value automatically 
> 
> eg.

```
  u = User(name="Jon", created_at="Datetime('2009-10-10 20:10:05')", age=30, blog="http://www.jonblog.com", email="jon@email.com")
  t = Template("""
  <%= using form("/user/new", model=user) do f %>
    <%= f.name("name") %>
    <%= f.datetime("created_at") %>
    <%= f.number("age") %>
    <%= f.url("blog") %>
    <%= f.email("email") %>
  <% end %>
  """)
  t.render(user=u)

  <form action="/user/new" method="GET" accept-charset="UTF8">
    <input id="user_name" name="user['name']" type="text" value="Jon" />
    <input id="user_created_at" name="user['created_at']" type="datetime" value="2019-10-10T20:10:05" />
    <input id="user_age" name="user['age']" type="number" value="30" />
    <input id="user_blog" name="user['blog']" type="url" value="http://www.jonblog.com" />
    <input id="user_email" name="user['email']" type="email" value="jon@email.com" />
  </form>
```
