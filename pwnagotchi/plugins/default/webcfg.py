__author__ = '33197631+dadav@users.noreply.github.com'
__version__ = '0.0.1'
__name__ = 'webcfg'
__license__ = 'GPL3'
__description__ = 'This plugin allows the user to make runtime changes.'

import logging
import json
from pwnagotchi.config import SharedConfig
import pwnagotchi.plugins as plugins


OPTIONS = dict()
CFG = SharedConfig.get_instance()

INDEX = """
<html>
    <head>
        <meta name="viewport" content="width=device-width; user-scalable=0;" />
        <title>
            webcfg
        </title>
        <style>
            #divTop {
                position: -webkit-sticky;
                position: sticky;
                top: 0px;
                width: 100%;
                font-size: 16px;
                padding: 5px;
                border: 1px solid #ddd;
                margin-bottom: 5px;
            }
            #searchText {
                width: 100%;
            }
            table {
                table-layout: auto;
                width: 100%;
            }
            table, th, td {
              border: 1px solid black;
              border-collapse: collapse;
            }
            th, td {
              padding: 15px;
              text-align: left;
            }
            @media screen and (max-width: 500px) {
                th, td {
                    width: 100%;
                }
            }
            table tr:nth-child(even) {
              background-color: #eee;
            }
            table tr:nth-child(odd) {
             background-color: #fff;
            }
            table th {
              background-color: black;
              color: white;
            }

            .remove {
                background-color: #f44336;
                color: white;
                border: 2px solid #f44336;
                padding: 4px 8px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 12px;
                margin: 4px 2px;
                -webkit-transition-duration: 0.4s; /* Safari */
                transition-duration: 0.4s;
                cursor: pointer;
            }

            .remove:hover {
                background-color: white;
                color: black;
            }

            #btnSend {
                position: -webkit-sticky;
                position: sticky;
                bottom: 0px;
                width: 100%;
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
            }

            #divTop {
                display: table;
                width: 100%;
            }
            #divTop > * {
                display: table-cell;
            }
            #divTop > span {
                width: 1%;
            }
            #divTop > input {
                width: 100%;
            }

            @media screen and (max-width:700px) {
                table, tr, td {
                    padding:0;
                    border:1px solid black;
                }

                table {
                    border:none;
                }

                thead {
                    display:none;
                }

                tr {
                    float: left;
                    width: 100%;
                    margin-bottom: 2em;
                }

                td {
                    float: left;
                    width: 100%;
                    padding:1em;
                }

                td::before {
                    content:attr(data-label);
                    word-wrap: break-word;
                    background: #eee;
                    border-right:2px solid black;
                    width: 20%;
                    float:left;
                    padding:1em;
                    font-weight: bold;
                    margin:-1em 1em -1em -1em;
                }
            }
        </style>
    </head>
    <body>
        <div id="divTop">
            <input type="text" id="searchText" onkeyup="filterTable()" placeholder="Search for options ..." title="Type an option name">
            <span><button id="btnAdd" type="button" onclick="addOption()">+</button></span>
        </div>
        <div id="content"></div>
        <button id="btnSend" type="button" onclick="sendConfig()">Apply</button>
    </body>
    <script type="text/javascript">
        function addOption() {
          var input, table, tr, td, btnDel
          input = document.getElementById("searchText");
          inputVal = input.value;
          table = document.getElementById("tableOptions");
          if (table) {
            tr = table.insertRow();
            // del button
            td = document.createElement("td");
            btnDel = document.createElement("Button");
            btnDel.innerHTML = "X";
            btnDel.onclick = function(){ delRow(this);};
            btnDel.className = "remove";
            td.appendChild(btnDel);
            tr.appendChild(td);
            // option
            td = document.createElement("td");
            td.innerHTML = inputVal;
            tr.appendChild(td);
            // value
            td = document.createElement("td");
            input = document.createElement("input");
            input.type = "text";
            input.value = "";
            td.appendChild(input);
            tr.appendChild(td);

            input.value = "";
          }
        }

        function sendConfig(){
            // get table
            var table = document.getElementById("tableOptions");
            if (table) {
                var json = tableToJson(table);
                sendJSON("webcfg/update-config", json, function(response) {
                    if (response) {
                        if (response.status == "200") {
                            alert("Config got updated");
                        } else {
                            alert("Error while updating the config (err-code: " + response.status + ")");
                        }
                    }
                });
            }
        }

        function filterTable(){
            var input, filter, table, tr, td, i, txtValue;
            input = document.getElementById("searchText");
            filter = input.value.toUpperCase();
            table = document.getElementById("tableOptions");
            if (table) {
                tr = table.getElementsByTagName("tr");

                for (i = 0; i < tr.length; i++) {
                    td = tr[i].getElementsByTagName("td")[1];
                    if (td) {
                        txtValue = td.textContent || td.innerText;
                        if (txtValue.toUpperCase().indexOf(filter) > -1) {
                            tr[i].style.display = "";
                        }else{
                            tr[i].style.display = "none";
                        }
                    }
                }
            }
        }

        function sendJSON(url, data, callback) {
          var xobj = new XMLHttpRequest();
          xobj.open("POST", url);
          xobj.setRequestHeader("Content-Type", "application/json");
          xobj.onreadystatechange = function () {
                if (xobj.readyState == 4) {
                  callback(xobj);
                }
          };
          xobj.send(JSON.stringify(data));
        }

        function loadJSON(url, callback) {
          var xobj = new XMLHttpRequest();
          xobj.overrideMimeType("application/json");
          xobj.open('GET', url, true);
          xobj.onreadystatechange = function () {
                if (xobj.readyState == 4 && xobj.status == "200") {
                  callback(JSON.parse(xobj.responseText));
                }
          };
          xobj.send(null);
        }

        // https://stackoverflow.com/questions/19098797/fastest-way-to-flatten-un-flatten-nested-json-objects
        function unFlattenJson(data) {
            "use strict";
            if (Object(data) !== data || Array.isArray(data))
                return data;
            var result = {}, cur, prop, idx, last, temp;
            for(var p in data) {
                cur = result, prop = "", last = 0;
                do {
                    idx = p.indexOf(".", last);
                    temp = p.substring(last, idx !== -1 ? idx : undefined);
                    cur = cur[prop] || (cur[prop] = (!isNaN(parseInt(temp)) ? [] : {}));
                    prop = temp;
                    last = idx + 1;
                } while(idx >= 0);
                cur[prop] = data[p];
            }
            return result[""];
        }

        function flattenJson(data) {
            var result = {};
            function recurse (cur, prop) {
                if (Object(cur) !== cur) {
                    result[prop] = cur;
                } else if (Array.isArray(cur)) {
                     for(var i=0, l=cur.length; i<l; i++)
                         recurse(cur[i], prop ? prop+"."+i : ""+i);
                    if (l == 0)
                        result[prop] = [];
                } else {
                    var isEmpty = true;
                    for (var p in cur) {
                        isEmpty = false;
                        recurse(cur[p], prop ? prop+"."+p : p);
                    }
                    if (isEmpty)
                        result[prop] = {};
                }
            }
            recurse(data, "");
            return result;
        }

        function delRow(btn) {
            var tr = btn.parentNode.parentNode;
            tr.parentNode.removeChild(tr);
        }

        function jsonToTable(json) {
            var table = document.createElement("table");
            table.id = "tableOptions";

            // create header
            var tr = table.insertRow();
            var thDel = document.createElement("th");
            thDel.innerHTML = "";
            var thOpt = document.createElement("th");
            thOpt.innerHTML = "Option";
            var thVal = document.createElement("th");
            thVal.innerHTML = "Value";
            tr.appendChild(thDel);
            tr.appendChild(thOpt);
            tr.appendChild(thVal);

            var td;
            var btnDel;
            // iterate over keys
            Object.keys(json).forEach(function(key) {
                tr = table.insertRow();
                // del button
                td = document.createElement("td");
                td.setAttribute("data-label", "");
                btnDel = document.createElement("Button");
                btnDel.innerHTML = "X";
                btnDel.onclick = function(){ delRow(this);};
                btnDel.className = "remove";
                td.appendChild(btnDel);
                tr.appendChild(td);
                // option
                td = document.createElement("td");
                td.setAttribute("data-label", "Option");
                td.innerHTML = key;
                tr.appendChild(td);
                // value
                td = document.createElement("td");
                td.setAttribute("data-label", "Value");
                input = document.createElement("input");
                input.type = "text";
                input.value = json[key];
                td.appendChild(input);
                tr.appendChild(td);
            });

            return table;
        }

        function toNumberMaybe(txt) {
            if (txt == "") {
                return txt;
            }
            num = Number(txt);
            if (Number.isNaN(num)) {
                return txt;
            }
            return num;
        }

        function tableToJson(table) {
            var rows = table.getElementsByTagName("tr");
            var i, td, key, value;
            var json = {};

            for (i = 0; i < rows.length; i++) {
                td = rows[i].getElementsByTagName("td");
                if (td.length == 3) {
                    // td[0] = del button
                    key = td[1].textContent || td[1].innerText;
                    input = td[2].getElementsByTagName("input");
                    if (input) {
                        json[key] = toNumberMaybe(input[0].value); // hack hack hack
                    }
                }
            }
            return unFlattenJson(json);
        }

        loadJSON("webcfg/get-config", function(response) {
            var flat_json = flattenJson(response);
            var table = jsonToTable(flat_json);
            var divContent = document.getElementById("content");
            divContent.innerHTML = "";
            divContent.appendChild(table);
        });
    </script>
</html>
"""


def on_loaded():
    """
    Gets called when the plugin gets loaded
    """
    logging.info("webcfg: Plugin succesful loaded. Run %s:%d/plugins/webcfg to use me!",
                 CFG['ui']['display']['video']['address'],
                 CFG['ui']['display']['video']['port'])


def on_webhook(response, path):
    """
    Serves the current configuration
    """
    global CFG
    if path == "/" or not path:
        # send index page
        res = INDEX
        response.send_response(200)
    elif path == "/get-config":
        # send configuration
        res = json.dumps(CFG.copy())
        response.send_response(200)
    elif path == "/update-config":
        # receive new configuration and reload
        try:
            content_len = int(response.headers.get('content-length'))
            post_body = response.rfile.read(content_len)
            data = json.loads(post_body)
        except Exception as json_ex:
            logging.error(json_ex)
            response.send_response(500)
            res = "config error"
        else:
            # will clean the current config and use the new one
            CFG = SharedConfig(data)
            plugins.load(CFG)
            response.send_response(200)
            res = "success"
    else:
        response.send_response(500)

    response.send_header('Content-type', 'text/html')
    response.end_headers()


    try:
        response.wfile.write(bytes(res, "utf-8"))
    except Exception as ex:
        logging.error(ex)
