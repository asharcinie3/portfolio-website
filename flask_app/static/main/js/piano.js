document.addEventListener('DOMContentLoaded', function() {
    // Only run piano code if we're on the piano page
    const pianoElement = document.querySelector('.piano');
    if (!pianoElement) return; // Exit if no piano element found
    
    // constants
    const pianoKeysContainer = document.querySelector('.piano-keys');
    let sequence = [];
    const weSeeyouSequence = [87, 69, 83, 69, 69, 89, 79, 85];
    const sound = {
        "65": "http://carolinegabriel.com/demo/js-keyboard/sounds/040.wav",
        "87": "http://carolinegabriel.com/demo/js-keyboard/sounds/041.wav",
        "83": "http://carolinegabriel.com/demo/js-keyboard/sounds/042.wav",
        "69": "http://carolinegabriel.com/demo/js-keyboard/sounds/043.wav",
        "68": "http://carolinegabriel.com/demo/js-keyboard/sounds/044.wav",
        "70": "http://carolinegabriel.com/demo/js-keyboard/sounds/045.wav",
        "84": "http://carolinegabriel.com/demo/js-keyboard/sounds/046.wav",
        "71": "http://carolinegabriel.com/demo/js-keyboard/sounds/047.wav",
        "89": "http://carolinegabriel.com/demo/js-keyboard/sounds/048.wav",
        "72": "http://carolinegabriel.com/demo/js-keyboard/sounds/049.wav",
        "85": "http://carolinegabriel.com/demo/js-keyboard/sounds/050.wav",
        "74": "http://carolinegabriel.com/demo/js-keyboard/sounds/051.wav",
        "75": "http://carolinegabriel.com/demo/js-keyboard/sounds/052.wav",
        "79": "http://carolinegabriel.com/demo/js-keyboard/sounds/053.wav",
        "76": "http://carolinegabriel.com/demo/js-keyboard/sounds/054.wav",
        "80": "http://carolinegabriel.com/demo/js-keyboard/sounds/055.wav",
        "186": "http://carolinegabriel.com/demo/js-keyboard/sounds/056.wav"
    };

    // functions
    function handleKeyDown(event) {
        const keyCode = event.keyCode.toString();
        playSoundAndAnimate(keyCode);
    }

    const playSoundAndAnimate = function(keyCode) {
        // play the sound
        const soundURL = sound[keyCode];
        if (soundURL) {
            const audio = new Audio(soundURL);
            audio.play();
        }

        // animate the key
        const pressedKey = document.querySelector(`.piano-key[data-key="${keyCode}"]`);
        if (pressedKey) {
            pressedKey.classList.add('key-pressed');
            setTimeout(function() {
                pressedKey.classList.remove('key-pressed');
            }, 200);
        }

        // check sequence length
        sequence.push(parseInt(keyCode));
        if (sequence.length > 8) {
            sequence.shift();
        }

        // check if sequence is correct and display new image/ play sound if so
        if (JSON.stringify(sequence) === JSON.stringify(weSeeyouSequence)) {
            const piano = document.querySelector('.piano');
            piano.style.transition = 'opacity 0s';
            piano.style.opacity = 0;

            const greatOneImg = document.querySelector('.great-one-img');
            greatOneImg.style.display = 'block';

            new Audio('https://orangefreesounds.com/wp-content/uploads/2020/09/Creepy-piano-sound-effect.mp3?_=1').play();

            document.removeEventListener('keydown', handleKeyDown);
        }
    };


    // event listeners
    // add press listener for keyboard
    document.addEventListener('keydown', handleKeyDown);

    pianoKeysContainer.addEventListener('mouseover', function(event) {
        // hide key letters
        const allKeyTexts = document.querySelectorAll('.key-text');
        allKeyTexts.forEach(text => text.style.display = 'none');

        // show letter for hovered key only
        const keyText = event.target.querySelector('.key-text');
        if (keyText) {
            keyText.style.display = 'block';
        }
    });

    // add click listener for piano keys
    pianoKeysContainer.addEventListener('click', function(event) {
        // get key code for clicked key
        const dataKey = event.target.dataset.key;
        if (dataKey) {
            playSoundAndAnimate(dataKey);
        }
    });
});