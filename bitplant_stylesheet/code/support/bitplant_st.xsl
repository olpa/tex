<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<!-- -->
<xsl:import href="bitplant.xsl"/>
<xsl:param name="main_sty" select="'bitplantst'" />

<xsl:variable name="enlarge-fonts" select="normalize-space($config/configuration/section/item[@id='enlarge_fonts']/value)"/>
<xsl:variable name="kustode-text" select="normalize-space($config/configuration/section/item[@id='kustode_text']/value)"/>
<xsl:param name="use-marketing-layout" select="false()"/>
<xsl:variable name="use-timeline-layout-aux" select="string($config/configuration/section/item[@id='use_timeline_layout']/value)"/>
<xsl:variable name="use-timeline-layout" select="('1'=$use-timeline-layout-aux) or ('true'=$use-timeline-layout-aux) or ('yes'=$use-timeline-layout-aux)" />

<xsl:template name="set-kustode-texts">
  <cmd name="renewcommand" nl2="1"><parm><cmd name="ConfigurationFgname" gr="0"/></parm><parm><xsl:value-of select="$config/configuration/section/item[@id='fgname']/value"/></parm></cmd>
  <cmd name="renewcommand" nl2="1"><parm><cmd name="ConfigurationEditor" gr="0"/></parm><parm><xsl:value-of select="$config/configuration/section/item[@id='editor']/value"/></parm></cmd>
  <xsl:if test="''!=$kustode-text">
    <cmd name="ForceKustodeText" nl2="1">
      <parm>
        <xsl:choose>
          <xsl:when test="'0'=$kustode-text"></xsl:when>
          <xsl:when test="'no'=translate($kustode-text,'NO','no')"></xsl:when>
          <xsl:when test="'false'=translate($kustode-text,'FALSE','false')"></xsl:when>
          <xsl:when test="'off'=translate($kustode-text,'OF','of')"></xsl:when>
          <xsl:otherwise><xsl:value-of select="$kustode-text"/></xsl:otherwise>
          </xsl:choose>
      </parm>
    </cmd>
  </xsl:if>
</xsl:template>

<xsl:template match="/*" mode="hook-after-indocument-settings">
  <xsl:if test="$use-timeline-layout">
    <cmd name="SwitchToTimelineBook"/>
  </xsl:if>
  <xsl:apply-imports/>
  <xsl:choose>
    <xsl:when test="''=$enlarge-fonts"/>
    <xsl:when test="'0'=$enlarge-fonts"/>
    <xsl:when test="'1'=$enlarge-fonts"><cmd name="enlargeFonts"/><cmd name="ActivateBodyFont"/></xsl:when>
    <xsl:when test="'2'=$enlarge-fonts"><cmd name="enlargeFonts"/><cmd name="enlargeFonts"/><cmd name="ActivateBodyFont"/></xsl:when>
    <xsl:when test="'3'=$enlarge-fonts"><cmd name="enlargeFonts"/><cmd name="enlargeFonts"/><cmd name="enlargeFonts"/><cmd name="ActivateBodyFont"/></xsl:when>
    <xsl:when test="'4'=$enlarge-fonts"><cmd name="enlargeFonts"/><cmd name="enlargeFonts"/><cmd name="enlargeFonts"/><cmd name="enlargeFonts"/><cmd name="ActivateBodyFont"/></xsl:when>
  </xsl:choose>
</xsl:template>

<xsl:template match="PDF"/>

</xsl:stylesheet>
