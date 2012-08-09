## SublimeText package for generating Yardoc

### Installation

### Without package manager

Go to your Sublime Text 2 Packages directory and clone the repository using the command below:

    git clone git@github.com:revathskumar/sublime-yardoc.git

Don't forget to keep updating it, though!

### Usage

Pressing **ctrl+enter** on the previous line of method definition

    def hello a,b, c

    end

results

    #
    # @param [] a
    # @param [] b
    # @param [] c
    #
    # @visibility public
    # @return
    def hello a, b, c

    end

![Method yardoc](https://lh6.googleusercontent.com/-MJw_xt1bo8s/UCNUwckhmoI/AAAAAAAAGaI/1hy2orZbpgk/s320/method-yardoc.gif)

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