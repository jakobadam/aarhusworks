---
layout: post
title: "Unattended installation of VM images with Packer"
---

*Installing different OSes has usually been a cumbersome
select-enter-point-click process. This post shows you how to
auto-install VM images from an Ubuntu 14.04 Server ISO and Windows
2012 R2 ditto for running with KVM. To do so it uses the VM building
tool Packer, which is also introduced.*

Most people, these days, use pre-baked OSes&mdash;known as
[base images](http://www.linux-kvm.com/content/how-you-can-use-qemukvm-base-images-be-more-productive-part-1)&mdash;as
building blocks for their virtual server setup. This results in a
significant productivity boost, avoiding repeated OS installs.

Now base images must come from somewhere, the easiest option at hand
being some 3. party. But do you trust them? And what if the OS is not
available? So I have often ended up installing nearly identical OSes
in the usual timewasting repeated manner. The reason being a mix of
complexity, lack of shareability of installation configurations, and
non-generality of building tools.

The VM building tool [Packer](http://packer.io) solves these issues,
and this post shows how it works.

## An example for the impatient

Install packer on Linux (for others look at
[Packer - Downloads](http://www.packer.io/downloads.html)):

```bash
$ wget https://dl.bintray.com/mitchellh/packer/packer_0.7.5_linux_amd64.zip
$ mkdir /usr/local/packer
$ unzip packer_0.7.5_linux_amd64.zip -d /usr/local/packer
$ ln -s /usr/local/packer/packer /usr/local/bin
```

Clone configuration templates:

```bash
$ git clone https://github.com/jakobadam/packer-qemu-templates
```

Install QEMU:

```bash
$ apt-get install qemu-kvm
```

Build **Ubuntu 14.04 Server** for running with QEMU:

```bash
$ cd packer-qemu-templates/ubuntu
$ packer build ubuntu-14.04-server-amd64.json
```

Build **Windows 2012 R2 Server (virtio)** for running with QEMU:

```bash
$ cd packer-qemu-templates/ubuntu
$ packer build windows-2012-R2-standard-amd64.json
```

And that's it. You should now have two qcow2 images for running with
QEMU.

## Short intro to Packer

[Packer](http://packer.io) is VM image building tool that aims to
streamline the OS installation process doing the heavy lifting of
creating and provisioning virtual images. A central component of
packer&mdash;from the users point of view&mdash;is the template.

Templates completely define the installation of an OS. Packer works by
taking these, in JSON format, and outputs runnable provisioned virtual
machine images without additional user input.

![Packer Input Output](/assets/packer-overview.jpg)

Packer has several virtual image output options runnable by
Virtualbox, QEMU etc.&ensp;Amazon is also supported but building
machines here are a very different story, since they rely on both the
presence of base images and building within Amazon.

Unfortunately, templates are specific for the output format, and
including common template code is not
([yet?](https://github.com/mitchellh/packer/issues/271)) possible. The
focus in this post is on the QEMU output format which we use for our
cloud at https://origo.io/

Let's jump into it, and see how it works. I'll explain some of the
essential elements in the templates for two different OSes: Ubuntu
14.04 Server and Windows 2012 R2.

## Ubuntu 14.04 Server Installation

This section describes and explains the template for pre-baking a
production-ready Ubuntu 14.04 server for running with QEMU. While
reading this, it would be beneficial to have a look at the whole
template at
[Github - Packer Ubuntu Template](https://github.com/jakobadam/packer-qemu-templates/blob/master/ubuntu/ubuntu-14.04-server-amd64.json).

A template typically consists of three sections: variables, builders
and provisioners.

### Variables

The variables section contains user suppliable values substituted in
the template. The Ubuntu template has three variables: username,
password and disk size.


```ruby
"variables": {
    "user": "adminubuntu",
    "password": "adminubuntu",
    "disk_size": 100000
}
```
<center>*Ubuntu 14.04 Template: Variables section*</center>

To replace the user default value when starting the packer build:

```bash
$ packer build -var 'user=u' ubuntu-14.04-server-amd64.json
```

### Building

The builders section contains a list of building specifications, one
for each output target, in our case only QEMU.
{% raw %}
```json
"builders":
    [
        {
            "type": "qemu",
            "name": "ubuntu",
            "format": "qcow2",
            "accelerator": "kvm",
            "disk_size": "{{ user `disk_size`}}",

            "iso_url": "http://releases.ubuntu.com/14.04/ubuntu-14.04-server-amd64.iso",
            "iso_checksum": "01545fa976c8367b4f0d59169ac4866c",
            "iso_checksum_type": "md5",

            "http_directory": "http",

            "ssh_username": "{{user `user`}}",
            "ssh_password": "{{user `password`}}",
            "shutdown_command": "echo '{{user `password`}}'|sudo -S shutdown -P now",

            "boot_wait": "2s",
            "boot_command": [
                "<esc><esc><enter><wait>",
                "/install/vmlinuz url=http://{{ .HTTPIP }}:{{ .HTTPPort }}/preseed.cfg ",
                "debian-installer=en_US auto locale=en_US kbd-chooser/method=us ",
                "hostname={{ .Name }} ",

                "keyboard-configuration/modelcode=SKIP ",
                "keyboard-configuration/layout=USA ",
                "keyboard-configuration/variant=USA ",

                "passwd/user-fullname={{user `user`}} ",
                "passwd/user-password-again={{user `password`}} ",
                "passwd/user-password={{user `password`}} ",
                "passwd/username={{user `user`}} ",

                "initrd=/install/initrd.gz -- <enter>"
            ]
        }
    ],
```
{% endraw %}
<center>*Ubuntu 14.04 Template: Builders section*</center>


In order to automate the Ubuntu install process, a
[preseed.cgf](https://github.com/jakobadam/packer-qemu-templates/blob/master/ubuntu/http/preseed.cfg)
file, with answers to install questions, must be supplied to the
installer. This file is most easy to create by taking an existing,
like
[example-preseed](https://help.ubuntu.com/10.04/installation-guide/example-preseed.txt),
massaging it and checking it by running:

```bash
$ debconf-set-selections -c preseed.cfg
```

*For more on preseeding, have a look at the
[debian handbook](http://debian-handbook.info/browse/stable/sect.automated-installation.html#sect.d-i-preseeding)*
{% raw %}
The template includes an URL reference to `preseed.cfg` in the
`boot_command` property. When Packer is started it fires up a web
server serving the contents of the directory supplied in the
`http_directory` property. The wired looking magic variables
`{{.HTTPIP}}` and `{{.HTTPPort}}` are therefore part of the address to
`preseed.cfg` on this web server.
{% endraw %}
*Note:* Variables are substituted in the template&mdash;not in files
referred to from it, e.g., files served via HTTP or included on a
floppy.

The boot command is an array of commands which are typed in via
VNC. Since values for `user` and `password` are suppliable when
starting a build, the adhering debconf values can't be put in
`preseed.cfg`. Instead these settings are specified in the
`boot_command` option in the template, where variables are
substituted.

{% raw %}
```
"passwd/user-fullname={{user `user`}} ",
"passwd/user-password={{user `password`}} ",
"passwd/user-password-again={{user `password`}} ",
"passwd/username={{user `user`}} ",
```
{% endraw%}


### Provisioning

During install Packer continuously polls for SSH access. Upon
successful login packer either shuts down the OS or continues to the
`provisioners` step if supplied.

{% raw %}
```
"provisioners": [
        {
            "type": "shell",
            "scripts": [
                "scripts/update.sh",
                "scripts/packages.sh",
                "scripts/network.sh"
            ],
            "execute_command": "echo '{{user `password`}}' | {{.Vars}} sudo -E -S bash '{{.Path}}'"
        }
    ]
```
{%endraw%}
<center>*Ubuntu 14.04 Template: Provisioning step*</center>

In our template there is a single provisioner which uploads and executes three scripts on the machine: [update.sh](https://github.com/jakobadam/packer-qemu-templates/blob/master/ubuntu/scripts/update.sh), [packages.sh](https://github.com/jakobadam/packer-qemu-templates/blob/master/ubuntu/scripts/packages.sh), and [network.sh](https://github.com/jakobadam/packer-qemu-templates/blob/master/ubuntu/scripts/network.sh). The scripts update the machine, install some useful packages, and removes all traces from the network&mdash;MAC to network interface mapping&mdash;used during installation.  

The somewhat arcane `execute_command` stems from the fact that the SSH
user is not the root user, and therefore sudo is used to execute the
scripts as superuser.

## Windows 2012 R2 (virtio) installation 

The template is available at
[Packer - Windows 2012 R2 template](https://github.com/jakobadam/packer-qemu-templates/blob/master/windows/windows-2012-R2-standard-amd64.json)

### Building

The installation of the windows image is automated by utilizing
`Autounattend.xml`&mdash;an incomprehensible XML answer file that the
windows install process looks for on the floppy drive during
startup. The easiest way to create this, is to take an existing file,
and massage that one.

Microsoft provides a GUI tool which aids in creating the answer file,
named
[Windows System Image Manager](http://www.microsoft.com/en-US/download/details.aspx?id=39982). The
creation process, when running windows in a virtual machine, is as
follows: Mount install DVD → copy D:/sources/install.wmi somewhere →
Open up 'Windows System Image Manager' → Select 'Windows Image' →
Select install.wim → Create new answer file.

Although, possible to create arbitrary configurations to windows in
`Autounattend.xml`, I recommend sticking with the bare essentials,
leaving additional configurations to the provisioning phase of
packer. Just look at all the extra XML clutter to execute the single
script,
[configure.bat](https://github.com/jakobadam/packer-qemu-templates/blob/master/windows/floppy/windows-2012-standard-amd64/configure.bat):

```
<SynchronousCommand wcm:action="add">
  <CommandLine>cmd.exe /c a:\configure.bat</CommandLine>
  <Description>Run configure script</Description>
  <Order>1</Order>
</SynchronousCommand>
```

<center>*Autounattend.xml: Execute script*</center>

Our template goes with the first option, as seen below, and attaches
`Autounattend.xml` and relevant scripts referred from it in the
`floppy_files` template variable. Note: All files are put on the
floppy in one flat hierarchy, so don't duplicate file names.

{% raw %}
```json
"builders": [
        {
            "type": "qemu",
            "name": "windows-2012R2",
            "format":"qcow2",
            "accelerator": "kvm",
            "disk_size": "{{ user `disk_size`}}",

            "iso_url": "http://care.dlservice.microsoft.com/dl/download/6/2/A/62A76ABB-9990-4EFC-A4FE-C7D698DAEB96/9600.17050.WINBLUE_REFRESH.140317-1640_X64FRE_SERVER_EVAL_EN-US-IR3_SSS_X64FREE_EN-US_DV9.ISO",
            "iso_checksum_type": "md5",
            "iso_checksum": "5b5e08c490ad16b59b1d9fab0def883a",

            "boot_wait": "2m",
            "ssh_username": "Administrator",
            "ssh_password": "Administrator",
            "shutdown_command": "shutdown /s /t 10 /f /d p:4:1 /c \"Packer Shutdown\"",

            "floppy_files": [
                "floppy/drivers/virtio-win-0.1-81/WIN7/AMD64/*",
                "floppy/common/*",
                "floppy/windows-2012-standard-amd64/*"
            ],
            "disk_interface":"virtio",
            "qemuargs": [
                ["-m", "4096m"],
                ["-smp", 2]
            ]
        }
    ],
```
<center>*Windows Template: Builders section*</center>

The configure script does two things. First, it disables the firewall,
and then it installs SSH. It's essential to setup SSH in the building
step to let packer do its thing. This, of course, is a hack and
support for the windows alternative (WinRM) to SSH, for uploading and
executing files, is on the way
https://github.com/mitchellh/packer/issues/451. For now, we're left
with Cygwin which is setup, during the building phase as the last
step, before going to the provisioners section, which uses SSH.

#### Virtio

The template property `floppy_files` instructs packer to attach the
relevant
[virtio drivers](http://www.linux-kvm.org/page/WindowsGuestDrivers/Download_Drivers)
on a floppy and make them available during the installation. The
windows installation process is instructed by `Autounattend.xml` to
look for these drivers on the floppy drive. Hence, the installation is
performed with virtio, boosting performance.

### Provisioning

```json
"provisioners": [
        {
            "type": "shell",
            "inline": ["net user Administrator {{ user `password`}}"]
        },
        {
            "type": "shell",
            "remote_path": "/cygdrive/c/Windows/Temp/script.bat",
            "execute_command": "cmd /c C:/Windows/Temp/script.bat",
            "scripts": [
                "scripts/enable-rdp.bat",
                "scripts/execution-policy-unrestricted.bat",
                "scripts/unlimited-password-expiration.bat"
            ]
        }
    ]
```
<center>*Windows Template: Provisioners section*</center>

The provisioning step provides some saner defaults for most
environments. It enables RDP, allows execution of user powershell
scripts, and disables prompts for changing password. It also updates
the password, hereby letting the user supply one as a parameter to
packer build.

## Conclusion

This post showed you how to efficiently create two different VM
images&mdash;for running on KVM&mdash;with Packer. If you encounter
missing OS templates, I hope that you will now contribute your own.
{% endraw %}