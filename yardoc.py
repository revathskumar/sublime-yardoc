import sublime_plugin
import re

class YardocCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        point = self.view.sel()[0].end()
        scope = self.view.scope_name(point)
        if not re.search("source\\.ruby", scope):
            return
        line = self.read_line(point + 1)
        if not self.check_doc(point):
            return
        doc = self.compose_doc(line, edit)
        self.view.insert(edit, point, doc)

    def check_doc(self,point):
        current_line = self.read_line(point)
        params_match = re.search('#[ ]+@return|#[ ]+@param | # @author | # | # @', current_line)
        if not params_match:
            return True
        return False

    def method_doc(self,params_match,current_line):
        params = [p.strip() for p in params_match.group(1).split(',') if len(p.strip()) > 0]

        indent = re.search('(^ *)', current_line).group(0)

        lines = ["%s# @param [] %s" % (indent, param) for param in params]
        lines.insert(0, indent + "# ")
        lines.append(indent + "# ")
        lines.append(indent + "# @visibility public")
        lines.append(indent + "# @return ")

        return "\r\n" + "\r\n".join(lines)

    def class_doc(self, params_match, current_line):
        indent = re.search('(^ *)', current_line).group(0)
        lines = []
        lines.insert(0, indent + "# ")
        lines.append(indent + "# @author ")
        lines.append(indent + "# ")
        return "\r\n" + "\r\n".join(lines)

    def compose_doc(self,current_line, edit):
        params_match = re.search('def +[^ (]+[ (]*([^)]*)\)?', current_line)
        if params_match:
          return self.method_doc(params_match, current_line)
        params_match = re.search('class ', current_line)
        if params_match:
          return self.class_doc(params_match, current_line)

    def read_line(self, point):
        if (point >= self.view.size()):
            return

        next_line = self.view.line(point)
        return self.view.substr(next_line)


class AddhashtagCommand(YardocCommand):
    def run(self, edit):
        point = self.view.sel()[0].end()
        current_line = self.read_line(point)
        indent = re.search('(^ *)', current_line).group(0)
        line = "\r\n" + indent + "# "
        self.view.insert(edit, point, line)

