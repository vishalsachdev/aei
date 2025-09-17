.PHONY: run export clean

run:
	python -m marimo run marimo/aei_app.py

export:
	python -m marimo export wasm marimo/aei_app.py --output docs

clean:
	rm -rf docs
