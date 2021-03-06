function httpGetAsync(url, data, callback) {
    const xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function () {
        if (this.readyState === 4) {
            callback(xmlHttp.responseText, xmlHttp.status);
        }
    }

    xmlHttp.open("GET", url, true);
    xmlHttp.timeout = 5000;
    xmlHttp.send(null);
}

function httpPostAsync(url, data, callback) {
    const xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function () {
        if (this.readyState === 4) {
            callback(xmlHttp.responseText, xmlHttp.status);
        }
    }

    xmlHttp.open("POST", url, true);
    xmlHttp.timeout = 15000;
    xmlHttp.setRequestHeader('Content-Type', 'application/json');
    xmlHttp.send(JSON.stringify(data));
}

function httpDeleteAsync(url, data, callback) {
    const xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function () {
        if (this.readyState === 4) {
            callback(xmlHttp.responseText, xmlHttp.status);
        }
    }

    xmlHttp.open("DELETE", url, true);
    xmlHttp.timeout = 5000;
    xmlHttp.send();
}

function httpPutAsync(url, data, callback) {
    const xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function () {
        if (this.readyState === 4) {
            callback(xmlHttp.responseText, xmlHttp.status);
        }
    }

    xmlHttp.open("PUT", url, true);
    xmlHttp.timeout = 5000;
    xmlHttp.setRequestHeader('Content-Type', 'application/json');
    xmlHttp.send(JSON.stringify(data));
}


function isJson(str) {
    try {
        JSON.parse(str);
    } catch (e) {
        return false;
    }
    return true;
}

function findGetParameter(parameterName) {
    let result = null, tmp = [];
    location.search.substr(1).split("&").forEach(function (item) {
        tmp = item.split("=");
        if (tmp[0] === parameterName) result = decodeURIComponent(tmp[1]);
    });
    return result;
}

function selectHasValue(select, value) {
    let obj = document.getElementById(select);

    if (obj !== null) {
        return (obj.innerHTML.indexOf('value="' + value + '"') > -1);
    } else {
        return false;
    }
}

function setGetParameter(paramName, paramValue) {
    let url = window.location.href;
    let hash = location.hash;
    url = url.replace(hash, '');
    if (url.indexOf(paramName + "=") >= 0) {
        let prefix = url.substring(0, url.indexOf(paramName + "="));
        let suffix = url.substring(url.indexOf(paramName + "="));
        suffix = suffix.substring(suffix.indexOf("=") + 1);
        suffix = (suffix.indexOf("&") >= 0) ? suffix.substring(suffix.indexOf("&")) : "";
        url = prefix + paramName + "=" + paramValue + suffix;
    } else {
        if (url.indexOf("?") < 0)
            url += "?" + paramName + "=" + paramValue;
        else
            url += "&" + paramName + "=" + paramValue;
    }
    window.history.replaceState("", document.title, url + hash);
}

String.prototype.capitalize = function () {
    return this.charAt(0).toUpperCase() + this.slice(1);
}

function createNotification(type, message) {
    return  '<div class="alert alert-' + type + '" role="alert">' + message +
                '<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
                    '<span aria-hidden="true">&times;</span>' +
                '</button>' +
            '</div>';
}

function hslToHex(h, s, l) {
    l /= 100;
    const a = s * Math.min(l, 1 - l) / 100;
    const f = n => {
        const k = (n + h / 30) % 12;
        const color = l - a * Math.max(Math.min(k - 3, 9 - k, 1), -1);
        return Math.round(255 * color).toString(16).padStart(2, '0');   // convert to Hex and prefix "0" if needed
    };
    return `#${f(0)}${f(8)}${f(4)}`;
}