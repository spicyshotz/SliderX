# SliderX
![IMG](https://i.imgur.com/lTktL4X.png)
Control the volume of your Windows programs with physical sliders!
Seamlessly control the volume of your music player, Such as Spotify, your voice chat, Such as Discord and your game
without stopping whatever you're doing!
##### Windows Only
##### Updated 12/26/2022

------------
[How it works](#how-it-works) <br />
[Installation](#installation) <br />
[FAQ](#faq) <br />
[TODO](#todo)

------------

![IMG](https://i.imgur.com/873Og9d.png)
------------
#### SliderX GUI provides a Graphical User Interface to quickly edit the programs you wish to control with your mixer. Made in Unity.
------------
![IMG](https://i.imgur.com/CNiqJJr.png)
![IMG](https://i.imgur.com/QjUbbNw.gif)
![IMG](https://i.imgur.com/W9QA54D.png)

------------
![IMG](https://i.imgur.com/9H8YM1x.png)
#### SliderX Driver is what actually controls the volume of the selected programs based on physical potentiometer values. Written in Python. <br />
#### While I call it a driver, It's just a regular program running in your system tray.
------------
# How It Works
SliderX is a program that is written in Python that controls the volume of programs based on
potentiometer values sent from Arduino hardware.



# Installation

#### Recommended:

```bash
  Download the installer from release which will install both the driver and the GUI
  interface automatically.
```
#### Else:
Download SliderX "Driver":

```bash
  Download "slide.exe" from release
```
Download SliderX GUI:

```bash
  Download "SliderXGUI.zip" from release
```

    
# FAQ

### Is the SliderX GUI necessary to use the program?

No, The GUI makes it easy to quickly edit the programs you wish to control with your mixer.
but its optional as you can edit the JSON yourself.

### Where can I find the JSON
```bash
documents/sliderX/Settings.JSON
```
If using the GUI, the GUI will create this path and this file the first time.
if not using the GUI, you have to create this path yourself.
#### Settings.JSON structure:
```bash
{"COM_PORT":"COM3","flip":false,"POT1":"Spotify.exe","POT2":"chrome.exe, firefox.exe","POT3":"Discord.exe","POT4":"example.exe, example2.exe"}
```

# TODO
### Add source code for the GUI
### Add hardware tutorial
