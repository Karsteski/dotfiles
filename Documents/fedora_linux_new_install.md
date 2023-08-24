# 

# Install

- Update packages.

- swap ffmpeg-free for ffmpeg: [HowToMultimedia-Fedora](https://rpmfusion.org/Howto/Multimedia)
- For Fedora Sway Spin, gvfs-smb package needed to be installed to access an SMB Share


## Sway
- .desktop files are stored in "~/.local/share/applications" by default

## KDE Connect
- Had to open ports for firewalld: [KDE Connect - Troubleshooting](https://userbase.kde.org/KDEConnect#Troubleshooting)

```
# firewalld
If your firewall is firewalld, you can open the necessary ports with:

sudo firewall-cmd --permanent --zone=public --add-service=kdeconnect
sudo firewall-cmd --reload
```

# Pamixer
- For controlling pulseaudio via CLI: https://github.com/cdemoulins/pamixer

# Change hostname (Name of computer)
- Check with `$ hostnamectl`

# Chezmoi
- For managing dotfiles

# Fancy git
- For a pretty git CLI
