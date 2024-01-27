/**************************************************
* Autostart
***************************************************/
async function setAutostart() {
    await eel.setAutostart()();
}

/**************************************************
* Notification
***************************************************/
function showModal(content) {
    modal = document.getElementById("modal");

    modal.innerHTML = content;

    comfortable_delay = Math.random() * (350 - 250) + 250;

    if (modal.classList.value == "modal") {
        modal.classList.add("hidden");
    }

    setTimeout(() => { 
        modal.classList.remove("hidden");
    }, comfortable_delay);

    setTimeout(() => { 
        modal.classList.add("hidden");
    }, 2000);
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

async function saveProcesses() {
    processes = { items : [] };

    for (let row of process_table.rows) {
        processes.items.push(
            {
                id : row.children[0].children[0].value, 
                name : row.children[1].children[0].innerHTML, 
                wallpaper : row.children[3].children[0].innerHTML
            });
    }

    await eel.saveProcesses(processes)();

    showModal('Changes applied');
}

function deleteProcess(event) {
    process_id = event.target.attributes.process_id.nodeValue;
    document.getElementById("process_" + process_id).remove();

    //Меняем все ID на новые
    updateProcessIdForRows();

    reOrder();
    
    saveProcesses();
}

function addNewProcess() {
    addProcess('', '');
}

function updateProcessIdForRows() {
    //Меняем все ID на новые
    let rows = document.getElementsByClassName("process_rows");

    new_process_id = 0;
    
    for (let row of rows) {
        new_process_id += 1;
        //row parameters
        row.id = "process_" + new_process_id;
        row.dataset.process_id = new_process_id;

        //process order select
        row.children[0].dataset.process_id = new_process_id;

        for (let option of row.children[0].children[0].children) {
            option.dataset.current_index = new_process_id;
        }

        //for delete button
        row.children[4].dataset.process_id = new_process_id;
        row.children[4].children[0].attributes.process_id.nodeValue = new_process_id;
        row.children[4].children[0].id = "process_" + new_process_id;
    }
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
    updateProcessIdForRows();

    //Задаем правильные выборы в селектах процессов
    for (let select of document.getElementsByClassName("process_order_select")) { 
        select.selectedIndex = select.children[0].dataset.current_index - 1;
    }

    saveProcesses();
}

function reOrder() {
    //Add new order to each cell
    max_index = null;

    for (let order_cell of Array.from(document.getElementsByClassName("order_cell")).reverse()) {
        order_select = "<select onchange='onOrderChange(this)' class='process_order_select'>";

        current_index = order_cell.dataset.process_id;

        if (max_index == null) {
            max_index = order_cell.dataset.process_id;
        }

        i = 1;
        while (i != (parseInt(max_index) + 1)) {
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
    process_choice_cell = new_row.insertCell(2);
    wallpaper_cell = new_row.insertCell(3);
    delete_cell = new_row.insertCell(4);

    process_cell.innerHTML = "<div class='process_item half-round'>" + name + "</div>";
    process_choice_cell.innerHTML = "<button id='process_choice_" + (new_row_id+ 1) + "' class='custom-file-upload''>SET</button>";
    wallpaper_cell.innerHTML = "<div class='process_item hundred'>" + wallpaper + "</div>";
    delete_cell.innerHTML = "<div class='delete_process' id='delete_process_"+(new_row_id+ 1)+"' process_id='" + (new_row_id + 1) + "'></div>";

    document.getElementById("delete_process_"+(new_row_id+ 1)).onclick = deleteProcess;
    document.getElementById("process_choice_"+(new_row_id+ 1)).onclick = changeProcessfile;

    reOrder();
}

function clearProcessTable() {
    process_table.children[0].remove();
}

async function changeProcessfile(event) {
    file_path = await eel.getFileWithPath()();

    file_with_path = file_path.replace(/^.*\\/, "");

    path_array = file_with_path.split('/').slice();

    file_name = path_array[path_array.length - 1];

    process_cell = event.target.parentElement.parentElement.children[1].children[0];
    process_cell.innerHTML=file_name;

    saveProcesses();
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

    showModal('Auto mode is enabled');
}

async function setDefault() {
    await eel.setDefaultMode()();
    setMode('default');

    showModal('Default mode is enabled');
}

async function setBlack() {
    await eel.setBlackMode()();
    setMode('black');

    showModal('Black mode is enabled');
}

/**************************************************
* ACTIONS
***************************************************/
async function onConfigReload() {

    clearProcessTable();

    await eel.onConfigReload()();

    initConfig();

    showModal('Reloaded');
}

async function getCurrentWindowsWallpaper() {
    await eel.getCurrentWindowsWallpaper()();

    showModal('Setted');
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