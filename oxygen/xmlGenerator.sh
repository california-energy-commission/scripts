#!/bin/sh
# XML Generator Startup script
# (c) 2017 Syncro Soft SRL.

oldpwd=`pwd`

# Resolve the location of the oxygen installation.
# This includes resolving any symlinks.
PRG=$0

# Check OS
OS=`uname -s`
if [ "$OS" == "Darwin" ]
then
# OS X was detected
    cd "`dirname "$PRG"`"
    PRG=`basename "$PRG"`

    while [ -L "$PRG" ]
    do
        PRG="`readlink "$PRG"`"
        cd "`dirname "$PRG"`"
        PRG="`basename "$PRG"`"
    done
else
# Assuming is Linux
    while [ -h "$PRG" ]; do
        ls=`ls -ld "$PRG"`
        link=`expr "$ls" : '^.*-> \(.*\)$' 2>/dev/null`
        if expr "$link" : '^/' 2> /dev/null >/dev/null; then
            PRG="$link"
        else
            PRG="`dirname "$PRG"`/$link"
        fi
    done
fi

OXYGEN_HOME=`dirname "$PRG"`/../

# Absolutize dir
cd "${OXYGEN_HOME}"; OXYGEN_HOME=`pwd`
cd "${oldpwd}"; unset oldpwd

# Classpath
CP=$OXYGEN_HOME:$OXYGEN_HOME/classes:$OXYGEN_HOME/lib:$OXYGEN_HOME/lib/oxygen.jar:$OXYGEN_HOME/lib/oxygenDeveloper.jar:$OXYGEN_HOME/lib/*

OXYGEN_JAVA=java
if [ -f "${JAVA_HOME}/bin/java" ]
then
  OXYGEN_JAVA="${JAVA_HOME}/bin/java"
fi
if [ -f "${OXYGEN_HOME}/jre/bin/java" ]
then
  OXYGEN_JAVA="${OXYGEN_HOME}/jre/bin/java"
fi
if [ -f "${OXYGEN_HOME}/.install4j/jre.bundle/Contents/Home/jre/bin/java" ]
then
  OXYGEN_JAVA="${OXYGEN_HOME}/.install4j/jre.bundle/Contents/Home/jre/bin/java"
fi
if [ -f "${OXYGEN_HOME}/.install4j/jre.bundle/Contents/Home/bin/java" ]
then
  OXYGEN_JAVA="${OXYGEN_HOME}/.install4j/jre.bundle/Contents/Home/bin/java"
fi

"${OXYGEN_JAVA}"\
 -Xmx512m\
 -XX:SoftRefLRUPolicyMSPerMB=10\
 -cp "$CP"\
 -Djava.awt.headless=true\
 ro.sync.xml.generator.XMLInstanceGenerator "$@"