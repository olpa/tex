<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<!-- -->

<xsl:template match="index">
  <TeXML>
    <xsl:apply-templates/>
  </TeXML>
</xsl:template>

<xsl:template match="index_section/s">
  <xsl:if test=".!=''">
    <cmd name="IndexSectionTitle" nl2="1">
      <parm><xsl:value-of select="."/></parm>
    </cmd>
  </xsl:if>
</xsl:template>

<xsl:template match="primary">
  <cmd name="IndexPrimary" nl2="1">
    <parm><xsl:call-template name="put-refs"/></parm>
    <parm><xsl:value-of select="s"/></parm>
  </cmd>
  <xsl:apply-templates select="secondary"/>
</xsl:template>

<xsl:template match="secondary">
  <cmd name="IndexSecondary" nl2="1">
    <parm><xsl:call-template name="put-refs"/></parm>
    <parm><xsl:value-of select="s"/></parm>
  </cmd>
</xsl:template>

<xsl:template name="put-refs">
  <xsl:param name="idrefs" select="@idrefs"/>
  <xsl:choose>
    <xsl:when test="string($idrefs)=''"/>
    <xsl:when test="contains($idrefs,' ')">
      <cmd name="IndexRef">
        <parm><xsl:value-of select="substring-before($idrefs,' ')"/></parm>
      </cmd>
      <xsl:call-template name="put-refs">
        <xsl:with-param name="idrefs" select="substring-after($idrefs,' ')"/>
      </xsl:call-template>
    </xsl:when>
    <xsl:otherwise>
      <cmd name="IndexRef"><parm><xsl:value-of select="$idrefs"/></parm></cmd>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

</xsl:stylesheet>
