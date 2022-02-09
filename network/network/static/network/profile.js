document.addEventListener('DOMContentLoaded', function() {

	var following = []
	var userData = {}
	var info = document.querySelector(".profileInfo")

	let unfollowButton = document.querySelector('.toUnfollow')
	let followButton = document.querySelector('.toFollow')

	let numFollowers = document.querySelector('#followers')
	let numFollowing = document.querySelector('#following')

	fetch(`/user/${info.dataset.user}`)
	.then(response => response.json())
	.then(data => {
		userData = data;
		following = data.follower;
		if (following[0] == info.id)
			unfollowButton.style.display = "block"
		else {
			followButton.style.display = "block"
		}
		numFollowers.innerHTML = userData.follower.length
		numFollowing.innerHTML = userData.following.length
	})

	try {
		var updated = following.splice(following.indexOf(unfollowButton.value),1)
		unfollowButton.onclick  = () => { 
			numFollowers.innerHTML = parseInt(numFollowers.innerHTML) - 1
			console.log(numFollowers.innerHTML)
			
			fetch(`/user/${unfollowButton.id.substring(0,1)}`, {
				method: 'PUT',
				body: JSON.stringify({
					follower: updated
					})
				})

			followButton.style.display = "block"
			unfollowButton.style.display = "none"
			};
	}
	catch(err) {console.log("problem with the unfollowButton")}

	try {
		var updated1 = following.concat(followButton.value);
		
		followButton.onclick = () => {
			numFollowers.innerHTML = parseInt(numFollowers.innerHTML) + 1;
			console.log(numFollowers.innerHTML)
			
			fetch(`/user/${followButton.id.substring(0,1)}`, {
				method: 'PUT',
				body: JSON.stringify({
					follower: updated1
				})
			})
			followButton.style.display = "none"
			unfollowButton.style.display = "block"
		};
	}
	catch(err) {console.log("problem with the FollowButton")}

	let buttons = document.querySelectorAll('.toEdit')
	let buttonsCount = buttons.length
	for (var j = 0; j<buttonsCount; j++)
		document.querySelector(`#post-content-${buttons[j].id}`).style.display='block';
	for (let i = 0;i < buttonsCount; i++ )
	{
		buttons[i].onclick = () => {
			document.querySelector(`#post-form-${buttons[i].id}`).style.display='block'; 
			
			for (var j = 0; j<buttonsCount; j++){
			   document.querySelector(`#tr-${buttons[j].id}`).style.display='none';
			}	

			document.querySelector(`#form-${buttons[i].id}`).onsubmit = function() {

				fetch(`/posts/${buttons[i].id}`, {
					method: 'PUT',
					body: JSON.stringify({
						content: document.querySelector(`#text-${buttons[i].id}`).value
					})
				})
				.then(response => response.json())
			}
		}
	}	
})