/*otwieranie treningu*/

function openModal(modalId) {
    document.getElementById(modalId).style.display = "flex";
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = "none";
}


/*sumowanie punktow xp uzytkownika*/

function getCSRF() {
    return document.getElementById("csrf_token").value;
}

function doWorkout(workoutId) {
    workoutId = parseInt(workoutId);
    fetch("/do_workout/", {
        method: 'POST',
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCSRF(),
        },
        body: new URLSearchParams({ workout_id: workoutId })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            document.querySelector(".level h4").textContent = `${data.new_score}/100 XP`;
        } else {
            alert("err: " + data.error);
        }
    })
    .catch(err => console.error("web err:", err));
}

/*profil menu przy kliknieciu*/

document.querySelector("img[alt='Profil']").onclick = function() {
    document.getElementById("subMenu").classList.toggle("open-menu");
};
