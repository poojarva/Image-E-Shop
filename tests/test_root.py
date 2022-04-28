from webapp import client

landing = client.get("/")
html = landing.data.decode()

#Testing to see if the Reset database exists
assert "<a href=\"/reset\">Reset Database!</a>" in html


