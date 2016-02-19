<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
    xmlns:saxon="http://icl.com/saxon" 
    extension-element-prefixes="saxon">

<!-- 
This stylesheet splits a Template-Designer container file and saves each template definition in a separate file.

It makes use of the currently proprietary element output, which requires saxon as xsl processor.
Xslt 2.0 includes this element in general, but python or xsltproc are not able to parse this element.
-->

	<xsl:template match="designer">
		<xsl:for-each select="template">
			<saxon:output href="{@name}.xml">
				<xsl:copy-of select="." />
			</saxon:output>
		</xsl:for-each>
	</xsl:template>

</xsl:stylesheet>