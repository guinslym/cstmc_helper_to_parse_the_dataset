<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="xml" version="1.0" encoding="UTF-8"
        indent="yes" />
        <xsl:strip-space elements="*"/>
    <xsl:template match="@* | node()">
        <xsl:copy>
            <xsl:apply-templates select="@* | node()" />
        </xsl:copy>
    </xsl:template>
    <xsl:template match="atom">
        <xsl:element name="{@name}">
            <xsl:apply-templates />
        </xsl:element>
    </xsl:template>
    <xsl:template match="table">
        <xsl:element name="{@name}">
            <xsl:apply-templates />
        </xsl:element>
    </xsl:template>
    <xsl:template match="tuple">
      <xsl:choose>
        <xsl:when test="@name">
        <xsl:element name="{@name}">
             <xsl:apply-templates />
        </xsl:element>
        </xsl:when>
        <xsl:otherwise>
         <xsl:copy>
        <xsl:apply-templates />
          </xsl:copy>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:template>
</xsl:stylesheet>