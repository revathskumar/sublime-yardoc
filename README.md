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

Pressing **ctrl+enter** on the previous line of method definition

    def hello a, b

    end

results

    #
    # [hello description]
    # @param  a [type] [description]
    # @param  b [type] [description]
    #
    # @return [type] [description]
    def hello a, b

    end

![Method yardoc](https://lh6.googleusercontent.com/-C9V-e0vzDq0/UERyoS0I4oI/AAAAAAAAG48/M2cptkMfmgA/s458/123.gif)

Pressing **ctrl+enter** on the previous line of class definition

    class Hello

    end

results

    #
    # @author
    #
    class Hello

    end

### License

Please see [licence](http://github.com/revathskumar/sublime-yardoc/blob/master/LICENSE)