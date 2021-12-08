"""
Deine Aufgabe ist es eine Methode chars_by_count() zu schreiben, 
welche die Zeichen in einem Text zählt. Das Ergebnis soll eine 
Liste von Tupeln sein: (ZEICHEN, ANZAHL). Die Liste soll absteigend nach ANZAHL sortiert sein. ä


https://teams.microsoft.com/l/meetup-join/19%3ameeting_ZTE2YmI4MjMtZjIwMi00NTNjLTlkZTUtNTljMTI4NmM3ZjQ1%40thread.v2/0?context=%7b%22Tid%22%3a%226bf3a84e-217a-41f4-92e7-f46eee28d414%22%2c%22Oid%22%3a%22359a17a8-47cf-4056-953e-89cac3dafb98%22%7d
https://teams.microsoft.com/l/meetup-join/19:meeting_NWRhNWY1ZDgtMWQzZC00ODgxLWI4YjMtOGFkZDYwMTc5ZWIx@thread.v2
"""

def chars_by_count(text):
	""" Returns a list of tuples that are sorted descendingly 
	by count of characters.
	"""
	result = {}
	# check empty/invalid input
	if not text or type(text) != str:
		return None
	for c in text:
		if c in result:
			result[c] += 1
		else:
			result[c] = 1
	# transform dict to sorted list of tuple
	return tuple( sorted( result.items(), key=lambda item: item[1], reverse=True) )

if __name__ == "__main__":
	text = ''' 
	Der Potsdamer Postkutscher putzt den Potsdamer Postkutschkasten 
	''' 
	print(chars_by_count(text))
	#result = chars_by_count(text)
	#assert result == [(9, 't'), (7, 's'), (6, ' '), (6, 'e'), (4, 'o'), (4, 'P'), (4, 'r'), (3, 'a'), (3, 'k'), (3, 'u'), 
	#(3, 'd'), (2, 'c'), (2, 'h'), (2, '\n'), (2, 'm'), (2, 'n'), (1, 'D'), (1, 'p'), (1, 'z')], result 
