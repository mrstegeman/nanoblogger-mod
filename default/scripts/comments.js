function sanitize(data, isbody) {
    var clean = unescape(data).
                replace(/\+/g, ' ').
                replace(/</g, '&lt;').
                replace(/>/g, '&gt;');

    if (isbody)
        clean = clean.replace(/\n/g, '<br />');

    return clean;
}

var ajax_req;
var elements;
function get_comment_count(base_url) {
    var id_str = "";
    elements = document.getElementsByClassName('posted');
    for (var i = 0; i < elements.length; i++) {
        id_str += elements[i].id + ',';
        ajax_req = new XMLHttpRequest();
        ajax_req.onreadystatechange = function() {
            if (ajax_req.readyState == 4 && ajax_req.status == 200) {
                var data = eval('(' + ajax_req.responseText + ')');
                var com;
                for (com in data) {
                    document.getElementById('comments_' + com).innerHTML = data[com];
                }
            }
        };
    }
    if (id_str != '') {
        ajax_req.open("GET", base_url + "cgi-bin/comment.cgi?id=" + id_str + "&action=count", true);
        ajax_req.send();
    }
}


var ajax_req2;
var elements2;
function get_comment_list(base_url) {
    var id_str = "";
    elements2 = document.getElementsByClassName('posted');
    for (var i = 0; i < elements2.length; i++) {
        id_str += elements2[i].id + ',';
        ajax_req2 = new XMLHttpRequest();
        ajax_req2.onreadystatechange = function() {
            if (ajax_req2.readyState == 4 && ajax_req2.status == 200) {
                var data = eval('(' + ajax_req2.responseText + ')');
                var com;
                for (com in data.comments) {
                    document.getElementById('comment_list').innerHTML +=
                        '<div class="comments-post">' +
                        '<div class="comments-head">' +
                        '<span class="comments-title">' + sanitize(data.comments[com].title, false) + '</span>' +
                        '<span class="comments-author">By: ' + sanitize(data.comments[com].author, false) +
                        ' on ' + sanitize(data.comments[com].date, false) + '</span></div>' +
                        '<div class="comments-body">' + sanitize(data.comments[com].body, true) + '</div>' +
                        '</div>';
                }
            }
        };
    }
    if (id_str != '') {
        ajax_req2.open("GET", base_url + "cgi-bin/comment.cgi?id=" + id_str + "&action=get", true);
        ajax_req2.send();
    }
}
