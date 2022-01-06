
OUT = blog/asset/pandoc.min.css

all: $(OUT)
	blog/bin/gen.py

%.min.css: %.css
	minify $<  > $@

TEST_OPT = --tb=native --capture=tee-sys

test:
	pytest $(TEST_OPT)

coverage:
	coverage erase
	coverage run -m pytest $(TEST_OPT)
	coverage html
	coverage report
