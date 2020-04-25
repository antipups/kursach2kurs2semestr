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