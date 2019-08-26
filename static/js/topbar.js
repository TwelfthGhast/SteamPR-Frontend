NodeTop = document.createElement("div");
NodeTop.setAttribute("id", "top-bar");

NodeHomeWrapper = document.createElement("div");
NodeHomeWrapper.setAttribute("class", "top-bar-btn-wrapper");
NodeHome = document.createElement("div");
NodeHome.setAttribute("class", "top-bar-btn");
NodeHomeWrapper.appendChild(NodeHome);
NodeHomeText = document.createTextNode("Home");
NodeHome.appendChild(NodeHomeText);
NodeHome.onclick = function() {
    window.location.href = "/";
}
/*
NodeBlogWrapper = document.createElement("div");
NodeBlogWrapper.setAttribute("class", "top-bar-btn-wrapper");
NodeBlog = document.createElement("div");
NodeBlog.setAttribute("class", "top-bar-btn");
NodeBlogWrapper.appendChild(NodeBlog);
NodeBlogText = document.createTextNode("Blog");
NodeBlog.appendChild(NodeBlogText);
NodeBlog.onclick = function() {
    window.location.href = "https://www.12ghast.com/category/personal/steampr/";
}
*/
NodeLadderWrapper = document.createElement("div");
NodeLadderWrapper.setAttribute("class", "top-bar-btn-wrapper");
NodeLadder = document.createElement("div");
NodeLadder.setAttribute("class", "top-bar-btn")
NodeLadderWrapper.appendChild(NodeLadder);
NodeLadderText = document.createTextNode("Ladder");
NodeLadder.appendChild(NodeLadderText);
NodeLadder.onclick = function() {
    window.location.href = "/ladder";
}

NodeAPIWrapper = document.createElement("div");
NodeAPIWrapper.setAttribute("class", "top-bar-btn-wrapper");
NodeAPI = document.createElement("div");
NodeAPI.setAttribute("class", "top-bar-btn")
NodeAPIWrapper.appendChild(NodeAPI);
NodeAPIText = document.createTextNode("API");
NodeAPI.appendChild(NodeAPIText);
NodeAPI.onclick = function() {
    window.location.href = "/api";
}

NodeTop.appendChild(NodeAPIWrapper);
//NodeTop.appendChild(NodeBlogWrapper);
NodeTop.appendChild(NodeLadderWrapper);
NodeTop.appendChild(NodeHomeWrapper);

var breaks = document.getElementsByClassName("break");

for(var i = 0; i < breaks.length; i++) {
    NodeBreakText = document.createTextNode("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~");
    breaks.item(i).appendChild(NodeBreakText);
}

document.body.appendChild(NodeTop);