### krha

This plugin provides a bridge between krunner and home-assistant's assistant.

If you want to run the plugin manually to debug it you can do the following:  

```shell
mkdir -p ~/.local/share/krunner/dbusplugins/
cp plasma-runner-krha.desktop ~/.local/share/krunner/dbusplugins/
kquitapp6 krunner
python3 krha.py
```

