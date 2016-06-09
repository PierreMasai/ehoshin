#!/usr/bin/env bash

# Print on the stderr output
function _stderr() {
  echo -e >&2 "- $*"
}

# Print on the standard output
function _stdout() {
  echo -e >&1 "+ $*"
}

# Detect package type from /etc/issue
function _found_arch() {
  local _ostype="$1"
  shift
  grep -qis "$*" /etc/issue && _OSTYPE="$_ostype"
}

# Detect package type
function _OSTYPE_detect() {
  _found_arch PACMAN "Arch Linux" && return
  _found_arch DPKG   "Debian GNU/Linux" && return
  _found_arch DPKG   "Ubuntu" && return
  _found_arch YUM    "CentOS" && return
  _found_arch YUM    "Red Hat" && return
  _found_arch YUM    "Fedora" && return
  _found_arch ZYPPER "SUSE" && return

  [[ -z "$_OSTYPE" ]] || return

  # See also https://github.com/icy/pacapt/pull/22
  # Please not that $OSTYPE (which is `linux-gnu` on Linux system)
  # is not our $_OSTYPE. The choice is not very good because
  # a typo can just break the logic of the program.
  if [[ "$OSTYPE" != "darwin"* ]]; then
    _stderr "Can't detect OS type from /etc/issue. Running fallback method."
  fi
  [[ -x "/usr/bin/pacman" ]]           && _OSTYPE="PACMAN" && return
  [[ -x "/usr/bin/apt-get" ]]          && _OSTYPE="DPKG" && return
  [[ -x "/usr/bin/yum" ]]              && _OSTYPE="YUM" && return
  [[ -x "/opt/local/bin/port" ]]       && _OSTYPE="MACPORTS" && return
  command -v brew >/dev/null           && _OSTYPE="HOMEBREW" && return
  [[ -x "/usr/bin/emerge" ]]           && _OSTYPE="PORTAGE" && return
  [[ -x "/usr/bin/zypper" ]]           && _OSTYPE="ZYPPER" && return
  if [[ -z "$_OSTYPE" ]]; then
    _stderr "No supported package manager installed on system"
    _stderr "(supported: apt, homebrew, pacman, portage, yum)"
    exit 1
  fi
}

# Set the package manager
function _PKG_set() {
    case "$_OSTYPE" in
        "PACMAN")     _PKG="pacman";;
        "ZYPPER")     _PKG="zypper";;
        "DPKG")       _PKG="apt-get";;
        "HOMWWBREW")  _PKG="brew";;
        "MACPORTS")   _PKG="port";;
        "YUM")        _PKG="yum";;
        "PORTAGE")    _PKG="emerge";;
    esac
}

# Set the install option
function _INSTALL_OPT_set() {
    case "$_OSTYPE" in
        "PACMAN")   _INSTALL_OPT="-S";;
        "PORTAGE")  _INSTALL_OPT="";;
        *)          _INSTALL_OPT="install";;
    esac
}

# Set the force option
function _FORCE_set() {
    case "$_OSTYPE" in
        "DPKG")     _FORCE="-y --force-yes" ;;
        "MACPORTS") _FORCE="-f" ;;
        "PORTAGE")  _FORCE="" ;;
        *)          _FORCE="-y" ;;
    esac
}

# Install a package
function _install() {
    eval "sudo $_PKG $_INSTALL_OPT $_FORCE $1";
}

function _check() {
    return type $1 >/dev/null 2>&1
}

# Check application existance
function _check_or_install() {
    _check $1 || _install $1
}


_stdout "Configuring"

_OSTYPE_detect
_PKG_set
_INSTALL_OPT_set
_FORCE_set


_stdout "Installing dependencies"


case "$_OSTYPE" in
    "DPKG") _install "libsqlite3-dev" ;;
    *)      _install "sqlite-devel" ;;
esac

#_check python3.5 || {
    _check_or_install wget
    _check_or_install tar

    wget https://www.python.org/ftp/python/3.5.1/Python-3.5.1.tgz || {
	_stderr "There is no internet connection, please try it later."
	exit 1
    }
    tar -zxvf Python-3.5.1.tgz
    cd Python-3.5.1
    ./configure
    make
    sudo make install
    cd ..
    sudo rm -rf Python-3.5.1
    rm Python-3.5.1.tgz 
#}

_check_or_install npm
_check_or_install python-virtualenv

[ "$_OSTYPE" == "DPKG" ] && _check_or_install nodejs-legacy

case "$_OSTYPE" in
    "DPKG") _check_or_install libpq-dev;;
    *)      _check_or_install postgresql;;
esac


_stdout "Creating virtualenv"

mkdir -p venv
virtualenv -p python3.5 venv

echo -e "\n\nDJANGO_SETTINGS_MODULE=\"eHoshin.settings.local\"
export DJANGO_SETTINGS_MODULE\n\n" >> ./venv/bin/activate


_stdout "Installing node modules"

npm install --save-dev babel-cli babel-preset-react


_stdout "Installing python dependencies"

. venv/bin/activate
pip install -U setuptools
pip install -r requirements.txt


_stdout "Creating the local db"

./manage.py makemigrations
./manage.py migrate
