function arraysEqual(arr1, arr2) {
  return (
    arr1.length === arr2.length &&
    arr1.every((value, index) => value === arr2[index])
  );
}

function checkAnswer(userAnswerElement, correctAnswer) {
  userAnswerElement.focus();
  const userText = userAnswerElement.value.trim().toLowerCase();

  /* Teile den userText/correctAnswer bei den Kommas, entferne Leerzeichen,
    normalisiere mehrere Leerzeichen zu einem (z.B. "Ulan  Bator" → "Ulan Bator"),
    filtere leere Strings, sortiere alphabetisch */
  const userItems = userText
    .split(",")
    .map((item) => item.trim().replace(/\s+/g, " "))
    .filter((item) => item !== "")
    .sort();

  const correctItems = correctAnswer
    .split(",")
    .map((item) => item.trim().replace(/\s+/g, " "))
    .filter((item) => item !== "")
    .sort();

  // Überprüfe auf (teil-)korrekte Antworten
  const isCorrect = arraysEqual(userItems, correctItems);
  const isPartialCorrect = correctItems.some((item) =>
    userItems.includes(item),
  );
  const hasWrongAnswer = userItems.some((item) => !correctItems.includes(item));

  // Reset TextInput coloring
  userAnswerElement.classList.remove("is-valid");
  userAnswerElement.classList.remove("is-invalid");
  userAnswerElement.classList.remove("is-partial-correct");

  if (isCorrect) {
    userAnswerElement.classList.add("is-valid");

    setTimeout(function () {
      location.reload();
      userAnswerElement.value = "";
    }, 1000);
  } else if (isPartialCorrect && !hasWrongAnswer) {
    userAnswerElement.classList.add("is-partial-correct");
  } else {
    userAnswerElement.classList.add("is-invalid");
  }
}

// Add event listener for Enter key
function addEnterKeyListener(userAnswerElement, correctAnswer) {
  userAnswerElement.addEventListener("keyup", function (event) {
    if (event.key === "Enter") {
      checkAnswer(userAnswerElement, correctAnswer);
    }
  });
}
