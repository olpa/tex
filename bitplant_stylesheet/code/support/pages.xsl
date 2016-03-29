<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:fo="http://www.w3.org/1999/XSL/Format" xmlns:tch="table:conversion:helper">
<!-- -->

<xsl:variable name="turbo_default_config" select="document('')/xsl:stylesheet/x:default_config" xmlns:x="x:x:x"/>
<x:default_config xmlns:x="x:x:x">
  <use_marketing_layout>1</use_marketing_layout>
</x:default_config>

<xsl:variable name="use-hybrix-kustode-aux" select="string($config/configuration/section/item[@id='use_hybrix_kustode']/value)"/>
<xsl:variable name="use-hybrix-kustode" select="('1'=$use-hybrix-kustode-aux) or ('true'=$use-hybrix-kustode-aux) or ('yes'=$use-hybrix-kustode-aux)" />
<xsl:param name="use-hybrix-kustode" select="false()" />
<xsl:variable name="use-marketing-layout-aux" select="string($config/configuration/section/item[@id='use_marketing_2014_layout']/value | $turbo_default_config/use_marketing_layout)"/>
<xsl:variable name="use-marketing-layout" select="('1'=$use-marketing-layout-aux) or ('true'=$use-marketing-layout-aux) or ('yes'=$use-marketing-layout-aux)" />
<xsl:variable name="frontpage-context-default">lang:frontpage-operation-manual</xsl:variable>
<xsl:variable name="frontpage-context-aux" select="$config/configuration/section/item[@id='fpcontext']/value"/>
<xsl:variable name="frontpage-context">
  <xsl:choose>
    <xsl:when test="''=normalize-space($frontpage-context-aux)"><xsl:value-of select="$frontpage-context-default"/></xsl:when>
    <xsl:otherwise><xsl:value-of select="normalize-space($frontpage-context-aux)"/></xsl:otherwise>
  </xsl:choose>
</xsl:variable>

<xsl:template name="set-kustode-texts">
  <cmd name="renewcommand" nl2="1"><parm><cmd name="ConfigurationFgname" gr="0"/></parm><parm><xsl:value-of select="$config/configuration/section/item[@id='fgname']/value"/></parm></cmd>
  <cmd name="renewcommand" nl2="1"><parm><cmd name="ConfigurationFgnumber" gr="0"/></parm><parm><xsl:value-of select="$config/configuration/section/item[@id='fgnumber']/value"/></parm></cmd>
  <cmd name="renewcommand" nl2="1"><parm><cmd name="ConfigurationCodeword" gr="0"/></parm><parm><xsl:value-of select="$config/configuration/section/item[@id='codeword']/value"/></parm></cmd>
  <cmd name="renewcommand" nl2="1"><parm><cmd name="ConfigurationSerialno" gr="0"/></parm><parm><xsl:value-of select="$config/configuration/section/item[@id='machineno']/value"/><xsl:value-of select="$config/configuration/section/item[@id='serialno']/value"/></parm></cmd>
  <cmd name="renewcommand" nl2="1"><parm><cmd name="ConfigurationAuthor" gr="0"/></parm><parm><xsl:value-of select="$config/configuration/section/item[@id='author']/value"/></parm></cmd>
  <cmd name="renewcommand" nl2="1"><parm><cmd name="ConfigurationManual" gr="0"/></parm><parm><xsl:value-of select="$config/configuration/section/item[@id='manual']/value"/></parm></cmd>
  <cmd name="renewcommand" nl2="1"><parm><cmd name="ConfigurationRevision" gr="0"/></parm><parm><xsl:value-of select="$config/configuration/section/item[@id='revision']/value"/></parm></cmd>
  <cmd name="renewcommand" nl2="1"><parm><cmd name="ConfigurationAsof" gr="0"/></parm><parm><xsl:value-of select="$config/configuration/section/item[@id='asof']/value"/></parm></cmd>
  <cmd name="renewcommand" nl2="1"><parm><cmd name="ConfigurationEditor" gr="0"/></parm><parm><xsl:value-of select="$config/configuration/section/item[@id='editor']/value"/></parm></cmd>
  <cmd name="renewcommand" nl2="1"><parm><cmd name="ConfigurationTranslator" gr="0"/></parm><parm><xsl:value-of select="$config/configuration/section/item[@id='translator']/value"/></parm></cmd>
  <cmd name="renewcommand" nl2="1"><parm><cmd name="ConfigurationLanguage" gr="0"/></parm><parm><xsl:value-of select="$config/configuration/section/item[@id='language']/value"/></parm></cmd>
  <cmd name="renewcommand" nl2="1"><parm><cmd name="RunningHeaderRowI" gr="0"/></parm><parm><xsl:value-of select="$config/configuration/section/item[@id='fgname']/value"/></parm></cmd>
  <cmd name="renewcommand" nl2="1"><parm><cmd name="RunningHeaderRowII" gr="0"/></parm><parm><cmd name="rightmark" gr="0"/></parm></cmd>
  <cmd name="renewcommand" nl2="1"><parm><cmd name="BgtextKustodeRowIPartI" gr="0"/></parm><parm><xsl:value-of select="$config/configuration/section/item[@id='fgname']/value"/></parm></cmd>
  <cmd name="renewcommand" nl2="1"><parm><cmd name="BgtextKustodeRowIPartII" gr="0"/></parm><parm><xsl:value-of select="$config/configuration/section/item[@id='fgnumber']/value"/></parm></cmd>
  <cmd name="renewcommand" nl2="1">
    <parm><cmd name="ConfigurationSafetyClass" gr="0"/></parm>
    <parm>
      <xsl:variable name="sc-as-given" select="$config/configuration/section/item[@id='safetyclass']/value"/>
      <xsl:choose>
        <xsl:when test="('0' = $sc-as-given) or ('1' = $sc-as-given)">
          <xsl:call-template name="translate">
            <xsl:with-param name="id" select="concat('frontpage-safety-class-',$sc-as-given)"/>
            <xsl:with-param name="language" select="$language"/>
          </xsl:call-template>
        </xsl:when>
        <xsl:otherwise><xsl:value-of select="$sc-as-given"/></xsl:otherwise>
      </xsl:choose>
    </parm>
  </cmd>
  <cmd name="renewcommand" nl2="1">
    <parm><cmd name="ConfigurationContext" gr="0"/></parm>
    <parm>
      <xsl:choose>
        <xsl:when test="''!=substring-after($frontpage-context,'lang:')">
          <xsl:call-template name="translate">
            <xsl:with-param name="id" select="substring-after($frontpage-context,'lang:')"/>
            <xsl:with-param name="language" select="$language"/>
            <xsl:with-param name="default-value" select="''"/>
          </xsl:call-template>
        </xsl:when>
        <xsl:otherwise><xsl:value-of select="$frontpage-context"/></xsl:otherwise>
      </xsl:choose>
    </parm>
  </cmd>
  <cmd name="renewcommand" nl2="1">
    <parm><cmd name="BgtextKustodeRowIIPartI" gr="0"/></parm>
    <parm>
      <xsl:value-of select="$config/configuration/section/item[@id='editor']/value"/>
      <xsl:text> - TeXML v.</xsl:text>
      <xsl:value-of select="$VERSION"/>
    </parm>
  </cmd>
  <cmd name="renewcommand" nl2="1">
    <parm><cmd name="BgtextCreator" gr="0"/></parm>
    <parm>
      <cmd name="TeX" gr="0"/>
      <xsl:text>ML v.</xsl:text>
      <xsl:value-of select="$VERSION"/>
    </parm>
  </cmd>
  <xsl:if test="$use-hybrix-kustode">
    <cmd name="SwitchToHybrixKustode" gr="0" nl2="1"/>
  </xsl:if>
</xsl:template>

<!-- === Register === -->

<xsl:template match="Register">
  <!--<xsl:variable name="nchaptersp" select="count(/Book/Chapter)+1"/>-->
  <cmd name="RegisterPage" nl1="1" nl2="1">
    <parm>
      <xsl:for-each select="/Book/Chapter">
        <cmd name="RegisterPageItem" nl1="1" nl2="1">
          <parm><xsl:value-of select="Heading"/></parm>
        </cmd>
      </xsl:for-each>
      <xsl:if test="//IndexEntry">
        <cmd name="RegisterPageItem" nl1="1" nl2="1">
          <parm><xsl:call-template name="translate">
              <xsl:with-param name="id" select="'index'"/>
              <xsl:with-param name="language" select="$language"/>
          </xsl:call-template></parm>
        </cmd>
      </xsl:if>
    </parm>
  </cmd>
</xsl:template>

<!-- === Front page === -->

<xsl:template name="frontpage-layout-2013">
  <env name="Frontpage">
    <cmd name="FrontpageHead"><parm><xsl:value-of select="$config/configuration/section/item[@id='fgname']/value"/></parm></cmd>
    <cmd name="FrontpageHead"><parm><xsl:value-of select="$config/configuration/section/item[@id='fgnumber']/value"/></parm></cmd>
    <cmd name="FrontpageAfterhead"/>
    <cmd name="FrontpageSubHead"><parm><xsl:value-of select="$config/configuration/section/item[@id='codeword']/value"/></parm></cmd>
    <cmd name="FrontpageSubHead"><parm><xsl:value-of select="$config/configuration/section/item[@id='serialno']/value"/></parm></cmd>
    <cmd name="FrontpageSubHead"><parm></parm></cmd>
    <cmd name="FrontpageSubHead"><parm>
        <xsl:if test="'de'=$language"><xsl:text>Ausgabe: </xsl:text></xsl:if>
        <cmd name="DateYYYYmMMmmDD"/>
    </parm></cmd>
    <xsl:for-each select="Graphic">
      <cmd name="vspace"><parm>5mm</parm></cmd>
      <xsl:apply-templates select="."/>
    </xsl:for-each>
    <xsl:call-template name="generate-frontpage-keepit"/>
  </env>
</xsl:template>

<xsl:template name="generate-frontpage-keepit">
  <xsl:param name="cmdname" select="'FrontpageKeepit'"/>
  <cmd name="{$cmdname}">
    <parm><xsl:call-template name="translate">
        <xsl:with-param name="id" select="'frontpage-original-or-translation'"/>
        <xsl:with-param name="language" select="$language"/>
    </xsl:call-template></parm>
    <parm><xsl:call-template name="translate">
        <xsl:with-param name="id" select="'frontpage-save-for-reference'"/>
        <xsl:with-param name="language" select="$language"/>
    </xsl:call-template></parm>
  </cmd>
</xsl:template>

<!-- === Back page === -->

<xsl:template match="Backpage | BackPage">
  <env name="Backpage">
    <xsl:apply-templates />
  </env>
</xsl:template>

<!-- === new layout marketing-2014 === -->

<xsl:template match="/*" mode="hook-master-pages">
  <xsl:if test="$use-marketing-layout">
    <cmd name="SetMmxivPages" gr="0"/>
  </xsl:if>
</xsl:template>

<xsl:template match="/*" mode="hook-before-indocument-settings">
  <xsl:if test="$use-marketing-layout">
    <cmd name="FontProfileArial" gr="0"/>
  </xsl:if>
</xsl:template>

<xsl:template match="/*" mode="hook-after-indocument-settings">
  <xsl:if test="$use-marketing-layout">
    <xsl:if test="not($use-av-layout)">
      <cmd name="SetMmxivPages" gr="0"/>
    </xsl:if>
    <cmd name="SwitchToMmxivAdmonitions" gr="0"/>
    <cmd name="SetMmxivParagraphs" gr="0" nl2="0"/>
    <cmd name="ActivateBodyFont" gr="0" nl2="1"/>
  </xsl:if>
  <xsl:if test="$use-thomas-admonitions">
    <cmd name="SwitchToThomasAdmonitions" gr="0"/>
  </xsl:if>
</xsl:template>

<xsl:template match="FrontPage">
  <xsl:choose>
    <xsl:when test="$use-marketing-layout"><xsl:call-template name="frontpage-marketing-2014"/></xsl:when>
    <xsl:otherwise><xsl:call-template name="frontpage-layout-2013"/></xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template name="frontpage-marketing-2014">
  <xsl:variable name="nimages" select="count(Graphic)"/>
  <env name="FrontpageMmxiv">
    <cmd name="FrontpageMmxivTitle"/>
    <cmd name="FrontpageMmxivDivLine"/>
    <cmd name="FrontpageMmxivUnderTitle"/>
    <xsl:choose>
      <xsl:when test="$use-av-layout"/>
      <xsl:when test="1=$nimages">
        <cmd name="enlargethispage"><parm>30pt</parm></cmd>
        <cmd name="FrontpageMmxivOneImage">
          <parm><xsl:value-of select="Graphic/Figure/@file"/></parm>
        </cmd>
      </xsl:when>
      <xsl:when test="2=$nimages">
        <cmd name="FrontpageMmxivTwoImages">
          <parm><xsl:value-of select="Graphic[1]/Figure/@file"/></parm>
          <parm><xsl:value-of select="Graphic[2]/Figure/@file"/></parm>
        </cmd>
      </xsl:when>
      <xsl:otherwise><xsl:apply-templates select="Graphic/Figure"/></xsl:otherwise>
    </xsl:choose>
    <xsl:call-template name="generate-frontpage-keepit">
      <xsl:with-param name="cmdname" select="'FrontpageMmxivKeepit'"/>
    </xsl:call-template>
  </env>
</xsl:template>

<xsl:template name="chapter-number-presentation">
  <xsl:param name="chnum"/>
  <xsl:value-of select="$chnum"/>
  <xsl:if test="$use-marketing-layout">
    <xsl:text>.</xsl:text>
  </xsl:if>
</xsl:template>

<xsl:template name="table-without-caption">
  <cmd name="BitplantTFoot"/>
</xsl:template>

</xsl:stylesheet>
