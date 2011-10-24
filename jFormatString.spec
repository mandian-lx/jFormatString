Name:           jFormatString
Version:        0
Release:        0.5.20081016svn
Summary:        Java format string compile-time checker

Group:          Development/Java
License:        GPLv2 with exceptions
URL:            https://jformatstring.dev.java.net/
# There has been no official release yet.  This is a snapshot of the Subversion
# repository as of 16 Oct 2008.  Use the following commands to generate the
# tarball:
#   svn export -r 8 https://jformatstring.dev.java.net/svn/jformatstring/trunk \
#     jformatstring --username guest
#   (The password is "guest".)
#   tar -cjvf jFormatString-0.tar.bz2 jformatstring
Source0:        %{name}-%{version}.tar.bz2
# This patch has not been sent upstream, since it is Fedora specific.  This
# gives the build system the path to the appropriate junit jar.
Patch0:         %{name}-build.patch

BuildRequires:  ant, java-devel, java-javadoc, jpackage-utils, junit4
Requires:       java, jpackage-utils

BuildArch:      noarch

%description
This project is derived from Sun's implementation of java.util.Formatter.  It
is designed to allow compile time checks as to whether or not a use of a
format string will be erroneous when executed at runtime.

%package javadoc
Summary:        Javadoc documentation for %{name}
Group:          Development/Java
Requires:       %{name} = %{version}-%{release}, java-javadoc
Requires:       jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n jformatstring
%patch0 -p1

%build
# Build the JAR
cd jFormatString
ant
cd ..

# Create the javadocs
mkdir docs
javadoc -d docs -source 1.5 -sourcepath jFormatString/src/java \
  -classpath jFormatString/build/classes:%{_javadir}/junit4.jar \
  -link file://%{_javadocdir}/java edu.umd.cs.findbugs.formatStringChecker

%install
rm -rf $RPM_BUILD_ROOT

# JAR files
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p %{name}/build/%{name}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

# Javadocs
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -rp docs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%files
%defattr(-,root,root,-)
%doc www/index.html jFormatString/LICENSE
%{_javadir}/%{name}*

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}*

