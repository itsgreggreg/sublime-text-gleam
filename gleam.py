import os
import os.path
import re
import sublime
import sublime_plugin
import subprocess



#### COMMAND ####


class GleamFormatCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        gleam_format = find_gleam_executable(self.view)

        if gleam_format == None:
            return

        region = sublime.Region(0, self.view.size())
        content = self.view.substr(region)

        stdout, stderr = subprocess.Popen(
            [gleam_format, 'format', '--stdin'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=os.name=="nt").communicate(input=bytes(content, 'UTF-8'))

        if stderr.strip():
            open_panel(self.view, re.sub('\x1b\[\d{1,2}m', '', stderr.strip().decode()))
        else:
            self.view.replace(edit, region, stdout.decode('UTF-8'))
            self.view.window().run_command("hide_panel", {"panel": "output.gleam_format"})



#### ON SAVE ####


class GleamFormatOnSave(sublime_plugin.EventListener):
    def on_pre_save(self, view):
        scope = view.scope_name(0)
        if scope.find('source.gleam') != -1 and needs_format(view):
            view.run_command('gleam_format')


def needs_format(view):
    settings = sublime.load_settings('gleam-format-on-save.sublime-settings')
    on_save = settings.get('on_save', True)

    if isinstance(on_save, bool):
        return on_save

    if isinstance(on_save, dict):
        path = view.file_name()
        included = is_included(on_save, path)
        excluded = is_excluded(on_save, path)
        if isinstance(included, bool) and isinstance(excluded, bool):
            return included and not excluded

    open_panel(view, invalid_settings)
    return False


def is_included(on_save, path):
    if "including" in on_save:
        if not isinstance(on_save.get("including"), list):
            return None

        for string in on_save.get("including"):
            if string in path:
                return True

        return False

    return True


def is_excluded(on_save, path):
    if "excluding" in on_save:
        if not isinstance(on_save.get("excluding"), list):
            return None

        for string in on_save.get("excluding"):
            if string in path:
                return True

        return False

    return False



#### EXPLORE PATH ####


def find_gleam_executable(view):
    settings = sublime.load_settings('gleam.sublime-settings')
    given_path = settings.get('absolute_path')
    if given_path != None and given_path != '':
        if isinstance(given_path, str) and os.path.isabs(given_path) and os.access(given_path, os.X_OK):
            return given_path

        open_panel(view, bad_absolute_path)
        return None

    # shutil.which('gleam-format', mode=os.X_OK) # only available in Python 3.3
    exts = os.environ['PATHEXT'].lower().split(os.pathsep) if os.name == 'nt' else ['']
    for directory in os.environ['PATH'].split(os.pathsep):
        for ext in exts:
            path = os.path.join(directory, 'gleam' + ext)
            if os.access(path, os.X_OK):
                return path

    open_panel(view, cannot_find_gleam_format())
    return None



#### ERROR MESSAGES ####


def open_panel(view, content):
    window = view.window()
    panel = window.create_output_panel("gleam_format")
    panel.set_read_only(False)
    panel.run_command('erase_view')
    panel.run_command('append', {'characters': content})
    panel.set_read_only(True)
    window.run_command("show_panel", {"panel": "output.gleam_format"})



#### ERROR MESSAGES ####


def cannot_find_gleam_format():
    return """-- GLEAM NOT FOUND -----------------------------------------------

I tried run gleam format, but I could not find gleam on your computer.

NOTE: Your PATH variable led me to check in the following directories:

    """ + '\n    '.join(os.environ['PATH'].split(os.pathsep)) + """

But I could not find `gleam` in any of them.
"""


invalid_settings = """-- INVALID SETTINGS ---------------------------------------------------

The "on_save" field in your settings is invalid.

For help, check out the section on including/excluding files within:

  https://github.com/evancz/gleam-format-on-save/blob/master/README.md

-----------------------------------------------------------------------
"""


bad_absolute_path = """-- INVALID SETTINGS ---------------------------------------------------

The "absolute_path" field in your settings is invalid.

I need the following Python expressions to be True with the given path:

    os.path.isabs(absolute_path)
    os.access(absolute_path, os.X_OK)

Is the path correct? Do you need to run "chmod +x" on the file?

-----------------------------------------------------------------------
"""

