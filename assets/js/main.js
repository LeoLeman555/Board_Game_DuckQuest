const difficultySlider = document.getElementById("difficultySlider");
const difficultyValue = document.getElementById("difficultyValue");
const weightsDisplay = document.getElementById("weightsDisplay");
const difficultyImage = document.getElementById("difficultyImage");

// Mapping of difficulty levels to weights
const difficultyWeights = {
  1: [1],
  2: [1, 5],
  3: [1, 4],
  4: [1, 3],
  5: [1, 2],
  6: [1, 3, 5],
  7: [1, 4, 5],
  8: [1, 2, 5],
  9: [1, 3, 4, 5],
  10: [1, 2, 3, 5],
  11: [1, 2, 3, 4, 5],
};

function updateDifficulty() {
  const level = difficultySlider.value;
  difficultyValue.textContent = level;
  weightsDisplay.textContent =
    "Weights Used: " + difficultyWeights[level].join(", ");

  // Update example image
  difficultyImage.src = `../assets/images/example_difficulty_${level}.png`;
  difficultyImage.alt = `Graph example for difficulty level ${level}`;

  // Visual difficulty indication (color gradient from green → red)
  const percentage = (level - 1) / 10; // 0 → 1
  const color = `rgb(${Math.floor(255 * percentage)}, ${Math.floor(
    255 * (1 - percentage)
  )}, 0)`;
  weightsDisplay.style.color = color;
}

difficultySlider.addEventListener("input", updateDifficulty);

// Initialize on page load
updateDifficulty();
