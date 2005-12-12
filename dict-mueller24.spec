%define		dictname mueller24
Summary:	English-Russian dictionary for dictd
Summary(pl):	S³ownik angielsko-rosyjski dla dictd
Name:		dict-%{dictname}
Version:	1.6
Release:	1
License:	unknown
Group:		Applications/Dictionaries
Source0:	http://mueller-dic.chat.ru/Mueller24.tgz
# Source0-md5:	386d71c149f3f793d3ff064fd4b16c65
# This one is compressed with szip: http://www.compressconsult.com/szip
#Source0:	http://www.geocities.com/mueller_dic/Mueller24.tgz
Source1:	http://www.math.sunysb.edu/~comech/tools/to-dict
# Source1-md5:	3c1b69c290fb4c06bf3456baf5bf8b97
URL:		http://mueller-dic.chat.ru/
BuildRequires:	dictfmt
BuildRequires:	dictzip
Requires:	%{_sysconfdir}/dictd
Requires:	dictd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Electronic version of 24th edition of English-Russian dictionary by V.
K. Mueller.

%description -l pl
Elektroniczna wersja 24. wydania s³ownika angielsko rosyjskiego V. K.
Muellera.

%prep
%setup -q -c

%build
cp %{SOURCE1} .
chmod +x ./to-dict
./to-dict --src-data usr/local/share/dict/Mueller24.koi mueller24.data
./to-dict --data-dict mueller24.data mueller24 && rm -f mueller24.data

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir}/dictd,%{_sysconfdir}/dictd}

dictprefix=%{_datadir}/dictd/%{dictname}
echo "# Mueller English-Russian dictionary, 24-th edition (%{version})
database %{dictname} {
	data  \"$dictprefix.dict.dz\"
	index \"$dictprefix.index\"
}" > $RPM_BUILD_ROOT%{_sysconfdir}/dictd/%{dictname}.dictconf
mv %{dictname}.* $RPM_BUILD_ROOT%{_datadir}/dictd

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/dictd ]; then
	/etc/rc.d/init.d/dictd restart 1>&2
fi

%postun
if [ -f /var/lock/subsys/dictd ]; then
	/etc/rc.d/init.d/dictd restart 1>&2 || true
fi

%files
%defattr(644,root,root,755)
%doc usr/local/share/mova/Mueller24.txt
%lang(ru) %doc usr/local/share/mova/Mueller24_koi.txt
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dictd/%{dictname}.dictconf
%{_datadir}/dictd/%{dictname}.*
