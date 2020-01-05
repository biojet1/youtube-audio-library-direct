def make1(tbody, etree, kind, items):
	for x in items:
		mood = x.get('mood',)
		genre = x.get('genre')
		tr = etree.SubElement(tbody, "tr",)
		td = etree.SubElement(tr, "td",)
		a = etree.SubElement(td, "a",)
		a.text = x['name']
		a.attrib['href'] = x['link']
		td = etree.SubElement(tr, "td",)
		if mood and hasattr(mood, 'capitalize'):
			mood = [mood]
		if mood:
			td.text = ','.join(mood)
		td = etree.SubElement(tr, "td",)
		if genre and hasattr(genre, 'capitalize'):
			genre = [genre]
		if genre:
			td.text = ','.join(genre)
		td = etree.SubElement(tr, "td",)
		l = None
		a = x.get('artist',)
		if not a:
			pass
		elif hasattr(a, 'capitalize'):
			l = etree.SubElement(td, "span",)
			l.text = a
		elif hasattr(a[0], 'capitalize'):
			l = etree.SubElement(td, "a",)
			l.text = a[0]
			l.attrib['href'] = a[1]
		else:
			for a in x.get('artist', ''):
				if not a:
					continue
				if l:
					l.tail = ", "
				if hasattr(a, 'capitalize'):
					l = etree.SubElement(td, "span",)
					l.text = a
				else:
					l = etree.SubElement(td, "a",)
					l.text = a[0]
					l.attrib['href'] = a[1]

def enum_x(item, what, **kwargs):
	l = item.get(what)
	if not l:
		return
	elif hasattr(l, 'capitalize'):
		yield l
	else:
		for x in l:
			yield x
def html(items, **kwargs):
	from os import makedirs, listdir
	from io import BytesIO
	from lxml import etree
	data=br"""<!DOCTYPE html>
<html lang="en"><head><meta http-equiv="content-type" content="text/html; charset=UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Youtube Audio Library Direct</title></head><body>
<table>
  <tbody>
  </tbody>
</table>
</body>
</html>
"""
	from xml.etree.ElementTree import ElementTree, Element
	dom = etree.parse(BytesIO(data), etree.HTMLParser())
	root = dom.getroot()
	tbody = root.xpath(r".//tbody")[0]
	make1(tbody, etree, None, (x for x in items if not x.get("from")))
	music_html = kwargs.get('music_html', "music-all.html")
	with open(music_html, 'wb') as h:
		dom.write(h, pretty_print=True)
	genre, mood, artmap = {}, {}, {}
	for x in items:
		for a in enum_x(x, 'genre'):
			genre[a.lower()] = a
		for a in enum_x(x, 'mood'):
			mood[a.lower()] = a
		a = x.get('artist',)
		if not a:
			pass
		elif hasattr(a, 'capitalize'):
			a = [(a, a.lower())]
		elif hasattr(a[0], 'capitalize'):
			a = [a]
		for (name, _id) in a:
			artmap[_id] = name
	category = {"genre":genre, "mood":mood, "artist":artmap}
	category_json = kwargs.get('category_json', "category.json")
	from json import dump
	with open(category_json, 'w') as h:
		dump(category, h, indent=True)


# from os import chdir
# chdir('youtube-audio-library-direct')
from json import load
with open('items.json', 'r') as h:
	html(items=load(h))
