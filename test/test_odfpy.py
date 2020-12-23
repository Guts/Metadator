from odf.opendocument import OpenDocumentText
from odf.text import P
textdoc = OpenDocumentText()
p = P(text="Hello World!")
textdoc.text.addElement(p)
textdoc.save("helloworld", True)