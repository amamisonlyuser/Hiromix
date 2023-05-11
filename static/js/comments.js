function submitComment(pollId) {
    const commentText = document.getElementById('comment-text').value;
    const csrftoken = getCookie('csrftoken');
    fetch(`/polls/${pollId}/comments/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            text: commentText,
        }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                refreshComments(pollId);
            } else {
                console.error('Failed to submit comment');
            }
        })
        .catch(error => console.error(error));
}

function refreshComments(pollId) {
    fetch(`/polls/${pollId}/comments/`)
        .then(response => response.json())
        .then(data => {
            const commentsContainer = document.getElementById('comments-container');
            commentsContainer.innerHTML = '';
            data.comments.forEach(comment => {
                const commentElem = document.createElement('div');
                commentElem.classList.add('comment');
                const usernameElem = document.createElement('span');
                usernameElem.classList.add('username');
                usernameElem.textContent = comment.user__username;
                commentElem.appendChild(usernameElem);
                const textElem = document.createElement('span');
                textElem.classList.add('text');
                textElem.textContent = comment.text;
                commentElem.appendChild(textElem);
                const dateElem = document.createElement('span');
                dateElem.classList.add('date');
                dateElem.textContent = new Date(comment.created_date).toLocaleString();
                commentElem.appendChild(dateElem);
                commentsContainer.appendChild(commentElem);
            });
        })
        .catch(error => console.error(error));
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}