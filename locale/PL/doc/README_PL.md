#Metadator

Outil WINDOWS de création automatisée de fiches de métadonnées d'après des shapefiles (information géographique). Plusieurs formats de sortie : html, word, excel et xml (ISO 19139).

##HISTORIQUE

Metadator est un petit programme sans prétention, développé dans le cadre d’un projet de recherche de l'[IRD](http://www.perou.ird.fr/la-recherche/programmes-de-recherche/pacivur) afin d’automatiser la création de fiches de métadonnées de shapefiles. La thématique des métadonnées est souvent aussi complexe qu’essentielle. Il s’agissait donc de disposer d’un petit outil simple pour produire des catalogues de métadonnées dignes de ce nom dans un contexte (le Pérou) peu habitué à renseigner les données. Il est fortement inspiré d’un script écrit en python par [Pierre Vernier] (https://github.com/pvernier) qui s’appelait alors `Data Inspector`.


##PRECISIONS ET PRECAUTIONS

Le programme, créé à partir de 6 mois d’apprentissage de Python, n’a aucune autre prétention que de faciliter la vie du « sigiste » de tous les jours. La qualité du code est d’ailleurs certainement déplorable pour les développeurs avertis ! Il a cependant l’avantage de nous faciliter énormément le travail et d’encourager la création de métadonnées. C’est parce-que je pense qu’il peut (peut-être) dépanner d’autres personnes que je le mets à disposition. 
Merci de votre indulgence qui ne doit pas interdire les commentaires et critiques constructives bien sûr.


##PRINCIPE

Metadator traite par lot les shapefiles présents dans une arborescence en en extrayant les informations techniques de base et en se basant sur des profils personnalisables pour créer des fiches de métadonnées en différents formats :
* HTML transformé en Word 2003/2007 (.doc/.docx)
* Tableur Excel 2003 (.xls)
* Document .XML selon standard ISO19139

Les métadonnées en sortie sont évidemment incomplètes. Le programme n’est là que pour préparer et faciliter le travail. Les modèles de sortie ont été réalisés en fonction de nos exigences professionnelles. Le principe étant d’avoir à modifier, mettre en page ou supprimer des informations techniques (caractéristiques techniques, statistiques de base, etc.), plutôt que d’avoir à en rajouter, chercher, calculer. À l’utilisateur de juger ensuite de la pertinence de telle ou telle information. On considère que les couches d’information à traiter sont prêtes à être transmises et répondent donc à un minimum d’exigences.


##DEUX VERSIONS (dans le dossier downloads) :

###Version script :

Utilisation plus souple mais nécessite des prérequis importants :
- `Windows` XP SP3 ou plus
- `Microsoft Word 2003 ou plus`
- `Python 2.7.x` : http://www.python.org/download/releases/2.7
- Modules python installables depuis [PyPi](http://pypi.python.org) ou [le site de Christoph Gohlke](http://www.lfd.uci.edu/~gohlke/pythonlibs):
	+ `GDAL/OGR` : http://www.gdal.org/ogr
	+ `Pmw` : http://pmw.sourceforge.net/doc/starting.html
	+ `Pywin32` : http://sourceforge.net/projects/pywin32/
	+ `Dateutil` : http://pypi.python.org/pypi/python-dateutil/
	+ `xlwt` : https://github.com/python-excel/xlwt
	+ `numpy` : http://numpy.scipy.org/

Il est fortement recommandé aux utilisateurs windows d'installer les différents modules via des setup exécutables téléchargeable sur le site de [Christoph Gohlke](http://www.lfd.uci.edu/~gohlke/pythonlibs) et notamment [le package Base] (http://www.lfd.uci.edu/~gohlke/pythonlibs/#base). Une fois l'archive décompressée, lancer `Metadator.py`,

###Version exécutable :

Utilisation plus facile mais plus rigide ne nécessitant que Windows et Microsoft Word. Une fois l'archive décompressée, lancer `Metadator.exe`

