<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<!-- -->

<xsl:variable name="lang-file" select="document('lang.xml')"/>

<xsl:template name="translate">
  <xsl:param name="id"/>
  <xsl:param name="language"/>
  <xsl:param name="default-value" select="'??????'"/>
  <xsl:variable name="ret" select="$lang-file/strings/string[@id=$id]/lang[(@id=$language)]"/>
  <xsl:choose>
    <xsl:when test="$ret"><xsl:value-of select="$ret"/></xsl:when>
    <xsl:otherwise>
      <xsl:message>Can't translate ID '<xsl:value-of select="$id"/>' to language '<xsl:value-of select="$language"/>'</xsl:message>
      <xsl:value-of select="$default-value"/>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template name="text-before-number-pos">
  <xsl:param name="s"/>
  <xsl:choose>
    <xsl:when test="contains($s,'#')">
      <xsl:value-of select="substring-before($s,'#')"/>
    </xsl:when>
    <xsl:otherwise><xsl:value-of select="$s"/></xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template name="text-after-number-pos">
  <xsl:param name="s"/>
  <xsl:value-of select="substring-after($s,'#')"/>
</xsl:template>

<!-- -->

<xsl:template name="create-babel-header">
  <xsl:variable name="babel">
    <xsl:call-template name="translate">
      <xsl:with-param name="id" select="'babel'"/>
      <xsl:with-param name="language" select="$language"/>
    </xsl:call-template>
  </xsl:variable>
  <xsl:if test="normalize-space($babel)!=''">
    <cmd name="usepackage" nl2="1"><parm>polyglossia</parm></cmd>
    <xsl:call-template name="set-polyglossia-options">
      <xsl:with-param name="main" select="$babel"/>
      <xsl:with-param name="others" select="''"/>
    </xsl:call-template>
  </xsl:if>
  <xsl:variable name="FontProfile">
    <xsl:call-template name="translate">
      <xsl:with-param name="id" select="'font-profile'"/>
      <xsl:with-param name="language" select="$language"/>
    </xsl:call-template>
  </xsl:variable>
</xsl:template>

<xsl:template name="set-polyglossia-options">
  <xsl:param name="main"/>
  <xsl:param name="others"/>
  <xsl:choose>
    <xsl:when test="contains($main,',')">
      <xsl:call-template name="set-polyglossia-options">
        <xsl:with-param name="main" select="substring-after($main,',')"/>
        <xsl:with-param name="others" select="concat($others, ',', substring-before($main, ','))"/>
      </xsl:call-template>
    </xsl:when>
    <xsl:otherwise>
      <cmd name="setmainlanguage"><parm><xsl:value-of select="$main"/></parm></cmd>
      <cmd name="setotherlanguages" nl2="1"><parm><xsl:value-of select="substring-after($others,',')"/></parm></cmd>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

</xsl:stylesheet>
