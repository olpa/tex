<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:exsl="http://exslt.org/common" extension-element-prefixes="exsl">
<!-- -->

<xsl:template name="write-outlines">
  <xsl:param name="file"/>
  <xsl:variable name="content">
    <Bookmark>
      <xsl:apply-templates select="/*" mode="outlines"/>
    </Bookmark>
  </xsl:variable>
  <exsl:document href="{$file}" method="xml">
    <xsl:copy-of select="$content"/>
  </exsl:document>
</xsl:template>

<xsl:template match="*" mode="outlines">
  <xsl:apply-templates select="*" mode="outlines"/>
</xsl:template>

<xsl:template match="Chapter | SubChapter | Section | SubSection | MinorSubSection | GenericSubSection" mode="outlines">
  <xsl:apply-templates select="Heading" mode="outlines"/>
</xsl:template>

<xsl:template match="Chapter/Heading" mode="outlines">
  <xsl:call-template name="write-outline">
    <xsl:with-param name="prefix"><xsl:call-template name="chapter-number"/></xsl:with-param>
  </xsl:call-template>
</xsl:template>

<xsl:template match="SubChapter/Heading" mode="outlines">
  <xsl:call-template name="write-outline">
    <xsl:with-param name="prefix"><xsl:call-template name="subchapter-number"/></xsl:with-param>
  </xsl:call-template>
</xsl:template>

<xsl:template match="Section/Heading" mode="outlines">
  <xsl:call-template name="write-outline">
    <xsl:with-param name="prefix"><xsl:call-template name="section-number"/></xsl:with-param>
  </xsl:call-template>
</xsl:template>

<xsl:template match="SubSection/Heading" mode="outlines">
  <xsl:call-template name="write-outline">
    <xsl:with-param name="prefix"><xsl:call-template name="subsection-number"/></xsl:with-param>
  </xsl:call-template>
</xsl:template>

<xsl:template match="MinorSubSection/Heading" mode="outlines">
  <xsl:call-template name="write-outline">
    <xsl:with-param name="prefix"><xsl:call-template name="minorsubsection-number"/></xsl:with-param>
  </xsl:call-template>
</xsl:template>

<xsl:template match="GenericSubSection/Heading" mode="outlines">
  <xsl:call-template name="write-outline">
    <xsl:with-param name="prefix"></xsl:with-param>
  </xsl:call-template>
</xsl:template>

<xsl:template name="write-outline">
  <xsl:param name="prefix"/>
  <Title Action="GoTo">
    <xsl:attribute name="Named">
      <xsl:call-template name="genid">
        <xsl:with-param name="tail">
          <xsl:if test="''!=$prefix">
            <xsl:text>head.</xsl:text><xsl:value-of select="$prefix"/>
          </xsl:if>
        </xsl:with-param>
      </xsl:call-template>
    </xsl:attribute>
    <xsl:if test="parent::Chapter">
      <xsl:attribute name="Open">false</xsl:attribute>
    </xsl:if>
    <xsl:value-of select="$prefix"/>
    <xsl:if test="'' != normalize-space($prefix)">
      <xsl:text>. </xsl:text>
    </xsl:if>
    <!-- iText1 bug: nbsp appears as euro-sign -->
    <xsl:value-of select="translate(normalize-space(.),'&#xa0;',' ')"/>
    <xsl:apply-templates select="following-sibling::*" mode="outlines"/>
  </Title>
</xsl:template>

<xsl:template match="IndexAnnex" mode="outlines">
  <Title Action="GoTo" Named="index">
    <xsl:call-template name="translate">
      <xsl:with-param name="id" select="'index'"/>
      <xsl:with-param name="language" select="$language"/>
    </xsl:call-template>
  </Title>
</xsl:template>

<xsl:template match="TableOfContents" mode="outlines">
  <Title Action="GoTo" Named="tableofcontents">
    <xsl:call-template name="translate">
      <xsl:with-param name="id" select="'table-of-contents'"/>
      <xsl:with-param name="language" select="$language"/>
    </xsl:call-template>
  </Title>
</xsl:template>

</xsl:stylesheet>
