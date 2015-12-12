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

function save(editor) {
    // 判断行末 添加换行符号
    ret = pycall('save', {
        data: editor.value()
    })
    if (!ret.success) {
        alert(ret.errmess)
    }
}

function save_as(editor) {
    // 判断行末 添加换行符号
    ret = pycall('save_as', {
        data: editor.value()
    })
    if (!ret.success) {
        alert(ret.errmess)
    }
}

function render(format, data) {
    ret = pycall('render', {
        data: data,
        format: format
    })
    if (ret.success) {
        return ret.data
    } else {
        return ret.errmess
    }
}
