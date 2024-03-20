const light = () => {
    document.querySelector("body").setAttribute("data-bs-theme","light")
    document.getElementById("theme").setAttribute("xlink:href", "#sun-fill");
    document.getElementById("lightButton").classList.add("active");
    document.getElementById("darkButton").classList.remove("active");
}

const dark = () => {
    document.querySelector("body").setAttribute("data-bs-theme","dark")
    document.getElementById("theme").setAttribute("xlink:href", "#moon-fill");
    document.getElementById("lightButton").classList.remove("active");
    document.getElementById("darkButton").classList.add("active");
}


