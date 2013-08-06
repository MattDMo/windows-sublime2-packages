"""
TextCommand:
    insert_timetamp
EventListener:
    on_pre_save: update_timestamp
"""
import datetime
import sublime_plugin

TIMESTAMP_PATTERN = 'FILE_CHANGED_ON\\s*=\\s*[\'"]201[0-9]-\\d+-\\d+\\s+\\d+:\\d+:\\d+(\\.\\d+)?[\'"]'


class InsertTimestampCommand(sublime_plugin.TextCommand):
    """
    Replace selection with a current timestamp in ISO format.
    """
    def run(self, edit, **args):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 2013-07-18 15:00:55
        # formatting options at http://docs.python.org/2/library/datetime.html#strftime-strptime-behavior
        self.view.replace(edit, self.view.sel()[0], timestamp)


class TimeStampListener(sublime_plugin.EventListener):
    """
    Search for a timestamp to update before saving the file.
    Maybe to simple.
    """
    def on_pre_save(self, view):
        region = view.find(TIMESTAMP_PATTERN, 1)
        if region:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            replacement = 'FILE_CHANGED_ON = "%s"' % timestamp
            edit = view.begin_edit()
            view.replace(edit, region, replacement)
            view.end_edit(edit)
