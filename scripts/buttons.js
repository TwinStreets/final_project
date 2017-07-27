function clickLike(likeButtonParam, artistKeyParam) {
  // Make a post call to /likes, passing along the like state and artist key
  $.post(
    '/like',
    {'like_button': likeButtonParam, 'artist_key': artistKeyParam},
    function(new_like_state) {
        updateLikeButtonClasses(new_like_state);
    });
}

function updateLikeButtonClasses(likeState) {
  console.log("updateLikeButtonClasses");

  // Get both of the like buttons.
  const likeButton = $('.like-button')
  const dislikeButton = $('.dislike-button')

  // Update the classes of the like buttons.
  if (likeState === "liked") {
    likeButton.addClass('selected')
    dislikeButton.removeClass('selected')
  } else if (likeState === "disliked") {
    likeButton.removeClass('selected')
    dislikeButton.addClass('selected')
  } else {
    likeButton.removeClass('selected')
    dislikeButton.removeClass('selected')
  }

}

// Get the current like state.
const likeState = $('#dataContainer')[0].dataset.likeState;
updateLikeButtonClasses(likeState);
