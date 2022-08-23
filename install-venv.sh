#!/bin/sh

###
# { install-venv.sh } // Creates, activates, and installs packages into a Python3 virtual environment.
###

version="0.0.5"
py_name="SHEA"
install_venv="y"
install_pycord="y"
venv_path=".venv"

tag_banner="\n{ install-venv.sh } // $version\n"
tag_done="[DONE]:"
tag_fail="[FAIL]:"
tag_info="[INFO]:"
tag_okay="[ OK ]:"

echo "$tag_banner"
echo "$tag_info Attempting to create Python3 virtual environment for $py_name!"
if ! type "python3" > /dev/null; then
  echo "$tag_fail python3 is not installed!"
  exit 1
elif [ -d "$venv_path" ]; then
  echo "$tag_fail A virtual environment already exists in this location!"
  echo "      You can attempt to activate the virtual environment with:"
  echo "        . $venv_path/bin/activate\n"
  echo "HINT: You can remove it with 'rm -rf .venv/' and run this script to try again."
  exit 1
else
  echo "$tag_okay No virtual environment exists!"
  # Y/N prompt goes here.
fi

# Attempt to create and build the desired venv.
if [ $install_venv = "y" ]; then
  echo "$tag_info Creating virtual environment!"
  python3 -m venv "$venv_path"
  . $venv_path/bin/activate
  echo "$tag_okay Created virtual environment \"$(pwd)/$venv_path\"!"
  if [ "$(which python3)" != "$(pwd)/$venv_path/bin/python3" ]; then
    echo "$tag_fail Failed to create and activate virtual environment!"
    exit 2
  else
    echo "$tag_okay Successfully created and activated virtual environment!"
  fi
  echo "$tag_info Upgrading pip!"
  if ! $venv_path/bin/python3 -m pip install pip --upgrade 1> /dev/null 2>&1; then
    echo "$tag_fail Failed to upgrade pip!"
    exit 2
  else
    echo "$tag_okay Successfully upgraded pip to latest!"
  fi
  echo "$tag_info Installing required modules from requirements.txt!"
  $venv_path/bin/pip3 install -r requirements.txt 1> /dev/null 2>&1
  if [ $? != 0 ]; then
    echo "$tag_fail Failed to install required modules from requirements.txt!"
    exit 2
  else
    echo "$tag_okay Successfully installed required modules from requirements.txt!"
  fi
  if [ $install_pycord = "y" ]; then
    echo "$tag_info Installing latest version of Py-cord!"
    $venv_path/bin/pip3 install -U git+https://github.com/Pycord-Development/pycord 1> /dev/null 2>&1
    if [ $? != 0 ]; then
      echo "$tag_fail Failed to upgrade to latest version of Py-cord!"
      echo "    NOTE: This may be fine if current version of Py-cord>=2.1.0."
    else
      echo "$tag_okay Successfully installed the latest version of Py-cord!"
    fi
  fi
  # Point of success.
  echo "$tag_okay Successfully installed virtual environment!"
  echo "$tag_done Successfully created virtual environment for $py_name!"
  echo "$tag_info You can attempt to activate the virtual environment with:"
  echo "\n      source "$venv_path/bin/activate"\n"
fi
