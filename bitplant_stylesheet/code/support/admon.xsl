<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<!-- -->

<xsl:template name="admon-set-texts">
  <xsl:call-template name="admon-set-text-for"><xsl:with-param name="for" select="'danger'"/></xsl:call-template>
  <xsl:call-template name="admon-set-text-for"><xsl:with-param name="for" select="'warning'"/></xsl:call-template>
  <xsl:call-template name="admon-set-text-for"><xsl:with-param name="for" select="'caution'"/></xsl:call-template>
  <xsl:call-template name="admon-set-text-for"><xsl:with-param name="for" select="'notice'"/></xsl:call-template>
</xsl:template>

<xsl:template name="admon-set-text-for">
  <xsl:param name="for"/>
  <cmd name="renewcommand" nl2="1">
    <parm><cmd name="zDXXXV{$for}Text" gr="0"/></parm>
    <parm>
      <xsl:call-template name="translate">
        <xsl:with-param name="id" select="$for"/>
        <xsl:with-param name="language" select="$language"/>
      </xsl:call-template>
    </parm>
  </cmd>
</xsl:template>

<xsl:template match="Note">
  <cmd name="note" nl1="1" nl2="1">
    <parm>
      <xsl:choose>
        <xsl:when test="@Info='Trouble'">t</xsl:when>
        <xsl:when test="@Info='Question'">q</xsl:when>
        <xsl:when test="@Info='Information'" >i</xsl:when>
        <xsl:when test="@Info='Environment'">e</xsl:when>
        <xsl:otherwise>
          <xsl:message>Unknown value of the attribute Note/@Info: '<xsl:value-of select="@Info"/>'</xsl:message>
          <xsl:text>i</xsl:text>
        </xsl:otherwise>
      </xsl:choose>
    </parm>
    <parm>
      <xsl:apply-templates select="NoteBody/NoteRow/NoteContent"/>
    </parm>
  </cmd>
</xsl:template>

<xsl:template match="NoteContent">
  <env name="BodyText" nl1="0" nl2="0" nl3="0" nl4="0"><xsl:apply-templates/></env>
</xsl:template>

<xsl:template name="SafetyAdviceLight">
  <xsl:param name="textcode" select="'notice'"/>
  <cmd name="SafetyAdviceLight" nl1="1" nl2="1">
    <parm>
      <xsl:call-template name="translate">
        <xsl:with-param name="id" select="$textcode"/>
        <xsl:with-param name="language" select="$language"/>
      </xsl:call-template>
    </parm>
    <parm>
      <xsl:apply-templates select="SafetyBodyLight/SafetyRowLight/SafetyContent"/>
    </parm>
  </cmd>
</xsl:template>

<xsl:template match="SafetyAdviceLight">
  <xsl:call-template name="SafetyAdviceLight"/>
</xsl:template>

<xsl:template match="SafetyContent">
  <xsl:apply-templates />
</xsl:template>

<xsl:template match="SafetyAdvice" name="SafetyAdvice">
  <cmd name="SafetyAdvice" nl1="1" nl2="1">
    <parm>
      <xsl:choose>
        <xsl:when test="@Classification='Warning'">w</xsl:when>
        <xsl:when test="@Classification='Danger'" >d</xsl:when>
        <xsl:when test="@Classification='Caution'">c</xsl:when>
        <xsl:otherwise>
          <xsl:message>Unknown value of the attribute SafetyAdvice/@Classification: '<xsl:value-of select="@Classification"/>'</xsl:message>
          <xsl:text>w</xsl:text>
        </xsl:otherwise>
      </xsl:choose>
    </parm>
    <parm>
      <xsl:call-template name="translate">
        <xsl:with-param name="id" select="translate(@Classification,'WDC','wdc')"/>
        <xsl:with-param name="language" select="$language"/>
      </xsl:call-template>
    </parm>
    <parm><xsl:value-of select="SafetyBody/SafetyRow/SafetyPictoContent/SafetyPicto/@file"/></parm>
    <parm>
      <xsl:apply-templates select="SafetyBody/SafetyRow/SafetyContent" mode="with-divider"/>
    </parm>
  </cmd>
</xsl:template>

<xsl:template match="SafetyContent" mode="with-divider">
  <xsl:apply-templates select="*" mode="with-divider"/>
</xsl:template>

<xsl:template match="*" mode="with-divider">
  <xsl:if test="(position()&gt;1) and (name()!=name(preceding-sibling::*[1]))">
    <cmd name="AdmonHrule" nl2="1"/>
  </xsl:if>
  <xsl:apply-templates select="."/>
</xsl:template>

<xsl:template match="Consequences">
  <env name="BodyText" nl2="0" nl3="0"><xsl:apply-templates/></env>
</xsl:template>

<xsl:template match="SourceOfDanger">
  <env name="SourceOfDanger" nl1="0" nl2="0" nl3="0"><xsl:apply-templates/></env>
</xsl:template>

</xsl:stylesheet>
