#!/bin/bash

###
# { setup-venv.sh } -- A helper script to quickly create and configure a Python3 virtual environment.
###

version="0.1.4"

py_name=$1
install_default=$3
install_venv="y"
install_latest_pycord="n"
venv_path=".venv"

if [ -n "$2" ]; then
  venv_path=$2
fi

# Output tags.
tag_banner="{ install-venv.sh } v$version"
tag_done="[DONE]"
tag_fail="[FAIL]"
tag_info="[INFO]"
tag_okay="[ OK ]"
tag_warn="[WARN]"

########################################################################################################################
# Begin.
########################################################################################################################

echo ""
echo "$tag_banner"
echo ""
echo "$tag_info Configuring Python3 virtual environment for $py_name!"

# Check for an existing virtual environment.
if ! type "python3" > /dev/null; then
  echo "$tag_fail python3 is not installed!"
  exit 1
elif [ -d "$venv_path" ]; then
  echo "$tag_fail A virtual environment already exists in this location!"
  echo ""
  echo "    You can attempt to activate and update the virtual environment with:"
  echo ""
  echo "    source $venv_path/bin/activate && pip3 install -r requirements.txt"
  echo ""
  echo "HINT: You can remove it with 'rm -rf .venv/' and run this script to try again."
  echo ""
  exit 1
else
  echo "$tag_okay No virtual environment exists at '$(pwd)/$venv_path'!"
  while [ "$install_default" != 'true' ]; do
    read -rp "[ ?? ] Create a new virtual environment? Y/n " prompt
    case $prompt in
      [Yy]) install_venv="y";
          break;;
      [Nn] ) install_venv="n"
          echo "$tag_done Exiting...";
          exit 1;;
      *) echo "$tag_warn Invalid entry! Please enter [y]es or [n]o."
    esac
  done
  while [ "$install_default" != 'true' ]; do
    read -rp "[ ?? ] Install latest version of Py-cord? (for testing) y/N " prompt
    case $prompt in
      [Yy])
        install_latest_pycord="y"
        echo "$tag_okay Will install latest version of Py-cord!"
        break;;
      [Nn])
        install_latest_pycord="n"
        echo "$tag_info Will not install latest version of Py-Cord."
        break;;
      *) echo "$tag_warn Invalid entry! Please enter [y]es or [n]o."
    esac
  done
fi

# Attempt to create, activate, and build the desired venv.
if [ $install_venv = "y" ]; then
  echo "$tag_info Creating virtual environment!"
  python3 -m venv "$venv_path"
  . "$venv_path"/bin/activate
  echo "$tag_okay Created virtual environment \"$(pwd)/$venv_path\"!"
  if [ "$(which python3)" != "$(pwd)/$venv_path/bin/python3" ]; then
    echo "$tag_fail Failed to create and activate virtual environment!"
    exit 2
  else
    echo "$tag_okay Successfully created and activated virtual environment!"
  fi
  echo "$tag_info Upgrading pip!"
  if ! "$venv_path"/bin/python3 -m pip install pip --upgrade; then
    echo "$tag_fail Failed to upgrade pip!"
    exit 2
  else
    echo "$tag_okay Successfully upgraded pip to latest!"
  fi
  if [ -f "$(pwd)/requirements.txt" ]; then
    echo "$tag_info Installing required modules from requirements.txt!"
  else
    echo "$tag_fail Failed to find 'requirements.txt'!"
  fi
  if ! "$venv_path"/bin/pip3 install -r requirements.txt; then
    echo "$tag_fail Failed to install required modules!"
    exit 2
  else
    echo "$tag_okay Successfully installed required modules from requirements.txt!"
  fi

  # For installation of latest version of Py-cord.
  if [ $install_latest_pycord = "y" ]; then
    echo "$tag_info Installing latest version of Py-cord!"
    if "$venv_path"/bin/pip3 install -U git+https://github.com/Pycord-Development/pycord; then
      echo "$tag_fail Failed to upgrade to latest version of Py-cord!"
      echo "    NOTE: This may be fine if current version of Py-cord>=2.1.0."
    else
      echo "$tag_okay Successfully installed the latest version of Py-cord!"
    fi
  fi

  # Point of completion.
  echo "$tag_okay Successfully installed virtual environment!"
  echo "$tag_done Successfully created virtual environment for $py_name!"
  echo "$tag_info You can now activate the virtual environment with:"
  echo ""
  echo "      source $venv_path/bin/activate"
  echo ""
fi

########################################################################################################################
# End.
########################################################################################################################
