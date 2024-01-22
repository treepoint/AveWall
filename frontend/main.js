/**************************************************
* Autostart
***************************************************/
async function setAutostart() {
    await eel.setAutostart()();
}

/**************************************************
* MODS
***************************************************/
function setMode(mode) {
    let list_mode = document.getElementById("mods").children;

    for (let mode of list_mode) {
        mode.classList.remove('active');
    }

    switch (mode) {
        case 'auto':
            document.getElementById("set-auto").classList.add('active');
            break;
        case 'default':
            document.getElementById("set-default").classList.add('active');
            break;
        case 'black':
            document.getElementById("set-black").classList.add('active');
            break;
    }
}

async function setAuto() {
    await eel.setAutoMode()();
    setMode('auto');
}

async function setDefault() {
    await eel.setDefaultMode()();
    setMode('default');
}

async function setBlack() {
    await eel.setBlackMode()();
    setMode('black');
}

/**************************************************
* ACTIONS
***************************************************/
async function onConfigReload() {
    await eel.onConfigReload()();
}

async function getCurrentWindowsWallpaper() {
    await eel.getCurrentWindowsWallpaper()();
}

function onClose() {
    window.close()
}

async function onExit() {
    window.close()
    await eel.onExit()();
}

/**************************************************
* INIT
***************************************************/
async function initState() {
    let state = await eel.getState()();

    //Autostart checkbox
    autostart_is_on = JSON.parse(state)['autostart_is_on'];
    document.getElementById("autostart").checked=autostart_is_on;
}

async function initConfig() {
    let config = await eel.getConfig()();

    //Инициируем мод
    mode = JSON.parse(config)['MAIN']['mode'];
    setMode(mode)
}

function setActions() {
    //Autostart
    document.getElementById('autostart').onchange = setAutostart;

    //MODS
    document.getElementById('set-auto').onclick = setAuto;
    document.getElementById('set-default').onclick = setDefault;
    document.getElementById('set-black').onclick = setBlack;

    //Actions
    document.getElementById('reload-config').onclick = onConfigReload;
    document.getElementById('set-wall-as-default').onclick = getCurrentWindowsWallpaper;
    document.getElementById('close').onclick = onClose;
    document.getElementById('exit').onclick = onExit;
}

async function init() {
    await initState();
    await initConfig();
    setActions();
};

//RUN
init();



/* {
    "MAIN": 
    {"black_wallpaper": "./assets/black.jpg",
    "default_wallpaper": "./assets/default.jpg", 
    "polling_timeout": "1", 
    "mode": "default"}, +

    "PROCESSES": 
    {"1": "APlagueTaleInnocence_x64_WIDESCREEN.exe, ./assets/black.jpg", 
    "2": "APlagueTaleInnocence_x64.exe, ./assets/black.jpg", 
    "3": "EoCApp.exe, ./assets/black.jpg", 
    "4": "launcher.exe, ./assets/black.jpg", 
    "5": "filezilla.exe, ./assets/black.jpg"}
} */