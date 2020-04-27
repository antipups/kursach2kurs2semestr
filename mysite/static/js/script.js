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
    // document.createElement("tr"). = 'black'
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

    // let array_of_row_to_del
    //
    // for (let trs of full_table.childNodes)
    //         if (trs instanceof HTMLTableRowElement)
    //             if (trs.style.backgroundColor === 'cyan')
    //             {
    //                 controls.style.visibility = 'visible'
    //                 break
    //             }

    // let table = child.parentElement.parentElement;
    // result_str = 'mode=Удалить из &name_of_table=' + table.firstChild.textContent.trim().slice(table.firstChild.textContent.trim().indexOf(':') + 2)
    // let count = 0;
    // for (const keks of row.childNodes)
    //     if (keks.textContent.trim().length > 0)
    //     {
    //         result_str += '&flag' + count + '=' +  keks.textContent.trim()
    //         count ++;
    //     }
    // let request = new XMLHttpRequest();
    // request.open('POST','http://127.0.0.1:8000/main/work_with_tables/',true);
    // request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    // request.addEventListener("readystatechange", () =>
    // {
    //     if(request.readyState === 4 && request.status === 200)
    //     {
    //         console.log("Запрос пришел");
    //     }
    // });
    // request.send(result_str);

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
        data_ = 'mode=Удалить из &name_of_table=' + table.firstChild.textContent.trim().slice(table.firstChild.textContent.trim().indexOf(':') + 2) + '&id=' + row.children[0].textContent + '&flag=1'
        console.log(data_)
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