<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:fo="http://www.w3.org/1999/XSL/Format" xmlns:tch="table:conversion:helper"  xmlns:exsl="http://exslt.org/common" extension-element-prefixes="exsl">
<!-- -->
<xsl:import href="unprocessed.xsl"/>
<xsl:import href="lang.xsl"/>
<xsl:import href="pdfoutlines.xsl"/>
<xsl:import href="admon.xsl" />
<xsl:import href="pages.xsl" />
<xsl:import href="version.xsl" />
<xsl:import href="xref.xsl" />

<xsl:variable name="default_config" select="document('')/xsl:stylesheet/x:default_config" xmlns:x="x:x:x"/>
<x:default_config xmlns:x="x:x:x">
  <language>en</language>
  <text_width>135mm</text_width>
  <show_variant_borders>0</show_variant_borders>
</x:default_config>

<xsl:param name="generate-chapter-toc" select="false()"/>

<xsl:param name="main_sty" select="'bitplant'" />
<xsl:variable name="config" select="document('../configuration.xml', /)" />
<xsl:variable name="language" select="$config/configuration/section/item[@id='language']/value" />
<xsl:variable name="text_width" select="$config/configuration/section/item[@id='text_width']/value | $default_config/text_width" />

<xsl:param name="dev">0</xsl:param>
<xsl:variable name="show-variant-borders-aux" select="string($config/configuration/section/item[@id='show_variant_borders']/value | $default_config/show_variant_borders)"/>
<xsl:variable name="show-variant-borders" select="('1'=$show-variant-borders-aux) or ('true'=$show-variant-borders-aux) or ('yes'=$show-variant-borders-aux)" />
<xsl:param name="outlines_file"/>
<xsl:param name="indexterms_file_basename"/>
<xsl:variable name="use-color-aux" select="string($config/configuration/section/item[@id='use_color']/value)"/>
<xsl:variable name="use-color" select="('1'=$use-color-aux) or ('true'=$use-color-aux) or ('yes'=$use-color-aux)" />
<xsl:variable name="use-av-layout-aux" select="string($config/configuration/section/item[@id='use_av_layout']/value)"/>
<xsl:variable name="use-av-layout" select="('1'=$use-av-layout-aux) or ('true'=$use-av-layout-aux) or ('yes'=$use-av-layout-aux)" />
<xsl:variable name="use-usa-paper-aux" select="string($config/configuration/section/item[@id='use_usa_paper']/value)"/>
<xsl:variable name="use-usa-paper" select="('1'=$use-usa-paper-aux) or ('true'=$use-usa-paper-aux) or ('yes'=$use-usa-paper-aux)" />
<xsl:variable name="ansizDXXXV-aux" select="string($config/configuration/section/item[@id='ansizDXXXV']/value)"/>
<xsl:variable name="ansizDXXXV" select="('1'=$ansizDXXXV-aux) or ('true'=$ansizDXXXV-aux) or ('yes'=$ansizDXXXV-aux)" />
<xsl:variable name="join-admonitions" select="$ansizDXXXV"/>
<xsl:variable name="hyphenation-aux" select="string($config/configuration/section/item[@id='hyphenation']/value)"/>
<xsl:variable name="disable-hyphenation" select="('0'=$hyphenation-aux) or ('false'=$hyphenation-aux) or ('no'=$hyphenation-aux)" />
<xsl:variable name="use-thomas-admonitions-aux" select="string($config/configuration/section/item[@id='use_thomas_admonitions']/value)"/>
<xsl:variable name="use-thomas-admonitions" select="('1'=$use-thomas-admonitions-aux) or ('true'=$use-thomas-admonitions-aux) or ('yes'=$use-thomas-admonitions-aux)" />
<xsl:variable name="use-twoside-layout-aux" select="string($config/configuration/section/item[@id='use_twoside_layout']/value)"/>
<xsl:variable name="use-twoside-layout" select="('1'=$use-twoside-layout-aux) or ('true'=$use-twoside-layout-aux) or ('yes'=$use-twoside-layout-aux)" />

<xsl:param name="MoreLatexHead"></xsl:param>

<xsl:key name="id" match="*[@id]" use="@id"/>
<xsl:key name="span" match="entry[@tch:span]" use="@tch:span"/>

<!-- entry point, catch-all, LaTeX header -->
<xsl:template match="/*">
  <xsl:variable name="FontProfile2">
    <xsl:call-template name="translate">
      <xsl:with-param name="id" select="'font-profile'"/>
      <xsl:with-param name="language" select="$language"/>
    </xsl:call-template>
  </xsl:variable>
  <TeXML>
    <xsl:call-template name="latex-header" />
    <xsl:apply-templates select="." mode="hook-before-document"/>
    <env name="document">
      <xsl:apply-templates select="." mode="hook-before-indocument-settings"/>
      <cmd nl2="1">
        <xsl:attribute name="name">
          <xsl:choose>
            <xsl:when test="normalize-space($FontProfile2)=''">FontProfileLatin</xsl:when>
            <xsl:when test="substring-after($FontProfile2,'??')!=''">FontProfileLatin</xsl:when>
            <xsl:otherwise><xsl:value-of select="$FontProfile2"/></xsl:otherwise>
          </xsl:choose>
        </xsl:attribute>
      </cmd>
      <xsl:if test="contains($FontProfile2,'Chinese') or contains($FontProfile2,'Korean') or contains($FontProfile2,'Japanese')">
        <cmd name="XeTeXlinebreaklocale" gr="0"/>
        <xsl:text>"</xsl:text>
        <xsl:value-of select="$language"/>
        <xsl:text>"</xsl:text>
        <cmd name="relax" nl2="1" gr="0"/>
      </xsl:if>
      <xsl:if test="contains($FontProfile2, 'Arabian')">
        <cmd name="setRTL" nl2="1" gr="0"/>
      </xsl:if>
      <cmd name="ActivateBodyFont" gr="0" nl2="1"/>
      <xsl:if test="$disable-hyphenation">
<TeXML escape="0" ws="1">\lefthyphenmin=62\relax
\righthyphenmin=62\relax
%\raggedright
\emergencystretch=2cm\relax
\setlength\overfullrule{0pt}
</TeXML>
      </xsl:if>
      <xsl:apply-templates select="." mode="hook-after-indocument-settings"/>
      <xsl:call-template name="set-kustode-texts"/>
      <xsl:apply-templates select="/*/*" />
    </env>
  </TeXML>
  <xsl:call-template name="write-outlines">
    <xsl:with-param name="file" select="$outlines_file"/>
  </xsl:call-template>
</xsl:template>

<xsl:template match="Chapter">
  <xsl:if test="$generate-chapter-toc">
    <xsl:call-template name="create-toc-environment">
      <xsl:with-param name="toc-nodes" select="."/>
      <xsl:with-param name="assign-id" select="false()"/>
      <xsl:with-param name="setup">
        <cmd name="TOCisForChapter" gr="0" nl2="1">
          <parm><xsl:apply-templates select="Heading"  mode="toc"/></parm>
        </cmd>
      </xsl:with-param>
    </xsl:call-template>
  </xsl:if>
  <xsl:apply-templates/>
</xsl:template>

<xsl:template match="RevisionSheet | DocHistory">
  <env name="RevisionSheet">
    <xsl:apply-templates/>
  </env>
</xsl:template>

<!-- plain text generation -->

<xsl:template match="node()" mode="plaintext">
  <xsl:apply-templates/>
</xsl:template>

<xsl:template match="text()" mode="plaintext">
  <xsl:copy-of select="."/>
</xsl:template>

<xsl:template match="Symbol[normalize-space(@Language)!='']" mode="plaintext">
  <cmd name="protect" gr="0"/>
  <env name="ForeignLanguage" nl1="0" nl2="0" nl3="0" nl4="0">
    <parm><xsl:value-of select="normalize-space(@Language)"/></parm>
    <xsl:value-of select="."/>
    <cmd name="protect" gr="0"/>
  </env>
</xsl:template>

<!-- polyglossia should be loaded before multifont (through main_sty) -->
<xsl:template name="latex-header">
<TeXML escape="0" ws="1">
% !TEX encoding = UTF-8 Unicode
% !TEX TS-program = MithilfeMac
% vim:enc=utf-8:
\documentclass{minimal}
\def\StylesheetVersion{<xsl:value-of select="$VERSION"/>}
\usepackage{cals}
<xsl:call-template name="create-babel-header"/>
\usepackage{<xsl:value-of select="$main_sty" />}
\usepackage{multifont}
\usepackage{fontprof}
\usepackage{paravesp}
\usepackage{paras}
\usepackage{pages}
\usepackage{pagesii}
\usepackage{graphicx}
\showboxdepth=100
\showboxbreadth=100
%\setlength\overfullrule{5pt}
<xsl:if test="$MoreLatexHead != ''">
  <xsl:value-of select="$MoreLatexHead"/>
</xsl:if>
</TeXML>
<xsl:variable name="FontProfile">
  <xsl:call-template name="translate">
    <xsl:with-param name="id" select="'font-profile'"/>
    <xsl:with-param name="language" select="$language"/>
  </xsl:call-template>
</xsl:variable>
<xsl:if test="contains($FontProfile, 'Arabian')">
  <cmd name="usepackage" nl2="1"><parm>bidiparts</parm></cmd>
</xsl:if>
<xsl:if test="'135mm' != $text_width">
  <cmd name="setlength">
    <parm><cmd name="BodyWidth" gr="0" /></parm>
    <parm><xsl:value-of select="$text_width" /></parm>
  </cmd>
</xsl:if>
<xsl:call-template name="admon-set-texts"/>
<xsl:if test="boolean($ansizDXXXV)">
  <cmd name="switchToAnsiSafety" nl2="1"/>
</xsl:if>
<xsl:apply-templates select="/*" mode="hook-master-pages"/>
<xsl:if test="$use-av-layout">
  <cmd name="SwitchToLayoutAV" gr="0" nl2="1"/>
</xsl:if>
<xsl:if test="$use-usa-paper">
  <xsl:if test="not($use-av-layout)">
    <cmd name="FromAIVtoLetter" gr="0" nl2="1"/>
  </xsl:if>
  <xsl:if test="$use-av-layout">
    <cmd name="FromAVtoHalfLetter" gr="0" nl2="1"/>
  </xsl:if>
</xsl:if>
<xsl:if test="$use-color">
  <cmd name="SwitchToColor" gr="0" nl2="1"/>
</xsl:if>
<xsl:if test="$use-twoside-layout">
  <TeXML escape="0" ws="1">\ifdefined\SwitchToLayoutTwoside\SwitchToLayoutTwoside\fi</TeXML>
</xsl:if>
</xsl:template>

<xsl:template match="Processing | Orientation | SubChapter | Description | Section | SubSection | MinorSubSection | GenericSubSection | Introduction | Generate">
  <xsl:apply-templates/>
</xsl:template>

<xsl:template match="SubChapter[@orientation='Landscape']">
  <env name="landscape">
    <xsl:apply-templates/>
  </env>
</xsl:template>

<xsl:template match="ListOfAbbreviations">
  <xsl:if test="*">
    <env name="ListOfAbbreviations">
      <xsl:if test="not(Head)">
        <xsl:variable name="abbr">
          <xsl:call-template name="translate">
            <xsl:with-param name="id" select="'abbreviations'"/>
            <xsl:with-param name="language" select="$language"/>
          </xsl:call-template>
        </xsl:variable>
        <xsl:call-template name="HeadInFrontpage">
          <xsl:with-param name="xml-content" select="$abbr"/>
          <xsl:with-param name="str-content" select="$abbr"/>
        </xsl:call-template>
      </xsl:if>
      <xsl:apply-templates/>
    </env>
  </xsl:if>
</xsl:template>

<xsl:template match="Coverpages | CoverPages | OpeningPages | ClosingPages">
  <cmd name="newpage" gr="0"/><cmd name="MasterPageIsEmpty" nl2="1"/>
  <xsl:apply-templates/>
</xsl:template>

<xsl:template match="Preface">
  <env name="IntroductionPage">
    <xsl:apply-templates/>
  </env>
</xsl:template>

<!-- grouped safety advices -->

<xsl:template match="SafetyAdvice">
  <xsl:choose>
    <xsl:when test="not($join-admonitions)"><xsl:apply-imports/></xsl:when>
    <xsl:when test="preceding-sibling::*[1][self::SafetyAdvice]/@Classification = @Classification"></xsl:when>
    <xsl:when test="not(following-sibling::*[1][self::SafetyAdvice]/@Classification = @Classification)"><xsl:apply-imports/></xsl:when>
    <xsl:otherwise>
      <xsl:variable name="grouped-advice">
        <SafetyAdvice Classification="{@Classification}">
          <SafetyBody><SafetyRow>
              <SafetyPictoContent><SafetyPicto/></SafetyPictoContent>
              <SafetyContent>
                <xsl:apply-templates select="." mode="join-admonitions-bodies"/>
              </SafetyContent>
          </SafetyRow></SafetyBody>
        </SafetyAdvice>
      </xsl:variable>
      <xsl:for-each select="exsl:node-set($grouped-advice)/SafetyAdvice">
        <xsl:call-template name="SafetyAdvice"/>
      </xsl:for-each>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template match="SafetyAdvice" mode="join-admonitions-bodies">
  <xsl:copy-of select="SafetyBody/SafetyRow/SafetyContent/node()"/>
  <xsl:apply-templates select="following-sibling::*[1][self::SafetyAdvice][@Classification = current()/@Classification]" mode="join-admonitions-bodies"/>
</xsl:template>

<xsl:template match="SafetyAdviceLight">
  <xsl:choose>
    <xsl:when test="not($join-admonitions)"><xsl:apply-imports/></xsl:when>
    <xsl:when test="preceding-sibling::*[1][self::SafetyAdviceLight]"></xsl:when>
    <xsl:when test="not(following-sibling::*[1][self::SafetyAdviceLight])"><xsl:apply-imports/></xsl:when>
    <xsl:otherwise>
      <xsl:variable name="grouped-advice">
        <SafetyAdviceLight>
          <SafetyBodyLight><SafetyRowLight>
              <SafetyContent>
                <xsl:apply-templates select="." mode="join-admonitions-bodies"/>
              </SafetyContent>
          </SafetyRowLight></SafetyBodyLight>
        </SafetyAdviceLight>
      </xsl:variable>
      <xsl:for-each select="exsl:node-set($grouped-advice)/SafetyAdviceLight">
        <xsl:call-template name="SafetyAdviceLight"/>
      </xsl:for-each>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template match="SafetyAdviceLight" mode="join-admonitions-bodies">
  <xsl:copy-of select="SafetyBodyLight/SafetyRowLight/SafetyContent/node()"/>
  <xsl:apply-templates select="following-sibling::*[1][self::SafetyAdviceLight]" mode="join-admonitions-bodies"/>
</xsl:template>

<!-- ============== Paragraphs ================ -->

<xsl:template match="Chapter/Heading">
  <xsl:variable name="chapter-number">
    <xsl:call-template name="chapter-number"/>
  </xsl:variable>
  <xsl:text>&#xa;&#xa;&#xa;</xsl:text>
  <cmd name="Chapter" nl2="1">
    <parm><xsl:value-of select="$chapter-number"/></parm>
  </cmd>
  <cmd name="HeadI" nl2="1">
    <parm>
      <xsl:call-template name="chapter-number-presentation">
        <xsl:with-param name="chnum" select="$chapter-number"/>
      </xsl:call-template>
    </parm>
    <parm>
      <xsl:call-template name="set-running-header"/>
      <xsl:call-template name="setid-heading">
        <xsl:with-param name="number" select="$chapter-number"/>
      </xsl:call-template>
      <xsl:apply-templates/>
      <xsl:call-template name="show-heading-variant"/>
    </parm>
  </cmd>
</xsl:template>

<xsl:template name="chapter-number-presentation">
  <xsl:param name="chnum"/>
  <xsl:value-of select="$chnum"/>
</xsl:template>

<xsl:template match="RevisionSheet/Head | DocHistory/Head | Introduction/Head | ListOfAbbreviations/Head">
  <xsl:call-template name="HeadInFrontpage"/>
</xsl:template>

<xsl:template name="HeadInFrontpage">
  <xsl:param name="xml-content"><xsl:apply-templates/></xsl:param>
  <xsl:param name="str-content"><xsl:apply-templates select="." mode="plaintext"/></xsl:param>
  <cmd name="HeadINoNum" nl2="1">
    <parm><xsl:copy-of select="$xml-content"/></parm>
  </cmd>
  <cmd name="SetRunningHeader">
    <parm><xsl:copy-of select="$str-content"/></parm>
    <parm/>
  </cmd>
</xsl:template>

<xsl:template match="Preface/Introduction/Head | Preface/Head">
  <xsl:if test="not(preceding-sibling::Head)"> <!-- in Preface -->
    <cmd name="newpage" nl2="1"/>
    <cmd name="SetRunningHeader" nl2="1">
      <parm><xsl:apply-templates select="." mode="plaintext"/></parm>
      <parm></parm>
    </cmd>
  </xsl:if>
  <xsl:apply-templates select="@StartPosition"/>
  <xsl:if test="preceding-sibling::Head">
    <cmd name="IntroPagePreHead" nl2="1"/>
  </xsl:if>
  <xsl:if test=".='Status Quo'">
    <cmd name="newpage" nl2="1"/> <!-- quick fix. in/20110505/letter3 -->
  </xsl:if>
  <cmd name="HeadINoNum" nl2="1">
    <parm><xsl:apply-templates/></parm>
  </cmd>
</xsl:template>

<xsl:template match="SubChapter/Heading">
  <xsl:apply-templates select="@StartPosition"/>
  <xsl:variable name="subchapter-number">
    <xsl:call-template name="subchapter-number"/>
  </xsl:variable>
  <cmd name="HeadII" nl2="1">
    <parm><xsl:value-of select="$subchapter-number"/></parm>
    <parm>
      <xsl:call-template name="setid-heading">
        <xsl:with-param name="number" select="$subchapter-number"/>
      </xsl:call-template>
      <xsl:call-template name="set-running-header"/>
      <xsl:apply-templates/>
      <xsl:call-template name="show-heading-variant"/>
    </parm>
  </cmd>
</xsl:template>

<xsl:template match="Section/Heading">
  <xsl:apply-templates select="@StartPosition"/>
  <xsl:variable name="section-number">
    <xsl:call-template name="section-number"/>
  </xsl:variable>
  <cmd name="HeadIII" nl2="1">
    <parm><xsl:value-of select="$section-number"/></parm>
    <parm>
      <xsl:call-template name="setid-heading">
        <xsl:with-param name="number" select="$section-number"/>
      </xsl:call-template>
      <xsl:call-template name="set-running-header-for-section"/>
      <xsl:apply-templates/>
      <xsl:call-template name="show-heading-variant"/>
    </parm>
  </cmd>
</xsl:template>

<xsl:template match="SubSection/Heading">
  <xsl:apply-templates select="@StartPosition"/>
  <xsl:variable name="subsection-number">
    <xsl:call-template name="subsection-number"/>
  </xsl:variable>
  <cmd name="HeadIV" nl2="1">
    <parm><xsl:value-of select="$subsection-number"/></parm>
    <parm>
      <xsl:call-template name="setid-heading">
        <xsl:with-param name="number" select="$subsection-number"/>
      </xsl:call-template>
      <xsl:apply-templates/>
      <xsl:call-template name="show-heading-variant"/>
    </parm>
  </cmd>
</xsl:template>

<xsl:template match="MinorSubSection/Heading">
  <xsl:apply-templates select="@StartPosition"/>
  <xsl:variable name="minorsubsection-number">
    <xsl:call-template name="minorsubsection-number"/>
  </xsl:variable>
  <cmd name="HeadV" nl2="1">
    <parm><xsl:value-of select="$minorsubsection-number"/></parm>
    <parm>
      <xsl:call-template name="setid-heading">
        <xsl:with-param name="number" select="$minorsubsection-number"/>
      </xsl:call-template>
      <xsl:apply-templates/>
      <xsl:call-template name="show-heading-variant"/>
    </parm>
  </cmd>
</xsl:template>

<xsl:template match="GenericSubSection/Heading">
  <xsl:apply-templates select="@StartPosition"/>
  <xsl:variable name="genericsubsection-number">
    <xsl:if test="not(../ancestor::GenericSubSection)">
      <xsl:call-template name="genericsubsection-number"/>
    </xsl:if>
  </xsl:variable>
  <cmd name="HeadIV" nl2="1">
    <parm><xsl:value-of select="$genericsubsection-number"/></parm>
    <parm>
      <xsl:call-template name="setid-heading">
        <xsl:with-param name="number" select="$genericsubsection-number"/>
      </xsl:call-template>
      <xsl:apply-templates/>
      <xsl:call-template name="show-heading-variant"/>
    </parm>
  </cmd>
</xsl:template>

<xsl:template match="Heading">
  <xsl:apply-templates select="@StartPosition"/>
  <cmd name="IHead">
    <parm><xsl:apply-templates/></parm>
  </cmd>
</xsl:template>

<xsl:template match="Bodytext | BodyText | Liability">
  <env name="BodyText" nl2="0" nl3="0">
    <xsl:if test="@dir='ltr'"><TeXML escape="0">&#x202a;</TeXML></xsl:if>
    <xsl:apply-templates/>
    <xsl:if test="@dir='ltr'"><TeXML escape="0">&#x202c;</TeXML></xsl:if>
  </env>
</xsl:template>

<xsl:template match="Bodytext[ancestor::entry] | BodyText[ancestor::entry]">
  <env name="TablePara" nl2="0" nl3="0">
    <xsl:apply-templates/>
  </env>
</xsl:template>

<xsl:template match="Blockquote/Bodytext">
  <env name="BodyText" nl2="0" nl3="0">
    <xsl:if test="not(preceding-sibling::Bodytext) and not(normalize-space(parent::*/@Class))">
      <cmd name="BlockStartQuote">
        <parm>
          <xsl:call-template name="translate">
            <xsl:with-param name="id" select="'startquote'"/>
            <xsl:with-param name="language" select="$language"/>
          </xsl:call-template>
        </parm>
      </cmd>
    </xsl:if>
    <xsl:apply-templates/>
    <xsl:if test="not(following-sibling::Bodytext) and not(normalize-space(parent::*/@Class))">
      <cmd name="BlockEndQuote">
        <parm>
          <xsl:call-template name="translate">
            <xsl:with-param name="id" select="'endquote'"/>
            <xsl:with-param name="language" select="$language"/>
          </xsl:call-template>
        </parm>
      </cmd>
    </xsl:if>
  </env>
</xsl:template>

<!-- signature field -->
<xsl:template match="Liability[contains(.,'__________')]">
  <cmd name="SignatureField" nl1="1" nl2="1">
    <parm><xsl:value-of select="substring-before(.,'__________')"/></parm>
  </cmd>
</xsl:template>

<xsl:template match="Orientation/Bodytext">
  <env name="OrientationBodyText" nl2="0" nl3="0">
    <xsl:apply-templates/>
  </env>
</xsl:template>

<!-- workaround for an error in XML data -->
<xsl:template match="Description/text()[normalize-space()!='']">
  <env name="BodyText" nl2="0" nl3="0"><xsl:value-of select="."/></env>
</xsl:template>

<xsl:template match="Caption">
  <xsl:variable name="capname">
    <xsl:call-template name="caption-tex-command-name"/>
  </xsl:variable>
  <xsl:variable name="caption">
    <cmd name="{$capname}" nl2="1">
      <parm>
        <xsl:apply-templates select="@id | ../@id"/>
        <xsl:call-template name="get-object-autotext-prefix">
          <xsl:with-param name="object" select="."/>
        </xsl:call-template>
      </parm>
      <parm>
        <xsl:apply-templates/>
        <xsl:if test="parent::table">
          <cmd name="TablePartKofN" gr="0"/>
        </xsl:if>
      </parm>
    </cmd>
  </xsl:variable>
  <xsl:choose>
    <xsl:when test="parent::table">
      <cmd name="BitplantTFoot" nl1="1" nl2="1">
        <parm><xsl:copy-of select="$caption"/></parm>
      </cmd>
    </xsl:when>
    <xsl:otherwise><xsl:copy-of select="$caption"/></xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template name="caption-tex-command-name">
  <xsl:choose>
    <xsl:when test="parent::table">CaptionTable</xsl:when>
    <xsl:when test="parent::Graphic">CaptionImage</xsl:when>
    <xsl:otherwise>Caption</xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template match="@StartPosition">
  <xsl:if test=".='RightPage'">
    <cmd name="cleardoublepage" nl2="1"/>
  </xsl:if>
  <xsl:if test=".='TopOfPage'">
    <cmd name="MaybeNewpage" nl2="1"/>
  </xsl:if>
</xsl:template>

<xsl:template match="Result">
  <env name="Result">
    <xsl:apply-templates/>
  </env>
</xsl:template>

<xsl:template match="ActionStep/Result">
  <env name="StepResult">
    <xsl:apply-templates/>
  </env>
</xsl:template>

<xsl:template match="Actionseq/Head | Description/Head">
  <xsl:if test="(ancestor::*[3]/self::entry) and (not (../../preceding-sibling::*))">
    <cmd name="TmpHackFirstInCell"/>
  </xsl:if>
  <cmd name="ActionseqHead">
    <parm>
      <xsl:apply-templates/>
    </parm>
  </cmd>
</xsl:template>

<xsl:template match="Address">
  <env name="Address" nl2="0" nl3="0"><xsl:apply-templates/></env>
</xsl:template>

<xsl:template name="smalldiv">
  <TeXML ws="1"><xsl:text>&#xa;&#xa;</xsl:text></TeXML>
</xsl:template>

<xsl:template match="SystemSupplier">
  <xsl:apply-templates/>
</xsl:template>

<xsl:template match="Blockquote">
  <env name="blockquote">
    <xsl:apply-templates/>
  </env>
</xsl:template>

<xsl:template match="Blockquote[@Class='copyright']">
  <env name="TextBlock" nl2="0" nl3="0">
    <cmd name="TextClassCopyright" gr="0"/>
    <xsl:apply-templates/>
  </env>
</xsl:template>

<!-- ============== / Paragraphs ============== -->

<!-- Variant -->

<xsl:template name="mk-variant-comment-text">
  <xsl:if test="(normalize-space(@Variable)!='') or (normalize-space(@KeySequence)!='')">
    <xsl:value-of select="@Variable"/>
    <xsl:value-of select="@KeySequence"/>
    <xsl:text>; </xsl:text>
  </xsl:if>
  <xsl:if test="normalize-space(@Comment)!=''">
    <xsl:text>(</xsl:text>
    <xsl:value-of select="@Comment"/>
    <xsl:text>)</xsl:text>
  </xsl:if>
</xsl:template>

<!-- Called also from other places. For example, from ActionStep -->
<!-- The element "Variant" now unpacked to PI in preprocess-step -->
<xsl:template match="Variant" name="Variant">
  <xsl:choose>
    <xsl:when test="1=$show-variant-borders">
      <xsl:variable name="comment">
        <xsl:call-template name="mk-variant-comment-text"/>
      </xsl:variable>
      <xsl:choose>
        <xsl:when test="''!=$comment">
          <env name="para" nl2="0" nl3="0"><cmd name="VariantBegin"><parm><xsl:value-of select="$comment"/></parm></cmd></env>
          <cmd name="nobreak" nl2="1"/>
          <xsl:apply-templates/>
          <cmd name="nobreak" nl2="1"/>
          <env name="para" nl2="0" nl3="0"><cmd name="VariantEnd"><parm><xsl:value-of select="$comment"/></parm></cmd></env>
        </xsl:when>
        <xsl:otherwise><xsl:apply-templates/></xsl:otherwise>
      </xsl:choose>
    </xsl:when>
    <xsl:otherwise><xsl:apply-templates/></xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template name="show-variant-inline">
  <xsl:variable name="s"><xsl:call-template name="mk-variant-comment-text"/></xsl:variable>
  <xsl:if test="'' != string($s)">
    <cmd name="VariantMarkerAlone"><parm><ctrl ch=" "/><xsl:value-of select="$s"/></parm></cmd>
  </xsl:if>
</xsl:template>

<xsl:template name="show-heading-variant">
  <xsl:if test="1=$show-variant-borders">
    <xsl:for-each select="..">
      <xsl:call-template name="show-variant-inline"/>
    </xsl:for-each>
  </xsl:if>
</xsl:template>

<xsl:template match="processing-instruction('epicentity-begin') | processing-instruction('variant-begin')">
  <xsl:if test="1=$show-variant-borders and parent::*">
    <env name="para" nl2="0" nl3="0"><cmd name="VariantBegin"><parm><xsl:value-of select="."/></parm></cmd></env>
    <cmd name="nobreak" nl2="1"/>
  </xsl:if>
</xsl:template>

<xsl:template match="processing-instruction('epicentity-end') | processing-instruction('variant-end')">
  <xsl:if test="1=$show-variant-borders and parent::*">
    <cmd name="nobreak" nl2="1"/>
    <env name="para" nl2="0" nl3="0"><cmd name="VariantEnd"><parm><xsl:value-of select="."/></parm></cmd></env>
  </xsl:if>
</xsl:template>

<!-- ================ Graphics ================ -->

<xsl:template match="Graphic">
  <!--
  <xsl:if test="'turbo'=$main_sty">
    <xsl:if test="parent::ActionStep">
      <cmd name="BeginDisplay"><parm><cmd name="BeginDisplayImageSkip" gr="0"/></parm></cmd>
    </xsl:if>
  </xsl:if>
  -->
  <cmd name="widegroup"><parm><xsl:apply-templates/></parm></cmd>
</xsl:template>

<xsl:template match="Figure">
  <cmd name="ImageWrapper">
    <parm>
      <xsl:if test="(@align='aright') or (@align='acenter')">
        <cmd name="ImgAlignHfill"/>
      </xsl:if>
      <cmd name="Image">
        <opt>
          <xsl:if test="normalize-space(@width)">
            <xsl:text>width=</xsl:text>
            <xsl:value-of select="@width"/>
            <xsl:text>,</xsl:text>
          </xsl:if>
          <xsl:if test="normalize-space(@height)">
            <xsl:text>height=</xsl:text>
            <xsl:value-of select="@height"/>
            <xsl:text>,</xsl:text>
          </xsl:if>
        </opt>
        <parm><xsl:value-of select="@file"/></parm>
      </cmd>
      <xsl:if test="(@align='aleft') or (@align='acenter')">
        <cmd name="ImgAlignHfill"/><cmd name="hbox"/>
      </xsl:if>
    </parm>
  </cmd>
</xsl:template>

<xsl:template match="Icon">
  <cmd name="Image">
    <opt>width=<xsl:value-of select="@width"/>,height=<xsl:value-of select="@height"/></opt>
    <parm><xsl:value-of select="@file"/></parm>
  </cmd>
</xsl:template>

<xsl:template match="LegendTab">
  <xsl:variable name="envnameplus">
    <xsl:if test="1=count(Legend)">OneItem</xsl:if>
  </xsl:variable>
  <env name="Legend{$envnameplus}">
    <parm>
      <xsl:variable name="img-width" select="preceding-sibling::Figure/@width"/>
      <xsl:choose>
        <xsl:when test="''!=normalize-space($img-width)"><xsl:value-of select="$img-width"/></xsl:when>
        <xsl:otherwise>0pt</xsl:otherwise>
      </xsl:choose>
    </parm>
    <xsl:apply-templates/>
  </env>
</xsl:template>

<xsl:template match="Legend">
  <xsl:apply-templates/>
</xsl:template>

<xsl:template match="LegendPos"/>

<xsl:template match="LegendText">
  <cmd name="LegendItem" nl1="1" nl2="1">
    <parm><xsl:value-of select="count(../preceding-sibling::Legend)+1"/></parm>
    <parm><xsl:apply-templates/></parm>
  </cmd>
</xsl:template>

<xsl:template match="Space">
  <xsl:apply-templates select="@StartPosition"/>  
</xsl:template>

<xsl:template match="LcdDisplay">
  <cmd name="LcdDisplay">
    <parm><xsl:value-of select="."/></parm>
  </cmd>
</xsl:template>

<!-- =============== / Graphics =============== -->

<!-- ============== Inline elements =========== -->

<xsl:template match="Software | SoftwarePath">
  <cmd name="Software">
    <parm><xsl:apply-templates/></parm>
  </cmd>
</xsl:template>

<xsl:template match="Switch | MechanicalSwitch">
  <cmd name="Switch">
    <parm><xsl:apply-templates/></parm>
  </cmd>
</xsl:template>

<xsl:template match="DataEntry">
  <xsl:apply-templates/>
</xsl:template>

<xsl:template match="Linefeed">
  <cmd name="Newline" gr="0" nl2="1"/>
</xsl:template>

<xsl:template match="Emphasis">
  <xsl:variable name="cmdname">
    <xsl:choose>
      <xsl:when test="'unverified'=normalize-space(@Highlight)">hl</xsl:when>
      <xsl:when test="'active' = normalize-space(@highlight)">hl</xsl:when>
      <xsl:when test="'underline'= normalize-space(@Highlight)">underline</xsl:when>
      <xsl:when test="'active' = normalize-space(@underline)">underline</xsl:when>
      <xsl:when test="'italic'=normalize-space(@Highlight)">emph</xsl:when>
      <xsl:when test="'active' = normalize-space(@italic)">emph</xsl:when>
      <xsl:when test="'inactive' = normalize-space(@bold)">relax</xsl:when>
      <xsl:otherwise>boldemphasis</xsl:otherwise>
    </xsl:choose>
  </xsl:variable>
  <cmd name="{$cmdname}">
    <parm><xsl:apply-templates/></parm>
  </cmd>
</xsl:template>

<xsl:template match="IndexEntry">
  <xsl:apply-templates select="@id"/>
  <xsl:apply-templates/>
</xsl:template>

<xsl:template match="ArrowRight">
  <cmd name="bitarrowright"/>
</xsl:template>

<xsl:template match="Symbol">
  <cmd name="Symbol">
    <parm><xsl:value-of select="."/></parm>
  </cmd>
</xsl:template>

<xsl:template match="Symbol[normalize-space(@Language)!='']">
  <env name="ForeignLanguage" nl1="0" nl2="0" nl3="0" nl4="0">
    <parm><xsl:value-of select="normalize-space(@Language)"/></parm>
    <xsl:value-of select="."/>
  </env>
</xsl:template>

<xsl:template match="SuperScript">
  <cmd name="textsuperscript">
    <parm><xsl:apply-templates/></parm>
  </cmd>
</xsl:template>

<xsl:template match="SubScript">
  <cmd name="textsubscript">
    <parm><xsl:apply-templates/></parm>
  </cmd>
</xsl:template>

<xsl:template match="suppressshy"/>

<xsl:template match="Number">
  <xsl:choose>
    <xsl:when test="normalize-space()!=''"><xsl:apply-templates/></xsl:when>
    <xsl:otherwise><xsl:number count="Number" from="table" level="any"/></xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template match="Mouse">
  <cmd name="Mouse">
    <parm>
      <xsl:choose>
        <xsl:when test="''=normalize-space(@Click)">LC</xsl:when>
        <xsl:otherwise><xsl:value-of select="normalize-space(@Click)"/></xsl:otherwise>
      </xsl:choose>
    </parm>
  </cmd>
</xsl:template>

<xsl:template match="Flag">
  <xsl:if test="@StartPosition='TopOfPage'">
    <cmd name="newpage"/>
  </xsl:if>
</xsl:template>

<xsl:template match="HyperReference">
  <xsl:variable name="target">
    <xsl:choose>
      <xsl:when test="''=normalize-space(@target)"><xsl:value-of select="."/></xsl:when>
      <xsl:otherwise><xsl:value-of select="@target"/></xsl:otherwise>
    </xsl:choose>
  </xsl:variable>
  <xsl:variable name="text">
    <xsl:choose>
      <xsl:when test="''=normalize-space(.)">
        <xsl:choose>
          <xsl:when test="starts-with($target,'./')"><xsl:value-of select="substring-after($target,'./')"/></xsl:when>
          <xsl:otherwise><xsl:value-of select="$target"/></xsl:otherwise>
        </xsl:choose>
        </xsl:when>
      <xsl:otherwise><xsl:value-of select="."/></xsl:otherwise>
    </xsl:choose>
  </xsl:variable>
  <xsl:variable name="full_target">
    <xsl:choose>
      <xsl:when test="starts-with($target,'./')"><xsl:value-of select="$target"/></xsl:when>
      <xsl:when test="not(contains($target,'//'))">
        <xsl:text>http://</xsl:text>
        <xsl:value-of select="$target"/>
      </xsl:when>
      <xsl:otherwise><xsl:value-of select="$target"/></xsl:otherwise>
    </xsl:choose>
  </xsl:variable>
  <cmd name="href">
    <parm><xsl:value-of select="$full_target"/></parm>
    <parm><xsl:value-of select="$text"/></parm>
  </cmd>
</xsl:template>

<!-- ============== / Inline elements =============== -->

<!-- =================== Tables ===================== -->

<xsl:template match="table">
  <env name="BitplantTable">
    <xsl:call-template name="mkcolwidths"/>
    <xsl:apply-templates select="Caption"/>
    <xsl:if test="not(Caption)">
      <xsl:call-template name="table-without-caption"/>
    </xsl:if>
    <xsl:apply-templates select="*[not(self::Caption)]"/>
  </env>
</xsl:template>

<xsl:template name="table-without-caption"/>

<xsl:template match="tbody | tfoot | tgroup">
  <xsl:apply-templates/>
</xsl:template>

<xsl:template match="thead">
  <cmd name="BitplantTHead" nl1="1" nl2="1">
    <parm>
      <xsl:apply-templates/>
    </parm>
  </cmd>
</xsl:template>

<xsl:template name="mkcolwidths">
  <cmd name="colwidths" nl2="1">
    <parm>
      <xsl:for-each select="tgroup/colspec">
        <group>
          <xsl:value-of select="@colwidth"/>
        </group>
      </xsl:for-each>
    </parm>
  </cmd>
</xsl:template>

<xsl:template match="colspec"/>

<xsl:template match="row">
  <cmd name="brow" nl1="1" gr="0" />
  <xsl:apply-templates />
  <cmd name="erow" nl2="1" gr="0" />
</xsl:template>

<xsl:template match="row[.//Counter]"/>

<xsl:template match="entry">
  <xsl:if test="'right'=@align">
    <cmd name="alignR"/>
  </xsl:if>
  <cmd name="cell" nl2="1">
    <parm>
      <xsl:apply-templates/>
    </parm>
  </cmd>
  <xsl:if test="@align and ('left' != @align)">
    <cmd name="alignL"/>
  </xsl:if>
</xsl:template>

<xsl:template match="*[@tch:span]">
  <cmd name="nullcell">
    <parm>
      <xsl:if test="@tch:left"  >l</xsl:if>
      <xsl:if test="@tch:right" >r</xsl:if>
      <xsl:if test="@tch:top"   >t</xsl:if>
      <xsl:if test="@tch:bottom">b</xsl:if>
    </parm>
  </cmd>
  <xsl:if test="@tch:right and @tch:bottom">
    <cmd name="spancontent" nl="2">
      <parm>
        <xsl:apply-templates select="key('span',@tch:span)/node()"/>
      </parm>
    </cmd>
  </xsl:if>
</xsl:template>

<xsl:template match="entry/Text">
  <env name="TablePara" nl1="0" nl2="0" nl3="0" nl4="0">
    <xsl:apply-templates/>
  </env>
</xsl:template>

<!-- ================= / Tables ===================== -->

<!-- just like in FrameMaker, $object is usually a header -->
<xsl:template name="get-object-autotext-prefix">
  <xsl:param name="object" select="key('id', @idref)"/>
  <xsl:param name="use-object" select="($object | $object/Caption | $object/Heading)[last()]" />
  <xsl:param name="object-name">
    <xsl:choose>
      <xsl:when test="('Caption'=name($object)) or ('Heading'=name($object))"><xsl:value-of select="name($object/..)"/></xsl:when>
      <xsl:otherwise><xsl:value-of select="name($object)"/></xsl:otherwise>
    </xsl:choose>
  </xsl:param>
  <xsl:for-each select="$use-object">
    <xsl:choose>
      <xsl:when test="'table' = $object-name">
        <xsl:call-template name="translate">
          <xsl:with-param name="id" select="'number-prefix-table'"/>
          <xsl:with-param name="language" select="$language"/>
        </xsl:call-template>
        <xsl:call-template name="table-number"/>
      </xsl:when>
      <xsl:when test="'Graphic' = $object-name">
        <xsl:call-template name="translate">
          <xsl:with-param name="id" select="'number-prefix-graphic'"/>
          <xsl:with-param name="language" select="$language"/>
        </xsl:call-template>
        <xsl:call-template name="figure-number"/>
      </xsl:when>
      <xsl:when test="'Chapter' = $object-name"><xsl:call-template name="chapter-number"/></xsl:when>
      <xsl:when test="'SubChapter' = $object-name"><xsl:call-template name="subchapter-number"/></xsl:when>
      <xsl:when test="'Section' = $object-name"><xsl:call-template name="section-number"/></xsl:when>
      <xsl:when test="'SubSection' = $object-name"><xsl:call-template name="subsection-number"/></xsl:when>
      <xsl:when test="'MinorSubSection' = $object-name"><xsl:call-template name="minorsubsection-number"/></xsl:when>
      <xsl:when test="'GenericSubSection' = $object-name"><xsl:call-template name="genericsubsection-number"/></xsl:when>
      <xsl:when test="'Legend' = $object-name">
        <xsl:value-of select="count(preceding-sibling::Legend)+1"/>
      </xsl:when>
      <xsl:when test="'ActionStep' = $object-name">
        <xsl:call-template name="translate">
          <xsl:with-param name="id" select="'number-prefix-action-step'"/>
          <xsl:with-param name="language" select="$language"/>
        </xsl:call-template>
        <xsl:value-of select="1+count(preceding-sibling::ActionStep)"/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:message>*** Don't know how to generate a prefix for '<xsl:value-of select="$object-name"/>'<xsl:if test="@id"> (id=<xsl:value-of select="@id"/>)</xsl:if></xsl:message>
        <xsl:text>??</xsl:text>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:for-each>
</xsl:template>

<xsl:template name="chapter-number">
  <xsl:param name="object" select="."/>
  <xsl:for-each select="$object">
    <xsl:value-of select="count(ancestor-or-self::Chapter/preceding-sibling::Chapter) + 1"/>
  </xsl:for-each>
</xsl:template>

<xsl:template name="subchapter-number">
  <xsl:param name="object" select="."/>
  <xsl:for-each select="$object">
  <xsl:call-template name="chapter-number"/>
    <xsl:text>.</xsl:text>
    <xsl:number level="any" from="Chapter" count="SubChapter/Heading"/>
  </xsl:for-each>
</xsl:template>

<xsl:template name="section-number">
  <xsl:param name="object" select="."/>
  <xsl:for-each select="$object">
    <xsl:call-template name="subchapter-number"/>
    <xsl:text>.</xsl:text>
    <xsl:number level="any" from="SubChapter" count="Section/Heading"/>
  </xsl:for-each>
</xsl:template>

<xsl:template name="subsection-number">
  <xsl:param name="object" select="."/>
  <xsl:for-each select="$object">
    <xsl:call-template name="section-number"/>
    <xsl:text>.</xsl:text>
    <xsl:number level="any" from="Section" count="SubSection/Heading"/>
  </xsl:for-each>
</xsl:template>

<xsl:template name="minorsubsection-number">
  <xsl:param name="object" select="."/>
  <xsl:for-each select="$object">
    <xsl:call-template name="subsection-number"/>
    <xsl:text>.</xsl:text>
    <xsl:number level="any" from="SubSection" count="MinorSubSection/Heading"/>
  </xsl:for-each>
</xsl:template>

<xsl:template name="genericsubsection-number">
  <xsl:param name="object" select="."/>
  <xsl:for-each select="$object">
    <xsl:call-template name="minorsubsection-number"/>
    <xsl:text>.</xsl:text>
    <xsl:number level="any" from="MinorSubSection" count="GenericSubSection/Heading"/>
  </xsl:for-each>
</xsl:template>

<xsl:template name="table-number">
  <xsl:param name="object" select="."/>
  <xsl:for-each select="$object">
    <xsl:call-template name="chapter-number"/>
    <xsl:text>-</xsl:text>
    <xsl:number level="any" from="Chapter" count="table/Caption"/>
  </xsl:for-each>
</xsl:template>

<xsl:template name="figure-number">
  <xsl:param name="object" select="."/>
  <xsl:for-each select="$object">
    <xsl:call-template name="chapter-number"/>
    <xsl:text>-</xsl:text>
    <xsl:number level="any" from="Chapter" count="Graphic/Caption"/>
  </xsl:for-each>
</xsl:template>

<!-- set ID only when the attribute exists -->
<xsl:template match="@id">
  <xsl:for-each select="..">
    <xsl:call-template name="setid"/>
  </xsl:for-each>
</xsl:template>

<!-- ID can be in heading or in section. Select one -->
<xsl:template name="setid-heading">
  <xsl:param name="number"/>
  <xsl:param name="tail">
    <xsl:if test="''!=$number">
      <xsl:text>head.</xsl:text><xsl:value-of select="$number"/>
    </xsl:if>
  </xsl:param>
  <xsl:call-template name="setid">
    <xsl:with-param name="tail" select="$tail"/>
  </xsl:call-template>
</xsl:template>

<!-- force set ID -->
<xsl:template name="setid">
  <xsl:param name="tail"/>
  <xsl:param name="id">
    <xsl:call-template name="genid">
      <xsl:with-param name="tail" select="$tail"/>
    </xsl:call-template>
  </xsl:param>
  <!-- for page numbers -->
  <cmd name="label">
    <parm><TeXML escape="0"><xsl:value-of select="$id"/></TeXML></parm>
  </cmd>
  <!-- for PDF links -->
  <cmd name="hypertarget">
    <parm><xsl:value-of select="$id"/></parm>
    <parm/>
  </cmd>
</xsl:template>

<xsl:template name="genid">
  <xsl:param name="tail"/>
  <xsl:choose>
    <xsl:when test="''!=@id"><xsl:value-of select="@id"/></xsl:when>
    <xsl:when test="''!=../@id"><xsl:value-of select="../@id"/></xsl:when>
    <xsl:when test="''!=$tail">id.<xsl:value-of select="$tail"/></xsl:when>
    <xsl:otherwise>id<xsl:value-of select="generate-id()"/></xsl:otherwise>
  </xsl:choose>
</xsl:template>

<!-- ============== Localization ==================== -->

<xsl:template match="i-Head | Margin">
  <xsl:apply-templates select="@StartPosition"/>
  <cmd name="IHead">
    <parm>
      <xsl:if test="@TransGuide">
        <xsl:call-template name="translate">
          <xsl:with-param name="id" select="concat('i-', translate(@TransGuide, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'))"/>
          <xsl:with-param name="language" select="$language"/>
        </xsl:call-template>
      </xsl:if>
      <xsl:apply-templates/>
    </parm>
  </cmd>
</xsl:template>

<!-- ============== Actions, lists ================== -->

<xsl:template match="Headword">
  <cmd name="IHead">
    <parm>
      <xsl:call-template name="translate">
        <xsl:with-param name="id" select="'i-result'"/>
        <xsl:with-param name="language" select="$language"/>
      </xsl:call-template>
    </parm>
  </cmd>

</xsl:template>
<xsl:template match="Actionseq">
  <xsl:apply-templates/>
</xsl:template>

<xsl:template match="List">
  <xsl:variable name="listname">
    <xsl:if test="ancestor::ActionStep or ancestor::List">
      <xsl:text>Nested</xsl:text>
    </xsl:if>
    <xsl:text>List</xsl:text>
  </xsl:variable>
  <env name="{$listname}">
    <xsl:apply-templates/>
  </env>
</xsl:template>

<xsl:template match="Actions">
  <env name="Actions">
    <xsl:apply-templates/>
  </env>
</xsl:template>

<!--
List styles:
* LBullet
* LSquare (probably isn't used; using LBullet style instead)
* LNumber1, LNumber2: not numbered lists, only actions. Using LBullet.
-->
<xsl:template match="ListEntry">
  <xsl:variable name="stylename">
    <xsl:choose>
      <xsl:when test="parent::List/parent::ListEntry/parent::List">ParaListNested</xsl:when>
      <xsl:otherwise>ParaListBullet</xsl:otherwise>
    </xsl:choose>
  </xsl:variable>
  <xsl:if test="*[not(self::List)]">
    <cmd name="{$stylename}" nl1="1" nl2="1">
      <parm>
        <xsl:choose>
          <xsl:when test="parent::List/parent::ListEntry/parent::List"><cmd name="listndash"/></xsl:when>
          <xsl:when test="parent::List[@Type='Numbered']">
            <xsl:value-of select="count(preceding-sibling::ListEntry)+1"/>
            <xsl:text>.</xsl:text>
          </xsl:when>
          <xsl:when test="parent::List[@Type='Square']"><cmd name="listsquare"/></xsl:when>
          <xsl:when test="parent::List[@Type='Slide-in']"></xsl:when>
          <xsl:when test="parent::List"><cmd name="listbullet"/></xsl:when>
        </xsl:choose>
      </parm>
      <parm><xsl:apply-templates select="*[not(self::List)]"/></parm>
    </cmd>
  </xsl:if>
  <xsl:apply-templates select="List"/>
</xsl:template>

<!-- Actions:
* Action1, ActionN, ActionAlone (all three are the same)
* ActionNone (don't know when is used)
Initially was processed as lists, but due to wide material
(images, admonitions), which should have indent, we make
a trick: only Text is indented -->
<xsl:template match="ActionStep">
  <xsl:apply-templates select="@StartPosition"/>
  <!-- <xsl:apply-templates/> -->
  <xsl:call-template name="Variant"/>
  <!--
  <xsl:if test="*[1][self::Graphic]">
    <cmd name="BeginDisplay"><parm><cmd name="BeginDisplayImageSkip" gr="0"/></parm></cmd>
  </xsl:if>
  -->
</xsl:template>

<xsl:template match="ActionStep/Text">
  <xsl:variable name="cmdname">
    <xsl:choose>
      <xsl:when test="../parent::SafetyContent">ParaSafetyAdviceStep</xsl:when>
      <xsl:otherwise>ParaListAction</xsl:otherwise>
    </xsl:choose>
  </xsl:variable>
  <xsl:if test="preceding-sibling::Graphic">
    <cmd name="ActionStepTextAfterImage"/>
  </xsl:if>
  <cmd name="{$cmdname}" nl1="1" nl2="1">
    <parm>
      <xsl:if test="not(preceding-sibling::Text)">
        <xsl:choose>
          <xsl:when test="count(../../ActionStep)=1"><cmd name="bitactionarrow"/></xsl:when>
          <xsl:when test="../parent::Actionseq"><xsl:value-of select="count(../preceding-sibling::ActionStep)+1"/>.</xsl:when>
          <xsl:otherwise><cmd name="bitactionarrow"/></xsl:otherwise>
        </xsl:choose>
      </xsl:if>
    </parm>
    <parm>
      <xsl:if test="not(preceding-sibling::Text)">
        <xsl:apply-templates select="../@id"/>
      </xsl:if>
      <xsl:apply-templates/>
    </parm>
  </cmd>
</xsl:template>

<xsl:template match="Alternative">
  <cmd name="Alternative">
    <parm>
      <xsl:apply-templates/>
    </parm>
  </cmd>
</xsl:template>

<xsl:template match="Text | List2/BodyText">
  <env name="BodyText" nl2="0" nl3="0">
    <xsl:apply-templates/>
  </env>
</xsl:template>

<xsl:template match="ListHead">
  <env name="BodyText" nl2="0" nl3="0"><xsl:apply-templates/></env>
  <cmd name="nobreak" gr="0" nl2="1"/>
</xsl:template>

<xsl:template match="ListHead[ancestor::entry]">
  <env name="TablePara" nl2="0" nl3="0">
    <xsl:apply-templates/>
  </env>
</xsl:template>

<!-- ============= / Actions, lists ================= -->

<!-- ================== TOC ========================= -->

<xsl:template name="create-toc-environment">
  <xsl:param name="toc-nodes" />
  <xsl:param name="assign-id" select="true()"/>
  <xsl:param name="setup"/>
  <xsl:variable name="toc-title">
    <xsl:call-template name="translate">
      <xsl:with-param name="id" select="'table-of-contents'"/>
      <xsl:with-param name="language" select="$language"/>
    </xsl:call-template>
  </xsl:variable>
  <env name="TOCpages">
    <parm><xsl:value-of select="$toc-title"/></parm>
    <parm>
      <xsl:if test="$assign-id">
        <xsl:call-template name="setid">
          <xsl:with-param name="id" select="'tableofcontents'"/>
        </xsl:call-template>
      </xsl:if>
    </parm>
    <xsl:copy-of select="$setup"/>
    <xsl:apply-templates select="$toc-nodes" mode="toc"/>
  </env>
</xsl:template>

<xsl:template match="Coverpages/TableOfContents | CoverPages/TableOfContents | OpeningPages/TableOfContents">
  <xsl:call-template name="create-toc-environment">
    <xsl:with-param name="toc-nodes" select="/Book/Chapter | /Book/Generate/IndexAnnex"/>
  </xsl:call-template>
</xsl:template>

<xsl:template match="TableOfContents">
  <xsl:call-template name="create-toc-environment">
    <xsl:with-param name="toc-nodes" select="following-sibling::Chapter[1]"/>
  </xsl:call-template>
</xsl:template>

<xsl:template match="node()" mode="toc"/>

<xsl:template match="text()" mode="toc">
  <xsl:copy-of select="."/>
</xsl:template>

<xsl:template match="Symbol[normalize-space(@Language)!='']" mode="toc">
  <xsl:apply-templates select="."/>
</xsl:template>

<xsl:template match="*" mode="toc">
  <xsl:apply-templates/>
</xsl:template>

<xsl:template match="Chapter | SubChapter | Section | SubSection | Title" mode="toc">
  <xsl:param name="parent-number"/>
  <xsl:variable name="local-number" select="1+count(preceding-sibling::*[name()=name(current())])"/>
  <xsl:variable name="number">
    <xsl:if test="$parent-number">
      <xsl:value-of select="$parent-number"/>
      <xsl:text>.</xsl:text>
    </xsl:if>
    <xsl:value-of select="$local-number"/>
  </xsl:variable>
  <xsl:variable name="cmdname">
    <xsl:choose>
      <xsl:when test="self::Chapter">TOClineI</xsl:when>
      <xsl:when test="self::SubChapter">TOClineII</xsl:when>
      <xsl:when test="self::Section">TOClineIII</xsl:when>
      <xsl:when test="self::SubSection">TOClineIV</xsl:when>
      <xsl:otherwise>TOClineV</xsl:otherwise>
    </xsl:choose>
  </xsl:variable>
  <cmd name="{$cmdname}" nl2="1">
    <parm>
      <xsl:for-each select="Heading">
        <xsl:call-template name="genid">
          <xsl:with-param name="tail">
            <xsl:text>head.</xsl:text><xsl:value-of select="$number"/>
          </xsl:with-param>
        </xsl:call-template>
      </xsl:for-each>
    </parm>
    <parm>
      <xsl:variable name="s-prefix">
        <xsl:choose>
          <xsl:when test="self::Chapter">
            <xsl:call-template name="translate">
              <xsl:with-param name="id" select="'toc-chapter'"/>
              <xsl:with-param name="language" select="$language"/>
            </xsl:call-template>
          </xsl:when>
          <xsl:otherwise></xsl:otherwise>
        </xsl:choose>
      </xsl:variable>
      <xsl:call-template name="text-before-number-pos">
        <xsl:with-param name="s" select="$s-prefix"/>
      </xsl:call-template>
      <xsl:value-of select="$number"/>
      <xsl:call-template name="text-after-number-pos">
        <xsl:with-param name="s" select="$s-prefix"/>
      </xsl:call-template>
    </parm>
    <parm><xsl:apply-templates select="Heading/node()" mode="toc"/></parm>
  </cmd>
  <xsl:apply-templates select="Chapter | SubChapter | Section | SubSection | Title" mode="toc">
    <xsl:with-param name="parent-number" select="$number"/>
  </xsl:apply-templates>
</xsl:template>

<xsl:template match="IndexAnnex" mode="toc">
  <cmd name="TOClineIb">
    <parm>index</parm>
    <parm>
      <xsl:call-template name="translate">
        <xsl:with-param name="id" select="'index'"/>
        <xsl:with-param name="language" select="$language"/>
      </xsl:call-template>
    </parm>
  </cmd>
</xsl:template>

<!-- ================= / TOC ======================== -->

<!-- =============== Special pages ================== -->

<xsl:template name="set-running-header">
  <cmd name="SetRunningHeader"><parm>
    <xsl:if test="parent::SubChapter">
      <xsl:apply-templates select="../parent::Chapter/Heading/node()" mode="plaintext"/>
      <xsl:text> / </xsl:text>
    </xsl:if>
    <xsl:apply-templates mode="plaintext"/>
  </parm></cmd>
</xsl:template>

<xsl:template name="set-running-header-for-section">
</xsl:template>

<!-- index page -->

<xsl:template match="IndexAnnex">
  <!-- generate data for future index -->
  <xsl:variable name="content">
    <IndexTerms language="{$language}">
      <xsl:copy-of select="//IndexEntry"/>
    </IndexTerms>
  </xsl:variable>
  <exsl:document href="{$indexterms_file_basename}.xml" method="xml">
    <xsl:copy-of select="$content"/>
  </exsl:document>
  <!-- create an index page, include generated index -->
  <env name="IndexPages">
    <parm>
      <xsl:call-template name="translate">
        <xsl:with-param name="id" select="'index'"/>
        <xsl:with-param name="language" select="$language"/>
      </xsl:call-template>
    </parm>
    <parm>
      <xsl:call-template name="setid">
        <xsl:with-param name="id" select="'index'"/>
      </xsl:call-template>
    </parm>
    <TeXML escape="0">
      <cmd name="input">
        <parm><xsl:value-of select="substring($indexterms_file_basename,0,string-length($indexterms_file_basename)-4)"/></parm>
      </cmd>
    </TeXML>
  </env>
</xsl:template>

<xsl:template match="TeXDirect">
  <TeXML escape="0" ligatures="1" emptylines="1" ws="1">
    <xsl:value-of select="."/>
  </TeXML>
</xsl:template>

<xsl:template match="Wingdings">
  <xsl:choose>
    <xsl:when test="'Released'=@Character"><cmd name="bitcheckbld"/></xsl:when>
    <xsl:when test="'CheckboxEmpty'=@Character"><cmd name="bitcheckbox"/></xsl:when>
    <xsl:when test="'CheckboxMarked'=@Character"><cmd name="bitsquareVI"/></xsl:when>
    <xsl:when test="'ArrowBlack'=@Character"><cmd name="bitarrowright"/></xsl:when>
    <xsl:when test="'ArrowWhite'=@Character"><cmd name="bitactionarrow"/></xsl:when>
    <xsl:when test="'CircleBlack'=@Character"><cmd name="bitcircleVI"/></xsl:when>
    <xsl:when test="'CircleWhite'=@Character"><cmd name="bitringII"/></xsl:when>
    <xsl:otherwise>
      <xsl:message>*** Unknown Wingdings character: '<xsl:value-of select="@Character"/>'</xsl:message>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template match="Code">
  <env name="BitListing" nl2="1" nl3="1">
    <env name="lstlisting">
      <xsl:if test="@Language">
        <opt>language=<xsl:value-of select="@Language"/></opt>
      </xsl:if>
      <TeXML escape="0" ws="1" ligatures="1" emptylines="1">
        <xsl:value-of select="."/>
      </TeXML>
    </env>
  </env>
</xsl:template>

<xsl:template match="Footnote">
  <cmd name="footnote">
    <parm><xsl:apply-templates/></parm>
  </cmd>
</xsl:template>

<xsl:template match="SoftwareButton">
  <cmd name="SoftwareButton">
    <parm><xsl:apply-templates/></parm>
  </cmd>
</xsl:template>

</xsl:stylesheet>
