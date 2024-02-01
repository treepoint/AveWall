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
    return child(table.querySelector('tbody'), 'tr', index);
  }
  
  function moveRow(table, fromIndex, toIndex, isBefore) {
    move(row(table, fromIndex), row(table, toIndex), isBefore);
  }

/**************************************************
* Processes
***************************************************/
process_table = document.getElementById("process_table");

function changeWallpaperRowVisibility() {
    //Скрываем столбец с wallpaper если там ничего нету больше
    i = 0;

    for (let row of process_table.rows) {
        if (i == 0) {
            i += 1;
            continue;
        }

        type = row.children[3].children[0].value;

        if (type == 'CUSTOM') {
            document.getElementById("wallpaper_header").classList.remove("invisible");

            for (let row of process_table.rows) {
                row.children[1].children[0].classList.add("half");
                row.children[1].children[0].classList.remove("reasonable_full");
            }

            return;
        }

        i += 1;
    }

    document.getElementById("wallpaper_header").classList.add("invisible");

    for (let row of process_table.rows) {
        row.children[1].children[0].classList.remove("half");
        row.children[1].children[0].classList.add("reasonable_full");
    }
}

async function saveProcesses() {
    processes = { items : [] };

    i = 0;

    //Проверяем целостность
    for (let row of process_table.rows) {
        if (i == 0) {
            i += 1;
            continue;
        }

        process_name = row.children[1].children[0].innerHTML.replace(" ", "");

        if (process_name == "") {
            return;
        }

        type = row.children[3].children[0].value;
        wallpaper = row.children[4].children[0].children[0].innerHTML.replace(" ", "");
        if (type == 'CUSTOM' && wallpaper == "") {
            return;
        }

        i += 1;
    }


    //Сохраняем
    i = 0;

    for (let row of process_table.rows) {
        if (i == 0) {
            i += 1;
            continue;
        }

        processes.items.push(
            {
                id : row.children[0].children[0].value, 
                name : row.children[1].children[0].innerHTML, 
                type : row.children[3].children[0].value,
                wallpaper : row.children[4].children[0].children[0].innerHTML
            });

        i += 1;
    }

    await eel.saveProcesses(processes)();

    showModal('Processes saved');
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
    addProcess('', 'DEFAULT' ,'');

    //Лайфхак, ага. Добавили процесс — обновили локализацию. 
    //Да, костыль, но и у нас тут MVP. Быстродействие в интерфейсе нас особо не интересует
    setLocale(locale);
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
        row.children[6].dataset.process_id = new_process_id;
        row.children[6].children[0].attributes.process_id.nodeValue = new_process_id;
        row.children[6].children[0].id = "process_" + new_process_id;
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

    moveRow(process_table, current_index + 1, new_index + 1, isBefore);

    //Меняем все ID на новые
    updateProcessIdForRows();

    //Задаем правильные выборы в селектах процессов
    for (let select of document.getElementsByClassName("process_order_select")) { 
        select.selectedIndex = select.children[0].dataset.current_index - 1;
    }

    saveProcesses();
}

function onTypeChange(select) {

    current_type = select.options[select.selectedIndex].value;

    if (current_type == 'CUSTOM') {
        row_id = select.parentElement.parentElement.dataset.process_id;

        select.parentElement.parentElement.children[4].innerHTML = "<div class='input_item half-round hundred rtl half' dir='RTL'><bdi id='process_wallpaper_" + row_id + "' class='rtl'></bdi></div>";
        select.parentElement.parentElement.children[5].innerHTML = "<button id='wallpaper_choice_" + row_id + "' class='custom-file-upload''>ВЫБРАТЬ</button>";
        document.getElementById("wallpaper_choice_" + row_id).onclick = changeProcessWallpaper;
    } else {
        select.parentElement.parentElement.children[4].innerHTML = "<div class='invisible'><bdi> </bdi></div>";
        select.parentElement.parentElement.children[5].innerHTML = " ";
    }

    saveProcesses();

    changeWallpaperRowVisibility();
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

function addProcess(name, current_type, wallpaper) {
    new_row_id = process_table.rows.length;

    new_row = process_table.insertRow(new_row_id);
    new_row.id = "process_" + (new_row_id);
    new_row.dataset.process_id = new_row_id;
    new_row.classList.add("process_rows");

    order_cell = new_row.insertCell(0);
    order_cell.classList.add("order_cell");
    order_cell.dataset.process_id = new_row_id;

    process_cell = new_row.insertCell(1);
    process_choice_cell = new_row.insertCell(2);
    type_cell = new_row.insertCell(3);
    wallpaper_cell = new_row.insertCell(4);
    wallpaper_choice_cell = new_row.insertCell(5);
    delete_cell = new_row.insertCell(6);

    process_cell.innerHTML = "<div class='input_item half-round reasonable_full'>" + name + "</div>";
    process_choice_cell.innerHTML = "<button id='process_choice_" + new_row_id + "' class='custom-file-upload''>ВЫБРАТЬ</button>";
    document.getElementById("process_choice_" + new_row_id).onclick = changeProcessfile;

    types = ["CUSTOM", "BLACK", "DEFAULT"]

    type_select = "<select onchange='onTypeChange(this)'>";
    for (type of types) {
        if (type != current_type) {
            type_select += "<option id='option_process_type_" + type + "_" + new_row_id + "' value='" + type + "'>" + type + "</option>";
        } else {
            type_select += "<option id='option_process_type_" + type + "_" + new_row_id + "' value='" + type + "' selected>" + type + "</option>";
        }
    }
    type_select += "</select>";
 
    type_cell.innerHTML = type_select;
    type_cell.dataset.process_id = new_row_id;
    type_cell.dataset.value = new_row_id;

    if (current_type == "CUSTOM") {
        wallpaper_cell.innerHTML = "<div class='input_item half-round hundred rtl half' dir='RTL'><bdi id='process_wallpaper_" + new_row_id + "' class='rtl'>"+ wallpaper + "</bdi></div>";
        wallpaper_choice_cell.innerHTML = "<button id='wallpaper_choice_" + new_row_id + "' class='custom-file-upload''>ВЫБРАТЬ</button>";
        document.getElementById("wallpaper_choice_" + new_row_id).onclick = changeProcessWallpaper;
    } else {
        wallpaper_cell.innerHTML = "<div class='invisible'><bdi> </bdi></div>";
        wallpaper_choice_cell.innerHTML = " ";
    }
    
    delete_cell.innerHTML = "<div class='delete_process' id='delete_process_" + new_row_id + "' process_id='" + new_row_id + "'></div>";

    document.getElementById("delete_process_" + new_row_id).onclick = deleteProcess;

    reOrder();
}

function clearProcessTable() {
    if (process_table.children[0]) {
        process_table.children[0].remove();
    }
}

async function changeProcessfile(event) {
    file_path = await eel.getFileWithPath('exe')();

    if (file_path == '') {
        return;
    }

    file_with_path = file_path.replace(/^.*\\/, "");

    path_array = file_with_path.split('/').slice();

    file_name = path_array[path_array.length - 1];

    process_cell = event.target.parentElement.parentElement.children[1].children[0];
    process_cell.innerHTML=file_name;

    saveProcesses();
}

async function changeProcessWallpaper(event) {
    file_path = await eel.getFileWithPath('image')();

    if (file_path == '') {
        return;
    }

    file_with_path = file_path.replace(/^.*\\/, "");

    wallpaper_cell = event.target.parentElement.parentElement.children[4].children[0].children[0];
    wallpaper_cell.innerHTML=file_with_path;

    saveProcesses();
}

async function changeDefaultWallpaper(event) {
    file_path = await eel.getFileWithPath('image')();

    if (file_path == '') {
        return;
    }

    file_with_path = file_path.replace(/^.*\\/, "");

    document.getElementById("default_wallpaper").innerHTML=file_with_path;

    await eel.changeDefaultWallpaper(file_with_path)();

    showModal('Changes applied');
}

function initProcesses(processes) {

    header = process_table.insertRow(0);

    order_th = header.insertCell(0);
    process_th = header.insertCell(1);
    process_th.innerHTML = "<div id='processes_header_process' class='processes_header'>process</div>";

    process_set_th = header.insertCell(2);
    type_th = header.insertCell(3);
    type_th.innerHTML = "<div id='processes_header_mode' class='processes_header'>mode</div>";

    wallpaper_th = header.insertCell(4);
    wallpaper_th.id = 'wallpaper_header'
    wallpaper_th.innerHTML = "<div id='processes_header_wallpaper' class='processes_header'>wallpaper</div>";
    wallpaper_set_th = header.insertCell(5);
    delete_th = header.insertCell(6);

    for (let process of Object.values(processes)) {
        split_process = process.split(",");

        addProcess(
            split_process[0].replace(" ", ""), 
            split_process[1].replace(" ", ""),  
            split_process[2].replace(" ", ""));
    }

    changeWallpaperRowVisibility();
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
* LOCALES
***************************************************/

locale = "EN";

async function onLanguageChange(select) {
    locale = select.options[select.selectedIndex].value;
    await eel.changeLanguage(locale)();
    setLocale(locale);
}

function setLocale(locale) {
    if (locale == "RU" ) {
        setRussian();
        document.getElementById("language_changer").value="RU";

    } else {
        setEnglish();
        document.getElementById("language_changer").value="EN";
    }
}


function setRussian() {
    document.getElementById("h1_settings").innerHTML = "НАСТРОЙКИ";
        document.getElementById("autostart_label").innerHTML = "Запускать вместе с Windows";
        document.getElementById("h2_language").innerHTML = "Язык";
        document.getElementById("h2_default_wallpaper").innerHTML = "Обои по умолчанию";
        document.getElementById("default_wallpaper_choice").innerHTML = "ВЫБРАТЬ";
        document.getElementById("set-wall-as-default").innerHTML = "УСТАНОВИТЬ ТЕКУЩИЕ ПО УМОЛЧАНИЮ";

    document.getElementById("h1_processes").innerHTML = "СПИСОК ПРОЦЕССОВ";
        document.getElementById("processes_hint").innerHTML = "Расположите процессы в порядке их важности. Например, если вы хотите, чтобы обои Outlook имели более высокий приоритет чем Filezilla, то поставьте Outlook приоритет 1, а Filezilla — приоритет 2.";
        document.getElementById("processes_header_process").innerHTML = "процесс";
        document.getElementById("processes_header_mode").innerHTML = "режим";
        document.getElementById("processes_header_wallpaper").innerHTML = "обои";

    document.getElementById("h1_mode").innerHTML = "РЕЖИМЫ";
        document.getElementById("mode_hint").innerHTML = "Автоматический — AveWall будет работать по как указано в списке процессов. По умолчанию — принудительная установка обоев по умолчанию. Чернй экран — принудительная установка черных обоев.";
        document.getElementById("set-auto").innerHTML = "АВТОМАТИЧЕСКИЙ";
        document.getElementById("set-default").innerHTML = "ОБОИ ПО УМОЛЧАНИЮ";
        document.getElementById("set-black").innerHTML = "ЧЕРНЫЙ ЭКРАН";

    document.getElementById("h1_actions").innerHTML = "ДЕЙСТВИЯ";
        document.getElementById("reload-config").innerHTML = "ПЕРЕЗАГРУЗИТЬ КОНФИГ";
        document.getElementById("close").innerHTML = "ЗАКРЫТЬ ОКНО";
        document.getElementById("exit").innerHTML = "ЗАКРЫТЬ ПРИЛОЖЕНИЕ";

    //Выбор типа обоев в таблице
    i = 0;
    for (let row of process_table.rows) {
        if (i == 0) {
            i += 1;
            continue;
        }

        for (let option of row.children[3].children[0]) {                
            switch (option.value) {
                case 'CUSTOM':
                    option.innerHTML = 'СВОИ';
                    break;
                case 'DEFAULT':
                    option.innerHTML = 'ПО УМОЛЧАНИЮ';
                    break;
                case 'BLACK':
                    option.innerHTML = 'ЧЕРНЫЙ ЭКРАН';
                    break;
            }
        }

        i += 1;
    }

    //Кнопки в таблице
    let set_buttons = document.getElementsByClassName("custom-file-upload");

    for (button of set_buttons) {
        button.innerHTML = "ВЫБРАТЬ";
    }
}

function setEnglish() {
    document.getElementById("h1_settings").innerHTML = "SETTINGS";
        document.getElementById("autostart_label").innerHTML = "Autostart with windows";
        document.getElementById("h2_language").innerHTML = "Language";
        document.getElementById("h2_default_wallpaper").innerHTML = "Default wallpaper";
        document.getElementById("default_wallpaper_choice").innerHTML = "MANUAL SET";
        document.getElementById("set-wall-as-default").innerHTML = "GET CURRENT AS DEFAULT";

    document.getElementById("h1_processes").innerHTML = "PROCESS LIST";
        document.getElementById("processes_hint").innerHTML = "Arrange the processes in order of importance. For example, if you want the Outlook wallpaper to have a higher priority than Filezilla, put Outlook priority 1 and Filezilla priority 2.";
        document.getElementById("processes_header_process").innerHTML = "process";
        document.getElementById("processes_header_mode").innerHTML = "mode";
        document.getElementById("processes_header_wallpaper").innerHTML = "wallpaper";

    document.getElementById("h1_mode").innerHTML = "MODE";
        document.getElementById("mode_hint").innerHTML = "Auto — AveWall will work by process list. Default — forced set up default wallpaper. Black — forced black wallpaper.";
        document.getElementById("set-auto").innerHTML = "AUTO";
        document.getElementById("set-default").innerHTML = "DEFAULT";
        document.getElementById("set-black").innerHTML = "BLACK";

    document.getElementById("h1_actions").innerHTML = "ACTIONS";
        document.getElementById("reload-config").innerHTML = "RELOAD CONFIG";
        document.getElementById("close").innerHTML = "CLOSE WINDOW";
        document.getElementById("exit").innerHTML = "EXIT APPLICATION";

    //Выбор типа обоев в таблице
    i = 0;
    for (let row of process_table.rows) {
        if (i == 0) {
            i += 1;
            continue;
        }

        for (let option of row.children[3].children[0]) {
            switch (option.value) {
                case 'CUSTOM':
                    option.innerHTML = 'CUSTOM';
                    break;
                case 'DEFAULT':
                    option.innerHTML = 'DEFAULT';
                    break;
                case 'BLACK':
                    option.innerHTML = 'BLACK';
                    break;
            }
        }

        i += 1;
    }

    //Кнопки в таблице
    let set_buttons = document.getElementsByClassName("custom-file-upload");

    for (button of set_buttons) {
        button.innerHTML = "SET";
    }
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

    //Init default wallpaper
    document.getElementById("default_wallpaper").innerHTML=config['MAIN']['default_wallpaper'];

    //Init Processes
    initProcesses(config['PROCESSES']);

    //Init MODS
    mode = config['MAIN']['mode'];
    setMode(mode)

    //Init locale
    locale = config['MAIN']['locale'];
    setLocale(locale);
}

function setActions() {
    //Settings
    document.getElementById('autostart').onchange = setAutostart;
    document.getElementById('default_wallpaper_choice').onclick = changeDefaultWallpaper;

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