let score = 0;
let currentPokemonID = 0;
let hasGuessed = false;

// Cache frequently used DOM elements
const nextButton = document.getElementById('nextButton');
const resultElement = document.getElementById('result');
const pokemonImage = document.getElementById('pokemonImage');
const scoreElement = document.getElementById('score');
const answersContainer = document.getElementById('answers');

async function fetchRandomPokemon() {
    nextButton.disabled = true;
    resultElement.innerText = 'Loading...';

    try {
        const response = await fetch('/pokemon');
        if (!response.ok) throw new Error('Failed to load Pokémon');

        const data = await response.json();
        currentPokemonID = data.pokemonID;

        //
        // Set silhouette image and reset properties
        //
        pokemonImage.src = data.silhouetteImage;
        pokemonImage.style.filter = 'brightness(0)';
        pokemonImage.style.opacity = 1;

        //
        // Generate answer buttons
        //
        let buttonsHTML = '';

        for (let i = 0; i < data.pokemonNamesList.length; i++) {
            const name = data.pokemonNamesList[i];
            buttonsHTML += '<button class="btn answer-btn btn-lg" onclick="checkAnswer(\'' + name + '\')">' + name + '</button>';
        }

        answersContainer.innerHTML = buttonsHTML;

        resultElement.innerText = '';
        hasGuessed = false;
    } catch (error) {
        handleError(error, 'Error loading Pokémon. Please try again.');
    }
}

async function checkAnswer(guessedName) {
    if (hasGuessed) return;
    hasGuessed = true;

    try {
        const response = await fetch('/verify', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ pokemonID: currentPokemonID, guessedName })
        });
        const data = await response.json();

        //
        // Show full image and remove filter
        //
        pokemonImage.src = data.fullImage;
        pokemonImage.style.filter = 'none';

        //
        // Display game result
        //
        let resultHTML = `<p>True Name: ${data.trueName}</p>`;
        if (data.isCorrect) {
            score++;
            resultHTML += `<p class="correct">Correct!</p>`;
        } else {
            resultHTML += `<p class="wrong">Wrong</p>`;
        }
        resultElement.innerHTML = resultHTML;
        scoreElement.innerText = `Score: ${score}`;
        
        nextButton.disabled = false;
    } catch (error) {
        handleError(error, 'Error verifying answer. Please try again.');
        hasGuessed = false;
    }
}

function handleError(error, message) {
    console.error('Error:', error);
    resultElement.innerText = message;
}

// Load the first Pokémon when the page loads
window.onload = fetchRandomPokemon;