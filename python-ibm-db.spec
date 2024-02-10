#
# Conditional build:
%bcond_with	tests	# tests with IBM DB2
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Python DBI driver for DB2 (LUW, zOS, i5) and IDS
Summary(pl.UTF-8):	Sterownik DBI dla Pythona do baz DB2 (LUW, zOS, i5) oraz IDS
Name:		python-ibm_db
# keep 3.1.x here for python2 support
Version:	3.1.4
Release:	1
License:	Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/ibm-db/
Source0:	https://files.pythonhosted.org/packages/source/i/ibm_db/ibm_db-%{version}.tar.gz
# Source0-md5:	2ec8abb1e2050f670f6afd4c305dfdad
URL:		https://pypi.org/project/ibm-db/
BuildRequires:	ibm-db2-clidriver-devel
%if %{with python2}
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.5
BuildRequires:	python3-setuptools
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python-modules >= 1:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python DBI driver for DB2 (LUW, zOS, i5) and IDS.

%description -l pl.UTF-8
Sterownik DBI dla Pythona do baz DB2 (LUW, zOS, i5) oraz IDS.

%package -n python3-ibm_db
Summary:	Python DBI driver for DB2 (LUW, zOS, i5) and IDS
Summary(pl.UTF-8):	Sterownik DBI dla Pythona do baz DB2 (LUW, zOS, i5) oraz IDS
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.5

%description -n python3-ibm_db
Python DBI driver for DB2 (LUW, zOS, i5) and IDS.

%description -n python3-ibm_db -l pl.UTF-8
Sterownik DBI dla Pythona do baz DB2 (LUW, zOS, i5) oraz IDS.

%prep
%setup -q -n ibm_db-%{version}

%if %{with tests}
cat >config.py <<'EOF'
# TODO
test_dir = 'ibm_db_tests'
database = 'sample'
user = 'user'
password = 'password'
hostname = 'localhost'
port = 50000
auth_user = 'auth_user'
auth_pass = 'auth_pass'
tc_user = 'tc_user'
tc_pass = 'tc_pass'
EOF
%endif

%build
export IBM_DB_DIR=%{_libdir}/clidriver
export IBM_DB_LIB=%{_libdir}/clidriver/lib

%if %{with python2}
%py_build

%if %{with tests}
PYTHONPATH=$(echo $(pwd)/build-2/lib.linux-*) \
%{__python} ibmdb_tests.py
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTHONPATH=$(echo $(pwd)/build-3/lib.linux-*) \
%{__python3} ibmdb_tests.py
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/{ibmdb_tests,testfunctions}.py*
%{__rm} -r $RPM_BUILD_ROOT%{py_sitedir}/{certs,clidriver,ibm_db_dlls,ibm_db_tests}
%endif

%if %{with python3}
%py3_install

%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/{ibmdb_tests,testfunctions}.py*
%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/__pycache__/{ibmdb_tests,testfunctions}.*.py*
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/{certs,clidriver,ibm_db_dlls,ibm_db_tests}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.md NOTES.md README.md
%attr(755,root,root) %{py_sitedir}/ibm_db.so
%{py_sitedir}/ibm_db_dbi.py[co]
%{py_sitedir}/ibm_db-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-ibm_db
%defattr(644,root,root,755)
%doc CHANGES.md NOTES.md README.md
%attr(755,root,root) %{py3_sitedir}/ibm_db.cpython-*.so
%{py3_sitedir}/ibm_db_dbi.py
%{py3_sitedir}/__pycache__/ibm_db_dbi.cpython-*.py[co]
%{py3_sitedir}/ibm_db-%{version}-py*.egg-info
%endif
