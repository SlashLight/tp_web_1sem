function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const init = () => {
    const cards = document.querySelectorAll('.card')
    const answers = document.querySelectorAll('.answer');
    for (const card of cards) {

        const likeButton = card.querySelector('.like-button')
        const likeCounter = card.querySelector('.like-counter')
        const postId = card.dataset.postId

        likeButton.addEventListener('click', () => {
            const request = new Request(`//localhost:8000/${postId}/like/`, {
                method: 'post',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                }
            })
            fetch(request)
                .then((response) => response.json())
                .then((data) => likeCounter.innerHTML = data.likes_count)

            likeCounter.innerHTML = (Number(likeCounter.innerHTML) + 1).toString()
        })
    }

    for (const answer of answers) {
        const checkbox = answer.querySelector('.answer-checkbox');
        const answerId = answer.dataset.answerId
        checkbox.addEventListener('change', () => {
            const request = new Request(`//localhost:8000/${answerId}/correct/`, {
                method: 'post',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                }
            })
            fetch(request)
                .then((response) => response.json())

        })
    }
}

init()