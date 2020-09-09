# Nanny

Nanny - is a command line interface for creation Github Pull Requests for projects with multiple release versions.

## Installation
```bash
wget -qO - https://raw.githubusercontent.com/kolenkainc/Nanny.Releases/master/PUBLIC.KEY | sudo apt-key add -
echo "deb https://raw.githubusercontent.com/kolenkainc/Nanny.Releases/master/ focal main" | sudo tee /etc/apt/sources.list.d/kolenka.list
sudo apt-get update
sudo apt-get install nanny
```

