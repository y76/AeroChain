**https://py4web.com/_documentation/static/en/chapter-03.html**

git clone https://github.com/web2py/py4web.git
cd py4web
python3 -m pip install  --upgrade -r requirements.txt

*Linux and MacOS*

Linux and MacOS
./py4web.py setup apps
./py4web.py set_password
./py4web.py run apps
If you have installed py4web both globally and locally, notice the ./ ; it forces the run of the local folder’s py4web and not the globally installed one.

*Windows*

python3 py4web.py setup apps
python3 py4web.py set_password
python3 py4web.py run apps
On Windows, the programs on the local folder are always executed before the ones in the path (hence you don’t need the ./ as on Linux). But running .py files directly it’s not usual and you’ll need an explicit python3/python command.

*this repo contains the py4web/apps/AeroChain folder*