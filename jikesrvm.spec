Summary:	Jikes RVM (Research Virtual Machine)
Name:		jikesrvm
Version:	2.3.3
Release:	0.1
License:	CPL v1.0
Group:		Development/Languages/Java
Source0:	ftp://www-126.ibm.com/pub/%{name}/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	ec0fb55a9573727928f82dce46ca5d49
# classpath license: GPL with a special exception.
# http://www.gnu.org/software/classpath/license.html
Source1:	ftp://ftp.gnu.org/gnu/classpath/classpath-0.10.tar.gz
# Source1-md5:	a59a5040f9c1237dbf27bfc668919943
URL:		http://oss.software.ibm.com/developerworks/oss/jikesrvm/index.shtml
BuildRequires:	gcc
BuildRequires:	jikes = 1.18
BuildRequires:	jre
BuildRequires:	sed >= 4.0
#Requires:	-
#Provides:	-
#Obsoletes:	-
#Conflicts:	-
ExclusiveArch:	i686 pentium3 pentium4 athlon ppc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Jikes RVM (Research Virtual Machine) provides the research community
with a flexible open testbed to prototype virtual machine technologies
and experiment with a large variety of design alternatives.

Jikes RVM runs on Linux/IA-32, AIX/PowerPC, OSX/PowerPC, and
Linux/PowerPC platforms and advances the state-of-the-art of virtual
machine technologies for dynamic compilation, adaptive optimization,
garbage collection, thread scheduling, and synchronization. A
distinguishing characteristic of Jikes RVM is that it is implemented
in the Java programming language and is self-hosted i.e., its Java
code runs on itself without requiring a second virtual machine. Most
other virtual machines for the Java platform are written in native
code (typically, C or C++). A Java implementation provides ease of
portability, and a seamless integration of virtual machine and
application resources such as objects, threads, and operating-system
interfaces.

%prep
%setup -q
mkdir classpath && tar xzf %{SOURCE1} -C classpath && mv classpath/classpath{-*,}
sed -i "s:HOST_JAVA_HOME=.*:HOST_JAVA_HOME=%{_libdir}/java:" rvm/config/*-linux-gnu

%build
export RVM_ROOT=$PWD
%ifarch %{ix86}
export RVM_HOST_CONFIG="$RVM_ROOT/rvm/config/i686-pc-linux-gnu"
%endif
%ifarch ppc
export RVM_HOST_CONFIG="$RVM_ROOT/rvm/config/powerpc-unknown-linux-gnu"
%endif
export RVM_BUILD=$RVM_ROOT/build
export PATH=$PATH:$RVM_ROOT/rvm/bin
export CLASSPATH_ROOT=$RVM_ROOT/classpath

# fast build, low rvm performance.
rvm/bin/jconfigure prototype
# very slow build with optimization (it needs ~0.5GBram) -> high rvmperformance.
# rvm/bin/jconfigure production

cd $RVM_BUILD
./jbuild

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_javadir}}

cd build
install	JikesRVM \
	$RPM_BUILD_ROOT%{_bindir}/rvm
install	RVM.classes/{jksvm,rvmrt}.jar \
	$RPM_BUILD_ROOT%{_javadir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc rvm/ReleaseNotes*
%attr(755,root,root) %{_bindir}/rvm
%{_javadir}/*.jar