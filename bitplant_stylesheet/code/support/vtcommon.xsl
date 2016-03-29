<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:fo="http://www.w3.org/1999/XSL/Format" xmlns:tch="table:conversion:helper">
<!-- -->

<xsl:import href="pages.xsl"/>
<xsl:import href="bitplant.xsl"/>

<xsl:template match="Preface[Bodytext[normalize-space()='']]">
  <env name="IntroductionPage">
    <cmd name="IntroPageMmxivFormat"/>
    <xsl:apply-templates/>
  </env>
</xsl:template>

<xsl:template match="Preface/Bodytext[normalize-space()='']">
  <cmd name="IntroPageSplitMarker"/>
</xsl:template>

</xsl:stylesheet>
