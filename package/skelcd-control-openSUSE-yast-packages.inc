######################################################################
#
# Here is the list of Yast packages which are needed in the
# installation system (inst-sys) for the Yast installer
#
# Generic Yast packages needed for the installer
#
######################################################################
Requires:       autoyast2
Requires:       yast2-add-on
Requires:       yast2-fcoe-client
# For creating the AutoYast profile at the end of installation (bnc#887406)
Requires:       yast2-firewall
# instsys_cleanup
Requires:       yast2-installation >= 3.1.201
Requires:       yast2-iscsi-client
Requires:       yast2-kdump
Requires:       yast2-multipath
Requires:       yast2-network >= 3.1.24
Requires:       yast2-nfs-client
Requires:       yast2-ntp-client
Requires:       yast2-proxy
# this is the default theme
Requires:       yast2-qt-branding-openSUSE
Requires:       yast2-services-manager
Requires:       yast2-configuration-management
Requires:       yast2-slp
Requires:       yast2-theme
Requires:       yast2-trans-stats
Requires:       yast2-tune
Requires:       yast2-update
Requires:       yast2-users
Requires:       yast2-x11
# Ruby debugger in the inst-sys (FATE#318421)
Requires:       rubygem(%{rb_default_ruby_abi}:byebug)

# Architecture specific packages
%ifarch s390 s390x
Requires:       yast2-reipl >= 3.1.4
Requires:       yast2-s390
%endif

%ifarch %ix86 x86_64
Requires:       yast2-vm
%endif

# vim:syntax=spec
