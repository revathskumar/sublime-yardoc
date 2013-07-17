"""
Sublime Yardoc
by Revath S Kumar
https://github.com/revathskumar/sublime-yardoc
"""
import sublime
import sublime_plugin
import re


class YardocCommand(sublime_plugin.TextCommand):

    def load_config(self):
        self.settings = {}
        settings = sublime.load_settings('Sublime-Yardoc.sublime-settings')
        for setting in ['trailing_spaces', 'initial_empty_line']:
            if settings.get(setting) is None:
                continue
            self.settings[setting] = settings.get(setting)
        self.trailing_spaces = ""
        if settings.get('trailing_spaces'):
            self.trailing_spaces = " "

    def counter(self):
        count = 0
        while True:
            count += 1
            yield(count)

    def set_tab_index(self, doc):
        if doc:
            tabIndex = self.counter()
            for index, outputLine in enumerate(doc):
                doc[index] = re.sub("(\\$\\{)\\d+(:[^}]+\\})", lambda m: "%s%d%s" % (m.group(1),  tabIndex.next() if hasattr(tabIndex, 'next') else next(tabIndex), m.group(2)), outputLine)
        return doc

    def write(self, view, str, point):
        if None == str:
            str = self.line_ending()
        self.view.sel().clear()
        self.view.sel().add(point)
        print "New selection point: "
        print self.view.sel()
        print "write str: [" + str + "]"
        # auto_indent = self.view.settings().get('auto_indent')
        # indent_subsequent_lines = self.view.settings().get('indent_subsequent_lines')
        # print "auto_indent: "
        # print auto_indent
        # self.view.settings().set('auto_indent', False)
        # self.view.settings().set('indent_subsequent_lines', False)
        # print "auto_indent: "
        # print self.view.settings().get('auto_indent')
        # print self.view.settings().get('indent_subsequent_lines')
        self.view.run_command(
            'insert_snippet', {
                'contents': str.decode('utf-8') if hasattr(str, 'decode') else bytes(str, 'utf-8').decode('utf-8')
            }
        )
        # self.view.settings().set('auto_indent', auto_indent)
        # self.view.settings().set('indent_subsequent_lines', indent_subsequent_lines)
        # print self.view.settings().get('auto_indent')
        # print self.view.settings().get('indent_subsequent_lines')

    def run(self, edit):
        self.load_config()
        point = self.view.sel()[0].end()
        # mark = [s for s in self.view.sel()]
        # self.view.add_regions("mark", mark, "mark", "dot",
        #                       sublime.HIDDEN | sublime.PERSISTENT)
        print "Original point: " + str(point)
        scope = self.view.scope_name(point)
        if not re.search("source\\.ruby", scope):
            self.view.insert(edit, point, self.line_ending())
            return
        line = self.read_line(point)
        print "First read_line: " + line
        if not self.check_doc(line):
            self.view.insert(edit, point, self.line_ending())
            return
        doc = self.compose_doc(line, edit)
        print "Doc: [" + doc + "]"
        point = self.view.line(point).begin()
        print "New point before write: " + str(point)
        self.view.insert(edit, point, self.line_ending())
        self.write(self.view, doc, point)
        print "edit: " + str(edit)
        # self.view.erase(edit, self.view.get_regions("mark")[0])

    def check_doc(self, line):
        params_match = re.search('#\s+@return |#\s+@param |#\s+@author |# ?|#\s+@', line)
        print "params_match: " + str(params_match)
        if not params_match:
            print "check_doc return True"
            return True
        print "check_doc return False"
        return False

    def get_author(self):
        author = "${1:[author]}"
        return ["#" + self.trailing_spaces, "# @author " + author, "#" + self.trailing_spaces]

    def line_ending(self):
        ending = "\n"
        if(self.view.line_endings() == "Windows"):
            ending = "\r\n"
        return ending

    def format_lines(self, indent, lines):
        ending = self.line_ending()
        lines = self.set_tab_index(lines)
        # indent = ""
        return indent + (ending + indent).join(lines)

    def method_doc(self, params_match, current_line):
        params = [p.strip() for p in params_match.group(1).split(',') if len(p.strip()) > 0]

        indent = re.search('(^\s*)', current_line).group(0)
        print "indent: [" + indent + "]"
        # col = self.view.rowcol(self.view.sel()[0].end())[1]
        # print "col: " + str(col)

        # if(col != 0):
        #     indent = " " * (len(indent) - col)
        # print "new indent: [" + indent + "]"

        # includes all operator methods as per http://stackoverflow.com/a/10542599/120818
        method_name = re.search("def (?P<name>[a-zA-Z_][a-zA-Z_0-9]+[!?=]?|~|\+|\*\*|-|\*|/|%|<<|>>|&|\||\^|<=>|<|<=|=>|>|==|===|!=|=~|!~|!|\[\]=|\[\])", current_line).group("name")
        lines = []
        if(self.settings.get('initial_empty_line')):
            lines.append("#" + self.trailing_spaces)
        lines.append("# ${1:[%s description]}" % (method_name))

        for param in params:
            lines.append("# @param  %s [${1:type}] ${1:[description]}" % (param))

        lines.append("#" + self.trailing_spaces)
        lines.append("# @return [${1:type}] ${1:[description]}")

        return self.format_lines(indent, lines)

    def module_doc(self, current_line):
        indent = re.search('(^\s*)', current_line).group(0)
        # col = self.view.rowcol(self.view.sel()[0].end())[1]

        # if(col != 0):
        #     indent = " " * (len(indent) - col)

        lines = []
        if(self.settings.get('initial_empty_line')):
            lines.append("#" + self.trailing_spaces)
        lines.append("# ${1:[ module description]}")
        lines.extend(self.get_author())
        return self.format_lines(indent, lines)

    def class_doc(self, params_match, current_line):
        indent = re.search('(^\s*)', current_line).group(0)
        # col = self.view.rowcol(self.view.sel()[0].end())[1]

        # if(col != 0):
        #     indent = " " * (len(indent) - col)

        lines = []
        if(self.settings.get('initial_empty_line')):
            lines.append("#" + self.trailing_spaces)
        lines.append("# ${1:[ class description]}")
        lines.extend(self.get_author())
        return self.format_lines(indent, lines)

    def compose_doc(self, current_line, edit):
        params_match = re.search('def +[^ (]+[ (]*([^)]*)\)?', current_line)
        if params_match:
            return self.method_doc(params_match, current_line)
        params_match = re.search('class ', current_line)
        if params_match:
            return self.class_doc(params_match, current_line)
        params_match = re.search('module ', current_line)
        if params_match:
            return self.module_doc(current_line)

    def read_line(self, point):
        if (point >= self.view.size()):
            return

        line = self.view.line(point)
        return self.view.substr(line)


class AddhashtagCommand(YardocCommand):
    def run(self, edit):
        point = self.view.sel()[0].end()
        scope = self.view.scope_name(point)
        ending = self.line_ending()
        if not re.search("source\\.ruby", scope):
            self.view.insert(edit, point, ending)
            return
        # line = ending + "#" + self.trailing_spaces
        line = ending + "# "
        self.write(self.view, line, point)
