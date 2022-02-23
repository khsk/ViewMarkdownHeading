import sublime
import sublime_plugin
import os

class ViewMarkdownHeading(sublime_plugin.ViewEventListener):
    STATUS_KEY = 'md_heading'

    def __init__(self, view):
        super().__init__(view)
        self.ENABLED = False
        self.view.settings().add_on_change('syntax', self.is_target_file)
        self.is_target_file()


# バッファファイルでトリガーしないのでinitに任せる
#    def on_load_async(self):
#        print('on_load_async')

# 実用面で入力≒selectionの移動＝on_selection_modifiedなので、不満が出るまで置いておく
#    def on_modified_async(self):
#        print('mod')
#        self.main()

    def on_selection_modified_async(self):
        print('selection')
        self.main()

    def is_target_file(self):
        syntax = os.path.splitext(os.path.basename(self.view.settings().get("syntax")))[0]

        targetSyntaxs = sublime.load_settings('ViewMarkdownHeading.sublime-settings').get('target_syntaxs')
        self.ENABLED = syntax in targetSyntaxs

    def reset_md_heading_key(self):
        self.view.erase_status(ViewMarkdownHeading.STATUS_KEY)

    def set_md_heading_key(self, str):
        self.view.set_status(ViewMarkdownHeading.STATUS_KEY, str[:sublime.load_settings('ViewMarkdownHeading.sublime-settings').get("max_length")])

    def main(self):
        if self.ENABLED == False:
            self.reset_md_heading_key()
            return

        sel = self.view.sel()
        carret = sel[0].begin()
        if carret == 0:
            self.reset_md_heading_key()
            return

        self.set_md_heading_key(str(sel[0].begin()) + 'des')
        headings =  self.view.find_all('(?m)^#+\s*.*')

        if len(headings) == 0:
            self.reset_md_heading_key()
            return

        for i, heading in enumerate(headings):
            # カーソル位置より下の見出しがあれば、一つ前の見出しに属している
            if heading.begin() > carret:
                if i == 0:
                    self.reset_md_heading_key()
                    break
                self.set_md_heading_key(self.view.substr(headings[i - 1]).lstrip('#').lstrip())
                break
            # 最後まで属してなければ最後の見出しに
            if i + 1 == len(headings):
                self.set_md_heading_key(self.view.substr(headings[i]).lstrip('#').lstrip())
