<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:udhr="http://www.unhchr.ch/udhr">
<!-- -->

<xsl:template match="/">
  <TeXML>
    <xsl:call-template name="latex-header"/>
    <xsl:apply-templates/>
  </TeXML>
</xsl:template>

<xsl:template match="*">
  <xsl:message>*** Unprocessed XML element <xsl:value-of select="local-name()"/></xsl:message>
</xsl:template>

<xsl:template match="udhr:udhr">
  <env name="document">
    <cmd name="UseParaDefault" gr="0" nl2="1" />
    <xsl:apply-templates/>
  </env>
</xsl:template>

<xsl:template match="udhr:article | udhr:preamble">
  <xsl:apply-templates/>
</xsl:template>

<xsl:template match="udhr:udhr/udhr:title">
  <cmd name="HeadI" nl2="1">
    <parm><xsl:apply-templates/></parm>
  </cmd>
</xsl:template>

<xsl:template match="udhr:preamble/udhr:title | udhr:article/udhr:title">
  <spec cat="nl?"/>
  <spec cat="comment"/>
  <spec cat="nl"/>
  <cmd name="HeadII" nl2="1">
    <parm><xsl:apply-templates/></parm>
  </cmd>
</xsl:template>

<xsl:template match="udhr:para">
  <env name="para" nl2="0" nl3="0">
    <xsl:if test="parent::udhr:listitem">
      <xsl:attribute name="nl1">0</xsl:attribute>
      <xsl:attribute name="nl4">0</xsl:attribute>
    </xsl:if>
    <xsl:apply-templates/>
  </env>
</xsl:template>

<xsl:template match="udhr:listitem/udhr:para">
  <xsl:apply-templates/>
</xsl:template>

<xsl:template match="udhr:orderedlist">
  <env name="udhrlist">
    <xsl:apply-templates/>
  </env>
</xsl:template>

<xsl:template match="udhr:listitem">
  <cmd name="listitem" nl2="1">
    <parm><xsl:value-of select="1+count(preceding-sibling::udhr:listitem)"/></parm>
    <parm><xsl:apply-templates select="*"/></parm>
  </cmd>
</xsl:template>

<xsl:template name="latex-header">
<TeXML escape="0" ws="1">\documentclass[a5paper]{article}
\usepackage{paravesp}
\usepackage{paras}
\usepackage[english]{babel}
\usepackage{hyperref}
</TeXML>
</xsl:template>

</xsl:stylesheet>
