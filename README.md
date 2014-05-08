## SublimeText package for generating Yardoc

### Installation

### With Package Control
The easiest way to install this is with [Package Control](http://wbond.net/sublime\_packages/package\_control).

   * If you just went and installed Package Control, you probably need to restart Sublime Text 2    before doing this next bit.
   * Bring up the Command Palette (Command+Shift+p on OS X, Control+Shift+p on Linux/Windows).
   * Select "Package Control: Install Package" (it'll take a few seconds)
   * Select Yardoc when the list appears.

Package Control will automatically keep Yardoc up to date with the latest version.

### Without Package Control

Go to your Sublime Text 2 **Packages** directory and clone the repository using the command below:

    git clone git@github.com:revathskumar/sublime-yardoc.git yardoc

Don't forget to keep updating it, though!

### Usage

Pressing **ctrl+enter** on the line of the method definition
```ruby
def hello a, b

end
```

results

```ruby
#
# [hello description]
# @param a [type] [description]
# @param b [type] [description]
#
# @return [type] [description]
def hello a, b

end
```

![Method yardoc](https://lh6.googleusercontent.com/-C9V-e0vzDq0/UERyoS0I4oI/AAAAAAAAG48/M2cptkMfmgA/s458/123.gif)

Pressing **ctrl+enter** on the line of the class definition

```ruby
class Hello

end
```

results

```ruby
#
# [class description]
#
# @author
#
class Hello

end
```

### Settings

Two settings are available:

```json
    // Determines if empty comment lines have a trailing space
    "trailing_spaces": false,
    // Add an initial empty line at the beginning of the comment
    "initial_empty_line": false
```

### License

```
The MIT License (MIT)
Copyright (c) 2013 Revath S Kumar

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in the
Software without restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN
AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```
