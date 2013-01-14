"""
Sublime Yardoc
by Revath S Kumar
https://github.com/revathskumar/sublime-yardoc
"""
import sublime
import sublime_plugin
import re
import os
import pwd


class YardocCommand(sublime_plugin.TextCommand):

    def counter(self):
        count = 0
        while True:
            count += 1
            yield(count)

    def setTabIndex(self, doc):
        if doc:
            tabIndex = self.counter()
            for index, outputLine in enumerate(doc):
                doc[index] = re.sub("(\\$\\{)\\d+(:[^}]+\\})", lambda m: "%s%d%s" % (m.group(1), tabIndex.next(), m.group(2)), outputLine)
        return doc

    def write(self, view, str):
        view.run_command(
            'insert_snippet', {
                'contents': str.decode('utf-8')
            }
        )

    def run(self, edit):
        point = self.view.sel()[0].end()
        scope = self.view.scope_name(point)
        if not re.search("source\\.ruby", scope):
            return
        line = self.read_line(point + 1)
        if not self.check_doc(point):
            return
        doc = self.compose_doc(line, edit)
        self.write(self.view, doc)

    def check_doc(self, point):
        current_line = self.read_line(point)
        params_match = re.search('#[ ]+@return|#[ ]+@param | # @author | # | # @', current_line)
        if not params_match:
            return True
        return False

    def get_author(self):
        author = "${1:[author]}"
        if(sublime.platform() == "linux"):
            author = pwd.getpwuid(os.getuid()).pw_gecos.split(',')[0]
        return ["# ", "# @author " + author, "# "]

    def method_doc(self, params_match, current_line):
        params = [p.strip() for p in params_match.group(1).split(',') if len(p.strip()) > 0]

        indent = re.search('(^ *)', current_line).group(0)
        col = self.view.rowcol(self.view.sel()[0].end())[1]

        if(col != 0):
            indent = " " * (len(indent) - col)

        method_name = re.search("def (?P<name>[a-zA-Z_]+|[a-zA-Z_]+[!|?])(?P<params>[(| ][a-zA-Z,]+|)", current_line).group("name")
        lines = [indent + "# ", "# ${1:[%s description]}" % (method_name)]

        for param in params:
            lines.append("# @param  %s [${1:type}] ${1:[description]}" % (param))

        lines.append("# ")
        lines.append("# @return [${1:type}] ${1:[description]}")

        lines = self.setTabIndex(lines)

        return "\n" + ("\n" + indent).join(lines)

    def module_doc(self, current_line):
        indent = re.search('(^ *)', current_line).group(0)
        col = self.view.rowcol(self.view.sel()[0].end())[1]

        if(col != 0):
            indent = " " * (len(indent) - col)

        lines = [indent + "# ", "# ${1:[ module description]}"]
        lines.extend(self.get_author())
        lines = self.setTabIndex(lines)
        return "\n" + ("\n" + indent).join(lines)

    def class_doc(self, params_match, current_line):
        indent = re.search('(^ *)', current_line).group(0)
        col = self.view.rowcol(self.view.sel()[0].end())[1]

        if(col != 0):
            indent = " " * (len(indent) - col)

        lines = [indent + "# ", "# ${1:[ class description]}"]
        lines.extend(self.get_author())
        lines = self.setTabIndex(lines)
        return "\n" + ("\n" + indent).join(lines)

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

        next_line = self.view.line(point)
        return self.view.substr(next_line)


class AddhashtagCommand(YardocCommand):
    def run(self, edit):
        point = self.view.sel()[0].end()
        scope = self.view.scope_name(point)
        if not re.search("source\\.ruby", scope):
            return
        line = "\n" + "# "
        self.write(self.view, line)

