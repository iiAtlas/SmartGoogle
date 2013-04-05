import sublime, sublime_plugin
import webbrowser

def searchFor(text):
	url = "https://www.google.com/search?q=" + text.replace(" ", "+")
	webbrowser.open_new_tab(url)

def getLanguage(view):
	lang = view.settings().get('syntax')
	lang = lang[lang.find("/", lang.find("/") + 1) + 1 : lang.find(".", lang.find("/") + 1)] #strip language name from /Packages/Folder/name.tmLangauge 
	return lang

class SearchGoogleFromInputCommand(sublime_plugin.WindowCommand):
	def run(self):
		self.window.show_input_panel("Smart search Google for", getLanguage(self.window.active_view()) + " ", self.done, None, None)

	def done(self, input):
		searchFor(input)

class SearchGoogleFromSelectionCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		for selection in self.view.sel():
			if selection.empty(): text = self.view.word(selection)
			text = self.view.substr(selection)

			text = getLanguage(self.view) + " " + text

		searchFor(text)