#
# spec file for package skelcd-control-openSUSE
#
# Copyright (c) 2017 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


######################################################################
#
# IMPORTANT: Please do not change the control file or this spec file
#   in build service directly, use
#   https://github.com/yast/skelcd-control-openSUSE repository
#
#   See https://github.com/yast/skelcd-control-openSUSE/blob/master/CONTRIBUTING.md
#   for more details.
#
######################################################################
Name:           skelcd-control-openSUSE
Version:        15.2.1
Release:        0
Summary:        The openSUSE Installation Control file
License:        MIT
Group:          Metapackages
Url:            https://github.com/yast/skelcd-control-openSUSE
Source:         skelcd-control-openSUSE-%{version}.tar.bz2
Source1:        skelcd-control-openSUSE-yast-packages.inc
# we do not distribute it, but need to have it here, otherwise build service checks complain
Source99:       README.md
# xmllint
BuildRequires:  libxml2-tools
# xsltproc
BuildRequires:  libxslt-tools
# RNG schema
BuildRequires:  yast2-installation-control >= 4.0.10

Conflicts:      product_control
Provides:       product_control
# yast requirements
%include %{SOURCE1}

%if 0%{?suse_version} >= 1500
%define skelcdpath /usr/lib/skelcd
%endif

%package -n skelcd-control-Iodine
Summary:        The Iodine Installation Control file
License:        MIT
Group:          Metapackages
Conflicts:      product_control
Provides:       product_control
# yast requirements
%include %{SOURCE1}
# rpm 4.13 feature
RemovePathPostfixes: .iodine

%description
This package contains the control file used for openSUSE installation.

%description -n skelcd-control-Iodine
This package contains the control file used for Iodine installation.


%prep

%setup -q -n skelcd-control-openSUSE-%{version}

%build
make %{?_smp_mflags} -C control

%check
make %{?_smp_mflags} -C control check

%install
#
# Add control file
#
%if "%{name}" == "skelcd-control-openSUSE-promo"
    CONTROL_FILE=control.openSUSE-promo.xml
%else
    CONTROL_FILE=control.openSUSE.xml
%endif

mkdir -p $RPM_BUILD_ROOT%{?skelcdpath}/CD1
install -m 644 control/${CONTROL_FILE} $RPM_BUILD_ROOT%{?skelcdpath}/CD1/control.xml
install -m 644 control/control.iodine.xml $RPM_BUILD_ROOT%{?skelcdpath}/CD1/control.xml.iodine

%ifarch aarch64 %arm ppc ppc64 ppc64le
    ports_arch="%{_arch}"
    %ifarch ppc ppc64 ppc64le
        ports_arch="ppc"
    %endif
    %ifarch armv6l armv6hl
        ports_arch="armv6hl"
    %endif
    %ifarch armv7l armv7hl
        ports_arch="armv7hl"
    %endif
    for control in %{buildroot}%{?skelcdpath}/CD1/control.xml*; do
	sed -i -e "s,http://download.opensuse.org/distribution/,http://download.opensuse.org/ports/$ports_arch/distribution/," $control
	sed -i -e "s,http://download.opensuse.org/tumbleweed/,http://download.opensuse.org/ports/$ports_arch/tumbleweed/," $control
	# Leap debug repo (from :Update) has a different path since all 'ports' (ARM and PPC) are in the same repo
	sed -i -e "s,http://download.opensuse.org/debug/update,http://download.opensuse.org/ports/debug/update," $control
	sed -i -e "s,http://download.opensuse.org/debug/,http://download.opensuse.org/ports/$ports_arch/debug/," $control
	sed -i -e "s,http://download.opensuse.org/source/,http://download.opensuse.org/ports/$ports_arch/source/," $control
	sed -i -e "s,http://download.opensuse.org/update/leap/,http://download.opensuse.org/ports/update/leap/," $control
	sed -i -e "s,http://download.opensuse.org/update/tumbleweed/,http://download.opensuse.org/ports/$ports_arch/update/tumbleweed/," $control
	#we parse out non existing non-oss repo for ports
	xsltproc -o ${control}_ports control/nonoss.xsl $control
	mv ${control}{_ports,}
	xmllint --noout --relaxng %{_datadir}/YaST2/control/control.rng $control
    done
%endif

%files
%defattr(644,root,root,755)
%if %{defined skelcdpath}
%dir %{skelcdpath}
%endif
%dir %{?skelcdpath}/CD1
%{?skelcdpath}/CD1/control.xml

%files -n skelcd-control-Iodine
%defattr(644,root,root,755)
%if %{defined skelcdpath}
%dir %{skelcdpath}
%endif
%dir %{?skelcdpath}/CD1
%{?skelcdpath}/CD1/control.xml.iodine

%changelog
