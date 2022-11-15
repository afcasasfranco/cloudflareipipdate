# CloudFlareIPUpdate
<h1 align="center">Hi 👋, I'm Andres</h1>
<h3 align="center">A Junior BackEnd developer from Colombia</h3>

- 🔭 I’m currently working on Python Scripts **CloudFlareIPUpdate** - The next step its have a record on SQL database (Cooming Soon)

<h3 align="center">Connect with me:</h3>
<p align="center">
<a href="https://twitter.com/afcasasfranco" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/twitter.svg" alt="afcasasfranco" height="30" width="40" /></a>
</p>

<h3 align="center">Description:</h3>
<p align="center"> <a href="https://www.python.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a> </p>
<p align="right">
  This is a Python Script to always have your ip updated on the type A DNS register on Cloude Flare
You can have multiple DNS Zone an multiple Type A registar to update, on the same way you can select what type a register the script not update and keep with the same ip.
  The Script run into all your zones and change only your type A ip by the new server ip (for dynamics ip)
</p>

## Installation
I recomment that put this script on a CRONJOB 60 seconds next to reboot
```bash
@reboot sleep 60; python3 /PATH/CloudFlareIP.py
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install request.

```bash
pip3 install request
```

## Usage

```python
python3 CloudFlareIP.py
```
You can change file .ini with multiple zone id or no update domains that you like
```bash
<ZONE_ID_X> ---> 49815q6f827fv42b21302e6d2fr36463 (its like see a zone domain)
<example.yourdomain.com> ---> home.techradar.com (its like you put to block update)
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

<p align="left">I need to give credit to <strong>pigeonburger</strong> im inspire on his <a align="center" href="https://github.com/pigeonburger/cloudflare-ip/blob/main/cfautoupdater.py">script</a></p>
