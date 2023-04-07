# Image filters

GUI application to apply global thresholding, global adaptive thresholding and highpass filters.

![](img/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%202023-04-07%20160731.png)

# Build
There is a list of required python packages for this application:
- opencv-python
- opencv-contrib-python
- tkinter
- pillow
- numpy

To run application use command:
```
    python main.py
```

# Build executable
At first download _pyinstaller_ package:
```
    pip install pyinstaller
```
 To create executable file use next command:
```
pyinstaller --noconfirm --onefile --windowed --distpath ./bin --icon ./img/bubble_chart_solid_icon_235318.ico --name Filter  ./main.py
```