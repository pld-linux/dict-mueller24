%define		dictname mueller24
Summary:	English-Russian dictionary for dictd
Summary(pl.UTF-8):	Słownik angielsko-rosyjski dla dictd
Name:		dict-%{dictname}
Version:	1.6
Release:	4
License:	unknown
Group:		Applications/Dictionaries
Source0:	http://mueller-dic.chat.ru/Mueller24.tgz
# Source0-md5:	386d71c149f3f793d3ff064fd4b16c65
#Source1:	http://www.math.sunysb.edu/~comech/tools/to-dict
Source1:	to-dict
URL:		http://mueller-dic.chat.ru/
BuildRequires:	dictfmt
BuildRequires:	dictzip
BuildRequires:	iconv
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	%{_sysconfdir}/dictd
Requires:	dictd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Electronic version of 24th edition of English-Russian dictionary by V.
K. Mueller.

%description -l pl.UTF-8
Elektroniczna wersja 24. wydania słownika angielsko rosyjskiego V. K.
Muellera.

%prep
%setup -q -c
cp %{SOURCE1} .
chmod +x ./to-dict

%build
iconv -f koi8-r -t utf-8 usr/local/share/dict/Mueller24.koi >usr/local/share/dict/Mueller24.utf8
iconv -f koi8-r -t utf-8 usr/local/share/mova/Mueller24_koi.txt >usr/local/share/mova/Mueller24_utf8.txt
LC_ALL=ru_RU.utf-8 ./to-dict --src-data usr/local/share/dict/Mueller24.utf8 mueller24.data
LC_ALL=ru_RU.utf-8 ./to-dict --data-dict mueller24.data mueller24 && rm -f mueller24.data

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
%service -q dictd restart

%postun
if [ "$1" = 0 ]; then
	%service -q dictd restart
fi

%files
%defattr(644,root,root,755)
%doc usr/local/share/mova/Mueller24.txt
%lang(ru) %doc usr/local/share/mova/Mueller24_utf8.txt
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dictd/%{dictname}.dictconf
%{_datadir}/dictd/%{dictname}.*
