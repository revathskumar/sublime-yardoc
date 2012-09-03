## SublimeText package for generating Yardoc

### Installation

### Without package manager

Go to your Sublime Text 2 Packages directory and clone the repository using the command below:

    git clone git@github.com:revathskumar/sublime-yardoc.git

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