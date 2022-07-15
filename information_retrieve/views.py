from django.shortcuts import render
from django.conf import settings
import os
import json
from django.shortcuts import render
from django.views import View
from django.contrib import messages
from .forms import KeywordSearchForm, UploadFileForm
from parsivar import Normalizer, Tokenizer, FindStems
from os.path import exists
from timeit import default_timer

dict={}
class ReadDocument(View):
	template_name = "information_retrieve/indexing.html"
	def get(self, request):
		list_stop_words = []
		def stop_words():
			file_stop_words = os.path.join(settings.BASE_DIR, 'file_project/stop.txt')
			stop_words = open(file_stop_words, encoding="utf8")
			stop_words.seek(0)
			for i in stop_words:
				list_stop_words.append(i.replace("\n", ""))
		list_normal_prefix = []
		def normal_prefix():
			file_normal_prefix = os.path.join(settings.BASE_DIR, 'file_project/normal_prefix.txt')
			normal_prefix = open(file_normal_prefix, encoding="utf8")
			for i in normal_prefix:
				list_normal_prefix.append(i.replace("\n", ""))

		def elim():
			file_punc = os.path.join(settings.BASE_DIR, 'file_project/elim.txt')
			punc = open(file_punc, encoding="utf8")
			result = []
			for i in punc.readlines():
				result.append(i.replace("\n", ""))
			return result

		dict = {}

		def read_document():
			file_dict = os.path.join(settings.BASE_DIR, 'document')
			number_dic = os.listdir(file_dict)
			stop_words()
			normal_prefix()
			for doc in range(0, len(number_dic)):
				tokeniz(doc)

		def tokeniz(doc):
			list_elim = elim()
			file = open(f"./document/{doc}.txt", encoding="utf8")
			text = file.read()
			normal = Normalizer()
			my_tokenizer = Tokenizer()
			text_normal = normal.normalize(text)
			words = my_tokenizer.tokenize_words(text_normal)
			length = len(words)
			for i in range(0, length):
				if (words[i] in list_elim):
					words[i] = words[i].replace(words[i], "")
				else:
					for j in list_elim:
						if j in words[i]:
							words[i] = words[i].replace(j, "")

			tokens_without_sw = [
				word.replace("\u200c", " ")
				for word in words
				if (not word in list_stop_words) and (word != "")
			]

			my_stemmer = FindStems()
			tokens_without_suffix = [
				my_stemmer.convert_to_stem(word) for word in tokens_without_sw
			]

			tokens_without_prefix = []
			for token in tokens_without_suffix:
				for item in list_normal_prefix:
					if token.startswith(item):
						token = token.replace(item, "")
				tokens_without_prefix.append(token)

			for word in tokens_without_prefix:
				if word in dict:
					if dict[word].count(doc) > 0:
						continue
					else:
						dict[word].append(doc)
				if word not in dict:
					dict[word] = [doc]

		read_document()

		with open('file_project/dictionary.txt', 'w', encoding="unicode_escape") as f:
			f.write(json.dumps(dict))
		print(dict)
		return render(request, self.template_name, {"dict": dict})





class FormView(View):
	form_class = KeywordSearchForm
	template_name = "information_retrieve/forms.html"

	def get(self, request):
		form = self.form_class

		return render(request, self.template_name, {'form': form})

	def post(self, request):
		if request.method == 'POST':
			form = self.form_class(request.POST)
			if form.is_valid():
				cd = form.cleaned_data

				def AND(x, y):
					list1 = []
					i = 0
					j = 0
					while (i <= x.__len__() - 1) & (j <= y.__len__() - 1):
						if (x[i] == y[j]):
							list1.append(x[i])
							i += 1
							j += 1
						elif (x[i] < y[j]):
							i += 1
						else:
							j += 1
					return list1

				def OR(x, y):
					list1 = []
					i = 0
					j = 0
					while (i <= x.__len__() - 1) & (j <= y.__len__() - 1):
						if (x[i] == y[j]):
							list1.append(x[i])
							i += 1
							j += 1
						elif (x[i] < y[j]):
							list1.append(x[i])
							i += 1
						else:
							list1.append(y[j])
							j += 1
					while (i <= x.__len__() - 1):
						list1.append(x[i])
						i += 1
					while (j <= y.__len__() - 1):
						list1.append(y[j])
						j += 1
					return list1
				with open('file_project/dictionary.txt', 'r', encoding="unicode_escape") as f:
					dict1 = json.load(f)

				while (1):
					query = cd['keyword']
					if (query.find("&") != -1 ):
						try:
							token1 = query[0:query.find("&") - 1]
							token2 = query[query.find("&") + 2:]
							list_id1 = dict1[token1]
							list_id2 = dict1[token2]
							return render(request, self.template_name, {'form': form, 'context': AND(list_id1, list_id2)})
						except:
							return render(request, self.template_name, {'form': form, 'context': '[]'})
					elif (query.find("|") != -1):
						try:
							token1 = query[0:query.find("|") - 1]
							token2 = query[query.find("|") + 2:]
							list_id1 = dict1[token1]
							list_id2 = dict1[token2]


							return render(request, self.template_name, {'form': form, 'context':OR(list_id1, list_id2)})
						except:
							return render(request, self.template_name, {'form': form, 'context': '[]'})
					else:
						if query!="":
							try:
								return render(request, self.template_name, {'form': form, 'context': dict1[query]})
							except:
								return render(request, self.template_name, {'form': form, 'context': '[]'})
						else:
							return render(request, self.template_name, {'form': form, 'context': '[]'})
			return render(request, self.template_name, {'form': form})


class FormTwo(View):
	form_class = UploadFileForm
	template_name = "information_retrieve/form_two.html"

	def get(self, request):
		form = self.form_class
		return render(request, self.template_name, {'form': form})

	def post(self, request):
		if request.method == 'POST':
			form = self.form_class(request.POST, request.FILES,)
			form.save()
			messages.success(request, 'اضافه کردن فایل با موفقیت انجام شد', 'success')
			return render(request, self.template_name, {'form': form})
