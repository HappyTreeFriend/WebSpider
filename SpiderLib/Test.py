from BeautifulSoup import BeautifulSoup
doc = ['<html><head><title>Page title</title><script src="http://123.js"></script></head>',
       '<body><p id="firstpara" align="center"><img src="http://123.jpg">This is paragraph <b>one</b>.',
       '<p id="secondpara" align="blah">This is paragraph <b>two<form action="login.php"></from></b>.',
       '</html>']
soup = BeautifulSoup(''.join(doc))
import pdb
pdb.set_trace()
print soup.prettify()
# <html>
#  <head>
#   <title>
#    Page title
#   </title>
#  </head>
#  <body>
#   <p id="firstpara" align="center">
#    This is paragraph
#    <b>
#     one
#    </b>
#    .
#   </p>
#   <p id="secondpara" align="blah">
#    This is paragraph
#    <b>
#     two
#    </b>
#    .
#   </p>
#  </body>
# </html>
