# Metadator

Terminate with painful metadata!

Tool to automatize the production of metadata files about geographic files (shapefiles, MapInfo tables, ...).  There are various different output options available: HTML, Word (.doc/.docx), Excel (.xls) and XML (ISO 19139). There is also an option to produce an unique Word indexed document like a catalog. It has been developed for a specific use in a research program of the French Institute of Research for Development ([IRD](http://en.ird.fr/)).

The goal is to make easier the adaptation to the INSPIRE norm, but also to keep a possibility to make human-readable metadata in universal formats (Word, Excel, etc.)

**THIS PROJECT IS NO LONGER ACTIVE**. To manage geographic metada, see [GeoNetwork](https://github.com/geonetwork), [Isogeo](https://github.com/isogeo) or [DicoGIS](https://github.com/Guts/DicoGIS).

## In a nutshell

Metadator does a recurring analysis into a folder structure and perform a serie of analysis and statistics. It uses 3 elements to generate the metadata:
* geographic data (SRS, geometry type, number of objects, etc.)
* statistics about fields depending on the type (integer, float, string or date)
* customizable profiles to allow the user to personalize the metadata (organization, contacts, update rhythm, INSPIRE themes, keywords, etc.)

## Two ways to use:

## On Ubuntu

```bash
sudo add-apt-repository ppa:ubuntugis/ubuntugis-unstable
sudo apt-get update && sudo apt-get dist-upgrade
sudo apt-get install python-setuptools python-pip python-dev python-tk python-gdal libxml2-dev libxslt-dev python-software-properties
git clone https://github.com/Guts/Metadator.git
sudo pip install -r requirements.txt
```

### Script (for advanced users):

Use more flexible but requires:
- `Windows` XP SP3 or more
- `Microsoft Word 2003` or more
- [`Python 2.7.x`](http://www.python.org/download/releases/2.7)
- Python libraries. Get them from [PyPi](http://pypi.python.org), or using pip install -r with the requirements.txt, or on [the website of Christoph Gohlke](http://www.lfd.uci.edu/~gohlke/pythonlibs):
	+ [`GDAL/OGR`](http://www.gdal.org/ogr)
	+ [`Pywin32`](http://sourceforge.net/projects/pywin32/)
	+ [`Dateutil`](http://pypi.python.org/pypi/python-dateutil/)
	+ [`xlwt`](https://github.com/python-excel/xlwt)
	+ [`numpy`](http://numpy.scipy.org/)

Optionally if you want to make your own executables:
- [`Microsoft Visual C++ 2008 Redistributable Package`](http://www.microsoft.com/en-us/download/details.aspx?id=29)
- [`py2exe`](http://www.py2exe.org)
	
Clone this repository or download it and then just launch Metadator.py.

### Executable (see [releases ](https://github.com/Guts/Metadator/releases) to download it):

Very easy to use due to the user-friendly interface and this is only requires Windows and Microsoft Word (tested with Office 2007 and 2010).
Just decompress the archive downloaded and then launch `Metadator.exe`.


## Create your own profiles

You can create as many profiles as you want to adapt the tool to each dataset. You can and share it easily with your colleagues.


## Internationalization

Developed first in French, the tool comes with translation in English and Spanish.

It's also possible to:

- add your own language copying and translating a locale folder (best use the FR as model). Take care about the prefix and all the INSPIRE stuffs.
- customize easily all the texts of the interface and the output files:  this is just XML! 

## Recurring attributes

Because describing the attributes (or fields) of geographic files is very important (perhaps the most to make a metadata useful and understandable) but it's a boring activity and hard to do well (worst is updating).
Above all, there is a lot of attributes we meet often and which have always the same reference/description (like FID or ID for example)! So, to make the work more efficient, customize your recurring attributes in Metadator and then it'll apply automatically the description you gave whenever it'll find the field.


### Credits
- Icons from [the noun project](http://thenounproject.com/tlb/)
