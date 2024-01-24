/**************************************************
* Autostart
***************************************************/
async function setAutostart() {
    await eel.setAutostart()();
}

/**************************************************
* Table
***************************************************/
function detach(element) {
    return element.parentElement.removeChild(element);
  }
  
  function move(src, dest, isBefore) {
    dest.insertAdjacentElement(isBefore ? 'beforebegin' : 'afterend', detach(src));
  }
  
  function children(element, selector) {
    return element.querySelectorAll(selector);
  }
  
  function child(element, selector, index) {
    return children(element, selector)[index];
  }
  
  function row(table, index) {
    // Generic Version: return child(table.querySelector('tbody'), 'tr', index);
    return child(table.querySelector('tbody'), 'tr', index);
  }
  
  function moveRow(table, fromIndex, toIndex, isBefore) {
    move(row(table, fromIndex), row(table, toIndex), isBefore);
  }

/**************************************************
* Processes
***************************************************/
process_table = document.getElementById("process_table");

function deleteProcess(event) {
    process_id = event.target.attributes.process_id.nodeValue;
    document.getElementById("process_" + process_id).remove();
}

function addNewProcess() {
    addProcess('', '');
}

function updateProcessIdForRow(row, new_process_id) {
    //row parameters
    row.id = "process_" + new_process_id;
    row.dataset.process_id = new_process_id;

    //process order select
    row.children[0].dataset.process_id = new_process_id;

    for (let option of row.children[0].children[0].children) {
        option.dataset.current_index = new_process_id;
    }

    //for delete button
    row.children[3].dataset.process_id = new_process_id;
    row.children[3].children[0].attributes.process_id.nodeValue = new_process_id;
    row.children[3].children[0].id = "process_" + new_process_id;
}

function onOrderChange(select) {
    new_index = select.value - 1;
    current_index = select.options[select.selectedIndex].dataset.current_index - 1;

    if (new_index == current_index) {
        return;
    }

    if (new_index > current_index) {
        isBefore = false;
    } else {
        isBefore = true;
    }

    moveRow(process_table, current_index, new_index, isBefore);

    //Меняем все ID на новые
    let rows = document.getElementsByClassName("process_rows");

    new_process_id = 0;
    
    for (let row of rows) {
        new_process_id += 1;
        updateProcessIdForRow(row, new_process_id);
    }

    //Задаем правильные выборы в селектах процессов
    for (let select of document.getElementsByClassName("process_order_select")) { 
        select.selectedIndex = select.children[0].dataset.current_index - 1;
    }
}

function reOrder() {
    //Add new order to each cell
    for (let order_cell of document.getElementsByClassName("order_cell")) {
        order_select = "<select onchange='onOrderChange(this)' class='process_order_select'>";

        current_index = order_cell.dataset.process_id;

        i = 1;
        while (i != (new_row_id + 2)) {
            if (i == current_index) {
                order_select += "<option selected value=" + i + " data-current_index=" + current_index + ">"+ i +"</option>";
            } else {
                order_select += "<option value=" + i + " data-current_index=" + current_index + ">"+ i +"</option>";
            }
            
            i += 1;
        }
    
        order_select += "</select>";        
        order_cell.innerHTML = order_select;
    }
}

function addProcess(name, wallpaper) {
    new_row_id = process_table.rows.length;

    new_row = process_table.insertRow(new_row_id);
    new_row.id = "process_" + (new_row_id + 1);
    new_row.dataset.process_id = new_row_id + 1;
    new_row.classList.add("process_rows");

    order_cell = new_row.insertCell(0);
    order_cell.classList.add("order_cell");
    order_cell.dataset.process_id = new_row_id + 1;

    process_cell = new_row.insertCell(1);
    wallpaper_cell = new_row.insertCell(2);
    delete_cell = new_row.insertCell(3);

    process_cell.innerHTML = "<div class='process_item'>" + name + "</div>";
    wallpaper_cell.innerHTML = "<div class='process_item'>" + wallpaper + "</div>";
    delete_cell.innerHTML = "<div class='delete_process' id='delete_process_"+(new_row_id+ 1)+"' process_id='" + (new_row_id + 1) + "'></div>";

    document.getElementById("delete_process_"+(new_row_id+ 1)).onclick = deleteProcess;

    reOrder();
}

function initProcesses(processes) {
    for (let process of Object.values(processes)) {
        split_process = process.split(", ");

        addProcess(split_process[0], split_process[1]);
    }
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

    config = JSON.parse(config)

    //Init Processes
    initProcesses(config['PROCESSES']);

    //Init MODS
    mode = config['MAIN']['mode'];
    setMode(mode)
}

function setActions() {
    //Autostart
    document.getElementById('autostart').onchange = setAutostart;

    //processes
    document.getElementById('plus').onclick = addNewProcess;

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