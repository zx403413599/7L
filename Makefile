SIMPLEMDE_TARGET := data/simplemde/simplemde.min.js data/simplemde/simplemde.min.css
SIMPLEMDE_SOURCE := node_modules/simplemde/src/js/simplemde.js node_modules/simplemde/src/css/simplemde.css

${SIMPLEMDE_TARGET}: ${SIMPLEMDE_SOURCE}
	cd node_modules/simplemde/ && gulp
	cp node_modules/simplemde/dist/* data/simplemde/

build: ${SIMPLEMDE_TARGET}
	pyinstaller main.spec
	cp python_modules/spynner/ dist/7L/ -r
	cp data/ dist/7L -r

clean:
	rm ${SIMPLEMDE_TARGET}
	rm dist/ -rf
	rm build/ -rf
