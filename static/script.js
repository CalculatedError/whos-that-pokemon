let score = 0;
let currentPokemonID = 0;
let hasGuessed = false;

async function fetchRandomPokemon() {
    document.getElementById('nextButton').disabled = true;
    document.getElementById('result').innerText = 'Loading...';

    try {
        const response = await fetch('/pokemon');
        if (!response.ok) throw new Error('Failed to load Pokémon');

        const data = await response.json();
        currentPokemonID = data.pokemonID;

        // Set the silhouette image (initially shows as a silhouette)
        const pokemonImage = document.getElementById('pokemonImage');
        pokemonImage.src = data.silhouetteImage;
        pokemonImage.style.filter = 'brightness(0)'; // Ensure it's a silhouette
        pokemonImage.style.opacity = 1; // Reset opacity for the new round

        // Clear previous buttons and add new ones
        const answersContainer = document.getElementById('answers');
        answersContainer.innerHTML = data.pokemonNamesList.map(name => 
            `<button class="btn fun-btn btn-lg" onclick="checkAnswer('${name}')">${name}</button>`
        ).join('');
        
        document.getElementById('result').innerText = '';
        hasGuessed = false;
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('result').innerText = 'Error loading Pokémon. Please try again.';
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

        const pokemonImage = document.getElementById('pokemonImage');
        pokemonImage.src = data.fullImage;
        pokemonImage.style.filter = 'none';

        const resultElement = document.getElementById('result');
        resultElement.innerHTML = `<p>True Name: ${data.trueName}</p>`;
        
        if (data.isCorrect) {
            score++;
            resultElement.innerHTML += `<p class="correct">Correct!</p>`;
        } else {
            resultElement.innerHTML += `<p class="wrong">Wrong</p>`;
        }

        document.getElementById('score').innerText = `Score: ${score}`;
        document.getElementById('nextButton').disabled = false;
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('result').innerText = 'Error verifying answer. Please try again.';
        hasGuessed = false;
    }
}


window.onload = fetchRandomPokemon;
