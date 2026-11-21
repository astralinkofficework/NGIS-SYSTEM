import urllib.request, json

req = urllib.request.Request('http://127.0.0.1:3000/api/academic/transcripts')
# In NGISAuth, how are tokens passed?
# Let's check assets/js/auth.js!
try:
    with urllib.request.urlopen(req) as res:
        print("Status:", res.status)
        print("Body:", res.read().decode())
except urllib.error.HTTPError as e:
    print("HTTP Error:", e.code)
    print("Body:", e.read().decode())
