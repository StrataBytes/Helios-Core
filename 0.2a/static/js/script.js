
// Welcome to the static javascript setup! Here is where the animations happen and the triggers from the core are recieved!

//A major thing is to switch to socketio instead of using JSON payloads.





function fetchEmotion() {
    fetch('/get_emotion')
        .then(response => response.json())
        .then(data => {
            changeEmotion(data.emotion);
            console.log("Emotion updated to:", data.emotion);
        })
        .catch(error => console.error('Error fetching emotion:', error));
}

setInterval(fetchEmotion, 2000);  //adjust fetch?


function changeEmotion(emotion) {
    var mouth = document.getElementById('mouth');

    //reset classes and styles
    mouth.className = '';
    mouth.style = ''; //clear styles if any

    //new class based on the emotion
    switch (emotion) {
        case 'happy':
        case 'sad':
        case 'neutral':
        case 'veryHappy':
        case 'surprised':
        case 'thinking':
            mouth.classList.add(emotion);
            break;
        default:
            console.warn('Received undefined emotion type:', emotion);
    }
}




function fetchCommand() {
    fetch('/get_command')
        .then(response => response.json())
        .then(data => {
            if (data.command === 'bark') {
                nodAnimation();
            }
            console.log("Command received:", data.command);
        })
        .catch(error => console.error('Error fetching command:', error));
}

setInterval(fetchCommand, 500);  //adjust interval?





function initializeBlinking() {
    function getRandomDelay(min, max) {
        return Math.random() * (max - min) + min;
    }

    function blink() {
        gsap.to(".eye", { scaleY: 0, duration: 0.1, yoyo: true, repeat: 1 });
    }

    blink();  //trigger initial blink
    setInterval(function() {
        blink();
    }, getRandomDelay(3000, 10000)); //rand blink timing
}



function changeEmotion(emotion) {
    var mouth = document.getElementById('mouth');

    //rst classes and styles
    mouth.className = '';
    mouth.style = ''; //clear inline styles if any

    //apply new class based on the emotion
    if (emotion === 'happy') {
        mouth.classList.add('mouth');
    } else if (emotion === 'neutral') {
        mouth.classList.add('neutral');
    } else if (emotion === 'sad') {
        mouth.classList.add('mouth', 'sad');
    } else if (emotion === 'veryHappy') {
        mouth.classList.add('veryHappy');
    } else if (emotion === 'surprised') {
        mouth.classList.add('surprised');
    } else if (emotion === 'thinking') {
        mouth.classList.add('thinking');
    }
}






//background color
function toggleBackgroundColor() {
    var body = document.body;
    var currentColor = window.getComputedStyle(body).backgroundColor;

    //check current, and switch.
    if (currentColor === 'rgb(255, 255, 255)') { 
        body.style.backgroundColor = '#080707'; 
    } else {
        body.style.backgroundColor = '#080707'; 
    }
}

//event listener
document.getElementById('toggle-bg-btn').addEventListener('click', toggleBackgroundColor);





function nodAnimation() {
    const duration = 0.3;
    const mouthContainer = document.getElementById('mouth-container');

    //move mouth container and eyes down
    gsap.to(mouthContainer, { y: 20, duration: duration });
    gsap.to(".eye", { y: 20, duration: duration, delay: 0.1 });

    //move back to original position
    gsap.to(mouthContainer, { y: 0, duration: duration, delay: duration });
    gsap.to(".eye", { y: 0, duration: duration, delay: duration + 0.1 });
}

function nod2xAnimation() {
    const duration = 0.3;
    const mouthContainer = document.getElementById('mouth-container');
    const timeline = gsap.timeline();

    //first nod
    timeline.to(mouthContainer, { y: 20, duration: duration })
            .to(".eye", { y: 20, duration: duration, delay: -duration }, 0) // Offset to start with mouth
            .to(mouthContainer, { y: 0, duration: duration })
            .to(".eye", { y: 0, duration: duration, delay: -duration }, duration);

    //second nod (broken)
    timeline.to(mouthContainer, { y: 20, duration: duration })
            .to(".eye", { y: 20, duration: duration, delay: -duration }, duration * 2)
            .to(mouthContainer, { y: 0, duration: duration })
            .to(".eye", { y: 0, duration: duration, delay: -duration }, duration * 3);
}


function lookLeftAnimation() {
    const duration = 0.3;

    //eyes to the left
    gsap.to(["#mouth-container", ".eye"], { x: -20, duration: duration });

    //og pos
    setTimeout(() => {
        gsap.to(["#mouth-container", ".eye"], { x: 0, duration: duration });
    }, 2000); //2 sec
}

function lookRightAnimation() {
    const duration = 0.3;

    //move to right
    gsap.to(["#mouth-container", ".eye"], { x: 20, duration: duration });
    setTimeout(() => {
        gsap.to(["#mouth-container", ".eye"], { x: 0, duration: duration });
    }, 2000);
}




function surprisedAnimation() {
    const duration = 0.5;
    changeEmotion('surprised');
    //spook the eye
    gsap.to(".eye", { scaleY: 1.5, duration: duration });
    //rtrn eyes to normal
    setTimeout(() => {
        gsap.to(".eye", { scaleY: 1, duration: duration });
    }, 3000); //hold 3 sec
}



function thinkingAnimation() {
    const duration = 0.5;
    //change the mouth to thinking
    changeEmotion('thinking');
    //move to side
    gsap.to(["#mouth-container", ".eye"], { x: 10, duration: duration });
    //retrun to normal
    setTimeout(() => {
        gsap.to(["#mouth-container", ".eye"], { x: 0, duration: duration });
    }, 4000); //holds for 4 sec
}
