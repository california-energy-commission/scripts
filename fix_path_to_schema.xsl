<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    exclude-result-prefixes="xs"
    version="2.0">
    
    <xsl:strip-space elements="*"/>
    
    <!-- Runs via a oxygen XSLT 2.0 transformation scenario with Saxon 9+ with the main template as entry point
         It updates all the XML files in the pathToXML directory with the correct xsi:schemaLocation or path to XML 
         Schema files that validates them.  Allows for each developer to have a different
         directory setup.  Which means for this project the parent folder of 'Prescriptive_Nonres'
         can be whatever you like. Also orders alphabetically all the namespace and attribute nodes on the 
         'ComplianceDocumentPackage' root element  -->
    
    <!-- Default path for this projects XML test files relative to this file 
         Could be changed to '../test_files/herinson/xml/'  -->
    <xsl:param name="pathToXML" select="'../test-files/john/xml/'"/>
    
    <!-- Default path for this project means that test-files/john/xml/
         directory is inside the project folder '2019-HERS-Documents-Development'
         Otherwise the project can be at any path relative to the
         XML test files -->
    <xsl:param name="projectPath" select="''"/>
    
    <!-- Must pass both pathToXML and projectPath if not using the default
         parameter values -->
    
    <xsl:template name="main"> 
        <xsl:for-each select="collection(concat(resolve-uri($pathToXML),'/?select=*.xml;recurse=yes;'))">
            <xsl:variable name="location" select="document-uri(.)"/>
            <xsl:apply-templates select="*[local-name(.) = 'ComplianceDocumentPackage']">
                <xsl:with-param name="location" select="$location"/>
                <xsl:with-param name="pathToProject" select="$projectPath"/>
                <xsl:with-param name="subFolders" select="'test-files/'"/>
            </xsl:apply-templates>
        </xsl:for-each>
    </xsl:template>    
    
    <xsl:template match="*[local-name(.) = 'ComplianceDocumentPackage']">
        <xsl:param name="location"/>
        <xsl:param name="pathToProject"/>
        <xsl:param name="subFolders"/>
        
        <xsl:variable name="pathOnDrive">
            <xsl:choose>
                <!--  default project setup with sub /test-files/ folders      -->
                <xsl:when test="$pathToProject = ''">
                    <xsl:value-of select="substring-before($location,$subFolders)"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:variable name="path" select="resolve-uri($pathToProject)"/>
                    <xsl:choose>
                        <xsl:when test="ends-with($path,'/')">
                            <xsl:value-of select="$path"/>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:value-of select="concat($path,'/')"/>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:otherwise>
            </xsl:choose>        
        </xsl:variable>
        <!--
        <xsl:message>1: <xsl:value-of select="$pathToProject"/></xsl:message>
        <xsl:message>2: <xsl:value-of select="$location"/></xsl:message>
        <xsl:message>3: <xsl:value-of select="$pathOnDrive"/></xsl:message>
        -->
        <xsl:result-document href="{$location}" indent="yes" encoding="UTF-8">            
            <xsl:variable name="namespaceUri" select="namespace-uri(.)"/>
            <xsl:element name="ComplianceDocumentPackage" namespace="{$namespaceUri}">
                <xsl:for-each select="namespace::*">
                    <xsl:sort select="name(.)"/>
                    <xsl:namespace name="{name(.)}">
                        <xsl:value-of select="."/>
                    </xsl:namespace>
                </xsl:for-each>
                <xsl:apply-templates select="@*">
                    <xsl:sort select="name(.)"/>
                    <xsl:with-param name="pathOnDrive" select="$pathOnDrive"/>
                </xsl:apply-templates>
                <xsl:if test="not(@xsi:schemaLocation)">
                    <xsl:variable name="nSpace" select="tokenize($namespaceUri,'/')[last()]"/>
                    <xsl:attribute name="xsi:schemaLocation" select="concat($namespaceUri, ' ', $pathOnDrive, 'system/2019-HERS-Documents-Schema/deployed/schema/', substring($nSpace,1,4), '/', $nSpace, '.xsd')"/>
                </xsl:if>
                <xsl:apply-templates select="node()"/>
            </xsl:element>
        </xsl:result-document>
    </xsl:template>    
    
    <xsl:template match="@xsi:schemaLocation">
        <xsl:param name="pathOnDrive"/>  
        <xsl:variable name="type" select="subsequence(reverse(tokenize(., '/')), 2, 1)"/>
        
        <xsl:attribute name="{name(.)}">
            <xsl:choose>
                <xsl:when test="$type = 'besm'">
                    <xsl:variable name="type" select="substring(tokenize(., '/')[last()],1,4)"/>
                    <xsl:value-of select="concat(.,' ',$pathOnDrive,'system/2019-HERS-Documents-Schema/deployed/schema/',$type,'/',subsequence(reverse(tokenize(., '/')), 1, 1),'.xsd')"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="concat(substring-before(.,' '),' ',$pathOnDrive,'system/2019-HERS-Documents-Schema/deployed/schema/',$type,'/',subsequence(reverse(tokenize(., '/')), 1, 1))"/>
                 </xsl:otherwise>
            </xsl:choose>
          </xsl:attribute>
    </xsl:template>
    
    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>
    
</xsl:stylesheet>