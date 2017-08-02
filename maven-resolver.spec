%{?scl:%scl_package maven-resolver}
%{!?scl:%global pkg_name %{name}}

Name:           %{?scl_prefix}maven-resolver
Epoch:          1
Version:        1.0.3
Release:        5.1%{?dist}
License:        ASL 2.0
Summary:        Apache Maven Artifact Resolver library
URL:            http://maven.apache.org/resolver/
Source0:        http://archive.apache.org/dist/maven/resolver/%{pkg_name}-%{version}-source-release.zip
BuildArch:      noarch

BuildRequires:  %{?scl_prefix}maven-local
BuildRequires:  %{?scl_prefix}mvn(javax.inject:javax.inject)
BuildRequires:  %{?scl_prefix}mvn(junit:junit)
BuildRequires:  %{?scl_prefix}mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  %{?scl_prefix}mvn(org.apache.httpcomponents:httpclient)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven:maven-parent:pom:)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.wagon:wagon-provider-api)
BuildRequires:  %{?scl_prefix}mvn(org.codehaus.plexus:plexus-classworlds)
BuildRequires:  %{?scl_prefix}mvn(org.codehaus.plexus:plexus-component-annotations)
BuildRequires:  %{?scl_prefix}mvn(org.codehaus.plexus:plexus-component-metadata)
BuildRequires:  %{?scl_prefix}mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  %{?scl_prefix}mvn(org.eclipse.sisu:org.eclipse.sisu.inject)
BuildRequires:  %{?scl_prefix}mvn(org.eclipse.sisu:org.eclipse.sisu.plexus)
BuildRequires:  %{?scl_prefix}mvn(org.eclipse.sisu:sisu-maven-plugin)
BuildRequires:  %{?scl_prefix}mvn(org.hamcrest:hamcrest-library)
BuildRequires:  %{?scl_prefix}mvn(org.slf4j:jcl-over-slf4j)
BuildRequires:  %{?scl_prefix}mvn(org.slf4j:slf4j-api)
BuildRequires:  %{?scl_prefix}mvn(org.sonatype.sisu:sisu-guice::no_aop:)


%description
Apache Maven Artifact Resolver is a library for working with artifact
repositories and dependency resolution. Maven Artifact Resolver deals with the
specification of local repository, remote repository, developer workspaces,
artifact transports and artifact resolution.

%package api
Summary:   Maven Artifact Resolver API
Provides:  %{?scl_prefix}aether-api = %{epoch}:%{version}-%{release}

%description api
The application programming interface for the repository system.

%package spi
Summary:   Maven Artifact Resolver SPI
Provides:  %{?scl_prefix}aether-spi = %{epoch}:%{version}-%{release}

%description spi
The service provider interface for repository system implementations and
repository connectors.

%package util
Summary:   Maven Artifact Resolver Utilities
Provides:  %{?scl_prefix}aether-util = %{epoch}:%{version}-%{release}

%description util
A collection of utility classes to ease usage of the repository system.

%package impl
Summary:   Maven Artifact Resolver Implementation
Provides:  %{?scl_prefix}aether-impl = %{epoch}:%{version}-%{release}

%description impl
An implementation of the repository system.

%package test-util
Summary:   Maven Artifact Resolver Test Utilities
Provides:  %{?scl_prefix}aether-test-util = %{epoch}:%{version}-%{release}

%description test-util
A collection of utility classes to ease testing of the repository system.

%package connector-basic
Summary:   Maven Artifact Resolver Connector Basic
Provides:  %{?scl_prefix}aether-connector-basic = %{epoch}:%{version}-%{release}

%description connector-basic
A repository connector implementation for repositories using URI-based layouts.

%package transport-classpath
Summary:   Maven Artifact Resolver Transport Classpath
Provides:  %{?scl_prefix}aether-transport-classpath = %{epoch}:%{version}-%{release}

%description transport-classpath
A transport implementation for repositories using classpath:// URLs.

%package transport-file
Summary:   Maven Artifact Resolver Transport File
Provides:  %{?scl_prefix}aether-transport-file = %{epoch}:%{version}-%{release}

%description transport-file
A transport implementation for repositories using file:// URLs.

%package transport-http
Summary:   Maven Artifact Resolver Transport HTTP
Provides:  %{?scl_prefix}aether-transport-http = %{epoch}:%{version}-%{release}

%description transport-http
A transport implementation for repositories using http:// and https:// URLs.

%package transport-wagon
Summary:   Maven Artifact Resolver Transport Wagon
Provides:  %{?scl_prefix}aether-transport-wagon = %{epoch}:%{version}-%{release}

%description transport-wagon
A transport implementation based on Maven Wagon.

%package        javadoc
Summary:        API documentation for %{pkg_name}

%description    javadoc
This package provides %{summary}.

%prep
%setup -n %{pkg_name}-%{version} -q

# tests require jetty 7
%pom_remove_dep :::test maven-resolver-transport-http
rm -r maven-resolver-transport-http/src/test

# generate OSGi manifests
for pom in $(find -mindepth 2 -name pom.xml) ; do
  %pom_add_plugin "org.apache.felix:maven-bundle-plugin" $pom \
  "<configuration>
    <instructions>
      <Bundle-SymbolicName>\${project.groupId}$(sed 's:./maven-resolver::;s:/pom.xml::;s:-:.:g' <<< $pom)</Bundle-SymbolicName>
      <_nouses>true</_nouses>
    </instructions>
  </configuration>
  <executions>
    <execution>
      <id>create-manifest</id>
      <phase>process-classes</phase>
      <goals><goal>manifest</goal></goals>
    </execution>
  </executions>"
done
%pom_add_plugin "org.apache.maven.plugins:maven-jar-plugin" pom.xml \
"<configuration>
  <archive>
    <manifestFile>\${project.build.outputDirectory}/META-INF/MANIFEST.MF</manifestFile>
  </archive>
</configuration>"

%mvn_package :maven-resolver
%mvn_alias 'org.apache.maven.resolver:maven-resolver{*}' 'org.eclipse.aether:aether@1'
%mvn_file ':maven-resolver{*}' %{pkg_name}/maven-resolver@1 aether/aether@1

%build
%mvn_build -s

%install
%mvn_install

%files -f .mfiles
%license LICENSE NOTICE

%files api -f .mfiles-%{pkg_name}-api
%license LICENSE NOTICE

%files spi -f .mfiles-%{pkg_name}-spi

%files util -f .mfiles-%{pkg_name}-util

%files impl -f .mfiles-%{pkg_name}-impl

%files test-util -f .mfiles-%{pkg_name}-test-util

%files connector-basic -f .mfiles-%{pkg_name}-connector-basic

%files transport-classpath -f .mfiles-%{pkg_name}-transport-classpath

%files transport-file -f .mfiles-%{pkg_name}-transport-file

%files transport-http -f .mfiles-%{pkg_name}-transport-http

%files transport-wagon -f .mfiles-%{pkg_name}-transport-wagon

%files javadoc -f .mfiles-javadoc
%license LICENSE NOTICE

%changelog
* Wed Jun 21 2017 Java Maintainers <java-maint@redhat.com> - 1:1.0.3-5.1
- Automated package import and SCL-ization

* Wed May 24 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:1.0.3-5
- Add aether alias for main POM file

* Tue May 23 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:1.0.3-4
- Fix duplicate Bundle-SymbolicName in OSGi manifests

* Mon May 15 2017 Mat Booth <mat.booth@redhat.com> - 1:1.0.3-3
- Restore OSGi metadata that was lost in the switch from "aether" to
  "maven-resolver"

* Wed Apr 12 2017 Michael Simacek <msimacek@redhat.com> - 1:1.0.3-2
- Split into subpackages
- Obsolete and provide aether

* Tue Apr 11 2017 Michael Simacek <msimacek@redhat.com> - 1.0.3-1
- Initial packaging
