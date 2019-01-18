### Keyboard layout 

Problem: Load keyboard layout

`setxkbmap us -variant intl` loads the keymap for the current session. 

http://www.x.org/releases/X11R7.6/doc/xorg-docs/input/XKB-Enhancing.html

xkeyboard-config

Create a new us layout that supports special danish letters.  

```
partial alphanumeric_keys 
xkb_symbols "basic" {
    include "us(altgr-intl)"
    name[Group1]="English (US, with Danish special letters)";

    key <AC10>	{ [	    semicolon,      colon,     ae,         AE ]	};
    key <AC11>	{ [    apostrophe,   quotedbl, oslash,   Ooblique ]	};
    key <AD11>	{ [   bracketleft,  braceleft,  aring,      Aring ]	};
};
```

The symbol map extends the us international symbol map. Out of the box this gives some frequently used letters: alt gr + e produce the
letter é, and alt gr + 5 produces the character €. 

I like the three danish special letters æøå located on the same
location as on the danish layout. 

áßð

how to extract key?
Rules:
Rules are 
/usr/share/X11/xkb/rules


 


cp us_dk /usr/share/X11/xkb/symbols

# Add layout to layout list
XML="
<layoutList>
  <layout>
    <configItem>
      <name>us_dk</name>
      <shortDescription>us_dk</shortDescription>
      <description>English (US, danish letters with Alt-Gr)</description>
      <languageList>
        <iso639Id>eng</iso639Id>
      </languageList>
    </configItem>
  </layout>
"

DATA=$(echo "$XML" | tr '\n' '\r')
sed -e "s|<layoutList>|${DATA}|" /usr/share/X11/xkb/rules/evdev.xml | tr '\r' '\n' > evdev.new.xml
cp /usr/share/applications/redshift-gtk.desktop /etc/xdg/autostart

### Ctrl on caps-lock
```
sudo apt-get install gnome-tweak-tool
```

## Unity annoyances

The Unity Launcher is just taking up space.
 
Hide it: Settings -> Appearance -> Behaviour -> Auto-hide the Launcher

There are no virtual desktops
Enable in: Settings -> Appearance -> Enable workspaces

### Middle mouse button paste


### Configure default browser
Open up clicked links in chromium:
```
$ xdg-settings set default-web-browser chromium-browser.desktop
```

## Packages
```bash
$ PACKAGES="
redshift-gtk
chromium-brower
curl
emacs
git
mercurial
nmap
virt-manager
zsh
virtualenv
virtualenvwrapper
python-pip
"
apt-get install $PACKAGES
```

```
$PACKAGES="
pyflakes
jedi
pip install 
```


curl -L http://install.ohmyz.sh | sh

### Start applications on startup
Launch redshift when starting up linux

```
$ cp /usr/share/applications/redshift-gtk.desktop /etc/xdg/autostart
```

### Emacs starter kit
```
$ git clone git@github.com:jakobadam/emacs24-starter-kit.git ~/.emacs.d
```

### Font
ttf-anonymous-pro

