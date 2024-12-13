let container = document.querySelector('#container');

window.onmousemove = e => {
    let x = e.clientX / 8;
    let y = e.clientY / 8;

    container.style.backgroundPositionX = x + "px";
    container.style.backgroundPositionY = y + "px";
}