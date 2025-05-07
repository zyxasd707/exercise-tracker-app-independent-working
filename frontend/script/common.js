let getBarItem = document.querySelector(".bar-item");
let getSideBar = document.querySelector(".sidebar");
let getXmark = document.querySelector(".xmark");
let getSidebarLink = document.querySelectorAll(".sidebar-link");
let activePage = window.location.pathname;
let getSideBarStatus = false;

getBarItem.onclick = () => {
    getSideBar.style = "transform: translateX(0px);width:220px";
    getSideBar.classList.add("sidebar-active");
};

getXmark.onclick = () => {
    getSideBar.style =
        "transform: translateX(-220px);width:220px;box-shadow:none;";
    getSideBarStatus = true;
    if (getSideBar.classList.contains("sidebar-active")) {
        getSideBar.classList.remove("sidebar-active");
    }
};

window.addEventListener("resize", (e) => {
    if (getSideBarStatus === true) {
        if (e.target.innerWidth > 768) {
            getSideBar.style = "transform: translateX(0px);width:220px";
        } else {
            getSideBar.style =
                "transform: translateX(-220px);width:220px;box-shadow:none;";
        }
    }
});

document.onclick = (e) => {
    if (getSideBar.classList.contains("sidebar-active")) {
        if (
            !e.target.classList.contains("bar-item") &&
            !e.target.classList.contains("sidebar") &&
            !e.target.classList.contains("brand") &&
            !e.target.classList.contains("brand-name")
        ) {
            getSideBar.style =
                "transform: translateX(-220px);width:220px;box-shadow:none;";
            getSideBar.classList.remove("sidebar-active");
            getSideBarStatus = true;
        }
    }
};

window.addEventListener("scroll", () => {
    if (getSideBar.classList.contains("sidebar-active")) {
        getSideBar.style =
            "transform: translateX(-220px);width:220px;box-shadow:none;";
        getSideBar.classList.remove("sidebar-active");
    }
});

getSidebarLink.forEach((item) => {
    if (item.id === activePage) {
        item.classList.add("active");
    }
});

/*************************************************************
 * Handle logout                                             *
 *************************************************************/
function handleLogout() {
    sessionStorage.removeItem('chatHistory');
}