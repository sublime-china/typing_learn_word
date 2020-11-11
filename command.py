import sublime
import sublime_plugin

from .data_struct import Book, BooksManager


class TlwAddWord(sublime_plugin.TextCommand):
    def run(self, edit):
        book = Book("unpack")

        def on_done(words):
            for word in words.split("\n"):
                book.add_word(word)

        caption = "Add Word:"
        window = sublime.active_window()
        window.show_input_panel(caption, "", on_done, None, None)


class TlwRemoveWord(sublime_plugin.TextCommand):
    def run(self, edit):
        book = Book("unpack")
        words = book.get_words()

        def on_select(index):
            if index < 0:
                return
            book.remove_word(words[index])

        window = sublime.active_window()
        window.show_quick_panel(words, on_select)


class TlwRemoveAllWord(sublime_plugin.TextCommand):
    def run(self, edit):
        book = Book("unpack")
        book.remove_all_words()


class TlwCreateBook(sublime_plugin.TextCommand):
    def run(self, edit):
        print("tlw_create_book")


class TlwRemoveBook(sublime_plugin.TextCommand):
    def run(self, edit):
        print("tlw_remove_book")


class TlwTypingWord(sublime_plugin.TextCommand):
    def run(self, edit):
        self.book_manager = BooksManager()
        book_list = self.book_manager.get_book_list()
        if len(book_list) == 0:
            return
        if len(book_list) == 1:
            return self.typing_book(book_list[0])

        def on_select(index):
            if index < 0:
                return
            self.typing_book(book_list[index])

        window = sublime.active_window()
        window.show_quick_panel(book_list, on_select)

    def typing_book(self, book_name):
        window = sublime.active_window()
        view = window.new_file()
        view.set_name("Typing Learn Word")
        view.set_scratch(True)

        words = self.book_manager.get_word_by_book_name(book_name)
        settings = view.settings()
        settings.set("isTypingLearnWord", True)
        settings.set("words", words)
        settings.set("examination", words)


class TlwNewWord(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        settings = view.settings()
        examination = settings.get("examination", [])
        if len(examination) == 0:
            if sublime.ok_cancel_dialog("Try Again?"):
                settings.set("examination", settings.get("words", []))
                view.run_command("tlw_new_word")
            else:
                view.close()
            return
        word = examination.pop()
        settings.set("examination", examination)
        if view.size() == 0:
            view.insert(edit, 0, word + "\n")
        else:
            view.replace(edit, sublime.Region(0, view.size()), word + "\n")


class TlwViewEventListener(sublime_plugin.EventListener):
    def on_modified(self, view):
        settings = view.settings()
        if not settings.get("isTypingLearnWord"):
            return

        contents = view.substr(sublime.Region(0, view.size()))
        contents = contents.strip()
        result = contents.split("\n")
        if len(result) == 2:
            if result[0].strip() == result[1].strip():
                view.run_command("tlw_new_word")

    def on_new(self, view):
        sublime.set_timeout(lambda: view.run_command("tlw_new_word"), 10)
