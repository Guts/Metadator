<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
<xsl:template match="/">
	<html>
		<head>
		  <script type="text/javascript" language="javascript" src="testjs.js"/>
		</head>
		<body>
		  
		  <xsl:for-each select="testjs/js">	
		    <div>
			<xsl:attribute name="onmouseover">showMenuElement('<xsl:value-of select="@name"/>')</xsl:attribute>
			<xsl:value-of select="@name"/>
		    </div>
		  </xsl:for-each>
		  <xsl:apply-templates/>
		</body>
	</html>
</xsl:template>

<xsl:template match="description">
	<div>
	  <xsl:attribute name="id"><xsl:value-of select="../@name"/></xsl:attribute>
	  <xsl:attribute name="style">visibility:hidden; position : absolute; top : 50px; left: 50px;</xsl:attribute>
	  <xsl:apply-templates/>
	</div>
</xsl:template>
<xsl:template match="br">
	<br/>
</xsl:template>
</xsl:stylesheet>