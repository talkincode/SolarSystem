#!/bin/bash

test -d web || mkdir web
test -d solarsystem_wasm && rm -rf solarsystem_wasm
mkdir -p solarsystem_wasm/solarsystem/assets/images
mkdir -p solarsystem_wasm/solarsystem/assets/sounds

cp -r solarsystem/* solarsystem_wasm/solarsystem/

rm -f solarsystem_wasm/main.py
cp main.py solarsystem_wasm/main.py

rm -fr solarsystem_wasm/solarsystem/__pycache__

python -m pygbag --build solarsystem_wasm
python3 -m pygbag --archive solarsystem_wasm/main.py

cp solarsystem_wasm/build/web/index.html web/index.html
cp solarsystem_wasm/build/web/solarsystem_wasm.apk web/solarsystem_wasm.apk
cp solarsystem_wasm/build/web.zip web/web.zip
rm -fr solarsystem_wasm