# Local Ansible Testing with Vagrant

Vagrant is a command-line wrapper around
VirtualBox and allows setting up one or more
virtual machines to test out Ansible playbooks
locally.

we have a vagrant file for the role, but if you don't you can do `vagrant init ubuntu/xenial64`

if you have a vagrant file, start a vagrant virtual machine with

```
vagrant up
```

if you have an ansible script that is intended to run on the vagrant machine when the vagrant machine starts up, you may need to run this commanad manually to execute the ansible script:

```
vagrant provision
```

now get ssh info to help ansible connect to the vagrant machine:

```
vagrant ssh-config
```



