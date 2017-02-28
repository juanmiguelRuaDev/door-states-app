DOOR-STATES-APP
=======================

This application aims to manage the state of two doors (entry and exit) independently.The implementation is based on [state pattern](https://en.wikipedia.org/wiki/State_pattern) where each state decides which will be the next state according to the input parameters

## Requirements --dev

* OS: Linux, Windows
* Python3, pip3, virtualenv


## Requirements --pro

* OS: Raspbian JESSIE LITE
* Python3, pip3, virtualenv


## install dependencies from scratch

Once the virtualenv is running, from the root folder just run either ``` pip3 install -r requirement.txt``` or ``` pip3 install -r requirement_dev.txt``` in development environment.


## Run the application

Since the application root folder, just run 
```
python3 app.py

```






## License
The MIT License (MIT)

Copyright (c) 2016 Juan Miguel Rúa

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.