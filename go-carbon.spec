# If any of the following macros should be set otherwise,
# you can wrap any of them with the following conditions:
# - %%if 0%%{centos} == 7
# - %%if 0%%{?rhel} == 7
# - %%if 0%%{?fedora} == 23
# Or just test for particular distribution:
# - %%if 0%%{centos}
# - %%if 0%%{?rhel}
# - %%if 0%%{?fedora}
#
# Be aware, on centos, both %%rhel and %%centos are set. If you want to test
# rhel specific macros, you can use %%if 0%%{?rhel} && 0%%{?centos} == 0 condition.
# (Don't forget to replace double percentage symbol with single one in order to apply a condition)

# Generate devel rpm
%global with_devel 1
# Build project from bundled dependencies
%global with_bundled 1
# Build with debug info rpm
%global with_debug 1
# Run tests in check section
%global with_check 1
# Generate unit-test rpm
%global with_unit_test 1

%if 0%{?with_debug}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

%if ! 0%{?gobuild:1}
%define gobuild(o:) go build -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v -x %{?**};
%endif

%global provider        github
%global provider_tld    com
%global project         lomik
%global repo            go-carbon
# https://github.com/lomik/go-carbon
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}
# %%global commit          v0.11.0
# %%global shortcommit     %%(c=%%{commit}; echo ${c:0:7})

%if 0%{?el5}%{?el6}%{?amzn}
%define use_systemd 0
%else
# fedora and el>=7
%define use_systemd 1
%endif

%define carbon_user carbon
%define carbon_group carbon

Name:           go-carbon
Version:        0.11.0
Release:        1%{?dist}
Summary:        Golang implementation of Graphite/Carbon server
License:        MIT
URL:            https://github.com/lomik/go-carbon
#Source0:        https://github.com/lomik/go-carbon/archive/v%%{version}/%%{repo}-%%{version}.tar.gz
Source0:        go-carbon-%{version}-bundled.tar.gz

Source1: get_tarball.sh
Source2: git-archive-all

# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
ExclusiveArch:  %{?go_arches:%{go_arches}}%{!?go_arches:%{ix86} x86_64 aarch64 %{arm}}
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

%if ! 0%{?with_bundled}
# go-carbon.go
BuildRequires: golang(github.com/lomik/zapwriter)
BuildRequires: golang(github.com/sevlyar/go-daemon)

# api/sample/cache-query/cache-query.go
BuildRequires: golang(google.golang.org/grpc)

# Remaining dependencies not included in main packages
BuildRequires: golang(github.com/syndtr/goleveldb/leveldb/opt)
BuildRequires: golang(github.com/alyu/configparser)
BuildRequires: golang(github.com/dgryski/go-trigram)
BuildRequires: golang(github.com/lomik/stop)
BuildRequires: golang(github.com/Shopify/sarama)
BuildRequires: golang(github.com/dgryski/go-expirecache)
BuildRequires: golang(github.com/dgryski/httputil)
BuildRequires: golang(golang.org/x/net/context)
BuildRequires: golang(github.com/lomik/go-whisper)
BuildRequires: golang(github.com/syndtr/goleveldb/leveldb/filter)
BuildRequires: golang(github.com/gogo/protobuf/gogoproto)
BuildRequires: golang(github.com/syndtr/goleveldb/leveldb)
BuildRequires: golang(github.com/gogo/protobuf/proto)
BuildRequires: golang(github.com/BurntSushi/toml)
BuildRequires: golang(github.com/lomik/og-rek)
BuildRequires: golang(github.com/NYTimes/gziphandler)
BuildRequires: golang(github.com/lomik/graphite-pickle)
BuildRequires: golang(github.com/lomik/graphite-pickle/framing)
BuildRequires: golang(google.golang.org/grpc/reflection)
%endif

%description
%{summary}

%if 0%{?with_devel}
%package devel
Summary:       %{summary}
BuildArch:     noarch

%if 0%{?with_check} && ! 0%{?with_bundled}
BuildRequires: golang(github.com/BurntSushi/toml)
BuildRequires: golang(github.com/NYTimes/gziphandler)
BuildRequires: golang(github.com/Shopify/sarama)
BuildRequires: golang(github.com/alyu/configparser)
BuildRequires: golang(github.com/dgryski/go-expirecache)
BuildRequires: golang(github.com/dgryski/go-trigram)
BuildRequires: golang(github.com/dgryski/httputil)
BuildRequires: golang(github.com/gogo/protobuf/gogoproto)
BuildRequires: golang(github.com/gogo/protobuf/proto)
BuildRequires: golang(github.com/lomik/go-whisper)
BuildRequires: golang(github.com/lomik/graphite-pickle)
BuildRequires: golang(github.com/lomik/graphite-pickle/framing)
BuildRequires: golang(github.com/lomik/og-rek)
BuildRequires: golang(github.com/lomik/stop)
BuildRequires: golang(github.com/lomik/zapwriter)
BuildRequires: golang(github.com/syndtr/goleveldb/leveldb)
BuildRequires: golang(github.com/syndtr/goleveldb/leveldb/filter)
BuildRequires: golang(github.com/syndtr/goleveldb/leveldb/opt)
BuildRequires: golang(golang.org/x/net/context)
BuildRequires: golang(google.golang.org/grpc)
BuildRequires: golang(google.golang.org/grpc/reflection)
%endif

%if 0%{?use_systemd}
%{?systemd_requires}
BuildRequires: systemd
%endif

Requires:      golang(github.com/BurntSushi/toml)
Requires:      golang(github.com/NYTimes/gziphandler)
Requires:      golang(github.com/Shopify/sarama)
Requires:      golang(github.com/alyu/configparser)
Requires:      golang(github.com/dgryski/go-expirecache)
Requires:      golang(github.com/dgryski/go-trigram)
Requires:      golang(github.com/dgryski/httputil)
Requires:      golang(github.com/gogo/protobuf/gogoproto)
Requires:      golang(github.com/gogo/protobuf/proto)
Requires:      golang(github.com/lomik/go-whisper)
Requires:      golang(github.com/lomik/graphite-pickle)
Requires:      golang(github.com/lomik/graphite-pickle/framing)
Requires:      golang(github.com/lomik/og-rek)
Requires:      golang(github.com/lomik/stop)
Requires:      golang(github.com/lomik/zapwriter)
Requires:      golang(github.com/syndtr/goleveldb/leveldb)
Requires:      golang(github.com/syndtr/goleveldb/leveldb/filter)
Requires:      golang(github.com/syndtr/goleveldb/leveldb/opt)
Requires:      golang(golang.org/x/net/context)
Requires:      golang(google.golang.org/grpc)
Requires:      golang(google.golang.org/grpc/reflection)

Provides:      golang(%{import_path}/api) = %{version}-%{release}
Provides:      golang(%{import_path}/cache) = %{version}-%{release}
Provides:      golang(%{import_path}/carbon) = %{version}-%{release}
Provides:      golang(%{import_path}/carbonserver) = %{version}-%{release}
Provides:      golang(%{import_path}/helper) = %{version}-%{release}
Provides:      golang(%{import_path}/helper/atomicfiles) = %{version}-%{release}
Provides:      golang(%{import_path}/helper/carbonpb) = %{version}-%{release}
Provides:      golang(%{import_path}/helper/carbonzipperpb) = %{version}-%{release}
Provides:      golang(%{import_path}/helper/qa) = %{version}-%{release}
Provides:      golang(%{import_path}/helper/stat) = %{version}-%{release}
Provides:      golang(%{import_path}/persister) = %{version}-%{release}
Provides:      golang(%{import_path}/points) = %{version}-%{release}
Provides:      golang(%{import_path}/receiver) = %{version}-%{release}
Provides:      golang(%{import_path}/receiver/http) = %{version}-%{release}
Provides:      golang(%{import_path}/receiver/kafka) = %{version}-%{release}
Provides:      golang(%{import_path}/receiver/parse) = %{version}-%{release}
Provides:      golang(%{import_path}/receiver/tcp) = %{version}-%{release}
Provides:      golang(%{import_path}/receiver/udp) = %{version}-%{release}

%description devel
%{summary}

This package contains library source intended for
building other packages which use import path with
%{import_path} prefix.
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%package unit-test-devel
Summary:         Unit tests for %{name} package
%if 0%{?with_check}
#Here comes all BuildRequires: PACKAGE the unit tests
#in %%check section need for running
%endif

# test subpackage tests code from devel subpackage
Requires:        %{name}-devel = %{version}-%{release}

%if 0%{?with_check} && ! 0%{?with_bundled}
BuildRequires: golang(github.com/stretchr/testify/assert)
%endif

Requires:      golang(github.com/stretchr/testify/assert)

%description unit-test-devel
%{summary}

This package contains unit tests for project
providing packages with %{import_path} prefix.
%endif

%prep
%setup -q -n %{repo}-%{version}

%build
mkdir -p src/%{provider}.%{provider_tld}/%{project}
ln -s ../../../ src/%{import_path}

%if ! 0%{?with_bundled}
export GOPATH=$(pwd):%{gopath}
%else
# No dependency directories so far
export GOPATH=$(pwd):%{gopath}
%endif

%gobuild  %{import_path}/

%install
install -d -p %{buildroot}%{_bindir}
install -p -m 0755 %{name} %{buildroot}%{_bindir}/%{name}

install -d -p %{buildroot}%{_localstatedir}/lib/graphite
install -d -p %{buildroot}%{_localstatedir}/log/%{name}

install -d -p %{buildroot}%{_sysconfdir}/%{name}
install -p -m 0644 deploy/%{name}.conf %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
install -p -m 0644 deploy/storage-schemas.conf %{buildroot}%{_sysconfdir}/%{name}/storage-schemas.conf
install -p -m 0644 deploy/storage-aggregation.conf %{buildroot}%{_sysconfdir}/%{name}/storage-aggregation.conf

install -d -p %{buildroot}%{_sysconfdir}/logrotate.d
install -p -m 0644 deploy/%{name}.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

%if 0%{?use_systemd}
install -d -p %{buildroot}%{_unitdir}
install -p -m 0644 deploy/%{name}.service %{buildroot}%{_unitdir}/%{name}.service
%else
install -d -p %{buildroot}%{_sysconfdir}/init.d
install -p -m 0755 deploy/%{name}.init %{buildroot}%{_sysconfdir}/init.d/%{name}
%endif

# source codes for building projects
%if 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
echo "%%dir %%{gopath}/src/%%{import_path}/." >> devel.file-list
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . \( -iname "*.go" -or -iname "*.s" \) \! -iname "*_test.go" | grep -v "vendor") ; do
    dirprefix=$(dirname $file)
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$dirprefix
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> devel.file-list

    while [ "$dirprefix" != "." ]; do
        echo "%%dir %%{gopath}/src/%%{import_path}/$dirprefix" >> devel.file-list
        dirprefix=$(dirname $dirprefix)
    done
done
%endif

# testing files for this project
%if 0%{?with_unit_test} && 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
# find all *_test.go files and generate unit-test-devel.file-list
for file in $(find . -iname "*_test.go" | grep -v "vendor") ; do
    dirprefix=$(dirname $file)
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$dirprefix
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> unit-test-devel.file-list

    while [ "$dirprefix" != "." ]; do
        echo "%%dir %%{gopath}/src/%%{import_path}/$dirprefix" >> devel.file-list
        dirprefix=$(dirname $dirprefix)
    done
done
%endif

%if 0%{?with_devel}
sort -u -o devel.file-list devel.file-list
%endif

%check
%if 0%{?with_check} && 0%{?with_unit_test} && 0%{?with_devel}
%if ! 0%{?with_bundled}
export GOPATH=%{buildroot}/%{gopath}:%{gopath}
%else
# Since we aren't packaging up the vendor directory we need to link
# back to it somehow. Hack it up so that we can add the vendor
# directory from BUILD dir as a gopath to be searched when executing
# tests from the BUILDROOT dir.
ln -s ./ ./vendor/src # ./vendor/src -> ./vendor

export GOPATH=%{buildroot}/%{gopath}:$(pwd)/vendor:%{gopath}
%endif

%if ! 0%{?gotest:1}
%global gotest go test
%endif

%gotest %{import_path}/cache
%gotest %{import_path}/carbon
%gotest %{import_path}/carbonserver
# Disabled, because it breaks on low-resource build environments
# %%gotest %%{import_path}/persister
%gotest %{import_path}/points
%gotest %{import_path}/receiver/http
%gotest %{import_path}/receiver/parse
%gotest %{import_path}/receiver/tcp
%gotest %{import_path}/receiver/udp
%endif

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files
%license LICENSE.md
%doc README.md
%{_bindir}/%{name}

%dir %attr(2770, %{carbon_user}, %{carbon_group}) %{_localstatedir}/lib/graphite
%dir %attr(2770, %{carbon_user}, %{carbon_group}) %{_localstatedir}/log/%{name}

%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}/storage-schemas.conf
%config(noreplace) %{_sysconfdir}/%{name}/storage-aggregation.conf

%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}

%if 0%{?use_systemd}
%{_unitdir}/%{name}.service
%else
%{_sysconfdir}/init.d/%{name}
%endif

%if 0%{?with_devel}
%files devel -f devel.file-list
%license LICENSE.md
%doc README.md
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%files unit-test-devel -f unit-test-devel.file-list
%license LICENSE.md
%doc README.md
%endif

%pre
if ! getent group %{icinga_group} >/dev/null; then
  %{_sbindir}/groupadd -r %{carbon_group}
fi

if ! getent passwd %{carbon_user} >/dev/null; then
  %{_sbindir}/useradd -c "User for Graphite carbon" \
    --system -s /sbin/nologin -d %{_localstatedir}/lib/graphite \
    -g %{carbon_group} %{carbon_user}
fi

%post
%if 0%{?use_systemd}
%systemd_post %{name}.service
%else
/sbin/chkconfig --add %{name}
%endif

%preun
%if 0%{?use_systemd}
%systemd_preun %{name}.service
%else
/sbin/chkconfig --del %{name} || :
%endif

%postun
%if 0%{?use_systemd}
%systemd_postun_with_restart %{name}.service
%endif

%changelog
* Tue Sep 26 2017 Markus Frosch <markus.frosch@icinga.com> - 0.11.0-1
- First package for RPM
