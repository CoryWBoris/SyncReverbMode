# SyncReverbMode

![Stable Badge](https://img.shields.io/badge/-stable-blue)  
By: Cory Boris  
© 2024 MIT License
## A Control Surface for Automatically Syncing Ableton's Native Reverb's Predelay with BPM In Ableton Live 11+ WITHOUT PLUGINS ;)

\*\*for Mac or Windows\*\*

### 6 Steps to setup:  
**Note: this assumes you are using the default user library folder. If you have moved this folder externally or otherwise, make a Remote Scripts folder inside of whatever user library folder you have pointed Ableton to, and start from step 2:**
1. Mac users:  
   Go to `/Users/your_username/Music/Ableton/User Library`  
   Windows users:  
   Go to `\Users\your_username\Documents\Ableton\User Library`
2. Create a folder 'Remote Scripts' if it's not already created.
3. Create a folder titled 'SyncReverbMode' inside the 'Remote Scripts' folder.
4. Download **both** .py files, "SyncReverbMode.py" and "\_\_init\_\_.py", and place them in the 'Remote Scripts/SyncReverbMode' folder.
5. Restart or open Ableton Live
6. In Ableton, select 'SyncReverbMode' in the "Link|Tempo|Midi" tab, and make sure the input and output are set to 'None'.

**Note**: You can add the 2 mentioned files from here to their respective folders as shown by my tutorial while Ableton is open or quit, but if Ableton is open, then you *will* have to restart Ableton for the selected control surface to go into effect. The reason being is that Ableton compiles python and loads python code into memory when Ableton starts, but not after it loads up. For you using the software, this means that in order to update this script if and when it is updated, then you will have to restart Ableton to use the updated software.

## Features:  
-There are two modes: _all_mode = False and _all_mode = True. False means only Ableton native reverbs named 'Reverb' which are added to the set after the set is loaded will be changed, True means all reverb modules named 'Reverb' which are native to ableton will be changed.
-You can modify the parameters' span in "calculate_value" as they pertain to a parameter other than predelay as i defined it here by changing the a and b values at the top. I lucked tf out and found out that the native Ableton Reverb's predelay paramter is logarithmic, but this isn't a guarantee for every parameter knob.
-You can change the note you use other than 32nd note by replacing the number 32 with whatever note you want to use.


## Open Issues:
N/A

## Future Updates:
It would cool to have a gui for interacting with the settings here. For now, this is more or less a boiler plate for anyone interested in hardwiring their own effects' mappings.

## Other Related Programs:
<a href="https://coryboris.gumroad.com/l/TrueAutoColor">TrueAutoColor</a>  
A stunning custom color layout maker for Ableton Live 11+ on Mac AND Windows which instantly changes track and clip colors based on name, no plugins necessary.

### Coffees Welcome!
- Paypal: tromboris@gmail.com
- Venmo: @Cory-Boris
- Ethereum Address: `0x3f6af994201c17eF1E86ff057AB2a2F6CB0D1f6a`

Thank you! 🔥🥰✌🏻🙏🏻

