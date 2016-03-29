<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="*" priority="-20">
  <xsl:message>*** Unprocessed element <xsl:value-of select="name()"/></xsl:message>
  <cmd name="TODO">
    <parm>???: <xsl:value-of select="name()" /></parm>
  </cmd>
</xsl:template>

<xsl:template match="/*" mode="hook-before-document" priority="0"/>
<xsl:template match="/*" mode="hook-master-pages" priority="0"/>

<xsl:template match="/*" mode="hook-before-indocument-settings" priority="0"/>
<xsl:template match="/*" mode="hook-after-indocument-settings" priority="0"/>

</xsl:stylesheet>
