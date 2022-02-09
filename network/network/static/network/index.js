function toLike(postId, postLikes, userId) {
	if (userId == -1) {
		document.getElementById(`${postId}-forThem`).innerHTML = `<span id='target-${postId}' onclick='fadeOutEffect(${postId})' style='background-color: yellow;'>It won't take much. Login/Register to like this post.</span>`
	}
	else {
		let likeButton = document.getElementById(`${userId}-${postId}-L`)
		let unlikeButton = document.getElementById(`${userId}-${postId}-U`)
		fetch(`/posts/${postId}`, {
			method: 'PUT',
			body: JSON.stringify ({
				likes: postLikes + 1
			})
		})

		likeButton.style.display = "none"
		unlikeButton.style.display = "inline"

		document.getElementById(`${postId}-likes`).innerHTML = postLikes+1
	}
} 

function toUnlike(postId, postLikes, userId) {
	let likeButton = document.getElementById(`${userId}-${postId}-L`)
	let unlikeButton = document.getElementById(`${userId}-${postId}-U`)
	fetch(`/posts/${postId}`, {
		method: 'PUT',
		body: JSON.stringify ({
			likes: postLikes
		})
	})

	likeButton.style.display = "inline"
	unlikeButton.style.display = "none"

	document.getElementById(`${postId}-likes`).innerHTML = postLikes
} 

function fadeOutEffect(postId) {
    var fadeTarget = document.getElementById(`target-${postId}`);
    var fadeEffect = setInterval(function () {
        if (!fadeTarget.style.opacity) {
            fadeTarget.style.opacity = 1;
        }
        if (fadeTarget.style.opacity > 0) {
            fadeTarget.style.opacity -= 0.1;
        } else {
            clearInterval(fadeEffect);
        }
    }, 75);
}