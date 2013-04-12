import sublime, sublime_plugin
import webbrowser
from xgoogle.search import GoogleSearch, SearchError

urls = []

def searchFor(text):
	gs = GoogleSearch(text)
	gs.results_per_page = 32
	page = 1
	results = []
	titles = []
	while page < 5:
		results.extend(gs.get_results())
		page += 1
	results = results[:10]
	for res in results:
		titles.append(str(res.title.encode("utf-8")))
		urls.append(str(res.url.encode("utf-8")))

	print len(results)
	print titles

	try: sublime.active_window().show_quick_panel(titles, onSelection, sublime.MONOSPACE_FONT)
	except: webbrowser.open_new_tab("https://www.google.com/search?q=" + text.replace(" ", "+"))

def onSelection(index):
	if(index >= 0):
		webbrowser.open_new_tab(urls[index])

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