function pycall(name) {
    var kwargs = arguments[1] || {}
    return JSON.parse(
        prompt(name,
            JSON.stringify(kwargs)
        )
    )
}
    
function open(editor) {
    ret = pycall('open')
    if (ret.success) {
        editor.value(ret.data)
    } else {
        alert(ret.errmess)
    }
}

function ensure_newline(editor) {
    text = editor.value()
    if (text.charAt(text.length - 1) != '\n')
        text += '\n'
        editor.value(text)
    return text
}

function save(editor) {
    ret = pycall('save', {
        data: ensure_newline(editor)
    })
    if (!ret.success) {
        alert(ret.errmess)
    }
}

function save_as(editor) {
    ret = pycall('save_as', {
        data: ensure_newline(editor)
    })
    if (!ret.success) {
        alert(ret.errmess)
    }
}

function render(data) {
    ret = pycall('render', {
        data: data
    })
    if (ret.success) {
        return ret.data
    } else {
        return ret.errmess
    }
}
