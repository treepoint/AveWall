async function setBlack() {
    await eel.setBlackMode()();
}

async function setDefault() {
    await eel.setDefaultMode()();
}

document.getElementById('set-black').onclick = setBlack;
document.getElementById('set-default').onclick = setDefault;