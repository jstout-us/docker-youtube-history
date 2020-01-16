export DEBIAN_FRONTEND=noninteractive

echo "Set Env Vars"
ln -sf /home/vagrant/config/do-token.sh /etc/profile.d/do-token.sh

echo "Set Time Zone"
timedatectl set-timezone America/Los_Angeles

echo "Install base Ubuntu dependencies"
apt-get update
apt-get install -y apt-transport-https \
                   ca-certificates \
                   curl \
                   software-properties-common

echo "Add docker repo"
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu  $(lsb_release -cs)  stable"
sudo apt-get update

echo "Add Ubuntu Dependencies"

apt-get install -y build-essential \
                   docker-ce \
                   git \
                   git-flow \
                   python3-dev \
                   python3-pip \
                   tig

echo "Install docker-machine"
DM_VER="0.16.2"
DM_URL="https://github.com/docker/machine/releases/download/v_${DM_VER}/docker-machine-`uname -s`-`uname -m`"
curl -L $DM_URL > /tmp/docker-machine && \
    chmod +x /tmp/docker-machine && \
    sudo mv /tmp/docker-machine /usr/local/bin/docker-machine

echo "Installing python dependencies"
/usr/bin/env python3 -m pip install --upgrade -r /vagrant/src/app/requirements_dev.txt \
                                              -r /vagrant/src/app/requirements_test.txt \
                                              -r /vagrant/src/app/requirements.txt
