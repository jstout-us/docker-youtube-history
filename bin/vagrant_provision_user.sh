echo "Set path"
echo 'PATH="/vagrant/bin:$PATH"' >> /home/$USER/.profile

echo "Cache github ssh fingerprint"
sh -c "ssh -T git@github.com -o StrictHostKeyChecking=no; true"

echo "Add user to docker group"
sudo usermod -aG docker $USER
