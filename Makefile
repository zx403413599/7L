SIMPLEMDE_TARGET := data/simplemde/simplemde.min.js data/simplemde/simplemde.min.css
SIMPLEMDE_SOURCE := node_modules/simplemde/src/js/simplemde.js node_modules/simplemde/src/css/simplemde.css

${SIMPLEMDE_TARGET}: ${SIMPLEMDE_SOURCE}
	cd node_modules/simplemde/ && gulp
	cp node_modules/simplemde/dist/* data/simplemde/
