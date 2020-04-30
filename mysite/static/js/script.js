function invis()
{
    let keks = document.getElementsByName("id_of_reason");
    for (let i = 0; i < 2; i++)
        if (keks[i].outerHTML.indexOf("hidden") > 1) keks[i].style.visibility = "visible"
        else
        {
            keks[i].style.visibility = "hidden";
            keks[1].options[0].selected = true;
        }
}

function mode_of_row(e) {
    child = e.target
    let full_table = child.parentElement.parentElement
    let row = child.parentElement;
    if (row.textContent.trim().startsWith('id') || row.textContent.trim().startsWith('Таб')) return

    let controls = document.getElementById('action_over_table')
    if (row.style.backgroundColor === 'cyan')
    {
        row.style.backgroundColor = '#343A40'
        row.style.color = 'white'
        for (let trs of full_table.childNodes)
            if (trs instanceof HTMLTableRowElement)
                if (trs.style.backgroundColor === 'cyan')
                {
                    controls.style.visibility = 'visible'
                    break
                }
                else controls.style.visibility = 'hidden'
    }
    else
    {
        row.style.backgroundColor = 'Cyan'
        row.style.color = 'black'
        controls.style.visibility = 'visible'
    }
}

function delete_rows() {
    let count_rows = 0
    let prepare_to_delete = []
    let indexs_to_delete = []
    let table;
    for (let row of document.getElementsByTagName('tr'))
    {
        table = row.parentElement;
        if (row.style.backgroundColor === 'cyan')
        {
            prepare_to_delete.push(row)
            indexs_to_delete.push(count_rows)
        }
        count_rows ++;
    }

    for (const ind of indexs_to_delete.reverse() )  table.deleteRow(ind);

    for (let row of prepare_to_delete)
    {
        data_ = 'mode=Удалить из &name_of_table=' + table.firstChild.textContent.trim().slice(table.firstChild.textContent.trim().indexOf(':') + 2, table.firstChild.textContent.trim().indexOf('(') - 1) + '&id=' + row.children[0].textContent + '&flag=1'
        let request = new XMLHttpRequest();
        request.open('POST','http://127.0.0.1:8000/main/work_with_tables/',true);
        request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        request.send(data_);
    }

    document.getElementById('action_over_table').style.visibility = 'hidden'
}


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function update_rows() {
    let count_rows = 0
    let prepare_to_delete = []
    let indexs_to_delete = []
    let table;
    for (let row of document.getElementsByTagName('tr'))
    {
        table = row.parentElement;
        if (row.style.backgroundColor === 'cyan')
        {
            prepare_to_delete.push(row)
            indexs_to_delete.push(count_rows)
        }
        count_rows ++;
    }

    for (const ind of indexs_to_delete.reverse() )  table.deleteRow(ind);

    let form = document.createElement('form')
    form.action = 'http://127.0.0.1:8000/main/work_with_tables/'
    form.method = 'POST'
    let count = 0;
    for (let row of prepare_to_delete)
    {
        form.innerHTML += `<input name="id${count++}" value="${row.children[0].textContent}">`;
    }
    form.innerHTML += `<input name="addon" value="">`;
    form.innerHTML += `<input name="mode" value="Изменить в ">`;
    form.innerHTML += `<input name="flag" value="1">`;
    form.innerHTML += `<input name="name_of_table" value="${table.firstChild.textContent.trim().slice(table.firstChild.textContent.trim().indexOf(':') + 2, table.firstChild.textContent.trim().indexOf('(') - 1)}">`;
    document.body.appendChild(form);
    form.submit()
    document.getElementById('action_over_table').style.visibility = 'hidden'
}