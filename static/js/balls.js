(function(){
    let ballContainer = document.getElementById("sea-of-balls");

    for (let i = 0; i < 10; i++) {
        let ball = document.createElement("span");
        ball.style.setProperty("--size", `${Math.random() * 200 + 100}px`)
        ball.style.setProperty("--speed", `${Math.random() * 5 + 20}s`)
        ball.style.setProperty("--delay", `-${Math.random() * 100 + 20}s`)
        ball.style.setProperty("left", `${Math.random() * 100}vw`)
        ballContainer.appendChild(ball);
    }
})();