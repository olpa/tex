<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xref="xref:xref:xref">
<!-- -->

<xsl:template match="CrossReference">
  <xsl:message>*** Unknown cross-reference format: '<xsl:value-of select="@format"/>'</xsl:message>
  <xsl:call-template name="xref-page-and-object"/>
</xsl:template>

<xsl:template name="xref-warning-if-no-target">
  <xsl:if test="not(key('id', @idref))">
    <xsl:message>*** Unresolved cross-reference: '<xsl:value-of select="@idref"/>'</xsl:message>
  </xsl:if>
</xsl:template>

<xsl:template match="CrossReference[(@format='CrossRef_Figure') or (@format='CrossRef_Table') or (@format='CrossRef_PageObj')]" name="xref-page-and-object">
  <xsl:call-template name="xref-warning-if-no-target"/>
  <cmd name="TwoPartCrossRef">
    <parm><xsl:value-of select="@idref"/></parm>
    <parm><xsl:call-template name="xref-prefixed-page-number"/></parm>
    <parm><xsl:call-template name="get-object-autotext-prefix"/></parm>
  </cmd>
</xsl:template>

<xsl:template match="CrossReference[@format='CrossRef_Chapter']">
  <xsl:call-template name="xref-warning-if-no-target"/>
  <cmd name="TwoPartCrossRef">
    <parm><xsl:value-of select="@idref"/></parm>
    <parm><xsl:call-template name="xref-prefixed-page-number"/></parm>
    <parm><xsl:call-template name="xref-prefixed-chapter-number"/></parm>
  </cmd>
</xsl:template>

<xsl:template match="CrossReference[@format='CrossRef to Object'] | CrossReference[@format='CrossRef_Figure_kurz']">
  <xsl:call-template name="xref-warning-if-no-target"/>
  <cmd name="ObjectCrossRef">
    <parm><xsl:value-of select="@idref"/></parm>
    <parm><xsl:call-template name="get-object-autotext-prefix"/></parm>
  </cmd>
</xsl:template>

<xsl:template match="CrossReference[@format='CrossRef']">
  <xsl:call-template name="xref-warning-if-no-target"/>
  <xsl:variable name="target" select="key('id', @idref)"/>
  <xsl:choose>
    <xsl:when test="$target/self::Legend"><xsl:value-of select="count($target/preceding-sibling::Legend)+1"></xsl:value-of></xsl:when>
    <xsl:otherwise>
      <cmd name="CrossReference">
        <parm><xsl:value-of select="@idref"/></parm>
        <parm></parm>
      </cmd>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template name="xref-prefixed-page-number">
  <xsl:param name="id" select="@idref"/>
  <xsl:variable name="s-prefix">
    <xsl:call-template name="translate">
      <xsl:with-param name="id" select="'number-prefix-page'"/>
      <xsl:with-param name="language" select="$language"/>
    </xsl:call-template>
  </xsl:variable>
  <TeXML ws="1">
    <xsl:call-template name="text-before-number-pos">
      <xsl:with-param name="s" select="$s-prefix"/>
    </xsl:call-template>
    <cmd name="pageref*"><parm><xsl:value-of select="$id"/></parm></cmd>
    <xsl:call-template name="text-after-number-pos">
      <xsl:with-param name="s" select="$s-prefix"/>
    </xsl:call-template>
  </TeXML>
</xsl:template>

<xsl:template name="xref-prefixed-chapter-number">
  <xsl:param name="id" select="@idref"/>
  <xsl:variable name="s-prefix">
    <xsl:call-template name="translate">
      <xsl:with-param name="id" select="'number-prefix-chapter'"/>
      <xsl:with-param name="language" select="$language"/>
    </xsl:call-template>
  </xsl:variable>
  <xsl:call-template name="text-before-number-pos">
    <xsl:with-param name="s" select="$s-prefix"/>
  </xsl:call-template>
  <xsl:call-template name="get-object-autotext-prefix"/>
  <xsl:call-template name="text-after-number-pos">
    <xsl:with-param name="s" select="$s-prefix"/>
  </xsl:call-template>
</xsl:template>

<xsl:template name="get-object-text-by-id">
  <xsl:param name="id" select="@idref"/>
  <xsl:variable name="obj" select="key('id', @idref)"/>
  <xsl:value-of select="$obj/Heading | self::Heading"/>
</xsl:template>

</xsl:stylesheet>
